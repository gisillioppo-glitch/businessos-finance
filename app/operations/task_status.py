from app.audit.audit_log import write_audit_log


def update_operations_task_status(
    conn,
    task_id,
    new_status,
    justification=None,
):
    valid_statuses = {"open", "in_progress", "blocked", "completed", "dismissed"}

    if new_status not in valid_statuses:
        raise ValueError(f"Invalid operations task status: {new_status}")

    row = conn.execute(
        """
        SELECT status, title
        FROM operations_tasks
        WHERE id = ?
        """,
        (task_id,),
    ).fetchone()

    if row is None:
        raise ValueError(f"Operations task not found: {task_id}")

    old_status, title = row

    conn.execute(
        """
        UPDATE operations_tasks
        SET status = ?,
            status_justification = ?
        WHERE id = ?
        """,
        (new_status, justification, task_id),
    )
    conn.commit()

    write_audit_log(
        conn,
        "operations_task_status_updated",
        "info",
        "Operations task status updated.",
        {
            "task_id": task_id,
            "old_status": old_status,
            "new_status": new_status,
            "justification": justification,
            "title": title,
        },
    )

    return {
        "task_id": task_id,
        "old_status": old_status,
        "new_status": new_status,
        "justification": justification,
        "title": title,
    }


def demo_update_first_open_operations_task(conn):
    row = conn.execute(
        """
        SELECT id
        FROM operations_tasks
        WHERE status = 'open'
        ORDER BY created_at ASC
        LIMIT 1
        """
    ).fetchone()

    if row is None:
        print("Operations Task Status Update: No open tasks found.")
        write_audit_log(
            conn,
            "operations_task_status_demo",
            "info",
            "No open operations tasks found for status update demo.",
            {},
        )
        return None

    task_id = row[0]

    result = update_operations_task_status(
        conn,
        task_id,
        "in_progress",
        "Demo mode moved the first open operations task to in_progress.",
    )

    print(
        "Operations Task Status Update: "
        f"{result['task_id']} changed from "
        f"{result['old_status']} to {result['new_status']}."
    )

    return result
