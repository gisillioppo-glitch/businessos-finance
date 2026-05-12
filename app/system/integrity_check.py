import os
import subprocess
from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.scheduler.scheduled_daily_close import create_scheduled_daily_close_table


ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR / "finance.db"
REPORTS_DIR = ROOT_DIR / "reports"

REQUIRED_MODULES = [
    "actions",
    "alerts",
    "approvals",
    "assistance",
    "audit",
    "command_center",
    "dashboard",
    "db",
    "demo",
    "evidence",
    "governance",
    "notifications",
    "operations",
    "people",
    "readiness",
    "reports",
    "rules",
    "scheduler",
    "security",
    "support",
]

REQUIRED_TABLES = [
    "audit_logs",
    "transactions",
    "recommended_actions",
    "operations_tasks",
    "support_incidents",
    "business_users",
    "assistance_requests",
    "approval_requests",
    "notification_outbox",
    "scheduled_daily_close",
]

REQUIRED_REPORT_PREFIXES = [
    "daily_brief",
    "governance_brief",
    "support_brief",
    "command_center",
    "approval_decisions",
    "executive_alerts",
    "executive_evidence_index",
    "daily_close",
    "daily_close_distribution",
    "runtime_stability",
    "private_demo_package",
    "notification_delivery_approval",
    "secure_email_delivery",
]

VALID_NOTIFICATION_STATUSES = {"queued", "sent", "dismissed", "failed"}
SENSITIVE_PUBLIC_PATHS = [
    "public/finance.db",
    "public/.env",
    "public/secrets.toml",
    "public/.streamlit/secrets.toml",
]

REQUIRED_GITIGNORE_PATTERNS = [
    "finance.db",
    ".env",
    ".venv/",
    ".streamlit/secrets.toml",
]

KNOWN_LOCAL_ARTIFACTS = {
    '?? "BussinessOS Avance.pdf"',
    '?? BussinessOS Avance.pdf',
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


def _get_tables(conn):
    rows = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()
    return {row[0] for row in rows}


def _latest_report(prefix):
    if not REPORTS_DIR.exists():
        return None

    reports = list(REPORTS_DIR.glob(f"{prefix}_*.md"))

    if prefix == "daily_close":
        reports = [
            report for report in reports
            if not report.name.startswith("daily_close_distribution_")
        ]

    reports = sorted(
        reports,
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return reports[0] if reports else None


def _run_git_status():
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return None, result.stderr.strip() or "git status failed"

    return [line.strip() for line in result.stdout.splitlines() if line.strip()], None


def generate_system_integrity_check(conn):
    create_scheduled_daily_close_table(conn)

    checks = []

    checks.append(_check("Repository root", (ROOT_DIR / "cli.py").exists(), str(ROOT_DIR)))
    checks.append(_check("Database file", DB_PATH.exists(), str(DB_PATH)))
    checks.append(_check("Reports folder", REPORTS_DIR.exists(), str(REPORTS_DIR)))

    for module_name in REQUIRED_MODULES:
        module_path = ROOT_DIR / "app" / module_name
        checks.append(
            _check(
                f"Module: {module_name}",
                module_path.exists() and module_path.is_dir(),
                str(module_path.relative_to(ROOT_DIR)),
            )
        )

    tables = _get_tables(conn)
    for table_name in REQUIRED_TABLES:
        checks.append(
            _check(
                f"Database table: {table_name}",
                table_name in tables,
                "present" if table_name in tables else "missing",
            )
        )

    for prefix in REQUIRED_REPORT_PREFIXES:
        report = _latest_report(prefix)
        checks.append(
            _check(
                f"Latest report: {prefix}",
                report is not None,
                str(report.relative_to(ROOT_DIR)) if report else "missing",
                severity="warning",
            )
        )

    gitignore_path = ROOT_DIR / ".gitignore"
    gitignore_content = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
    for pattern in REQUIRED_GITIGNORE_PATTERNS:
        checks.append(
            _check(
                f"Gitignore protects: {pattern}",
                pattern in gitignore_content,
                "protected" if pattern in gitignore_content else "missing from .gitignore",
            )
        )

    for sensitive_path in SENSITIVE_PUBLIC_PATHS:
        full_path = ROOT_DIR / sensitive_path
        checks.append(
            _check(
                f"Public secret boundary: {sensitive_path}",
                not full_path.exists(),
                "not present" if not full_path.exists() else "sensitive file exists in public surface",
            )
        )

    invalid_notification_statuses = []
    if "notification_outbox" in tables:
        rows = conn.execute(
            """
            SELECT DISTINCT status
            FROM notification_outbox
            """
        ).fetchall()
        invalid_notification_statuses = [
            row[0] for row in rows if row[0] not in VALID_NOTIFICATION_STATUSES
        ]

    checks.append(
        _check(
            "Notification statuses",
            not invalid_notification_statuses,
            "valid" if not invalid_notification_statuses else ", ".join(invalid_notification_statuses),
        )
    )

    git_lines, git_error = _run_git_status()
    if git_error:
        checks.append(_warning("Git status", git_error))
    else:
        relevant_lines = [line for line in git_lines if line not in KNOWN_LOCAL_ARTIFACTS]
        if relevant_lines:
            checks.append(_warning("Git working tree", "; ".join(relevant_lines)))
        else:
            checks.append(_check("Git working tree", True, "clean except known local artifacts", severity="warning"))

    failed = [check for check in checks if check["status"] == "failed" and check["severity"] == "critical"]
    warnings = [check for check in checks if check["status"] == "warning" or (check["status"] == "failed" and check["severity"] == "warning")]

    if failed:
        overall_status = "failed"
    elif warnings:
        overall_status = "warning"
    else:
        overall_status = "passed"

    return {
        "date": date.today().isoformat(),
        "overall_status": overall_status,
        "total_checks": len(checks),
        "passed_checks": sum(1 for check in checks if check["status"] == "passed"),
        "warning_checks": len(warnings),
        "failed_checks": len(failed),
        "checks": checks,
    }


def print_system_integrity_check(conn):
    result = generate_system_integrity_check(conn)

    print("System Integrity Check:")
    print(f"Date: {result['date']}")
    print(f"Overall status: {result['overall_status']}")
    print(f"Total checks: {result['total_checks']}")
    print(f"Passed checks: {result['passed_checks']}")
    print(f"Warning checks: {result['warning_checks']}")
    print(f"Failed checks: {result['failed_checks']}")

    for check in result["checks"]:
        label = check["status"].upper()
        print(f"[{label}] {check['name']} | {check['detail']}")

    write_audit_log(
        conn,
        "system_integrity_check_viewed",
        "info" if result["overall_status"] != "failed" else "warning",
        "System integrity check viewed.",
        {
            "overall_status": result["overall_status"],
            "total_checks": result["total_checks"],
            "warning_checks": result["warning_checks"],
            "failed_checks": result["failed_checks"],
        },
    )

    return result


def _format_check_rows(checks):
    rows = [
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]

    for check in checks:
        rows.append(f"| {check['name']} | {check['status']} | {check['detail']} |")

    return "\n".join(rows)


def export_system_integrity_report(conn):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = print_system_integrity_check(conn)
    report_path = REPORTS_DIR / f"system_integrity_{result['date']}.md"

    content = f"""# System Integrity Check

Date: {result['date']}

## Integrity Summary

Overall status: {result['overall_status']}
Total checks: {result['total_checks']}
Passed checks: {result['passed_checks']}
Warning checks: {result['warning_checks']}
Failed checks: {result['failed_checks']}

## Checks

{_format_check_rows(result['checks'])}
"""

    report_path.write_text(content, encoding="utf-8")
    print(f"System Integrity report exported: {report_path.relative_to(ROOT_DIR)}")

    write_audit_log(
        conn,
        "system_integrity_check_exported",
        "info" if result["overall_status"] != "failed" else "warning",
        "System integrity check exported.",
        {
            "report_path": str(report_path.relative_to(ROOT_DIR)),
            "overall_status": result["overall_status"],
        },
    )

    return str(report_path)

