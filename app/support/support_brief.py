from app.audit.audit_log import write_audit_log


def print_support_brief(conn, incident_kpis):
    print("Support Brief:")
    print(f"Open incidents: {incident_kpis['open']}")
    print(f"Investigating incidents: {incident_kpis['investigating']}")
    print(f"Waiting incidents: {incident_kpis['waiting']}")
    print(f"Resolved incidents: {incident_kpis['resolved']}")
    print(f"Dismissed incidents: {incident_kpis['dismissed']}")
    print(f"Critical incidents: {incident_kpis['critical']}")
    print(f"High incidents: {incident_kpis['high']}")

    if incident_kpis["critical"] > 0:
        highest_support_risk = "critical"
    elif incident_kpis["high"] > 0:
        highest_support_risk = "high"
    elif incident_kpis["medium"] > 0:
        highest_support_risk = "medium"
    elif incident_kpis["low"] > 0:
        highest_support_risk = "low"
    else:
        highest_support_risk = "none"

    print(f"Highest support risk: {highest_support_risk}")

    if incident_kpis["critical"] > 0:
        next_best_move = "Immediately investigate critical support incidents."
    elif incident_kpis["high"] > 0:
        next_best_move = "Prioritize high-severity support incidents."
    elif incident_kpis["waiting"] > 0:
        next_best_move = "Follow up on waiting support incidents."
    elif incident_kpis["investigating"] > 0:
        next_best_move = "Continue investigation and confirm resolution path."
    elif incident_kpis["open"] > 0:
        next_best_move = "Start investigation for open support incidents."
    else:
        next_best_move = "Maintain current support monitoring cadence."

    print(f"Next best support move: {next_best_move}")

    write_audit_log(
        conn,
        "support_brief_generated",
        "info",
        "Support brief generated.",
        {
            "open_incidents": incident_kpis["open"],
            "investigating_incidents": incident_kpis["investigating"],
            "waiting_incidents": incident_kpis["waiting"],
            "resolved_incidents": incident_kpis["resolved"],
            "dismissed_incidents": incident_kpis["dismissed"],
            "critical_incidents": incident_kpis["critical"],
            "high_incidents": incident_kpis["high"],
            "highest_support_risk": highest_support_risk,
            "next_best_move": next_best_move,
        },
    )

    return {
        "open_incidents": incident_kpis["open"],
        "investigating_incidents": incident_kpis["investigating"],
        "waiting_incidents": incident_kpis["waiting"],
        "resolved_incidents": incident_kpis["resolved"],
        "dismissed_incidents": incident_kpis["dismissed"],
        "critical_incidents": incident_kpis["critical"],
        "high_incidents": incident_kpis["high"],
        "highest_support_risk": highest_support_risk,
        "next_best_move": next_best_move,
    }
