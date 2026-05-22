import importlib.util
import subprocess
from datetime import date
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from app.audit.audit_log import write_audit_log


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"
DASHBOARD_URL = "http://localhost:8501"
STANDARD_SMOKE_COMMAND_LIMIT = 60

KNOWN_LOCAL_ARTIFACTS = {
    '?? "BussinessOS Avance.pdf"',
    "?? BussinessOS Avance.pdf",
}

HEAVY_RUNTIME_COMMANDS = {
    "python cli.py private-demo-dry-run",
    "python cli.py private-pilot-intake",
    "python cli.py private-pilot-plan",
    "python cli.py private-pilot-tracker",
    "python cli.py private-pilot-exit-decision",
    "python cli.py pilot-day-1-package",
    "python cli.py pilot-day-2-rhythm",
    "python cli.py pilot-day-3-evidence-review",
    "python cli.py pilot-day-4-owner-confirmation",
    "python cli.py pilot-day-5-narrow-continuation",
    "python cli.py pilot-expansion-review-prep",
    "python cli.py pilot-expansion-review-decision",
    "python cli.py pilot-expansion-approval-gate-prep",
}

RUNTIME_RECOMMENDATIONS = [
    "Use the standard smoke profile for daily development checks.",
    "Reserve the full smoke profile for release checkpoints and deep validation windows.",
    "Allow pilot package commands to reuse fresh artifacts instead of recalculating the full chain every time.",
    "Add timing metadata to runtime reports so slow commands become visible over time.",
    "Preserve approval-gated behavior while optimizing report generation.",
]


def _check(name, status, detail):
    return {
        "name": name,
        "status": status,
        "detail": detail,
    }


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


def _extract_metric(content, label, default=0):
    for line in content.splitlines():
        if line.startswith(f"{label}:"):
            value = line.split(":", 1)[1].strip()
            return int(value) if value.isdigit() else default
    return default


def _extract_status(content, label, default="unknown"):
    for line in content.splitlines():
        if line.startswith(f"{label}:"):
            return line.split(":", 1)[1].strip()
    return default


def _dashboard_responds():
    try:
        with urlopen(DASHBOARD_URL, timeout=3) as response:
            return response.status == 200, f"{DASHBOARD_URL} returned {response.status}"
    except URLError as error:
        return False, f"{DASHBOARD_URL} not reachable: {error.reason}"
    except TimeoutError:
        return False, f"{DASHBOARD_URL} not reachable: timeout"


def _git_status_lines():
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


def _load_smoke_module():
    smoke_path = ROOT_DIR / "scripts" / "smoke_test.py"
    if not smoke_path.exists():
        return None

    spec = importlib.util.spec_from_file_location("businessos_smoke_test", smoke_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _smoke_profiles():
    module = _load_smoke_module()
    if not module:
        return {}

    profiles = getattr(module, "PROFILES", {})
    return {
        profile: [f"python cli.py {command}" for command in commands]
        for profile, commands in profiles.items()
    }


def _format_check_rows(checks):
    rows = [
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]

    for check in checks:
        rows.append(f"| {check['name']} | {check['status']} | {check['detail']} |")

    return "\n".join(rows)


def _format_commands(commands):
    rows = [
        "| Command | Runtime Risk |",
        "| --- | --- |",
    ]

    for command in commands:
        risk = "heavy" if command in HEAVY_RUNTIME_COMMANDS else "normal"
        rows.append(f"| `{command}` | {risk} |")

    return "\n".join(rows)


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def generate_runtime_stability_review():
    checks = []

    system_report = _latest_report("system_integrity")
    if system_report:
        content = system_report.read_text(encoding="utf-8")
        failed = _extract_metric(content, "Failed checks")
        warnings = _extract_metric(content, "Warning checks")
        checks.append(
            _check(
                "System integrity",
                "passed" if failed == 0 else "failed",
                f"{system_report.relative_to(ROOT_DIR)} | failed: {failed} | warnings: {warnings}",
            )
        )
    else:
        checks.append(_check("System integrity", "failed", "No system integrity report found."))

    readiness_report = _latest_report("release_readiness")
    if readiness_report:
        content = readiness_report.read_text(encoding="utf-8")
        status = _extract_status(content, "Overall status")
        failed = _extract_metric(content, "Failed checks")
        warnings = _extract_metric(content, "Warning checks")
        checks.append(
            _check(
                "Release readiness",
                "passed" if failed == 0 else "failed",
                f"{readiness_report.relative_to(ROOT_DIR)} | status: {status} | failed: {failed} | warnings: {warnings}",
            )
        )
    else:
        checks.append(_check("Release readiness", "failed", "No release readiness report found."))

    daily_close = _latest_report("daily_close")
    checks.append(
        _check(
            "Daily close artifact",
            "passed" if daily_close else "failed",
            str(daily_close.relative_to(ROOT_DIR)) if daily_close else "missing",
        )
    )

    dashboard_ok, dashboard_detail = _dashboard_responds()
    checks.append(
        _check(
            "Dashboard local response",
            "passed" if dashboard_ok else "warning",
            dashboard_detail,
        )
    )

    git_lines, git_error = _git_status_lines()
    if git_error:
        checks.append(_check("Git working tree", "warning", git_error))
    else:
        relevant_lines = [line for line in git_lines if line not in KNOWN_LOCAL_ARTIFACTS]
        checks.append(
            _check(
                "Git working tree",
                "passed" if not relevant_lines else "warning",
                "clean except known local artifacts" if not relevant_lines else "; ".join(relevant_lines),
            )
        )

    smoke_profiles = _smoke_profiles()
    smoke_commands = smoke_profiles.get("standard", [])
    full_commands = smoke_profiles.get("full", [])
    heavy_commands = [command for command in smoke_commands if command in HEAVY_RUNTIME_COMMANDS]
    full_heavy_commands = [command for command in full_commands if command in HEAVY_RUNTIME_COMMANDS]

    checks.append(
        _check(
            "Standard smoke profile size",
            "warning" if len(smoke_commands) > STANDARD_SMOKE_COMMAND_LIMIT else "passed",
            f"{len(smoke_commands)} command(s) in standard profile | limit: {STANDARD_SMOKE_COMMAND_LIMIT}",
        )
    )
    checks.append(
        _check(
            "Default heavy pilot command chain",
            "warning" if heavy_commands else "passed",
            f"{len(heavy_commands)} heavy pilot command(s) in standard profile",
        )
    )
    checks.append(
        _check(
            "Full smoke profile reserve",
            "passed" if full_heavy_commands else "warning",
            f"{len(full_heavy_commands)} heavy pilot command(s) reserved for full profile",
        )
    )

    failed_checks = [check for check in checks if check["status"] == "failed"]
    warning_checks = [check for check in checks if check["status"] == "warning"]

    if failed_checks:
        overall_status = "runtime_blocked"
    elif heavy_commands or warning_checks:
        overall_status = "stable_with_runtime_optimization_needed"
    else:
        overall_status = "runtime_stable"

    return {
        "date": date.today().isoformat(),
        "overall_status": overall_status,
        "total_checks": len(checks),
        "passed_checks": sum(1 for check in checks if check["status"] == "passed"),
        "warning_checks": len(warning_checks),
        "failed_checks": len(failed_checks),
        "smoke_command_count": len(smoke_commands),
        "heavy_command_count": len(heavy_commands),
        "full_smoke_command_count": len(full_commands),
        "full_heavy_command_count": len(full_heavy_commands),
        "checks": checks,
        "heavy_commands": heavy_commands,
        "full_heavy_commands": full_heavy_commands,
        "recommendations": RUNTIME_RECOMMENDATIONS,
    }


def export_runtime_stability_review(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_runtime_stability_review()
    report_path = REPORTS_DIR / f"runtime_stability_{result['date']}.md"

    content = f"""# BusinessOS Runtime Stability Review v0.1

Date: {result['date']}

## Runtime Stability Summary

Overall status: {result['overall_status']}
Total checks: {result['total_checks']}
Passed checks: {result['passed_checks']}
Warning checks: {result['warning_checks']}
Failed checks: {result['failed_checks']}
Smoke command count: {result['smoke_command_count']}
Heavy pilot command count: {result['heavy_command_count']}
Full smoke command count: {result['full_smoke_command_count']}
Full heavy pilot command count: {result['full_heavy_command_count']}

## Checks

{_format_check_rows(result['checks'])}

## Heavy Pilot Commands

{_format_commands(result['heavy_commands']) if result['heavy_commands'] else 'No heavy pilot commands detected.'}

## Full Profile Heavy Pilot Commands

{_format_commands(result['full_heavy_commands']) if result['full_heavy_commands'] else 'No full-profile heavy pilot commands detected.'}

## Recommendations

{_format_bullets(result['recommendations'])}

## Operator Note

This review does not optimize runtime by itself. It identifies whether BusinessOS is operationally stable enough to continue and whether smoke/runtime hardening should be handled as a follow-up block.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "runtime_stability_review_exported",
            "info" if result["failed_checks"] == 0 else "warning",
            "Runtime stability review exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "overall_status": result["overall_status"],
                "warning_checks": result["warning_checks"],
                "failed_checks": result["failed_checks"],
                "heavy_command_count": result["heavy_command_count"],
                "full_heavy_command_count": result["full_heavy_command_count"],
            },
        )

    return result, str(report_path)


def print_runtime_stability_review(conn=None):
    result, report_path = export_runtime_stability_review(conn)

    print("BusinessOS Runtime Stability Review:")
    print(f"Date: {result['date']}")
    print(f"Overall status: {result['overall_status']}")
    print(f"Total checks: {result['total_checks']}")
    print(f"Passed checks: {result['passed_checks']}")
    print(f"Warning checks: {result['warning_checks']}")
    print(f"Failed checks: {result['failed_checks']}")
    print(f"Smoke command count: {result['smoke_command_count']}")
    print(f"Heavy pilot command count: {result['heavy_command_count']}")
    print(f"Full smoke command count: {result['full_smoke_command_count']}")
    print(f"Full heavy pilot command count: {result['full_heavy_command_count']}")

    for check in result["checks"]:
        print(f"[{check['status'].upper()}] {check['name']} | {check['detail']}")

    print(f"Runtime stability review exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
