from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.pilot_day_1_package import generate_pilot_day_1_package
from app.demo.private_pilot_start_gate import generate_private_pilot_start_gate


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"


OWNER_CONFIRMATION_CHECKLIST = [
    "Executive Owner accepts the pilot start gate status and conditions.",
    "Pilot stays limited to one primary workflow.",
    "Day 1 starts with Executive Daily Close and evidence review.",
    "No real external email delivery is enabled during Day 1.",
    "No private database, credentials, secrets, or local artifacts are exposed.",
    "Expansion remains out of scope until later evidence review and owner confirmation.",
]

CONDITION_ACKNOWLEDGEMENTS = [
    "Pilot plan warning context is accepted for a narrow Day 1 start.",
    "Pilot tracker needs_attention status is accepted as a controlled condition.",
    "Missing optional evidence does not block Day 1, but must be named.",
    "Any missing required evidence blocks start or continuation.",
]

DAY_1_CONFIRMATION_ACTIONS = [
    "Review private pilot start gate.",
    "Review Pilot Day 1 operations package.",
    "Confirm the executive owner and pilot operator.",
    "Confirm Day 1 close criteria before ending the first pilot day.",
    "Capture next action for Day 2 before expanding scope.",
]


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _confirmation_status(start_gate, day_1):
    if start_gate["start_gate_status"] == "blocked" or day_1["day_1_status"] == "blocked":
        return "blocked"

    if (
        start_gate["start_gate_status"] == "ready_with_conditions"
        or day_1["day_1_status"] == "ready_with_warnings"
    ):
        return "requires_owner_confirmation"

    return "confirmed_ready_for_day_1"


def _recommendation(status):
    if status == "blocked":
        return "Do not confirm Day 1. Resolve blocked start or Day 1 evidence first."

    if status == "requires_owner_confirmation":
        return "Executive Owner may confirm Day 1 only after accepting the listed conditions and keeping scope narrow."

    return "Day 1 is ready for owner-confirmed start with narrow scope and daily evidence review."


def generate_private_pilot_start_confirmation(conn=None):
    today = date.today().isoformat()
    start_gate = generate_private_pilot_start_gate(conn)
    day_1 = generate_pilot_day_1_package(conn)
    confirmation_status = _confirmation_status(start_gate, day_1)

    return {
        "date": today,
        "confirmation_status": confirmation_status,
        "recommendation": _recommendation(confirmation_status),
        "start_gate_status": start_gate["start_gate_status"],
        "day_1_status": day_1["day_1_status"],
        "pilot_owner": start_gate["pilot_owner"],
        "primary_workflow": start_gate["primary_workflow"],
        "passed_gates": start_gate["passed_gates"],
        "conditional_gates": start_gate["conditional_gates"],
        "blocked_gates": start_gate["blocked_gates"],
        "available_evidence": day_1["available_evidence"],
        "missing_required_evidence": day_1["missing_required_evidence"],
        "missing_optional_evidence": day_1["missing_optional_evidence"],
        "owner_confirmation_checklist": OWNER_CONFIRMATION_CHECKLIST,
        "condition_acknowledgements": CONDITION_ACKNOWLEDGEMENTS,
        "day_1_confirmation_actions": DAY_1_CONFIRMATION_ACTIONS,
        "day_1_next_action": day_1["next_action"],
    }


def export_private_pilot_start_confirmation(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_private_pilot_start_confirmation(conn)
    report_path = REPORTS_DIR / f"private_pilot_start_confirmation_{result['date']}.md"

    content = f"""# Private Pilot Start Confirmation v0.1

Date: {result['date']}

## Start Confirmation Summary

Confirmation status: {result['confirmation_status']}
Recommendation: {result['recommendation']}
Start gate status: {result['start_gate_status']}
Day 1 status: {result['day_1_status']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Passed gates: {result['passed_gates']}
Conditional gates: {result['conditional_gates']}
Blocked gates: {result['blocked_gates']}
Available evidence: {result['available_evidence']}
Missing required evidence: {result['missing_required_evidence']}
Missing optional evidence: {result['missing_optional_evidence']}
Day 1 next action: {result['day_1_next_action']}

## Executive Owner Confirmation Checklist

{_format_bullets(result['owner_confirmation_checklist'])}

## Condition Acknowledgements

{_format_bullets(result['condition_acknowledgements'])}

## Day 1 Confirmation Actions

{_format_bullets(result['day_1_confirmation_actions'])}

## Operator Note

This artifact does not start the pilot automatically. It records the conditions that must be accepted before Day 1 begins and keeps the pilot constrained to one workflow.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "private_pilot_start_confirmation_exported",
            "info" if result["confirmation_status"] != "blocked" else "warning",
            "Private pilot start confirmation exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "confirmation_status": result["confirmation_status"],
                "conditional_gates": result["conditional_gates"],
                "blocked_gates": result["blocked_gates"],
            },
        )

    return result, str(report_path)


def print_private_pilot_start_confirmation(conn=None):
    result, report_path = export_private_pilot_start_confirmation(conn)

    print("Private Pilot Start Confirmation:")
    print(f"Date: {result['date']}")
    print(f"Confirmation status: {result['confirmation_status']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Start gate status: {result['start_gate_status']}")
    print(f"Day 1 status: {result['day_1_status']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Missing required evidence: {result['missing_required_evidence']}")
    print(f"Private pilot start confirmation exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
