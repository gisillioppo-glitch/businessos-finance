from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.pilot_day_5_narrow_continuation import generate_pilot_day_5_narrow_continuation


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

EXPANSION_PREP_COMMANDS = [
    ("Refresh Day 5 continuation", "python cli.py pilot-day-5-narrow-continuation"),
    ("Refresh owner confirmation", "python cli.py pilot-day-4-owner-confirmation"),
    ("Review pilot start confirmation", "python cli.py private-pilot-start-confirmation"),
    ("Refresh pilot tracker", "python cli.py private-pilot-tracker"),
    ("Refresh exit decision", "python cli.py private-pilot-exit-decision"),
    ("Review evidence index", "python cli.py evidence-index"),
    ("Confirm release readiness", "python cli.py release-readiness"),
]

EXPANSION_REVIEW_CONDITIONS = [
    "Required pilot evidence remains complete.",
    "Pilot start confirmation state remains visible and not blocked.",
    "Narrow pilot has repeated the primary workflow without adding scope.",
    "Executive owner has acknowledged warning context.",
    "Expansion approval is requested and approved separately.",
    "Delivery controls remain approval-gated before any wider rollout.",
    "No private artifacts are exposed outside the private environment.",
]

EXPANSION_REVIEW_EVIDENCE = [
    "Private pilot start confirmation packet.",
    "Pilot Day 3 evidence review report.",
    "Pilot Day 4 owner confirmation packet.",
    "Pilot Day 5 narrow continuation report.",
    "Latest private pilot tracker.",
    "Latest private pilot exit decision.",
    "Latest release readiness report.",
    "Latest executive evidence index.",
]

EXPANSION_REVIEW_BOUNDARIES = [
    "Expansion review preparation is not expansion approval.",
    "Do not add a second workflow from this artifact alone.",
    "Do not enable external email delivery from this artifact alone.",
    "Do not bypass owner confirmation or governance approval.",
    "Do not expose private pilot materials publicly.",
]

EXPANSION_REVIEW_QUESTIONS = [
    "Which adjacent workflow would produce the clearest executive value with the least risk?",
    "Which warning must be acknowledged or resolved before expansion?",
    "What evidence proves the current workflow is repeatable?",
    "Who owns the expansion decision and approval boundary?",
    "What would cause the pilot to pause instead of expand?",
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


def _format_condition_rows(conditions):
    rows = [
        "| Condition | Status | Detail |",
        "| --- | --- | --- |",
    ]

    for condition in conditions:
        rows.append(f"| {condition['condition']} | {condition['status']} | {condition['detail']} |")

    return "\n".join(rows)


def _condition_statuses(day_5):
    required_complete = day_5["missing_required_evidence"] == 0
    start_confirmation_status = day_5.get("start_confirmation_status", "missing")
    start_confirmation_clear = start_confirmation_status != "blocked"
    narrow_continuation = day_5["day_5_status"] in ["continue_narrow_pilot", "continue_with_owner_confirmation"]
    owner_acknowledged = day_5["day_4_status"] == "owner_confirmation_ready"
    expansion_approved = day_5["expansion_status"] == "approved"
    delivery_gated = day_5["delivery_status"] == "approval_gated"

    return [
        {
            "condition": "Required pilot evidence",
            "status": "met" if required_complete else "missing",
            "detail": "No required evidence is missing." if required_complete else "Required evidence must be restored before review.",
        },
        {
            "condition": "Start confirmation state",
            "status": "met" if start_confirmation_clear else "blocked",
            "detail": f"Start confirmation status is {start_confirmation_status}.",
        },
        {
            "condition": "Narrow pilot repeatability",
            "status": "met" if narrow_continuation else "blocked",
            "detail": f"Day 5 status is {day_5['day_5_status']}.",
        },
        {
            "condition": "Owner warning acknowledgement",
            "status": "pending" if not owner_acknowledged else "met",
            "detail": f"Day 4 status is {day_5['day_4_status']}.",
        },
        {
            "condition": "Expansion approval",
            "status": "not_approved" if not expansion_approved else "met",
            "detail": f"Expansion status is {day_5['expansion_status']}.",
        },
        {
            "condition": "Delivery controls",
            "status": "met" if delivery_gated else "review_required",
            "detail": f"Delivery status is {day_5['delivery_status']}.",
        },
    ]


def _missing_or_pending_conditions(conditions):
    return [
        condition
        for condition in conditions
        if condition["status"] in ["missing", "blocked", "pending", "not_approved", "review_required"]
    ]


def _expansion_prep_status(day_5, conditions):
    if day_5["missing_required_evidence"] > 0:
        return "blocked_missing_required_evidence"

    if day_5.get("start_confirmation_status") == "blocked":
        return "blocked_start_confirmation"

    if day_5["continuation_scope"] != "single_workflow_narrow_pilot":
        return "blocked_scope_not_narrow"

    pending = _missing_or_pending_conditions(conditions)

    if pending:
        return "prep_ready_with_conditions"

    return "ready_for_expansion_review"


def _review_recommendation(status):
    if status.startswith("blocked"):
        return "pause_expansion_review_preparation"

    if status == "prep_ready_with_conditions":
        return "prepare_review_packet_only"

    return "schedule_expansion_review"


def _next_action(status):
    if status == "blocked_missing_required_evidence":
        return "Pause expansion review preparation and restore required pilot evidence."

    if status == "blocked_start_confirmation":
        return "Pause expansion review preparation and resolve the blocked start confirmation state."

    if status == "blocked_scope_not_narrow":
        return "Return to a single-workflow narrow pilot before preparing expansion review."

    if status == "prep_ready_with_conditions":
        return "Prepare the expansion review packet, but keep expansion not approved until pending conditions are cleared."

    return "Schedule an executive expansion review without changing operational scope yet."


def generate_pilot_expansion_review_prep(conn=None):
    day_5 = generate_pilot_day_5_narrow_continuation(conn)
    conditions = _condition_statuses(day_5)
    pending_conditions = _missing_or_pending_conditions(conditions)
    status = _expansion_prep_status(day_5, conditions)

    return {
        "date": date.today().isoformat(),
        "expansion_prep_status": status,
        "review_recommendation": _review_recommendation(status),
        "pilot_owner": day_5["pilot_owner"],
        "primary_workflow": day_5["primary_workflow"],
        "continuation_scope": day_5["continuation_scope"],
        "day_5_status": day_5["day_5_status"],
        "start_confirmation_status": day_5.get("start_confirmation_status", "missing"),
        "start_confirmation_report": day_5.get("start_confirmation_report", "not_available"),
        "start_confirmation_detail": day_5.get("start_confirmation_detail", "No start confirmation detail recorded."),
        "allowed_continuation": day_5["allowed_continuation"],
        "expansion_status": day_5["expansion_status"],
        "delivery_status": day_5["delivery_status"],
        "missing_required_evidence": day_5["missing_required_evidence"],
        "highest_exit_risk": day_5["highest_exit_risk"],
        "conditions": conditions,
        "pending_condition_count": len(pending_conditions),
        "pending_conditions": [condition["condition"] for condition in pending_conditions],
        "commands": EXPANSION_PREP_COMMANDS,
        "review_conditions": EXPANSION_REVIEW_CONDITIONS,
        "review_evidence": EXPANSION_REVIEW_EVIDENCE,
        "boundaries": EXPANSION_REVIEW_BOUNDARIES,
        "review_questions": EXPANSION_REVIEW_QUESTIONS,
        "next_action": _next_action(status),
    }


def export_pilot_expansion_review_prep(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_expansion_review_prep(conn)
    report_path = REPORTS_DIR / f"pilot_expansion_review_prep_{result['date']}.md"

    content = f"""# Pilot Expansion Review Preparation MVP v0.1

Date: {result['date']}

## Expansion Review Preparation Summary

Expansion prep status: {result['expansion_prep_status']}
Review recommendation: {result['review_recommendation']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Continuation scope: {result['continuation_scope']}
Day 5 status: {result['day_5_status']}
Start confirmation status: {result['start_confirmation_status']}
Start confirmation report: {result['start_confirmation_report']}
Start confirmation detail: {result['start_confirmation_detail']}
Allowed continuation: {result['allowed_continuation']}
Expansion status: {result['expansion_status']}
Delivery status: {result['delivery_status']}
Missing required evidence: {result['missing_required_evidence']}
Highest exit risk: {result['highest_exit_risk']}
Pending conditions: {result['pending_condition_count']}
Next action: {result['next_action']}

## Condition Gate

{_format_condition_rows(result['conditions'])}

## Preparation Commands

{_format_commands(result['commands'])}

## Expansion Review Conditions

{_format_bullets(result['review_conditions'])}

## Evidence To Include

{_format_bullets(result['review_evidence'])}

## Review Questions

{_format_bullets(result['review_questions'])}

## Boundaries

{_format_bullets(result['boundaries'])}

## Operator Note

This artifact prepares an executive expansion review package only. It does not approve expansion, add workflows, enable delivery, or expose private pilot materials.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "pilot_expansion_review_prep_exported",
            "info" if result["expansion_prep_status"] == "ready_for_expansion_review" else "warning",
            "Pilot expansion review preparation exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "expansion_prep_status": result["expansion_prep_status"],
                "review_recommendation": result["review_recommendation"],
                "pending_condition_count": result["pending_condition_count"],
            },
        )

    return result, str(report_path)


def print_pilot_expansion_review_prep(conn=None):
    result, report_path = export_pilot_expansion_review_prep(conn)

    print("Pilot Expansion Review Preparation:")
    print(f"Date: {result['date']}")
    print(f"Expansion prep status: {result['expansion_prep_status']}")
    print(f"Review recommendation: {result['review_recommendation']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Continuation scope: {result['continuation_scope']}")
    print(f"Day 5 status: {result['day_5_status']}")
    print(f"Start confirmation status: {result['start_confirmation_status']}")
    print(f"Expansion status: {result['expansion_status']}")
    print(f"Pending conditions: {result['pending_condition_count']}")
    print(f"Missing required evidence: {result['missing_required_evidence']}")
    print(f"Next action: {result['next_action']}")
    print(f"Pilot expansion review prep exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
