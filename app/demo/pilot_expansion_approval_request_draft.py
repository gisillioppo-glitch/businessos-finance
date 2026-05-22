from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.pilot_expansion_approval_gate_prep import generate_pilot_expansion_approval_gate_prep


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

REQUEST_TITLE = "Approve controlled pilot expansion"
REQUEST_TYPE = "decision"
REQUEST_PRIORITY = "high"
REQUESTER_EMAIL = "operations.manager@businessos.local"
REQUESTER_ROLE = "Operations Manager"
APPROVER_ROLE = "Executive Owner"
SOURCE_MODULE = "pilot_expansion"

REQUEST_DRAFT_BOUNDARIES = [
    "This draft does not create an approval request in the database.",
    "This draft does not approve controlled expansion.",
    "This draft does not add a workflow.",
    "This draft does not enable external delivery.",
    "This draft does not bypass owner acknowledgement or governance.",
]

REQUEST_DRAFT_COMMANDS = [
    ("Refresh approval gate prep", "python cli.py pilot-expansion-approval-gate-prep"),
    ("Review dashboard approval gate", "streamlit run app/dashboard/main.py"),
    ("Review approval queue", "python cli.py approvals"),
    ("Review delivery approval gate", "python cli.py notification-delivery-approval"),
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


def _draft_status(gate):
    if gate["approval_gate_status"] == "approval_gate_blocked":
        return "draft_blocked"

    if gate["pending_condition_count"] > 0:
        return "draft_ready_with_conditions"

    return "draft_ready"


def _recommended_request_action(status):
    if status == "draft_blocked":
        return "Do not create a formal approval request until blocking conditions are resolved."

    if status == "draft_ready_with_conditions":
        return "Review and explicitly acknowledge pending conditions before creating the formal approval request."

    return "Create the formal approval request as a separate controlled block."


def _request_description(gate):
    return (
        "Request executive decision approval for a controlled pilot expansion review. "
        f"Gate status is {gate['approval_gate_status']}; "
        f"recommended gate decision is {gate['recommended_gate_decision']}; "
        f"pending conditions: {gate['pending_condition_count']}; "
        f"expansion status: {gate['expansion_status']}; "
        f"delivery status: {gate['delivery_status']}. "
        "Approval must remain separate from execution."
    )


def generate_pilot_expansion_approval_request_draft(conn=None):
    gate = generate_pilot_expansion_approval_gate_prep(conn)
    status = _draft_status(gate)

    return {
        "date": date.today().isoformat(),
        "draft_status": status,
        "request_title": REQUEST_TITLE,
        "request_description": _request_description(gate),
        "approval_type": REQUEST_TYPE,
        "priority": REQUEST_PRIORITY,
        "requester_email": REQUESTER_EMAIL,
        "requester_role": REQUESTER_ROLE,
        "approver_role": APPROVER_ROLE,
        "source_module": SOURCE_MODULE,
        "source_reference_id": f"pilot-expansion-approval-gate-prep-{gate['date']}",
        "approval_gate_status": gate["approval_gate_status"],
        "recommended_gate_decision": gate["recommended_gate_decision"],
        "pending_condition_count": gate["pending_condition_count"],
        "pending_conditions": gate["pending_conditions"],
        "expansion_status": gate["expansion_status"],
        "delivery_status": gate["delivery_status"],
        "pilot_owner": gate["pilot_owner"],
        "primary_workflow": gate["primary_workflow"],
        "conditions": gate["conditions"],
        "commands": REQUEST_DRAFT_COMMANDS,
        "boundaries": REQUEST_DRAFT_BOUNDARIES,
        "recommended_request_action": _recommended_request_action(status),
    }


def export_pilot_expansion_approval_request_draft(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_expansion_approval_request_draft(conn)
    report_path = REPORTS_DIR / f"pilot_expansion_approval_request_draft_{result['date']}.md"

    content = f"""# Pilot Expansion Approval Request Draft v0.1

Date: {result['date']}

## Approval Request Draft Summary

Draft status: {result['draft_status']}
Request title: {result['request_title']}
Approval type: {result['approval_type']}
Priority: {result['priority']}
Requester email: {result['requester_email']}
Requester role: {result['requester_role']}
Approver role: {result['approver_role']}
Source module: {result['source_module']}
Source reference id: {result['source_reference_id']}
Approval gate status: {result['approval_gate_status']}
Recommended gate decision: {result['recommended_gate_decision']}
Pending conditions: {result['pending_condition_count']}
Expansion status: {result['expansion_status']}
Delivery status: {result['delivery_status']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Recommended request action: {result['recommended_request_action']}

## Request Description

{result['request_description']}

## Pending Conditions

{_format_bullets(result['pending_conditions']) if result['pending_conditions'] else 'None.'}

## Approval Conditions

{_format_condition_rows(result['conditions'])}

## Draft Commands

{_format_commands(result['commands'])}

## Boundaries

{_format_bullets(result['boundaries'])}

## Operator Note

This artifact prepares the approval request only. It does not create a database approval request, approve expansion, add workflows, enable delivery, or expose private pilot materials.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "pilot_expansion_approval_request_draft_exported",
            "info" if result["draft_status"] == "draft_ready" else "warning",
            "Pilot expansion approval request draft exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "draft_status": result["draft_status"],
                "approval_gate_status": result["approval_gate_status"],
                "pending_condition_count": result["pending_condition_count"],
            },
        )

    return result, str(report_path)


def print_pilot_expansion_approval_request_draft(conn=None):
    result, report_path = export_pilot_expansion_approval_request_draft(conn)

    print("Pilot Expansion Approval Request Draft:")
    print(f"Date: {result['date']}")
    print(f"Draft status: {result['draft_status']}")
    print(f"Request title: {result['request_title']}")
    print(f"Approval type: {result['approval_type']}")
    print(f"Priority: {result['priority']}")
    print(f"Approver role: {result['approver_role']}")
    print(f"Approval gate status: {result['approval_gate_status']}")
    print(f"Recommended gate decision: {result['recommended_gate_decision']}")
    print(f"Pending conditions: {result['pending_condition_count']}")
    print(f"Recommended request action: {result['recommended_request_action']}")
    print(f"Pilot expansion approval request draft exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
