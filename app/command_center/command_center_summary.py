from app.audit.audit_log import write_audit_log


def get_count(conn, query, params=None):
    if params is None:
        params = ()

    return conn.execute(query, params).fetchone()[0]


def generate_command_center_summary(conn):
    transactions_count = get_count(
        conn,
        "SELECT COUNT(*) FROM transactions",
    )

    active_finance_actions = get_count(
        conn,
        """
        SELECT COUNT(*)
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
        """,
    )

    active_operations_tasks = get_count(
        conn,
        """
        SELECT COUNT(*)
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
        """,
    )

    active_support_incidents = get_count(
        conn,
        """
        SELECT COUNT(*)
        FROM support_incidents
        WHERE status IN ('open', 'investigating', 'waiting')
        """,
    )

    governance_findings_recent = get_count(
        conn,
        """
        SELECT COUNT(*)
        FROM audit_logs
        WHERE event_type = 'governance_finding_detected'
        """,
    )

    error_events = get_count(
        conn,
        """
        SELECT COUNT(*)
        FROM audit_logs
        WHERE severity IN ('error', 'critical')
        """,
    )

    if error_events > 0 or active_support_incidents > 0:
        overall_health = "needs_attention"
    elif active_operations_tasks > 0 or active_finance_actions > 0:
        overall_health = "watch"
    else:
        overall_health = "healthy"

    summary = {
        "overall_health": overall_health,
        "transactions_count": transactions_count,
        "active_finance_actions": active_finance_actions,
        "active_operations_tasks": active_operations_tasks,
        "active_support_incidents": active_support_incidents,
        "governance_findings_recent": governance_findings_recent,
        "error_events": error_events,
    }

    print("Command Center Summary:")
    print(f"Overall health: {summary['overall_health']}")
    print(f"Transactions: {summary['transactions_count']}")
    print(f"Active finance actions: {summary['active_finance_actions']}")
    print(f"Active operations tasks: {summary['active_operations_tasks']}")
    print(f"Active support incidents: {summary['active_support_incidents']}")
    print(f"Governance findings: {summary['governance_findings_recent']}")
    print(f"Error/Critical events: {summary['error_events']}")

    write_audit_log(
        conn,
        "command_center_summary_generated",
        "info",
        "Command center summary generated.",
        summary,
    )

    return summary
