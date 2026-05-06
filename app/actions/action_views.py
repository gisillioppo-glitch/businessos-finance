from app.audit.audit_log import write_audit_log


def print_recommended_actions_list(conn):
    rows = conn.execute(
        """
        SELECT status, priority, owner_role, risk_type, recommended_action
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
        ORDER BY
            CASE priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                WHEN 'low' THEN 3
                ELSE 4
            END,
            created_at ASC
        """
    ).fetchall()

    if not rows:
        print("Action List: No open or in-progress actions.")
        write_audit_log(
            conn,
            "action_list_viewed",
            "info",
            "Action list viewed with no open or in-progress actions.",
            {"actions_visible": 0},
        )
        return []

    print("Action List:")

    for status, priority, owner_role, risk_type, recommended_action in rows:
        print(
            f"[{priority.upper()}] "
            f"Status: {status} | "
            f"Owner: {owner_role} | "
            f"Risk: {risk_type} | "
            f"Action: {recommended_action}"
        )

    write_audit_log(
        conn,
        "action_list_viewed",
        "info",
        "Action list viewed.",
        {"actions_visible": len(rows)},
    )

    return rows


def print_action_summary_kpis(conn):
    rows = conn.execute(
        """
        SELECT status, priority, COUNT(*) AS count
        FROM recommended_actions
        GROUP BY status, priority
        """
    ).fetchall()

    summary = {
        "open": 0,
        "in_progress": 0,
        "completed": 0,
        "dismissed": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for status, priority, count in rows:
        if status in summary:
            summary[status] += count

        if priority in summary:
            summary[priority] += count

    print("Action Summary KPIs:")
    print(f"Open actions: {summary['open']}")
    print(f"In-progress actions: {summary['in_progress']}")
    print(f"Completed actions: {summary['completed']}")
    print(f"Dismissed actions: {summary['dismissed']}")
    print(f"High priority actions: {summary['high']}")
    print(f"Medium priority actions: {summary['medium']}")
    print(f"Low priority actions: {summary['low']}")

    write_audit_log(
        conn,
        "action_summary_kpis_viewed",
        "info",
        "Action summary KPIs viewed.",
        summary,
    )

    return summary
