import sqlite3
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from app.audit.audit_log import write_audit_log
from app.system.boundary_classification import (
    format_boundary_classification_detail,
    get_boundary_classification_coverage,
)


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"
DB_PATH = ROOT_DIR / "finance.db"
DASHBOARD_URL = "http://localhost:8501"

KNOWN_LOCAL_ARTIFACTS = {
    '?? "BussinessOS Avance.pdf"',
    "?? BussinessOS Avance.pdf",
}


def _check(name, passed, detail, severity="critical"):
    return {
        "name": name,
        "status": "passed" if passed else "failed",
        "severity": severity,
        "detail": detail,
    }


def _warning(name, detail):
    return {
        "name": name,
        "status": "warning",
        "severity": "warning",
        "detail": detail,
    }


def _read_text(relative_path):
    return (ROOT_DIR / relative_path).read_text(encoding="utf-8")


def _latest_report(prefix):
    if not REPORTS_DIR.exists():
        return None

    reports = sorted(
        REPORTS_DIR.glob(f"{prefix}_*.md"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return reports[0] if reports else None


def _extract_metric(content, label, default=0):
    for line in content.splitlines():
        if line.startswith(f"{label}:"):
            value = line.split(":", 1)[1].strip()
            return int(value) if value.isdigit() else default
    return default


def _run_command(command, timeout=30):
    return subprocess.run(
        command,
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def _git_status_lines():
    result = _run_command(["git", "status", "--short"])

    if result.returncode != 0:
        return None, result.stderr.strip() or "git status failed"

    return [line.strip() for line in result.stdout.splitlines() if line.strip()], None


def _dashboard_responds():
    try:
        with urlopen(DASHBOARD_URL, timeout=3) as response:
            return response.status == 200, f"{DASHBOARD_URL} returned {response.status}"
    except URLError as error:
        return False, f"{DASHBOARD_URL} not reachable: {error.reason}"
    except TimeoutError:
        return False, f"{DASHBOARD_URL} not reachable: timeout"


def _database_tables():
    if not DB_PATH.exists():
        return set()

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    return {row[0] for row in rows}


def _notification_summary():
    if not DB_PATH.exists():
        return {"total": 0, "invalid_statuses": ["database_missing"]}

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT status, COUNT(*)
            FROM notification_outbox
            GROUP BY status
            """
        ).fetchall()

    valid_statuses = {"queued", "sent", "dismissed", "failed"}
    invalid_statuses = [row[0] for row in rows if row[0] not in valid_statuses]
    total = sum(row[1] for row in rows)
    return {"total": total, "invalid_statuses": invalid_statuses}


def _scheduled_close_status():
    if not DB_PATH.exists():
        return None

    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            """
            SELECT enabled, run_time_local, last_run_date, last_status
            FROM scheduled_daily_close
            WHERE schedule_name = 'executive_daily_close'
            LIMIT 1
            """
        ).fetchone()

    if not row:
        return None

    return {
        "enabled": bool(row[0]),
        "run_time_local": row[1],
        "last_run_date": row[2],
        "last_status": row[3],
    }


def generate_release_readiness():
    checks = []

    system_report = _latest_report("system_integrity")
    if system_report:
        content = system_report.read_text(encoding="utf-8")
        failed_checks = _extract_metric(content, "Failed checks")
        checks.append(
            _check(
                "System check",
                failed_checks == 0,
                f"{system_report.relative_to(ROOT_DIR)} | failed checks: {failed_checks}",
            )
        )
    else:
        checks.append(_check("System check", False, "No system integrity report found"))

    deployment_result = _run_command([sys.executable, "scripts/deployment_check.py"])
    checks.append(
        _check(
            "Deployment boundary check",
            deployment_result.returncode == 0,
            "Public/private boundary passed" if deployment_result.returncode == 0 else deployment_result.stdout + deployment_result.stderr,
        )
    )

    dashboard_ok, dashboard_detail = _dashboard_responds()
    if dashboard_ok:
        checks.append(_check("Dashboard local response", True, dashboard_detail, severity="warning"))
    else:
        checks.append(_warning("Dashboard local response", dashboard_detail))

    required_public_files = [
        "public/index.html",
        "public/styles.css",
        "public/lead-intake.js",
        "public/assets/dashboard-preview.png",
    ]
    missing_public_files = [
        path for path in required_public_files if not (ROOT_DIR / path).exists()
    ]
    checks.append(
        _check(
            "Landing public files",
            not missing_public_files,
            "present" if not missing_public_files else ", ".join(missing_public_files),
        )
    )

    landing_markers = ["demo-request-form", "request-demo", "lead-intake.js"]
    index_text = _read_text("public/index.html") if (ROOT_DIR / "public/index.html").exists() else ""
    missing_markers = [marker for marker in landing_markers if marker not in index_text]
    checks.append(
        _check(
            "Lead intake surface",
            not missing_markers,
            "ready" if not missing_markers else ", ".join(missing_markers),
        )
    )

    gitignore_text = _read_text(".gitignore") if (ROOT_DIR / ".gitignore").exists() else ""
    required_gitignore = ["finance.db", ".env", ".venv/", ".streamlit/secrets.toml"]
    missing_gitignore = [
        pattern for pattern in required_gitignore if pattern not in gitignore_text
    ]
    checks.append(
        _check(
            "Sensitive file protections",
            not missing_gitignore,
            "protected" if not missing_gitignore else ", ".join(missing_gitignore),
        )
    )

    blocked_public_paths = [
        "public/finance.db",
        "public/.env",
        "public/secrets.toml",
        "public/.streamlit/secrets.toml",
    ]
    exposed_public_paths = [
        path for path in blocked_public_paths if (ROOT_DIR / path).exists()
    ]
    checks.append(
        _check(
            "Public secret boundary",
            not exposed_public_paths,
            "clear" if not exposed_public_paths else ", ".join(exposed_public_paths),
        )
    )

    tables = _database_tables()
    required_tables = {
        "audit_logs",
        "transactions",
        "notification_outbox",
        "scheduled_daily_close",
    }
    missing_tables = sorted(required_tables - tables)
    checks.append(
        _check(
            "Private database readiness",
            not missing_tables,
            "required tables present" if not missing_tables else ", ".join(missing_tables),
        )
    )

    today = date.today().isoformat()
    daily_close_report = REPORTS_DIR / f"daily_close_{today}.md"
    checks.append(
        _check(
            "Daily close artifact",
            daily_close_report.exists(),
            str(daily_close_report.relative_to(ROOT_DIR)) if daily_close_report.exists() else "missing",
        )
    )

    notification_summary = _notification_summary()
    checks.append(
        _check(
            "Notification outbox readiness",
            notification_summary["total"] > 0 and not notification_summary["invalid_statuses"],
            f"{notification_summary['total']} notification(s), invalid statuses: {notification_summary['invalid_statuses'] or 'none'}",
        )
    )

    schedule = _scheduled_close_status()
    checks.append(
        _check(
            "Scheduled close readiness",
            bool(schedule and schedule["enabled"]),
            (
                f"enabled at {schedule['run_time_local']} | last status: {schedule['last_status']}"
                if schedule
                else "schedule missing"
            ),
        )
    )

    access_control_text = _read_text("app/security/access_control.py")
    required_pages = ["Notifications", "Delivery Approval", "Secure Email", "Scheduled Close", "System Integrity", "Release Readiness", "Runtime Stability", "Surface Audit", "Publish Checklist", "Boundary Index", "Session Handoff", "Demo Readiness", "Demo Package", "Demo Script", "Pilot Plan", "Pilot Tracker", "Pilot Exit", "Pilot Day 1", "Pilot Day 2", "Pilot Day 3", "Pilot Day 4", "Pilot Day 5", "Pilot Expansion"]
    missing_pages = [page for page in required_pages if page not in access_control_text]
    checks.append(
        _check(
            "Dashboard readiness pages",
            not missing_pages,
            "visible in navigation" if not missing_pages else ", ".join(missing_pages),
        )
    )

    boundary_coverage = get_boundary_classification_coverage()
    checks.append(
        _check(
            "Boundary classification coverage",
            boundary_coverage["total"] > 0 and not boundary_coverage["missing"],
            format_boundary_classification_detail(boundary_coverage),
        )
    )

    git_lines, git_error = _git_status_lines()
    if git_error:
        checks.append(_warning("Git working tree", git_error))
    else:
        relevant_lines = [line for line in git_lines if line not in KNOWN_LOCAL_ARTIFACTS]
        if relevant_lines:
            checks.append(_warning("Git working tree", "; ".join(relevant_lines)))
        else:
            checks.append(_check("Git working tree", True, "clean except known local artifacts"))

    critical_failures = [
        check for check in checks if check["status"] == "failed" and check["severity"] == "critical"
    ]
    warnings = [
        check
        for check in checks
        if check["status"] == "warning"
        or (check["status"] == "failed" and check["severity"] == "warning")
    ]

    if critical_failures:
        overall_status = "blocked"
    elif warnings:
        overall_status = "ready_with_warnings"
    else:
        overall_status = "ready"

    return {
        "date": today,
        "overall_status": overall_status,
        "total_checks": len(checks),
        "passed_checks": sum(1 for check in checks if check["status"] == "passed"),
        "warning_checks": len(warnings),
        "failed_checks": len(critical_failures),
        "checks": checks,
    }


def _format_check_rows(checks):
    rows = [
        "| Check | Status | Severity | Detail |",
        "| --- | --- | --- | --- |",
    ]

    for check in checks:
        detail = str(check["detail"]).replace("|", "\\|")
        rows.append(
            f"| {check['name']} | {check['status']} | {check['severity']} | {detail} |"
        )

    return "\n".join(rows)


def export_release_readiness_report(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_release_readiness()
    report_path = REPORTS_DIR / f"release_readiness_{result['date']}.md"

    content = f"""# Release Readiness MVP v0.1

Date: {result['date']}

## Demo Readiness Summary

Overall status: {result['overall_status']}
Total checks: {result['total_checks']}
Passed checks: {result['passed_checks']}
Warning checks: {result['warning_checks']}
Failed checks: {result['failed_checks']}

## Checks

{_format_check_rows(result['checks'])}
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "release_readiness_exported",
            "info" if result["overall_status"] != "blocked" else "warning",
            "Release readiness report exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "overall_status": result["overall_status"],
                "warning_checks": result["warning_checks"],
                "failed_checks": result["failed_checks"],
            },
        )

    return result, str(report_path)


def print_release_readiness(conn=None):
    result, report_path = export_release_readiness_report(conn)

    print("Release Readiness:")
    print(f"Date: {result['date']}")
    print(f"Overall status: {result['overall_status']}")
    print(f"Total checks: {result['total_checks']}")
    print(f"Passed checks: {result['passed_checks']}")
    print(f"Warning checks: {result['warning_checks']}")
    print(f"Failed checks: {result['failed_checks']}")

    for check in result["checks"]:
        label = check["status"].upper()
        print(f"[{label}] {check['name']} | {check['detail']}")

    print(f"Release readiness report exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result


