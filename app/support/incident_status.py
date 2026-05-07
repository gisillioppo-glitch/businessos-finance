from app.audit.audit_log import write_audit_log


def update_support_incident_status(
    conn,
    incident_id,
    new_status,
    justification=None,
):
    valid_statuses = {"open", "investigating", "waiting", "resolved", "dismissed"}

    if new_status not in valid_statuses:
        raise ValueError(f"Invalid support incident status: {new_status}")

    row = conn.execute(
        """
        SELECT status, title
        FROM support_incidents
        WHERE id = ?
        """,
        (incident_id,),
    ).fetchone()

    if row is None:
        raise ValueError(f"Support incident not found: {incident_id}")

    old_status, title = row

    conn.execute(
        """
        UPDATE support_incidents
        SET status = ?,
            status_justification = ?
        WHERE id = ?
        """,
        (new_status, justification, incident_id),
    )
    conn.commit()

    write_audit_log(
        conn,
        "support_incident_status_updated",
        "info",
        "Support incident status updated.",
        {
            "incident_id": incident_id,
            "old_status": old_status,
            "new_status": new_status,
            "justification": justification,
            "title": title,
        },
    )

    return {
        "incident_id": incident_id,
        "old_status": old_status,
        "new_status": new_status,
        "justification": justification,
        "title": title,
    }


def demo_update_first_open_support_incident(conn):
    row = conn.execute(
        """
        SELECT id
        FROM support_incidents
        WHERE status = 'open'
        ORDER BY created_at ASC
        LIMIT 1
        """
    ).fetchone()

    if row is None:
        print("Support Incident Status Update: No open incidents found.")
        write_audit_log(
            conn,
            "support_incident_status_demo",
            "info",
            "No open support incidents found for status update demo.",
            {},
        )
        return None

    incident_id = row[0]

    result = update_support_incident_status(
        conn,
        incident_id,
        "investigating",
        "Demo mode moved the first open support incident to investigating.",
    )

    print(
        "Support Incident Status Update: "
        f"{result['incident_id']} changed from "
        f"{result['old_status']} to {result['new_status']}."
    )

    return result
