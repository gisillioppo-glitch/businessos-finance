import uuid
from datetime import datetime

from app.audit.audit_log import write_audit_log


VALID_APPROVAL_TYPES = {"decision", "access", "budget", "policy", "incident"}
VALID_PRIORITIES = {"low", "medium", "high", "critical"}
ACTIVE_STATUSES = {"pending"}


def create_approval_request(
    conn,
    title,
    description,
    approval_type,
    priority,
    approver_role,
    requester_email=None,
    requester_role=None,
    source_module=None,
    source_reference_id=None,
):
    if approval_type not in VALID_APPROVAL_TYPES:
        raise ValueError(f"Invalid approval type: {approval_type}")

    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Invalid approval priority: {priority}")

    normalized_email = requester_email.strip().lower() if requester_email else None

    existing = conn.execute(
        """
        SELECT id, status
        FROM approval_requests
        WHERE title = ?
          AND source_module IS ?
          AND source_reference_id IS ?
          AND status = 'pending'
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (
            title,
            source_module,
            source_reference_id,
        ),
    ).fetchone()

    if existing:
        approval_id, status = existing

        write_audit_log(
            conn,
            "approval_request_duplicate_skipped",
            "info",
            "Duplicate approval request skipped.",
            {
                "approval_id": approval_id,
                "status": status,
                "title": title,
                "approval_type": approval_type,
                "source_module": source_module,
                "source_reference_id": source_reference_id,
            },
        )

        return {
            "id": approval_id,
            "title": title,
            "description": description,
            "approval_type": approval_type,
            "priority": priority,
            "requester_email": normalized_email,
            "requester_role": requester_role,
            "approver_role": approver_role,
            "status": status,
            "source_module": source_module,
            "source_reference_id": source_reference_id,
            "was_created": False,
        }

    approval_id = str(uuid.uuid4())

    conn.execute(
        """
        INSERT INTO approval_requests (
            id,
            created_at,
            title,
            description,
            approval_type,
            priority,
            requester_email,
            requester_role,
            approver_role,
            status,
            status_justification,
            source_module,
            source_reference_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            approval_id,
            datetime.now().isoformat(),
            title,
            description,
            approval_type,
            priority,
            normalized_email,
            requester_role,
            approver_role,
            "pending",
            None,
            source_module,
            source_reference_id,
        ),
    )
    conn.commit()

    write_audit_log(
        conn,
        "approval_request_created",
        priority,
        "Approval request created.",
        {
            "approval_id": approval_id,
            "title": title,
            "approval_type": approval_type,
            "priority": priority,
            "requester_email": normalized_email,
            "requester_role": requester_role,
            "approver_role": approver_role,
            "source_module": source_module,
            "source_reference_id": source_reference_id,
        },
    )

    return {
        "id": approval_id,
        "title": title,
        "description": description,
        "approval_type": approval_type,
        "priority": priority,
        "requester_email": normalized_email,
        "requester_role": requester_role,
        "approver_role": approver_role,
        "status": "pending",
        "source_module": source_module,
        "source_reference_id": source_reference_id,
        "was_created": True,
    }


def ensure_default_approval_requests(conn):
    default_approvals = [
        {
            "title": "Approve overdue operations intervention",
            "description": "Executive approval is required before escalating the overdue finance action follow-up.",
            "approval_type": "decision",
            "priority": "high",
            "approver_role": "Executive Owner",
            "requester_email": "operations.manager@businessos.local",
            "requester_role": "Operations Manager",
            "source_module": "assistance",
            "source_reference_id": "overdue-finance-action-follow-up",
        },
        {
            "title": "Approve support resolution path",
            "description": "Support needs approval for the proposed governance monitoring follow-up resolution path.",
            "approval_type": "incident",
            "priority": "medium",
            "approver_role": "Executive Owner",
            "requester_email": "support.manager@businessos.local",
            "requester_role": "Support Manager",
            "source_module": "assistance",
            "source_reference_id": "governance-monitoring-follow-up",
        },
    ]

    results = []

    for approval in default_approvals:
        results.append(create_approval_request(conn, **approval))

    return results
