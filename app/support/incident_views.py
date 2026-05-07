from app.audit.audit_log import write_audit_log


def print_support_incidents_list(conn):
    rows = conn.execute(
        """
        SELECT status, severity, owner_role, title
        FROM support_incidents
        WHERE status IN ('open', 'investigating', 'waiting')
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
        print("Support Incident List: No active support incidents.")
        write_audit_log(
            conn,
            "support_incident_list_viewed",
            "info",
            "Support incident list viewed with no active incidents.",
            {"incidents_visible": 0},
        )
        return []

    print("Support Incident List:")

    for status, severity, owner_role, title in rows:
        print(
            f"[{severity.upper()}] "
            f"Status: {status} | "
            f"Owner: {owner_role} | "
            f"Incident: {title}"
        )

    write_audit_log(
        conn,
        "support_incident_list_viewed",
        "info",
        "Support incident list viewed.",
        {"incidents_visible": len(rows)},
    )

    return rows


def print_support_incident_summary_kpis(conn):
    rows = conn.execute(
        """
        SELECT status, severity, COUNT(*) AS count
        FROM support_incidents
        GROUP BY status, severity
        """
    ).fetchall()

    summary = {
        "open": 0,
        "investigating": 0,
        "waiting": 0,
        "resolved": 0,
        "dismissed": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for status, severity, count in rows:
        if status in summary:
            summary[status] += count

        if severity in summary:
            summary[severity] += count

    print("Support Incident Summary KPIs:")
    print(f"Open incidents: {summary['open']}")
    print(f"Investigating incidents: {summary['investigating']}")
    print(f"Waiting incidents: {summary['waiting']}")
    print(f"Resolved incidents: {summary['resolved']}")
    print(f"Dismissed incidents: {summary['dismissed']}")
    print(f"Critical incidents: {summary['critical']}")
    print(f"High incidents: {summary['high']}")
    print(f"Medium incidents: {summary['medium']}")
    print(f"Low incidents: {summary['low']}")

    write_audit_log(
        conn,
        "support_incident_summary_kpis_viewed",
        "info",
        "Support incident summary KPIs viewed.",
        summary,
    )

    return summary
