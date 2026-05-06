from datetime import date

from app.audit.audit_log import write_audit_log


def evaluate_operations_escalation_rules(conn):
    escalations = []

    rows = conn.execute(
        """
        SELECT id, title, owner_role, priority, deadline_date, status
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
        """
    ).fetchall()

    today = date.today().isoformat()

    for task_id, title, owner_role, priority, deadline_date, status in rows:
        if deadline_date and deadline_date < today:
            escalations.append(
                {
                    "escalation_type": "overdue_task",
                    "severity": "high",
                    "task_id": task_id,
                    "title": title,
                    "owner_role": owner_role,
                    "priority": priority,
                    "deadline_date": deadline_date,
                    "status": status,
                    "message": f"Overdue operations task: {title}.",
                }
            )

        if status == "blocked" and priority in {"high", "critical"}:
            escalations.append(
                {
                    "escalation_type": "blocked_high_priority_task",
                    "severity": "critical",
                    "task_id": task_id,
                    "title": title,
                    "owner_role": owner_role,
                    "priority": priority,
                    "deadline_date": deadline_date,
                    "status": status,
                    "message": f"Blocked high-priority operations task: {title}.",
                }
            )

    if not escalations:
        print("Operations Escalation Rules: No escalations detected.")
        write_audit_log(
            conn,
            "operations_escalation_rules_evaluated",
            "info",
            "Operations escalation rules evaluated with no escalations detected.",
            {"escalations_found": 0},
        )
        return []

    print("Operations Escalation Rules:")

    for escalation in escalations:
        print(f"[{escalation['severity'].upper()}] {escalation['message']}")

        write_audit_log(
            conn,
            "operations_escalation_detected",
            escalation["severity"],
            escalation["message"],
            escalation,
        )

    write_audit_log(
        conn,
        "operations_escalation_rules_evaluated",
        "info",
        "Operations escalation rules evaluated.",
        {"escalations_found": len(escalations)},
    )

    return escalations
