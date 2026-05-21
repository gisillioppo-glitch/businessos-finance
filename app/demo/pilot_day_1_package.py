from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.private_pilot_exit_decision import generate_private_pilot_exit_decision
from app.demo.private_pilot_plan import generate_private_pilot_plan
from app.demo.private_pilot_tracker import generate_private_pilot_tracker


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

DAY_1_COMMANDS = [
    ("Pre-flight system check", "python cli.py system-check"),
    ("Release readiness gate", "python cli.py release-readiness"),
    ("Run executive daily close", "python cli.py daily-close"),
    ("Review notification outbox", "python cli.py notifications"),
    ("Review delivery approval", "python cli.py notification-delivery-approval"),
    ("Review pilot tracker", "python cli.py private-pilot-tracker"),
    ("Review pilot exit decision", "python cli.py private-pilot-exit-decision"),
]

DAY_1_EVIDENCE = [
    "reports/system_integrity_YYYY-MM-DD.md",
    "reports/release_readiness_YYYY-MM-DD.md",
    "reports/daily_close_YYYY-MM-DD.md",
    "reports/daily_close_distribution_YYYY-MM-DD.md",
    "reports/command_center_YYYY-MM-DD.md",
    "reports/private_pilot_start_confirmation_YYYY-MM-DD.md",
    "reports/private_pilot_tracker_YYYY-MM-DD.md",
    "reports/private_pilot_exit_decision_YYYY-MM-DD.md",
]

DAY_1_OWNER_REVIEW = [
    "Review the latest private pilot start confirmation packet.",
    "Confirm the pilot owner understands the current tracker status.",
    "Confirm the pilot owner accepts any start conditions before Day 1 begins.",
    "Confirm the recommended decision is advisory and requires owner approval.",
    "Confirm no private data, credentials, or raw database content is shared outside the private environment.",
    "Confirm the next action for Day 2 before ending the Day 1 review.",
]

DAY_1_RISKS = [
    "Dashboard local warning is acceptable only when Streamlit is intentionally off.",
    "Do not expand pilot scope on Day 1 if tracker status is needs_attention or blocked.",
    "Do not enable real email delivery unless delivery approvals and environment credentials are explicitly configured.",
    "Do not expose finance.db, .env, Streamlit secrets, or private reports in the public landing surface.",
]

DAY_1_CLOSE_CRITERIA = [
    "System integrity has no failed checks.",
    "Release readiness has no failed checks.",
    "Daily close artifact exists for the current date.",
    "Pilot tracker has zero missing required evidence.",
    "Executive owner has a documented next action for Day 2.",
]


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _format_commands(commands):
    rows = [
        "| Purpose | Command |",
        "| --- | --- |",
    ]

    for purpose, command in commands:
        rows.append(f"| {purpose} | `{command}` |")

    return "\n".join(rows)


def _latest_report(prefix):
    if not REPORTS_DIR.exists():
        return None

    reports = sorted(
        REPORTS_DIR.glob(f"{prefix}_*.md"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return reports[0] if reports else None


def _extract_value(content, label, default="missing"):
    for line in content.splitlines():
        if line.startswith(f"{label}:"):
            return line.split(":", 1)[1].strip()
    return default


def _start_confirmation_status():
    report = _latest_report("private_pilot_start_confirmation")

    if not report:
        return {
            "status": "missing",
            "report_path": "missing",
            "detail": "No private pilot start confirmation report found.",
        }

    content = report.read_text(encoding="utf-8")
    status = _extract_value(content, "Confirmation status")
    recommendation = _extract_value(content, "Recommendation")

    return {
        "status": status,
        "report_path": str(report.relative_to(ROOT_DIR)),
        "detail": recommendation,
    }


def _day_1_status(tracker, exit_decision):
    if tracker["tracker_status"] == "blocked" or tracker["missing_required"] > 0:
        return "blocked"

    if tracker["tracker_status"] == "needs_attention" or "warnings" in exit_decision["decision_status"]:
        return "ready_with_warnings"

    return "ready"


def _next_action(day_1_status, exit_decision):
    if day_1_status == "blocked":
        return "Resolve missing required evidence before starting the Day 1 pilot review."

    if day_1_status == "ready_with_warnings":
        return "Start Day 1 with Executive Daily Close, then confirm warnings with the executive owner before expanding scope."

    return "Start Day 1 and keep the pilot narrowed to the approved primary workflow."


def generate_pilot_day_1_package(conn=None):
    plan = generate_private_pilot_plan(conn)
    tracker = generate_private_pilot_tracker(conn)
    exit_decision = generate_private_pilot_exit_decision(conn)
    start_confirmation = _start_confirmation_status()
    day_1_status = _day_1_status(tracker, exit_decision)

    return {
        "date": date.today().isoformat(),
        "day_1_status": day_1_status,
        "start_confirmation_status": start_confirmation["status"],
        "start_confirmation_report": start_confirmation["report_path"],
        "start_confirmation_detail": start_confirmation["detail"],
        "pilot_owner": plan["pilot_owner"],
        "primary_workflow": plan["primary_workflow"],
        "plan_status": plan["plan_status"],
        "tracker_status": tracker["tracker_status"],
        "exit_decision_status": exit_decision["decision_status"],
        "recommended_exit_decision": exit_decision["recommended_decision"],
        "highest_exit_risk": exit_decision["highest_exit_risk"],
        "missing_required_evidence": tracker["missing_required"],
        "missing_optional_evidence": tracker["missing_optional"],
        "available_evidence": tracker["available_evidence"],
        "commands": DAY_1_COMMANDS,
        "expected_evidence": DAY_1_EVIDENCE,
        "owner_review": DAY_1_OWNER_REVIEW,
        "risks": DAY_1_RISKS,
        "close_criteria": DAY_1_CLOSE_CRITERIA,
        "next_action": _next_action(day_1_status, exit_decision),
    }


def export_pilot_day_1_package(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_day_1_package(conn)
    report_path = REPORTS_DIR / f"pilot_day_1_package_{result['date']}.md"

    content = f"""# Pilot Day 1 Operations Package MVP v0.1

Date: {result['date']}

## Day 1 Summary

Day 1 status: {result['day_1_status']}
Start confirmation status: {result['start_confirmation_status']}
Start confirmation report: {result['start_confirmation_report']}
Start confirmation detail: {result['start_confirmation_detail']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Plan status: {result['plan_status']}
Tracker status: {result['tracker_status']}
Exit decision status: {result['exit_decision_status']}
Recommended exit decision: {result['recommended_exit_decision']}
Highest exit risk: {result['highest_exit_risk']}
Available evidence: {result['available_evidence']}
Missing required evidence: {result['missing_required_evidence']}
Missing optional evidence: {result['missing_optional_evidence']}
Next action: {result['next_action']}

## Day 1 Command Runbook

{_format_commands(result['commands'])}

## Expected Evidence

{_format_bullets(result['expected_evidence'])}

## Executive Owner Review

{_format_bullets(result['owner_review'])}

## Day 1 Risks and Boundaries

{_format_bullets(result['risks'])}

## Day 1 Close Criteria

{_format_bullets(result['close_criteria'])}

## Operator Note

Day 1 is about proving a controlled operating rhythm. Do not expand scope, enable real delivery, or expose private artifacts until the executive owner confirms the warnings and next action.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "pilot_day_1_package_exported",
            "info" if result["day_1_status"] == "ready" else "warning",
            "Pilot Day 1 operations package exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "day_1_status": result["day_1_status"],
                "primary_workflow": result["primary_workflow"],
                "recommended_exit_decision": result["recommended_exit_decision"],
            },
        )

    return result, str(report_path)


def print_pilot_day_1_package(conn=None):
    result, report_path = export_pilot_day_1_package(conn)

    print("Pilot Day 1 Operations Package:")
    print(f"Date: {result['date']}")
    print(f"Day 1 status: {result['day_1_status']}")
    print(f"Start confirmation status: {result['start_confirmation_status']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Tracker status: {result['tracker_status']}")
    print(f"Recommended exit decision: {result['recommended_exit_decision']}")
    print(f"Missing required evidence: {result['missing_required_evidence']}")
    print(f"Next action: {result['next_action']}")
    print(f"Pilot Day 1 package exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
