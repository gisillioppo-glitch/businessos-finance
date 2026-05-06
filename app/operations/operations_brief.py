from app.audit.audit_log import write_audit_log


def print_operations_brief(conn, task_kpis, escalations):
    print("Operations Brief:")
    print(f"Open tasks: {task_kpis['open']}")
    print(f"In-progress tasks: {task_kpis['in_progress']}")
    print(f"Blocked tasks: {task_kpis['blocked']}")
    print(f"Completed tasks: {task_kpis['completed']}")
    print(f"Dismissed tasks: {task_kpis['dismissed']}")
    print(f"Escalations detected: {len(escalations)}")

    if escalations:
        highest_operational_risk = (
            "critical"
            if any(escalation["severity"] == "critical" for escalation in escalations)
            else "high"
        )
        print(f"Highest operational risk: {highest_operational_risk}")
    else:
        highest_operational_risk = "none"
        print("Highest operational risk: none")

    if escalations:
        next_best_move = "Review and resolve the highest-severity operations escalation."
    elif task_kpis["blocked"] > 0:
        next_best_move = "Unblock active operations tasks before starting new work."
    elif task_kpis["open"] > 0:
        next_best_move = "Start the highest-priority open operations task."
    elif task_kpis["in_progress"] > 0:
        next_best_move = "Follow up on in-progress operations tasks and confirm progress."
    else:
        next_best_move = "Maintain current operations cadence and monitor for new tasks."

    print(f"Next best move: {next_best_move}")

    write_audit_log(
        conn,
        "operations_brief_generated",
        "info",
        "Operations brief generated.",
        {
            "open_tasks": task_kpis["open"],
            "in_progress_tasks": task_kpis["in_progress"],
            "blocked_tasks": task_kpis["blocked"],
            "completed_tasks": task_kpis["completed"],
            "dismissed_tasks": task_kpis["dismissed"],
            "escalations_detected": len(escalations),
            "highest_operational_risk": highest_operational_risk,
            "next_best_move": next_best_move,
        },
    )

    return {
        "open_tasks": task_kpis["open"],
        "in_progress_tasks": task_kpis["in_progress"],
        "blocked_tasks": task_kpis["blocked"],
        "completed_tasks": task_kpis["completed"],
        "dismissed_tasks": task_kpis["dismissed"],
        "escalations_detected": len(escalations),
        "highest_operational_risk": highest_operational_risk,
        "next_best_move": next_best_move,
    }
