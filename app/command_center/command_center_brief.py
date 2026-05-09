from app.audit.audit_log import write_audit_log


def print_command_center_brief(conn, summary):
    print("Command Center Brief:")
    print(f"Overall health: {summary['overall_health']}")

    if summary["error_events"] > 0:
        highest_system_risk = "critical"
    elif summary["active_support_incidents"] > 0:
        highest_system_risk = "high"
    elif summary["active_operations_tasks"] > 0:
        highest_system_risk = "medium"
    elif summary["active_finance_actions"] > 0:
        highest_system_risk = "medium"
    else:
        highest_system_risk = "none"

    print(f"Highest system risk: {highest_system_risk}")

    if summary["error_events"] > 0:
        next_best_move = "Review critical or error events immediately and assign incident response."
    elif summary["active_support_incidents"] > 0:
        next_best_move = "Resolve active support incidents before expanding operational workload."
    elif summary["governance_findings_recent"] > 0:
        next_best_move = "Review governance findings and resolve audit trail issues."
    elif summary["active_operations_tasks"] > 0:
        next_best_move = "Review active operations tasks and unblock execution."
    elif summary["active_finance_actions"] > 0:
        next_best_move = "Review active finance actions and confirm owner follow-up."
    else:
        next_best_move = "Maintain current operating cadence and continue monitoring."

    print(f"Next best executive move: {next_best_move}")

    brief = {
        "overall_health": summary["overall_health"],
        "highest_system_risk": highest_system_risk,
        "next_best_move": next_best_move,
        "transactions_count": summary["transactions_count"],
        "active_finance_actions": summary["active_finance_actions"],
        "active_operations_tasks": summary["active_operations_tasks"],
        "active_support_incidents": summary["active_support_incidents"],
        "governance_findings_recent": summary["governance_findings_recent"],
        "error_events": summary["error_events"],
    }

    write_audit_log(
        conn,
        "command_center_brief_generated",
        "info",
        "Command center brief generated.",
        brief,
    )

    return brief
