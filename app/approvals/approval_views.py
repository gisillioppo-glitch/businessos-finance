from app.audit.audit_log import write_audit_log


def print_approval_requests_list(conn):
    rows = conn.execute(
        """
        SELECT status, priority, approval_type, approver_role, title
        FROM approval_requests
        WHERE status = 'pending'
        ORDER BY
            CASE priority
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
        print("Approval Request List: No pending approvals.")
        write_audit_log(
            conn,
            "approval_request_list_viewed",
            "info",
            "Approval request list viewed with no pending approvals.",
            {"approvals_visible": 0},
        )
        return []

    print("Approval Request List:")

    for status, priority, approval_type, approver_role, title in rows:
        print(
            f"[{priority.upper()}] "
            f"Status: {status} | "
            f"Type: {approval_type} | "
            f"Approver: {approver_role} | "
            f"Approval: {title}"
        )

    write_audit_log(
        conn,
        "approval_request_list_viewed",
        "info",
        "Approval request list viewed.",
        {"approvals_visible": len(rows)},
    )

    return rows


def print_approval_request_summary_kpis(conn):
    rows = conn.execute(
        """
        SELECT status, priority, approval_type, COUNT(*) AS count
        FROM approval_requests
        GROUP BY status, priority, approval_type
        """
    ).fetchall()

    summary = {
        "pending": 0,
        "approved": 0,
        "rejected": 0,
        "cancelled": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "decision": 0,
        "access": 0,
        "budget": 0,
        "policy": 0,
        "incident": 0,
    }

    for status, priority, approval_type, count in rows:
        if status in summary:
            summary[status] += count

        if priority in summary:
            summary[priority] += count

        if approval_type in summary:
            summary[approval_type] += count

    print("Approval Request Summary KPIs:")
    print(f"Pending approvals: {summary['pending']}")
    print(f"Approved approvals: {summary['approved']}")
    print(f"Rejected approvals: {summary['rejected']}")
    print(f"Cancelled approvals: {summary['cancelled']}")
    print(f"Critical approvals: {summary['critical']}")
    print(f"High approvals: {summary['high']}")
    print(f"Medium approvals: {summary['medium']}")
    print(f"Low approvals: {summary['low']}")
    print(f"Decision approvals: {summary['decision']}")
    print(f"Access approvals: {summary['access']}")
    print(f"Budget approvals: {summary['budget']}")
    print(f"Policy approvals: {summary['policy']}")
    print(f"Incident approvals: {summary['incident']}")

    write_audit_log(
        conn,
        "approval_request_summary_kpis_viewed",
        "info",
        "Approval request summary KPIs viewed.",
        summary,
    )

    return summary
