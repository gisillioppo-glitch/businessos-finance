from app.audit.audit_log import write_audit_log


VALID_ASSISTANCE_STATUSES = {
    "open",
    "triaged",
    "waiting_approval",
    "in_progress",
    "resolved",
    "dismissed",
}


def update_assistance_request_status(
    conn,
    request_id,
    new_status,
    justification=None,
):
    if new_status not in VALID_ASSISTANCE_STATUSES:
        raise ValueError(f"Invalid assistance request status: {new_status}")

    row = conn.execute(
        """
        SELECT status, title, request_type
        FROM assistance_requests
        WHERE id = ?
        """,
        (request_id,),
    ).fetchone()

    if row is None:
        raise ValueError(f"Assistance request not found: {request_id}")

    old_status, title, request_type = row

    conn.execute(
        """
        UPDATE assistance_requests
        SET status = ?,
            status_justification = ?
        WHERE id = ?
        """,
        (new_status, justification, request_id),
    )
    conn.commit()

    write_audit_log(
        conn,
        "assistance_request_status_updated",
        "info",
        "Assistance request status updated.",
        {
            "request_id": request_id,
            "old_status": old_status,
            "new_status": new_status,
            "justification": justification,
            "title": title,
            "request_type": request_type,
        },
    )

    return {
        "request_id": request_id,
        "old_status": old_status,
        "new_status": new_status,
        "justification": justification,
        "title": title,
        "request_type": request_type,
    }


def demo_triage_first_open_assistance_request(conn):
    row = conn.execute(
        """
        SELECT id
        FROM assistance_requests
        WHERE status = 'open'
        ORDER BY created_at ASC
        LIMIT 1
        """
    ).fetchone()

    if row is None:
        print("Assistance Request Status Update: No open assistance requests found.")
        write_audit_log(
            conn,
            "assistance_request_status_demo",
            "info",
            "No open assistance requests found for status update demo.",
            {},
        )
        return None

    request_id = row[0]

    result = update_assistance_request_status(
        conn,
        request_id,
        "triaged",
        "Demo mode triaged the first open assistance request.",
    )

    print(
        "Assistance Request Status Update: "
        f"{result['request_id']} changed from "
        f"{result['old_status']} to {result['new_status']}."
    )

    return result
