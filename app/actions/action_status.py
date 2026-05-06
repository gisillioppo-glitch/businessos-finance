from app.audit.audit_log import write_audit_log

def update_recommended_action_status(
    conn,
    action_id,
    new_status,
    justification=None,
):
    valid_statuses = {"open", "in_progress", "completed", "dismissed"}

    if new_status not in valid_statuses:
        raise ValueError(f"Invalid action status: {new_status}")

    row = conn.execute(
        """
        SELECT status, recommended_action
        FROM recommended_actions
        WHERE id = ?
        """,
        (action_id,),
    ).fetchone()

    if row is None:
        raise ValueError(f"Recommended action not found: {action_id}")

    old_status, recommended_action = row

    conn.execute(
        """
        UPDATE recommended_actions
        SET status = ?,
            status_justification = ?
        WHERE id = ?
        """,
        (new_status, justification, action_id),
    )
    conn.commit()

    write_audit_log(
        conn,
        "recommended_action_status_updated",
        "info",
        "Recommended action status updated.",
        {
            "action_id": action_id,
            "old_status": old_status,
            "new_status": new_status,
            "justification": justification,
            "recommended_action": recommended_action,
        },
    )

    return {
        "action_id": action_id,
        "old_status": old_status,
        "new_status": new_status,
        "justification": justification,
        "recommended_action": recommended_action,
    }


def demo_update_first_open_action(conn):
    row = conn.execute(
        """
        SELECT id
        FROM recommended_actions
        WHERE status = 'open'
        ORDER BY created_at ASC
        LIMIT 1
        """
    ).fetchone()

    if row is None:
        print("Action Status Update: No open actions found.")
        write_audit_log(
            conn,
            "recommended_action_status_demo",
            "info",
            "No open recommended actions found for status update demo.",
            {},
        )
        return None

    action_id = row[0]

    result = update_recommended_action_status(
    conn,
    action_id,
    "in_progress",
    "Demo mode moved the first open action to in_progress.",
)


    print(
        "Action Status Update: "
        f"{result['action_id']} changed from "
        f"{result['old_status']} to {result['new_status']}."
    )

    return result
