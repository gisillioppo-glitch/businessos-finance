from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.pilot_expansion_review_prep import generate_pilot_expansion_review_prep


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

EXPANSION_DECISION_COMMANDS = [
    ("Refresh expansion review prep", "python cli.py pilot-expansion-review-prep"),
    ("Refresh Day 5 continuation", "python cli.py pilot-day-5-narrow-continuation"),
    ("Review pilot tracker", "python cli.py private-pilot-tracker"),
    ("Review exit decision", "python cli.py private-pilot-exit-decision"),
    ("Confirm release readiness", "python cli.py release-readiness"),
]

DECISION_OPTIONS = [
    "maintain_narrow_pilot",
    "deny_expansion_now",
    "prepare_expansion_review",
    "schedule_expansion_review",
    "approve_controlled_expansion",
]

DECISION_RULES = [
    "If required evidence is missing, pause or deny expansion.",
    "If expansion is not approved, maintain narrow pilot or prepare review only.",
    "If owner acknowledgement is pending, do not approve expansion.",
    "If all conditions are met, schedule an expansion review before changing scope.",
    "Controlled expansion requires a separate explicit approval artifact.",
]

DECISION_BOUNDARIES = [
    "This decision does not add a new workflow.",
    "This decision does not enable delivery.",
    "This decision does not override governance conditions.",
    "This decision does not expose private pilot evidence publicly.",
    "Approval of controlled expansion must remain a separate future block.",
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


def _decision_status(prep):
    if prep["missing_required_evidence"] > 0:
        return "blocked_missing_required_evidence"

    if prep["continuation_scope"] != "single_workflow_narrow_pilot":
        return "blocked_scope_not_narrow"

    if prep["pending_condition_count"] > 0:
        return "decision_ready_with_conditions"

    if prep["expansion_prep_status"] == "ready_for_expansion_review":
        return "ready_to_schedule_expansion_review"

    return "decision_ready"


def _recommended_decision(status, prep):
    if status.startswith("blocked"):
        return "deny_expansion_now"

    if prep["expansion_status"] != "approved":
        return "maintain_narrow_pilot"

    if status == "decision_ready_with_conditions":
        return "prepare_expansion_review"

    if status == "ready_to_schedule_expansion_review":
        return "schedule_expansion_review"

    return "maintain_narrow_pilot"


def _decision_rationale(status, prep):
    rationale = []

    if prep["missing_required_evidence"] == 0:
        rationale.append("Required pilot evidence is complete.")
    else:
        rationale.append("Required pilot evidence is missing, so expansion cannot proceed.")

    rationale.append(f"Continuation scope is {prep['continuation_scope']}.")
    rationale.append(f"Expansion status is {prep['expansion_status']}.")
    rationale.append(f"Pending conditions: {prep['pending_condition_count']}.")

    if status == "decision_ready_with_conditions":
        rationale.append("Expansion review can be prepared, but expansion remains blocked until pending conditions are cleared.")
    elif status == "ready_to_schedule_expansion_review":
        rationale.append("Conditions are ready for scheduling an executive expansion review, not automatic expansion.")
    elif status.startswith("blocked"):
        rationale.append("Expansion should be denied or paused until the blocking condition is resolved.")
    else:
        rationale.append("Narrow pilot continuation remains the safest decision.")

    return rationale


def _next_action(recommended_decision):
    if recommended_decision == "deny_expansion_now":
        return "Deny expansion for now and resolve blocking conditions before another review."

    if recommended_decision == "prepare_expansion_review":
        return "Prepare the expansion review packet only; do not change pilot scope."

    if recommended_decision == "schedule_expansion_review":
        return "Schedule an executive expansion review while keeping scope unchanged."

    if recommended_decision == "approve_controlled_expansion":
        return "Create a separate controlled expansion approval artifact before execution."

    return "Maintain narrow pilot operations and continue collecting repeatability evidence."


def generate_pilot_expansion_review_decision(conn=None):
    prep = generate_pilot_expansion_review_prep(conn)
    status = _decision_status(prep)
    recommended_decision = _recommended_decision(status, prep)

    return {
        "date": date.today().isoformat(),
        "decision_status": status,
        "recommended_decision": recommended_decision,
        "pilot_owner": prep["pilot_owner"],
        "primary_workflow": prep["primary_workflow"],
        "continuation_scope": prep["continuation_scope"],
        "expansion_prep_status": prep["expansion_prep_status"],
        "review_recommendation": prep["review_recommendation"],
        "expansion_status": prep["expansion_status"],
        "delivery_status": prep["delivery_status"],
        "pending_condition_count": prep["pending_condition_count"],
        "pending_conditions": prep["pending_conditions"],
        "missing_required_evidence": prep["missing_required_evidence"],
        "highest_exit_risk": prep["highest_exit_risk"],
        "conditions": prep["conditions"],
        "decision_options": DECISION_OPTIONS,
        "decision_rules": DECISION_RULES,
        "commands": EXPANSION_DECISION_COMMANDS,
        "boundaries": DECISION_BOUNDARIES,
        "rationale": _decision_rationale(status, prep),
        "next_action": _next_action(recommended_decision),
    }


def export_pilot_expansion_review_decision(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_expansion_review_decision(conn)
    report_path = REPORTS_DIR / f"pilot_expansion_review_decision_{result['date']}.md"

    content = f"""# Pilot Expansion Review Decision MVP v0.1

Date: {result['date']}

## Expansion Review Decision Summary

Decision status: {result['decision_status']}
Recommended decision: {result['recommended_decision']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Continuation scope: {result['continuation_scope']}
Expansion prep status: {result['expansion_prep_status']}
Review recommendation: {result['review_recommendation']}
Expansion status: {result['expansion_status']}
Delivery status: {result['delivery_status']}
Pending conditions: {result['pending_condition_count']}
Missing required evidence: {result['missing_required_evidence']}
Highest exit risk: {result['highest_exit_risk']}
Next action: {result['next_action']}

## Condition Gate

{_format_condition_rows(result['conditions'])}

## Decision Rationale

{_format_bullets(result['rationale'])}

## Decision Commands

{_format_commands(result['commands'])}

## Decision Options

{_format_bullets(result['decision_options'])}

## Decision Rules

{_format_bullets(result['decision_rules'])}

## Boundaries

{_format_bullets(result['boundaries'])}

## Operator Note

This artifact records the expansion review decision recommendation only. It does not approve controlled expansion, add workflows, enable delivery, or expose private pilot evidence.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "pilot_expansion_review_decision_exported",
            "info" if result["recommended_decision"] == "schedule_expansion_review" else "warning",
            "Pilot expansion review decision exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "decision_status": result["decision_status"],
                "recommended_decision": result["recommended_decision"],
                "pending_condition_count": result["pending_condition_count"],
            },
        )

    return result, str(report_path)


def print_pilot_expansion_review_decision(conn=None):
    result, report_path = export_pilot_expansion_review_decision(conn)

    print("Pilot Expansion Review Decision:")
    print(f"Date: {result['date']}")
    print(f"Decision status: {result['decision_status']}")
    print(f"Recommended decision: {result['recommended_decision']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Continuation scope: {result['continuation_scope']}")
    print(f"Expansion prep status: {result['expansion_prep_status']}")
    print(f"Expansion status: {result['expansion_status']}")
    print(f"Pending conditions: {result['pending_condition_count']}")
    print(f"Missing required evidence: {result['missing_required_evidence']}")
    print(f"Next action: {result['next_action']}")
    print(f"Pilot expansion review decision exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
