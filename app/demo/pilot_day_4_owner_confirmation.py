from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.pilot_day_3_evidence_review import generate_pilot_day_3_evidence_review


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

DAY_4_CONFIRMATION_COMMANDS = [
    ("Refresh Day 3 evidence review", "python cli.py pilot-day-3-evidence-review"),
    ("Refresh pilot tracker", "python cli.py private-pilot-tracker"),
    ("Refresh exit decision", "python cli.py private-pilot-exit-decision"),
    ("Review evidence index", "python cli.py evidence-index"),
    ("Confirm release readiness", "python cli.py release-readiness"),
]

DAY_4_OWNER_CONFIRMATIONS = [
    "The executive owner has reviewed Day 3 evidence status.",
    "The executive owner understands the current warning context.",
    "The executive owner accepts continuing in narrow pilot mode only.",
    "The executive owner understands expansion remains blocked until a separate approval.",
    "The executive owner confirms no external delivery should be enabled without approved controls.",
]

DAY_4_BOUNDARIES = [
    "Owner confirmation does not approve expansion.",
    "Owner confirmation does not enable external email delivery.",
    "Owner confirmation does not expose private pilot artifacts.",
    "Owner confirmation does not override missing required evidence.",
]

DAY_4_NEXT_REVIEW_ITEMS = [
    "Confirm whether warnings are stable after owner acknowledgement.",
    "Confirm whether Day 5 should continue the narrow pilot rhythm.",
    "Confirm whether an expansion review package should be prepared separately.",
    "Confirm whether any new risks require support, governance, or approval follow-up.",
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


def _owner_confirmation_status(day_3):
    if day_3["day_3_status"] == "blocked" or day_3["missing_required_evidence"] > 0:
        return "blocked"

    if day_3["evidence_recommendation"] == "continue_narrow_pilot":
        return "owner_confirmation_required"

    if day_3["evidence_recommendation"] == "prepare_expansion_review":
        return "expansion_review_confirmation_required"

    return "owner_confirmation_ready"


def _allowed_continuation(status):
    if status == "blocked":
        return "pause_until_required_evidence_is_resolved"

    if status == "expansion_review_confirmation_required":
        return "prepare_expansion_review_only"

    return "continue_narrow_pilot_only"


def _next_action(status):
    if status == "blocked":
        return "Pause owner confirmation and resolve required evidence before continuing."

    if status == "expansion_review_confirmation_required":
        return "Collect explicit owner confirmation before preparing a separate expansion review package."

    if status == "owner_confirmation_required":
        return "Collect executive owner acknowledgement of warnings before continuing Day 5 narrow pilot rhythm."

    return "Record owner confirmation and continue the narrow pilot rhythm."


def generate_pilot_day_4_owner_confirmation(conn=None):
    day_3 = generate_pilot_day_3_evidence_review(conn)
    status = _owner_confirmation_status(day_3)

    return {
        "date": date.today().isoformat(),
        "day_4_status": status,
        "owner_confirmation_mode": "manual_executive_acknowledgement",
        "pilot_owner": day_3["pilot_owner"],
        "primary_workflow": day_3["primary_workflow"],
        "day_3_status": day_3["day_3_status"],
        "evidence_recommendation": day_3["evidence_recommendation"],
        "allowed_continuation": _allowed_continuation(status),
        "expansion_status": "not_approved",
        "delivery_status": "approval_gated",
        "missing_required_evidence": day_3["missing_required_evidence"],
        "highest_exit_risk": day_3["highest_exit_risk"],
        "commands": DAY_4_CONFIRMATION_COMMANDS,
        "owner_confirmations": DAY_4_OWNER_CONFIRMATIONS,
        "boundaries": DAY_4_BOUNDARIES,
        "next_review_items": DAY_4_NEXT_REVIEW_ITEMS,
        "next_action": _next_action(status),
    }


def export_pilot_day_4_owner_confirmation(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_day_4_owner_confirmation(conn)
    report_path = REPORTS_DIR / f"pilot_day_4_owner_confirmation_{result['date']}.md"

    content = f"""# Pilot Day 4 Owner Confirmation MVP v0.1

Date: {result['date']}

## Day 4 Summary

Day 4 status: {result['day_4_status']}
Owner confirmation mode: {result['owner_confirmation_mode']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Day 3 status: {result['day_3_status']}
Evidence recommendation: {result['evidence_recommendation']}
Allowed continuation: {result['allowed_continuation']}
Expansion status: {result['expansion_status']}
Delivery status: {result['delivery_status']}
Missing required evidence: {result['missing_required_evidence']}
Highest exit risk: {result['highest_exit_risk']}
Next action: {result['next_action']}

## Day 4 Confirmation Commands

{_format_commands(result['commands'])}

## Executive Owner Confirmation Checklist

{_format_bullets(result['owner_confirmations'])}

## Day 4 Boundaries

{_format_bullets(result['boundaries'])}

## Next Review Items

{_format_bullets(result['next_review_items'])}

## Operator Note

Day 4 creates an owner confirmation packet. It records the confirmation requirements for the executive owner, but it does not approve expansion, enable delivery, or expose private artifacts.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "pilot_day_4_owner_confirmation_exported",
            "info" if result["day_4_status"] == "owner_confirmation_ready" else "warning",
            "Pilot Day 4 owner confirmation packet exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "day_4_status": result["day_4_status"],
                "allowed_continuation": result["allowed_continuation"],
                "expansion_status": result["expansion_status"],
            },
        )

    return result, str(report_path)


def print_pilot_day_4_owner_confirmation(conn=None):
    result, report_path = export_pilot_day_4_owner_confirmation(conn)

    print("Pilot Day 4 Owner Confirmation:")
    print(f"Date: {result['date']}")
    print(f"Day 4 status: {result['day_4_status']}")
    print(f"Owner confirmation mode: {result['owner_confirmation_mode']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Day 3 status: {result['day_3_status']}")
    print(f"Evidence recommendation: {result['evidence_recommendation']}")
    print(f"Allowed continuation: {result['allowed_continuation']}")
    print(f"Expansion status: {result['expansion_status']}")
    print(f"Missing required evidence: {result['missing_required_evidence']}")
    print(f"Next action: {result['next_action']}")
    print(f"Pilot Day 4 owner confirmation exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
