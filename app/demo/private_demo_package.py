from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.readiness.release_readiness import generate_release_readiness


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"


DEMO_COMMANDS = [
    ("Release readiness gate", "python cli.py release-readiness"),
    ("System integrity check", "python cli.py system-check"),
    ("Executive daily close", "python cli.py daily-close"),
    ("Notification outbox", "python cli.py notifications"),
    ("Notification delivery approval", "python cli.py notification-delivery-approval"),
    ("Secure email delivery", "python cli.py secure-email-delivery"),
    ("Scheduled close status", "python cli.py daily-close-schedule"),
    ("Private dashboard", "streamlit run app/dashboard/main.py"),
    ("Private pilot tracker", "python cli.py private-pilot-tracker"),
    ("Private pilot exit decision", "python cli.py private-pilot-exit-decision"),
    ("Pilot Day 1 package", "python cli.py pilot-day-1-package"),
    ("Pilot Day 2 rhythm", "python cli.py pilot-day-2-rhythm"),
    ("Pilot Day 3 evidence review", "python cli.py pilot-day-3-evidence-review"),
    ("Full smoke test", "python scripts/smoke_test.py"),
]

DASHBOARD_PAGES = [
    "Dashboard",
    "Alerts",
    "Finance",
    "Operations",
    "Governance",
    "Sensitivity",
    "Support",
    "Assistance",
    "Approvals",
    "Daily Close",
    "Notifications",
    "Delivery Approval",
    "Secure Email",
    "Scheduled Close",
    "System Integrity",
    "Demo Readiness",
    "Pilot Plan",
    "Pilot Tracker",
    "Pilot Exit",
    "Pilot Day 1",
    "Pilot Day 2",
    "People",
]

DEMO_FLOW = [
    "Open with the public/private boundary and the institutional operating system positioning.",
    "Show the private Dashboard and Command Center as the executive control surface.",
    "Walk through Finance, Operations, Governance, Support, Alerts, and Approvals as connected operating layers.",
    "Show Daily Close and Evidence Index as the executive close-of-day package.",
    "Show Notifications and Scheduled Close as controlled automation readiness.",
    "Close with System Integrity and Release Readiness as the demo quality gate.",
]

SHOW_ITEMS = [
    "Private dashboard navigation and executive KPIs.",
    "Command Center report and highest-risk summary.",
    "Daily Close, Evidence Index, and Daily Close Distribution reports.",
    "Notification Outbox status counts and read-only dashboard view.",
    "Notification Delivery Approval report before any external delivery adapter.",
    "Secure Email Delivery report in disabled or dry-run mode unless credentials are explicitly enabled.",
    "Scheduled Close status and last scheduler result.",
    "System Integrity and Release Readiness reports.",
]

DO_NOT_SHOW_ITEMS = [
    "finance.db contents or raw database internals.",
    ".env, Streamlit secrets, credentials, tokens, or local machine paths beyond report names.",
    "Private repository settings or implementation details that are not part of the demo story.",
    "Real email delivery, because external sending is intentionally not enabled yet.",
    "Untracked local artifacts such as BussinessOS Avance.pdf.",
]

KNOWN_RISKS = [
    "Dashboard authentication is still local MVP auth; use private environment configuration before external access.",
    "Secure Email Delivery Adapter defaults to disabled/dry-run and requires explicit environment configuration before real sending.",
    "Release Readiness may show a Git working tree warning while an active development block is uncommitted.",
    "Lead intake requires a real external form endpoint before production capture.",
    "The private dashboard is not a public production deployment target.",
]

PRE_DEMO_CHECKLIST = [
    "Run python cli.py system-check.",
    "Run python cli.py release-readiness.",
    "Run python scripts/smoke_test.py when time allows.",
    "Confirm the private dashboard responds at http://localhost:8501.",
    "Confirm Git status has no unexpected changes beyond BussinessOS Avance.pdf.",
    "Confirm finance.db, .env, and Streamlit secrets are not in the public surface.",
]


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


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _format_numbered(items):
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def _format_commands(commands):
    rows = [
        "| Purpose | Command |",
        "| --- | --- |",
    ]

    for purpose, command in commands:
        rows.append(f"| {purpose} | `{command}` |")

    return "\n".join(rows)


def _format_report_links():
    report_prefixes = [
        ("Release Readiness", "release_readiness"),
        ("System Integrity", "system_integrity"),
        ("Daily Close", "daily_close"),
        ("Daily Close Distribution", "daily_close_distribution"),
        ("Executive Evidence Index", "executive_evidence_index"),
        ("Command Center", "command_center"),
    ]

    rows = [
        "| Artifact | Latest report |",
        "| --- | --- |",
    ]

    for label, prefix in report_prefixes:
        report = _latest_report(prefix)
        detail = str(report.relative_to(ROOT_DIR)) if report else "missing"
        rows.append(f"| {label} | {detail} |")

    return "\n".join(rows)


def generate_private_demo_package():
    readiness = generate_release_readiness()

    return {
        "date": date.today().isoformat(),
        "readiness": readiness,
        "demo_commands": DEMO_COMMANDS,
        "dashboard_pages": DASHBOARD_PAGES,
        "demo_flow": DEMO_FLOW,
        "show_items": SHOW_ITEMS,
        "do_not_show_items": DO_NOT_SHOW_ITEMS,
        "known_risks": KNOWN_RISKS,
        "pre_demo_checklist": PRE_DEMO_CHECKLIST,
    }


def export_private_demo_package(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    package = generate_private_demo_package()
    readiness = package["readiness"]
    report_path = REPORTS_DIR / f"private_demo_package_{package['date']}.md"

    content = f"""# Private Demo Package MVP v0.1

Date: {package['date']}

## System Summary

BusinessOS is a private institutional AI operating system that connects Finance, Operations, Governance, Support, Command Center, Executive Alerts, Evidence, Daily Close, Notifications, Scheduled Close, System Integrity, and Release Readiness.

## Demo Readiness

Overall status: {readiness['overall_status']}
Total checks: {readiness['total_checks']}
Passed checks: {readiness['passed_checks']}
Warning checks: {readiness['warning_checks']}
Failed checks: {readiness['failed_checks']}

## Demo Commands

{_format_commands(package['demo_commands'])}

## Dashboard Pages To Show

{_format_bullets(package['dashboard_pages'])}

## Recommended Demo Flow

{_format_numbered(package['demo_flow'])}

## Show

{_format_bullets(package['show_items'])}

## Do Not Show

{_format_bullets(package['do_not_show_items'])}

## Known Risks

{_format_bullets(package['known_risks'])}

## Pre-Demo Checklist

{_format_bullets(package['pre_demo_checklist'])}

## Latest Demo Artifacts

{_format_report_links()}
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "private_demo_package_exported",
            "info" if readiness["overall_status"] != "blocked" else "warning",
            "Private demo package exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "readiness_status": readiness["overall_status"],
                "warning_checks": readiness["warning_checks"],
                "failed_checks": readiness["failed_checks"],
            },
        )

    return package, str(report_path)


def print_private_demo_package(conn=None):
    package, report_path = export_private_demo_package(conn)
    readiness = package["readiness"]

    print("Private Demo Package:")
    print(f"Date: {package['date']}")
    print(f"Readiness status: {readiness['overall_status']}")
    print(f"Readiness checks: {readiness['passed_checks']} passed, {readiness['warning_checks']} warning, {readiness['failed_checks']} failed")
    print("Primary demo command: streamlit run app/dashboard/main.py")
    print(f"Private demo package exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return package

