import uuid
from datetime import datetime

from app.audit.audit_log import write_audit_log


VALID_REQUEST_TYPES = {"help", "approval", "incident", "access", "decision"}
VALID_SEVERITIES = {"low", "medium", "high", "critical"}
ACTIVE_STATUSES = {"open", "triaged", "waiting_approval", "in_progress"}


def create_assistance_request(
    conn,
    title,
    description,
    request_type,
    severity,
    owner_role,
    requester_email=None,
    requester_role=None,
    source_module=None,
    source_reference_id=None,
):
    if request_type not in VALID_REQUEST_TYPES:
        raise ValueError(f"Invalid assistance request type: {request_type}")

    if severity not in VALID_SEVERITIES:
        raise ValueError(f"Invalid assistance severity: {severity}")

    normalized_email = requester_email.strip().lower() if requester_email else None

    existing = conn.execute(
        """
        SELECT id, status
        FROM assistance_requests
        WHERE title = ?
          AND source_module IS ?
          AND source_reference_id IS ?
          AND status IN ('open', 'triaged', 'waiting_approval', 'in_progress')
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
        request_id, status = existing

        write_audit_log(
            conn,
            "assistance_request_duplicate_skipped",
            "info",
            "Duplicate assistance request skipped.",
            {
                "existing_request_id": request_id,
                "existing_status": status,
                "title": title,
                "request_type": request_type,
                "source_module": source_module,
                "source_reference_id": source_reference_id,
            },
        )

        return {
            "id": request_id,
            "title": title,
            "description": description,
            "request_type": request_type,
            "severity": severity,
            "requester_email": normalized_email,
            "requester_role": requester_role,
            "owner_role": owner_role,
            "status": status,
            "source_module": source_module,
            "source_reference_id": source_reference_id,
            "was_created": False,
        }

    request_id = str(uuid.uuid4())

    conn.execute(
        """
        INSERT INTO assistance_requests (
            id,
            created_at,
            title,
            description,
            request_type,
            severity,
            requester_email,
            requester_role,
            owner_role,
            status,
            status_justification,
            source_module,
            source_reference_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            request_id,
            datetime.now().isoformat(),
            title,
            description,
            request_type,
            severity,
            normalized_email,
            requester_role,
            owner_role,
            "open",
            None,
            source_module,
            source_reference_id,
        ),
    )
    conn.commit()

    write_audit_log(
        conn,
        "assistance_request_created",
        severity,
        "Assistance request created.",
        {
            "request_id": request_id,
            "title": title,
            "request_type": request_type,
            "severity": severity,
            "requester_email": normalized_email,
            "requester_role": requester_role,
            "owner_role": owner_role,
            "source_module": source_module,
            "source_reference_id": source_reference_id,
        },
    )

    return {
        "id": request_id,
        "title": title,
        "description": description,
        "request_type": request_type,
        "severity": severity,
        "requester_email": normalized_email,
        "requester_role": requester_role,
        "owner_role": owner_role,
        "status": "open",
        "source_module": source_module,
        "source_reference_id": source_reference_id,
        "was_created": True,
    }


def ensure_default_assistance_requests(conn):
    default_requests = [
        {
            "title": "Review overdue operations follow-up",
            "description": "Operations has an overdue finance action follow-up that needs executive attention.",
            "request_type": "decision",
            "severity": "high",
            "owner_role": "Operations Manager",
            "requester_email": "operations.manager@businessos.local",
            "requester_role": "Operations Manager",
            "source_module": "operations",
            "source_reference_id": "overdue-finance-action-follow-up",
        },
        {
            "title": "Confirm support incident resolution path",
            "description": "Support incident is under investigation and needs a clear resolution path.",
            "request_type": "help",
            "severity": "medium",
            "owner_role": "Support Manager",
            "requester_email": "support.manager@businessos.local",
            "requester_role": "Support Manager",
            "source_module": "support",
            "source_reference_id": "governance-monitoring-follow-up",
        },
    ]

    results = []

    for request in default_requests:
        results.append(create_assistance_request(conn, **request))

    return results
