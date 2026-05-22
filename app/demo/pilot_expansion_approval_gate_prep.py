from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.pilot_expansion_review_decision import generate_pilot_expansion_review_decision
from app.demo.pilot_owner_confirmation_chain_index import generate_pilot_owner_confirmation_chain_index


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

APPROVAL_GATE_COMMANDS = [
    ("Refresh expansion decision", "python cli.py pilot-expansion-review-decision"),
    ("Refresh confirmation chain", "python cli.py pilot-owner-confirmation-chain"),
    ("Review release readiness", "python cli.py release-readiness"),
    ("Review delivery approval gate", "python cli.py notification-delivery-approval"),
    ("Review secure email dry run", "python cli.py secure-email-delivery"),
]

APPROVAL_GATE_BOUNDARIES = [
    "This gate prep does not approve controlled expansion.",
    "This gate prep does not add a workflow.",
    "This gate prep does not enable external delivery.",
    "This gate prep does not bypass owner acknowledgement.",
    "This gate prep does not expose private pilot evidence publicly.",
]

APPROVAL_REQUIREMENTS = [
    "Owner confirmation chain is complete and not blocked.",
    "Owner acknowledgement conditions are resolved or explicitly accepted.",
    "Expansion decision recommendation is ready for an executive review.",
    "Required pilot evidence remains complete.",
    "Pilot scope remains single-workflow until approval is explicit.",
    "Delivery controls remain approval-gated.",
    "A separate controlled expansion approval artifact is created before execution.",
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


def _approval_conditions(decision, chain):
    artifacts_ready = chain["artifacts_present"] == chain["artifacts_total"] and chain["artifacts_total"] > 0
    chain_not_blocked = chain["blocked_artifacts"] == 0
    owner_acknowledged = chain["conditional_confirmation_artifacts"] == 0
    decision_review_ready = decision["recommended_decision"] in {
        "prepare_expansion_review",
        "schedule_expansion_review",
    }
    evidence_ready = decision["missing_required_evidence"] == 0
    scope_narrow = decision["continuation_scope"] == "single_workflow_narrow_pilot"
    delivery_gated = decision["delivery_status"] == "approval_gated"

    return [
        {
            "condition": "Owner confirmation chain",
            "status": "met" if artifacts_ready and chain_not_blocked else "blocked",
            "detail": f"Artifacts present: {chain['artifacts_present']}/{chain['artifacts_total']}; blocked artifacts: {chain['blocked_artifacts']}.",
        },
        {
            "condition": "Owner acknowledgement",
            "status": "met" if owner_acknowledged else "pending",
            "detail": f"Conditional confirmation artifacts: {chain['conditional_confirmation_artifacts']}.",
        },
        {
            "condition": "Expansion decision recommendation",
            "status": "met" if decision_review_ready else "pending",
            "detail": f"Recommended decision is {decision['recommended_decision']}.",
        },
        {
            "condition": "Required evidence",
            "status": "met" if evidence_ready else "missing",
            "detail": f"Missing required evidence: {decision['missing_required_evidence']}.",
        },
        {
            "condition": "Scope control",
            "status": "met" if scope_narrow else "blocked",
            "detail": f"Continuation scope is {decision['continuation_scope']}.",
        },
        {
            "condition": "Delivery control",
            "status": "met" if delivery_gated else "review_required",
            "detail": f"Delivery status is {decision['delivery_status']}.",
        },
        {
            "condition": "Separate approval artifact",
            "status": "pending",
            "detail": "Controlled expansion approval must be created as a separate future artifact before execution.",
        },
    ]


def _pending_conditions(conditions):
    return [
        condition
        for condition in conditions
        if condition["status"] in {"pending", "missing", "blocked", "review_required"}
    ]


def _approval_gate_status(conditions):
    statuses = {condition["status"] for condition in conditions}

    if "blocked" in statuses or "missing" in statuses:
        return "approval_gate_blocked"

    if "pending" in statuses or "review_required" in statuses:
        return "approval_gate_ready_with_conditions"

    return "approval_gate_ready"


def _recommended_gate_decision(status, conditions):
    pending = [condition["condition"] for condition in _pending_conditions(conditions)]

    if status == "approval_gate_blocked":
        return "do_not_approve_expansion"

    if pending == ["Separate approval artifact"]:
        return "prepare_controlled_expansion_approval"

    if status == "approval_gate_ready_with_conditions":
        return "resolve_conditions_before_approval"

    return "prepare_controlled_expansion_approval"


def _next_action(recommended_gate_decision):
    if recommended_gate_decision == "do_not_approve_expansion":
        return "Do not approve controlled expansion; resolve blocking conditions first."

    if recommended_gate_decision == "resolve_conditions_before_approval":
        return "Resolve or explicitly acknowledge pending conditions before creating an approval artifact."

    return "Create a separate controlled expansion approval artifact, then keep execution gated until approval is recorded."


def generate_pilot_expansion_approval_gate_prep(conn=None):
    decision = generate_pilot_expansion_review_decision(conn)
    chain = generate_pilot_owner_confirmation_chain_index()
    conditions = _approval_conditions(decision, chain)
    pending = _pending_conditions(conditions)
    status = _approval_gate_status(conditions)
    recommended_gate_decision = _recommended_gate_decision(status, conditions)

    return {
        "date": date.today().isoformat(),
        "approval_gate_status": status,
        "recommended_gate_decision": recommended_gate_decision,
        "decision_status": decision["decision_status"],
        "recommended_expansion_decision": decision["recommended_decision"],
        "chain_status": chain["chain_status"],
        "artifacts_present": chain["artifacts_present"],
        "artifacts_total": chain["artifacts_total"],
        "blocked_artifacts": chain["blocked_artifacts"],
        "conditional_confirmation_artifacts": chain["conditional_confirmation_artifacts"],
        "pending_condition_count": len(pending),
        "pending_conditions": [condition["condition"] for condition in pending],
        "pilot_owner": decision["pilot_owner"],
        "primary_workflow": decision["primary_workflow"],
        "continuation_scope": decision["continuation_scope"],
        "delivery_status": decision["delivery_status"],
        "expansion_status": decision["expansion_status"],
        "missing_required_evidence": decision["missing_required_evidence"],
        "conditions": conditions,
        "approval_requirements": APPROVAL_REQUIREMENTS,
        "commands": APPROVAL_GATE_COMMANDS,
        "boundaries": APPROVAL_GATE_BOUNDARIES,
        "next_action": _next_action(recommended_gate_decision),
    }


def export_pilot_expansion_approval_gate_prep(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_expansion_approval_gate_prep(conn)
    report_path = REPORTS_DIR / f"pilot_expansion_approval_gate_prep_{result['date']}.md"

    content = f"""# Pilot Expansion Approval Gate Prep v0.1

Date: {result['date']}

## Approval Gate Summary

Approval gate status: {result['approval_gate_status']}
Recommended gate decision: {result['recommended_gate_decision']}
Decision status: {result['decision_status']}
Recommended expansion decision: {result['recommended_expansion_decision']}
Chain status: {result['chain_status']}
Artifacts present: {result['artifacts_present']}/{result['artifacts_total']}
Blocked artifacts: {result['blocked_artifacts']}
Conditional confirmation artifacts: {result['conditional_confirmation_artifacts']}
Pending conditions: {result['pending_condition_count']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Continuation scope: {result['continuation_scope']}
Expansion status: {result['expansion_status']}
Delivery status: {result['delivery_status']}
Missing required evidence: {result['missing_required_evidence']}
Next action: {result['next_action']}

## Approval Conditions

{_format_condition_rows(result['conditions'])}

## Pending Conditions

{_format_bullets(result['pending_conditions']) if result['pending_conditions'] else 'None.'}

## Approval Requirements

{_format_bullets(result['approval_requirements'])}

## Gate Prep Commands

{_format_commands(result['commands'])}

## Boundaries

{_format_bullets(result['boundaries'])}

## Operator Note

This artifact prepares a future controlled expansion approval gate only. It does not approve expansion, add workflows, enable delivery, or expose private pilot materials.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "pilot_expansion_approval_gate_prep_exported",
            "info" if result["approval_gate_status"] == "approval_gate_ready" else "warning",
            "Pilot expansion approval gate prep exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "approval_gate_status": result["approval_gate_status"],
                "recommended_gate_decision": result["recommended_gate_decision"],
                "pending_condition_count": result["pending_condition_count"],
            },
        )

    return result, str(report_path)


def print_pilot_expansion_approval_gate_prep(conn=None):
    result, report_path = export_pilot_expansion_approval_gate_prep(conn)

    print("Pilot Expansion Approval Gate Prep:")
    print(f"Date: {result['date']}")
    print(f"Approval gate status: {result['approval_gate_status']}")
    print(f"Recommended gate decision: {result['recommended_gate_decision']}")
    print(f"Decision status: {result['decision_status']}")
    print(f"Recommended expansion decision: {result['recommended_expansion_decision']}")
    print(f"Chain status: {result['chain_status']}")
    print(f"Artifacts present: {result['artifacts_present']}/{result['artifacts_total']}")
    print(f"Blocked artifacts: {result['blocked_artifacts']}")
    print(f"Conditional confirmation artifacts: {result['conditional_confirmation_artifacts']}")
    print(f"Pending conditions: {result['pending_condition_count']}")
    print(f"Next action: {result['next_action']}")
    print(f"Pilot expansion approval gate prep exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
