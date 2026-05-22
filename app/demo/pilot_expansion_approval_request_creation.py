from datetime import date
from pathlib import Path

from app.approvals.requests import create_approval_request
from app.approvals.schema import create_approval_requests_table
from app.audit.audit_log import write_audit_log
from app.demo.pilot_expansion_approval_request_draft import (
    generate_pilot_expansion_approval_request_draft,
)


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

REQUEST_CREATION_BOUNDARIES = [
    "This command creates or reuses a pending approval request only.",
    "This command does not approve controlled expansion.",
    "This command does not add a workflow.",
    "This command does not enable external delivery.",
    "This command does not bypass owner acknowledgement or governance review.",
]

REQUEST_CREATION_COMMANDS = [
    ("Review approval queue", "python cli.py approvals"),
    ("Review approval report", "python cli.py approval-report"),
    ("Approve first pending demo request", "python cli.py approval-approve"),
    ("Reject first pending demo request", "python cli.py approval-reject"),
    ("Refresh approval request draft", "python cli.py pilot-expansion-approval-request-draft"),
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


def _creation_status(draft):
    if draft["draft_status"] == "draft_blocked":
        return "request_not_created_blocked"

    if draft["pending_condition_count"] > 0:
        return "request_created_with_conditions"

    return "request_created"


def _creation_note(status, approval):
    if status == "request_not_created_blocked":
        return "Formal request was not created because the draft is blocked."

    if approval["was_created"]:
        return "Formal pending approval request was created for executive review."

    return "Existing formal pending approval request was reused."


def _create_approval_from_draft(conn, draft):
    if draft["draft_status"] == "draft_blocked":
        return None

    return create_approval_request(
        conn,
        title=draft["request_title"],
        description=draft["request_description"],
        approval_type=draft["approval_type"],
        priority=draft["priority"],
        approver_role=draft["approver_role"],
        requester_email=draft["requester_email"],
        requester_role=draft["requester_role"],
        source_module=draft["source_module"],
        source_reference_id=draft["source_reference_id"],
    )


def generate_pilot_expansion_approval_request_creation(conn):
    create_approval_requests_table(conn)
    draft = generate_pilot_expansion_approval_request_draft(conn)
    status = _creation_status(draft)
    approval = _create_approval_from_draft(conn, draft)

    return {
        "date": date.today().isoformat(),
        "creation_status": status,
        "approval_request": approval,
        "approval_request_id": approval["id"] if approval else None,
        "approval_request_status": approval["status"] if approval else "not_created",
        "approval_request_created": approval["was_created"] if approval else False,
        "request_title": draft["request_title"],
        "approval_type": draft["approval_type"],
        "priority": draft["priority"],
        "requester_email": draft["requester_email"],
        "requester_role": draft["requester_role"],
        "approver_role": draft["approver_role"],
        "source_module": draft["source_module"],
        "source_reference_id": draft["source_reference_id"],
        "draft_status": draft["draft_status"],
        "approval_gate_status": draft["approval_gate_status"],
        "recommended_gate_decision": draft["recommended_gate_decision"],
        "pending_condition_count": draft["pending_condition_count"],
        "pending_conditions": draft["pending_conditions"],
        "request_description": draft["request_description"],
        "commands": REQUEST_CREATION_COMMANDS,
        "boundaries": REQUEST_CREATION_BOUNDARIES,
        "creation_note": _creation_note(status, approval) if approval else _creation_note(status, None),
    }


def export_pilot_expansion_approval_request_creation(conn):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_expansion_approval_request_creation(conn)
    report_path = REPORTS_DIR / f"pilot_expansion_approval_request_creation_{result['date']}.md"

    content = f"""# Pilot Expansion Approval Request Creation v0.1

Date: {result['date']}

## Approval Request Creation Summary

Creation status: {result['creation_status']}
Approval request id: {result['approval_request_id'] or 'None'}
Approval request status: {result['approval_request_status']}
Approval request created this run: {result['approval_request_created']}
Request title: {result['request_title']}
Approval type: {result['approval_type']}
Priority: {result['priority']}
Requester email: {result['requester_email']}
Requester role: {result['requester_role']}
Approver role: {result['approver_role']}
Source module: {result['source_module']}
Source reference id: {result['source_reference_id']}
Draft status: {result['draft_status']}
Approval gate status: {result['approval_gate_status']}
Recommended gate decision: {result['recommended_gate_decision']}
Pending conditions: {result['pending_condition_count']}

## Request Description

{result['request_description']}

## Pending Conditions

{_format_bullets(result['pending_conditions']) if result['pending_conditions'] else 'None.'}

## Creation Commands

{_format_commands(result['commands'])}

## Boundaries

{_format_bullets(result['boundaries'])}

## Operator Note

{result['creation_note']} The request remains pending until an authorized governance action changes its status.
"""

    report_path.write_text(content, encoding="utf-8")

    write_audit_log(
        conn,
        "pilot_expansion_approval_request_creation_exported",
        "info" if result["approval_request_created"] else "warning",
        "Pilot expansion approval request creation exported.",
        {
            "report_path": str(report_path.relative_to(ROOT_DIR)),
            "creation_status": result["creation_status"],
            "approval_request_id": result["approval_request_id"],
            "approval_request_status": result["approval_request_status"],
            "approval_request_created": result["approval_request_created"],
            "pending_condition_count": result["pending_condition_count"],
        },
    )

    return result, str(report_path)


def print_pilot_expansion_approval_request_creation(conn):
    result, report_path = export_pilot_expansion_approval_request_creation(conn)

    print("Pilot Expansion Approval Request Creation:")
    print(f"Date: {result['date']}")
    print(f"Creation status: {result['creation_status']}")
    print(f"Approval request id: {result['approval_request_id'] or 'None'}")
    print(f"Approval request status: {result['approval_request_status']}")
    print(f"Approval request created this run: {result['approval_request_created']}")
    print(f"Draft status: {result['draft_status']}")
    print(f"Approval gate status: {result['approval_gate_status']}")
    print(f"Pending conditions: {result['pending_condition_count']}")
    print(f"Pilot expansion approval request creation exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
