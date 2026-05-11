from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.private_demo_package import (
    DASHBOARD_PAGES,
    DO_NOT_SHOW_ITEMS,
    export_private_demo_package,
)
from app.demo.private_demo_script import DEMO_ARC, export_private_demo_script
from app.readiness.release_readiness import generate_release_readiness


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

REQUIRED_DEMO_PAGES = [
    "Dashboard",
    "Daily Close",
    "Notifications",
    "Scheduled Close",
    "System Integrity",
]

REQUIRED_BOUNDARY_MARKERS = [
    "finance.db",
    ".env",
    "secrets",
    "BussinessOS Avance.pdf",
]

DEMO_RUN_SEQUENCE = [
    "Open public landing only for positioning.",
    "Switch to private dashboard at localhost:8501.",
    "Show Command Center and system health first.",
    "Walk through Finance, Operations, Governance, Support.",
    "Show Assistance, Approvals, Sensitivity, People as human-control layer.",
    "Show Daily Close, Notifications, Delivery Approval, Secure Email, Scheduled Close.",
    "Close with System Integrity, Release Readiness, and pilot questions.",
]


def _check(name, status, detail, severity="critical"):
    return {
        "name": name,
        "status": status,
        "severity": severity,
        "detail": detail,
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


def _format_numbered(items):
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def generate_private_demo_dry_run(conn=None):
    today = date.today().isoformat()
    readiness = generate_release_readiness()
    package, package_path = export_private_demo_package(conn)
    script, script_path = export_private_demo_script(conn)

    checks = []

    if readiness["overall_status"] == "blocked":
        checks.append(
            _check(
                "Release readiness gate",
                "failed",
                "Release readiness is blocked; do not run private demo.",
            )
        )
    elif readiness["overall_status"] == "ready_with_warnings":
        checks.append(
            _check(
                "Release readiness gate",
                "warning",
                "Ready with warnings; name the warning honestly if asked.",
                severity="warning",
            )
        )
    else:
        checks.append(
            _check("Release readiness gate", "passed", "Release readiness is green.")
        )

    package_exists = Path(package_path).exists()
    checks.append(
        _check(
            "Private demo package",
            "passed" if package_exists else "failed",
            str(Path(package_path).relative_to(ROOT_DIR)) if package_exists else "missing",
        )
    )

    script_exists = Path(script_path).exists()
    checks.append(
        _check(
            "Private demo script",
            "passed" if script_exists else "failed",
            str(Path(script_path).relative_to(ROOT_DIR)) if script_exists else "missing",
        )
    )

    missing_pages = [page for page in REQUIRED_DEMO_PAGES if page not in DASHBOARD_PAGES]
    checks.append(
        _check(
            "Required demo pages",
            "passed" if not missing_pages else "failed",
            "present" if not missing_pages else ", ".join(missing_pages),
        )
    )

    boundary_text = " ".join(DO_NOT_SHOW_ITEMS).lower()
    missing_boundaries = [
        marker for marker in REQUIRED_BOUNDARY_MARKERS if marker.lower() not in boundary_text
    ]
    checks.append(
        _check(
            "Demo safety boundary",
            "passed" if not missing_boundaries else "failed",
            "sensitive items excluded" if not missing_boundaries else ", ".join(missing_boundaries),
        )
    )

    checks.append(
        _check(
            "Demo arc coverage",
            "passed" if len(DEMO_ARC) >= 6 else "warning",
            f"{len(DEMO_ARC)} segment(s)",
            severity="warning" if len(DEMO_ARC) < 6 else "critical",
        )
    )

    failed_checks = [check for check in checks if check["status"] == "failed"]
    warning_checks = [check for check in checks if check["status"] == "warning"]

    if failed_checks:
        overall_status = "blocked"
    elif warning_checks:
        overall_status = "ready_with_warnings"
    else:
        overall_status = "ready_for_private_demo"

    return {
        "date": today,
        "overall_status": overall_status,
        "total_checks": len(checks),
        "passed_checks": sum(1 for check in checks if check["status"] == "passed"),
        "warning_checks": len(warning_checks),
        "failed_checks": len(failed_checks),
        "checks": checks,
        "package_path": package_path,
        "script_path": script_path,
        "readiness_status": readiness["overall_status"],
        "readiness_warnings": readiness["warning_checks"],
        "demo_segments": len(script["demo_arc"]),
        "dashboard_pages": package["dashboard_pages"],
        "run_sequence": DEMO_RUN_SEQUENCE,
    }


def export_private_demo_dry_run(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_private_demo_dry_run(conn)
    report_path = REPORTS_DIR / f"private_demo_dry_run_{result['date']}.md"

    content = f"""# Private Demo Dry Run MVP v0.1

Date: {result['date']}

## Dry Run Status

Overall status: {result['overall_status']}
Total checks: {result['total_checks']}
Passed checks: {result['passed_checks']}
Warning checks: {result['warning_checks']}
Failed checks: {result['failed_checks']}
Release readiness source: {result['readiness_status']}

## Checks

{_format_check_rows(result['checks'])}

## Generated Demo Evidence

- Private demo package: {Path(result['package_path']).relative_to(ROOT_DIR)}
- Private demo script: {Path(result['script_path']).relative_to(ROOT_DIR)}

## Demo Run Sequence

{_format_numbered(result['run_sequence'])}

## Dashboard Pages Available

{_format_bullets(result['dashboard_pages'])}

## Operator Note

Run this dry run before a private demo. If the status is blocked, do not present. If it is ready_with_warnings, name the warning clearly and keep the demo within the protected boundary.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "private_demo_dry_run_exported",
            "info" if result["overall_status"] != "blocked" else "warning",
            "Private demo dry run exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "overall_status": result["overall_status"],
                "warning_checks": result["warning_checks"],
                "failed_checks": result["failed_checks"],
            },
        )

    return result, str(report_path)


def print_private_demo_dry_run(conn=None):
    result, report_path = export_private_demo_dry_run(conn)

    print("Private Demo Dry Run:")
    print(f"Date: {result['date']}")
    print(f"Overall status: {result['overall_status']}")
    print(f"Checks: {result['passed_checks']} passed, {result['warning_checks']} warning, {result['failed_checks']} failed")
    print(f"Demo segments: {result['demo_segments']}")
    print(f"Package: {Path(result['package_path']).relative_to(ROOT_DIR)}")
    print(f"Script: {Path(result['script_path']).relative_to(ROOT_DIR)}")
    print(f"Private demo dry run exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
