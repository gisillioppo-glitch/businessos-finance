import uuid
from datetime import datetime

from app.audit.audit_log import write_audit_log


def create_support_incident(
    conn,
    title,
    description,
    severity,
    owner_role,
    source_module=None,
    source_reference_id=None,
):
    valid_severities = {"low", "medium", "high", "critical"}

    if severity not in valid_severities:
        raise ValueError(f"Invalid incident severity: {severity}")

    existing = conn.execute(
        """
        SELECT id, status
        FROM support_incidents
        WHERE title = ?
          AND source_module IS ?
          AND source_reference_id IS ?
          AND status IN ('open', 'investigating', 'waiting')
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
        incident_id, status = existing

        write_audit_log(
            conn,
            "support_incident_duplicate_skipped",
            "info",
            "Duplicate support incident skipped.",
            {
                "existing_incident_id": incident_id,
                "existing_status": status,
                "title": title,
                "source_module": source_module,
                "source_reference_id": source_reference_id,
            },
        )

        return {
            "id": incident_id,
            "title": title,
            "description": description,
            "severity": severity,
            "owner_role": owner_role,
            "status": status,
            "source_module": source_module,
            "source_reference_id": source_reference_id,
            "was_created": False,
        }

    incident_id = str(uuid.uuid4())

    conn.execute(
        """
        INSERT INTO support_incidents (
            id,
            created_at,
            title,
            description,
            severity,
            owner_role,
            status,
            status_justification,
            source_module,
            source_reference_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            incident_id,
            datetime.now().isoformat(),
            title,
            description,
            severity,
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
        "support_incident_created",
        severity,
        "Support incident created.",
        {
            "incident_id": incident_id,
            "title": title,
            "severity": severity,
            "owner_role": owner_role,
            "source_module": source_module,
            "source_reference_id": source_reference_id,
        },
    )

    return {
        "id": incident_id,
        "title": title,
        "description": description,
        "severity": severity,
        "owner_role": owner_role,
        "status": "open",
        "source_module": source_module,
        "source_reference_id": source_reference_id,
        "was_created": True,
    }
