from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.pilot_day_4_owner_confirmation import generate_pilot_day_4_owner_confirmation


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

DAY_5_CONTINUATION_COMMANDS = [
    ("Refresh owner confirmation", "python cli.py pilot-day-4-owner-confirmation"),
    ("Review pilot start confirmation", "python cli.py private-pilot-start-confirmation"),
    ("Run daily close", "python cli.py daily-close"),
    ("Refresh evidence index", "python cli.py evidence-index"),
    ("Review notifications", "python cli.py notifications"),
    ("Review delivery approval gate", "python cli.py notification-delivery-approval"),
    ("Confirm release readiness", "python cli.py release-readiness"),
]

DAY_5_OPERATING_RHYTHM = [
    "Continue with Executive Daily Close as the only active pilot workflow.",
    "Confirm the linked start confirmation state before collecting Day 5 repeatability evidence.",
    "Review Day 4 warning acknowledgement before presenting any expansion option.",
    "Observe whether the same evidence package can be repeated without missing required evidence.",
    "Keep notification delivery approval-gated and external sending disabled unless explicitly approved.",
    "Record any new owner questions as evidence for a later expansion review package.",
]

DAY_5_EVIDENCE_TO_OBSERVE = [
    "Daily Close generated successfully.",
    "Start confirmation state remains visible in the continuation package.",
    "Evidence Index remains complete.",
    "Notification outbox remains valid.",
    "Release Readiness remains failed-check free.",
    "Owner warning acknowledgement remains pending or manually confirmed outside the system.",
]

DAY_5_BOUNDARIES = [
    "Do not add a second workflow during Day 5.",
    "Do not treat Day 5 continuation as expansion approval.",
    "Do not enable external email delivery without approved controls.",
    "Do not expose private reports or local artifacts outside the private environment.",
]

DAY_5_NEXT_DECISION_POINTS = [
    "Continue narrow pilot if warnings remain stable and evidence remains complete.",
    "Pause if required evidence becomes missing.",
    "Prepare expansion review only after explicit owner acknowledgement.",
    "Escalate to governance if new sensitive findings appear during continuation.",
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


def _day_5_status(day_4):
    if day_4["day_4_status"] == "blocked" or day_4["missing_required_evidence"] > 0:
        return "blocked"

    if day_4.get("start_confirmation_status") == "blocked":
        return "blocked"

    if day_4["allowed_continuation"] == "continue_narrow_pilot_only":
        return "continue_narrow_pilot"

    if day_4["allowed_continuation"] == "prepare_expansion_review_only":
        return "prepare_expansion_review_only"

    return "continue_with_owner_confirmation"


def _continuation_scope(status):
    if status == "blocked":
        return "paused_until_evidence_restored"

    if status == "prepare_expansion_review_only":
        return "expansion_review_preparation_only"

    return "single_workflow_narrow_pilot"


def _next_action(status):
    if status == "blocked":
        return "Pause Day 5 and restore required evidence before continuing."

    if status == "prepare_expansion_review_only":
        return "Prepare a separate expansion review package without expanding operational scope."

    return "Run Day 5 narrow pilot rhythm and collect repeatability evidence for the executive owner."


def generate_pilot_day_5_narrow_continuation(conn=None):
    day_4 = generate_pilot_day_4_owner_confirmation(conn)
    status = _day_5_status(day_4)

    return {
        "date": date.today().isoformat(),
        "day_5_status": status,
        "continuation_scope": _continuation_scope(status),
        "pilot_owner": day_4["pilot_owner"],
        "primary_workflow": day_4["primary_workflow"],
        "day_4_status": day_4["day_4_status"],
        "start_confirmation_status": day_4.get("start_confirmation_status", "missing"),
        "start_confirmation_report": day_4.get("start_confirmation_report", "not_available"),
        "start_confirmation_detail": day_4.get("start_confirmation_detail", "No start confirmation detail recorded."),
        "owner_confirmation_mode": day_4["owner_confirmation_mode"],
        "allowed_continuation": day_4["allowed_continuation"],
        "expansion_status": day_4["expansion_status"],
        "delivery_status": day_4["delivery_status"],
        "missing_required_evidence": day_4["missing_required_evidence"],
        "highest_exit_risk": day_4["highest_exit_risk"],
        "commands": DAY_5_CONTINUATION_COMMANDS,
        "operating_rhythm": DAY_5_OPERATING_RHYTHM,
        "evidence_to_observe": DAY_5_EVIDENCE_TO_OBSERVE,
        "boundaries": DAY_5_BOUNDARIES,
        "next_decision_points": DAY_5_NEXT_DECISION_POINTS,
        "next_action": _next_action(status),
    }


def export_pilot_day_5_narrow_continuation(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_day_5_narrow_continuation(conn)
    report_path = REPORTS_DIR / f"pilot_day_5_narrow_continuation_{result['date']}.md"

    content = f"""# Pilot Day 5 Narrow Pilot Continuation MVP v0.1

Date: {result['date']}

## Day 5 Summary

Day 5 status: {result['day_5_status']}
Continuation scope: {result['continuation_scope']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Day 4 status: {result['day_4_status']}
Start confirmation status: {result['start_confirmation_status']}
Start confirmation report: {result['start_confirmation_report']}
Start confirmation detail: {result['start_confirmation_detail']}
Owner confirmation mode: {result['owner_confirmation_mode']}
Allowed continuation: {result['allowed_continuation']}
Expansion status: {result['expansion_status']}
Delivery status: {result['delivery_status']}
Missing required evidence: {result['missing_required_evidence']}
Highest exit risk: {result['highest_exit_risk']}
Next action: {result['next_action']}

## Day 5 Continuation Commands

{_format_commands(result['commands'])}

## Day 5 Operating Rhythm

{_format_bullets(result['operating_rhythm'])}

## Evidence To Observe

{_format_bullets(result['evidence_to_observe'])}

## Day 5 Boundaries

{_format_bullets(result['boundaries'])}

## Next Decision Points

{_format_bullets(result['next_decision_points'])}

## Operator Note

Day 5 continues the pilot in a single-workflow narrow mode. It may collect evidence for a later expansion review, but it does not approve expansion or change delivery controls.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "pilot_day_5_narrow_continuation_exported",
            "info" if result["day_5_status"] in ["continue_narrow_pilot", "continue_with_owner_confirmation"] else "warning",
            "Pilot Day 5 narrow continuation exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "day_5_status": result["day_5_status"],
                "continuation_scope": result["continuation_scope"],
                "expansion_status": result["expansion_status"],
            },
        )

    return result, str(report_path)


def print_pilot_day_5_narrow_continuation(conn=None):
    result, report_path = export_pilot_day_5_narrow_continuation(conn)

    print("Pilot Day 5 Narrow Pilot Continuation:")
    print(f"Date: {result['date']}")
    print(f"Day 5 status: {result['day_5_status']}")
    print(f"Continuation scope: {result['continuation_scope']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Day 4 status: {result['day_4_status']}")
    print(f"Start confirmation status: {result['start_confirmation_status']}")
    print(f"Allowed continuation: {result['allowed_continuation']}")
    print(f"Expansion status: {result['expansion_status']}")
    print(f"Delivery status: {result['delivery_status']}")
    print(f"Missing required evidence: {result['missing_required_evidence']}")
    print(f"Next action: {result['next_action']}")
    print(f"Pilot Day 5 narrow continuation exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
