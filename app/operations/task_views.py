from app.audit.audit_log import write_audit_log


def print_operations_tasks_list(conn):
    rows = conn.execute(
        """
        SELECT status, priority, owner_role, deadline_date, title
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
        ORDER BY
            CASE priority
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            deadline_date ASC
        """
    ).fetchall()

    if not rows:
        print("Operations Task List: No active operations tasks.")
        write_audit_log(
            conn,
            "operations_task_list_viewed",
            "info",
            "Operations task list viewed with no active tasks.",
            {"tasks_visible": 0},
        )
        return []

    print("Operations Task List:")

    for status, priority, owner_role, deadline_date, title in rows:
        print(
            f"[{priority.upper()}] "
            f"Status: {status} | "
            f"Owner: {owner_role} | "
            f"Deadline: {deadline_date} | "
            f"Task: {title}"
        )

    write_audit_log(
        conn,
        "operations_task_list_viewed",
        "info",
        "Operations task list viewed.",
        {"tasks_visible": len(rows)},
    )

    return rows


def print_operations_task_summary_kpis(conn):
    rows = conn.execute(
        """
        SELECT status, priority, COUNT(*) AS count
        FROM operations_tasks
        GROUP BY status, priority
        """
    ).fetchall()

    summary = {
        "open": 0,
        "in_progress": 0,
        "blocked": 0,
        "completed": 0,
        "dismissed": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for status, priority, count in rows:
        if status in summary:
            summary[status] += count

        if priority in summary:
            summary[priority] += count

    print("Operations Task Summary KPIs:")
    print(f"Open tasks: {summary['open']}")
    print(f"In-progress tasks: {summary['in_progress']}")
    print(f"Blocked tasks: {summary['blocked']}")
    print(f"Completed tasks: {summary['completed']}")
    print(f"Dismissed tasks: {summary['dismissed']}")
    print(f"Critical priority tasks: {summary['critical']}")
    print(f"High priority tasks: {summary['high']}")
    print(f"Medium priority tasks: {summary['medium']}")
    print(f"Low priority tasks: {summary['low']}")

    write_audit_log(
        conn,
        "operations_task_summary_kpis_viewed",
        "info",
        "Operations task summary KPIs viewed.",
        summary,
    )

    return summary
