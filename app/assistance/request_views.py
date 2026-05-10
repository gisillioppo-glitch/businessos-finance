from app.audit.audit_log import write_audit_log


def print_assistance_requests_list(conn):
    rows = conn.execute(
        """
        SELECT status, severity, request_type, owner_role, title
        FROM assistance_requests
        WHERE status IN ('open', 'triaged', 'waiting_approval', 'in_progress')
        ORDER BY
            CASE severity
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            created_at ASC
        """
    ).fetchall()

    if not rows:
        print("Assistance Request List: No active assistance requests.")
        write_audit_log(
            conn,
            "assistance_request_list_viewed",
            "info",
            "Assistance request list viewed with no active requests.",
            {"requests_visible": 0},
        )
        return []

    print("Assistance Request List:")

    for status, severity, request_type, owner_role, title in rows:
        print(
            f"[{severity.upper()}] "
            f"Status: {status} | "
            f"Type: {request_type} | "
            f"Owner: {owner_role} | "
            f"Request: {title}"
        )

    write_audit_log(
        conn,
        "assistance_request_list_viewed",
        "info",
        "Assistance request list viewed.",
        {"requests_visible": len(rows)},
    )

    return rows


def print_assistance_request_summary_kpis(conn):
    rows = conn.execute(
        """
        SELECT status, severity, request_type, COUNT(*) AS count
        FROM assistance_requests
        GROUP BY status, severity, request_type
        """
    ).fetchall()

    summary = {
        "open": 0,
        "triaged": 0,
        "waiting_approval": 0,
        "in_progress": 0,
        "resolved": 0,
        "dismissed": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "help": 0,
        "approval": 0,
        "incident": 0,
        "access": 0,
        "decision": 0,
    }

    for status, severity, request_type, count in rows:
        if status in summary:
            summary[status] += count

        if severity in summary:
            summary[severity] += count

        if request_type in summary:
            summary[request_type] += count

    print("Assistance Request Summary KPIs:")
    print(f"Open requests: {summary['open']}")
    print(f"Triaged requests: {summary['triaged']}")
    print(f"Waiting approval requests: {summary['waiting_approval']}")
    print(f"In-progress requests: {summary['in_progress']}")
    print(f"Resolved requests: {summary['resolved']}")
    print(f"Dismissed requests: {summary['dismissed']}")
    print(f"Critical requests: {summary['critical']}")
    print(f"High requests: {summary['high']}")
    print(f"Medium requests: {summary['medium']}")
    print(f"Low requests: {summary['low']}")
    print(f"Help requests: {summary['help']}")
    print(f"Approval requests: {summary['approval']}")
    print(f"Incident requests: {summary['incident']}")
    print(f"Access requests: {summary['access']}")
    print(f"Decision requests: {summary['decision']}")

    write_audit_log(
        conn,
        "assistance_request_summary_kpis_viewed",
        "info",
        "Assistance request summary KPIs viewed.",
        summary,
    )

    return summary
