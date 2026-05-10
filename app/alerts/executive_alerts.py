from app.audit.audit_log import write_audit_log
from app.governance.sensitivity_rules import get_governance_sensitivity_findings


SEVERITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "info": 4,
}


def _add_alert(alerts, title, message, severity, source_module, owner_role, recommended_action):
    alerts.append(
        {
            "title": title,
            "message": message,
            "severity": severity,
            "source_module": source_module,
            "owner_role": owner_role,
            "recommended_action": recommended_action,
        }
    )


def _sort_alerts(alerts):
    return sorted(
        alerts,
        key=lambda alert: (
            SEVERITY_ORDER.get(alert["severity"], 9),
            alert["source_module"],
            alert["title"],
        ),
    )


def get_executive_alerts(conn):
    alerts = []

    for finding in get_governance_sensitivity_findings(conn):
        _add_alert(
            alerts,
            finding["message"],
            f"Sensitivity finding from {finding['source']}.",
            finding["severity"],
            "governance",
            finding["metadata"].get("owner_role")
            or finding["metadata"].get("approver_role")
            or "Executive Owner",
            "Review sensitivity finding and confirm whether approval or justification is required.",
        )

    finance_rows = conn.execute(
        """
        SELECT priority, owner_role, risk_type, recommended_action, status
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
          AND priority IN ('high', 'medium')
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

    for priority, owner_role, risk_type, recommended_action, status in finance_rows:
        _add_alert(
            alerts,
            f"Finance action requires attention: {risk_type}",
            f"{status} finance recommendation assigned to {owner_role}.",
            priority,
            "finance",
            owner_role,
            recommended_action,
        )

    support_rows = conn.execute(
        """
        SELECT title, severity, status, owner_role
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
        LIMIT 5
        """
    ).fetchall()

    for title, severity, status, owner_role in support_rows:
        _add_alert(
            alerts,
            f"Support incident active: {title}",
            f"Incident is currently {status}.",
            severity,
            "support",
            owner_role,
            "Confirm resolution path and communicate expected next step.",
        )

    return _sort_alerts(alerts)


def print_executive_alerts(conn):
    alerts = get_executive_alerts(conn)

    if not alerts:
        print("Executive Alerts: No active executive alerts detected.")
        write_audit_log(
            conn,
            "executive_alerts_viewed",
            "info",
            "Executive alerts viewed with no active alerts.",
            {"alerts_visible": 0},
        )
        return []

    print("Executive Alerts:")

    for alert in alerts:
        print(
            f"[{alert['severity'].upper()}] "
            f"Source: {alert['source_module']} | "
            f"Owner: {alert['owner_role']} | "
            f"Alert: {alert['title']} | "
            f"Next: {alert['recommended_action']}"
        )

    write_audit_log(
        conn,
        "executive_alerts_viewed",
        "info",
        "Executive alerts viewed.",
        {"alerts_visible": len(alerts)},
    )

    return alerts


def print_executive_alerts_brief(conn, alerts=None):
    if alerts is None:
        alerts = get_executive_alerts(conn)

    critical_alerts = sum(1 for alert in alerts if alert["severity"] == "critical")
    high_alerts = sum(1 for alert in alerts if alert["severity"] == "high")
    medium_alerts = sum(1 for alert in alerts if alert["severity"] == "medium")

    if critical_alerts > 0:
        highest_alert_risk = "critical"
        next_best_move = "Stop dependent execution and review critical executive alerts immediately."
    elif high_alerts > 0:
        highest_alert_risk = "high"
        next_best_move = "Review high executive alerts and assign owner follow-up today."
    elif medium_alerts > 0:
        highest_alert_risk = "medium"
        next_best_move = "Review medium executive alerts and confirm next owner action."
    else:
        highest_alert_risk = "low"
        next_best_move = "Maintain current monitoring and continue regular operating rhythm."

    brief = {
        "total_alerts": len(alerts),
        "critical_alerts": critical_alerts,
        "high_alerts": high_alerts,
        "medium_alerts": medium_alerts,
        "highest_alert_risk": highest_alert_risk,
        "next_best_move": next_best_move,
    }

    print("Executive Alerts Brief:")
    print(f"Total alerts: {brief['total_alerts']}")
    print(f"Critical alerts: {brief['critical_alerts']}")
    print(f"High alerts: {brief['high_alerts']}")
    print(f"Medium alerts: {brief['medium_alerts']}")
    print(f"Highest alert risk: {brief['highest_alert_risk']}")
    print(f"Next best alert move: {brief['next_best_move']}")

    write_audit_log(
        conn,
        "executive_alerts_brief_viewed",
        "info",
        "Executive alerts brief viewed.",
        brief,
    )

    return brief
