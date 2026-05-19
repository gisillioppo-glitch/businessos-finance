from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.operations.escalation_rules import evaluate_operations_escalation_rules
from app.operations.operations_brief import print_operations_brief
from app.operations.task_views import print_operations_task_summary_kpis


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

REVIEW_COMMANDS = [
    ("Review active operations tasks", "python cli.py ops-tasks"),
    ("Evaluate operations escalations", "python cli.py ops-escalations"),
    ("Refresh operations brief", "python cli.py ops-brief"),
    ("Review command center impact", "python cli.py command-center"),
    ("Confirm release readiness", "python cli.py release-readiness"),
]

REVIEW_CLOSE_CRITERIA = [
    "Task has a documented outcome or justified dismissal.",
    "Owner confirms no unresolved operational dependency remains.",
    "No blocked high-priority operations task remains active.",
    "No overdue active task is driving Command Center attention.",
    "Daily Close can reference the operational status without ambiguity.",
]


def _active_tasks(conn):
    rows = conn.execute(
        """
        SELECT id, created_at, title, description, owner_role, priority,
               deadline_date, status, COALESCE(status_justification, ''),
               COALESCE(source_module, ''), COALESCE(source_reference_id, '')
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
        ORDER BY
            CASE priority
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            deadline_date ASC,
            created_at ASC
        """
    ).fetchall()

    return [
        {
            "id": row[0],
            "created_at": row[1],
            "title": row[2],
            "description": row[3] or "",
            "owner_role": row[4],
            "priority": row[5],
            "deadline_date": row[6] or "n/a",
            "status": row[7],
            "status_justification": row[8],
            "source_module": row[9],
            "source_reference_id": row[10],
        }
        for row in rows
    ]


def _review_status(kpis, escalations, tasks):
    if any(escalation["severity"] == "critical" for escalation in escalations):
        return "operations_review_critical_escalation"

    if escalations:
        return "operations_review_escalated"

    if kpis["blocked"] > 0:
        return "operations_review_blocked"

    if kpis["open"] > 0:
        return "operations_review_triage_required"

    if kpis["in_progress"] > 0:
        return "operations_review_monitoring_required"

    if tasks:
        return "operations_review_active"

    return "operations_clear"


def _review_recommendation(status):
    if status == "operations_review_critical_escalation":
        return "resolve_critical_blocker"

    if status == "operations_review_escalated":
        return "resolve_escalated_tasks"

    if status == "operations_review_blocked":
        return "unblock_active_tasks"

    if status == "operations_review_triage_required":
        return "start_highest_priority_task"

    if status == "operations_review_monitoring_required":
        return "confirm_progress"

    if status == "operations_review_active":
        return "confirm_owner_resolution_path"

    return "maintain_operations_cadence"


def _next_action(status, tasks, escalations):
    if escalations:
        first = escalations[0]
        return f"Resolve escalation for {first['title']} with {first['owner_role']}."

    if not tasks:
        return "Maintain operations monitoring cadence."

    first = tasks[0]

    if status == "operations_review_blocked":
        return f"Unblock {first['title']} with {first['owner_role']} before starting new work."

    if status == "operations_review_triage_required":
        return f"Start or assign {first['title']} and capture first progress evidence."

    if status == "operations_review_monitoring_required":
        return f"Follow up on {first['title']} and confirm measurable progress."

    return f"Confirm owner and close path for {first['title']}."


def _format_task_rows(tasks):
    rows = [
        "| ID | Status | Priority | Owner | Deadline | Title | Source |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for task in tasks:
        source = task["source_module"] or "n/a"
        if task["source_reference_id"]:
            source = f"{source}:{task['source_reference_id']}"
        rows.append(
            f"| {task['id']} | {task['status']} | {task['priority']} | {task['owner_role']} | {task['deadline_date']} | {task['title']} | {source} |"
        )

    return "\n".join(rows)


def _format_escalation_rows(escalations):
    rows = [
        "| Severity | Type | Owner | Task | Message |",
        "| --- | --- | --- | --- | --- |",
    ]

    for escalation in escalations:
        rows.append(
            f"| {escalation['severity']} | {escalation['escalation_type']} | {escalation['owner_role']} | {escalation['title']} | {escalation['message']} |"
        )

    return "\n".join(rows)


def _format_bullets(items):
    if not items:
        return "- None."

    return "\n".join(f"- {item}" for item in items)


def _format_commands(commands):
    rows = [
        "| Purpose | Command |",
        "| --- | --- |",
    ]

    for purpose, command in commands:
        rows.append(f"| {purpose} | `{command}` |")

    return "\n".join(rows)


def generate_operations_area_review(conn):
    task_kpis = print_operations_task_summary_kpis(conn)
    escalations = evaluate_operations_escalation_rules(conn)
    operations_brief = print_operations_brief(conn, task_kpis, escalations)
    tasks = _active_tasks(conn)
    status = _review_status(task_kpis, escalations, tasks)

    return {
        "date": date.today().isoformat(),
        "review_status": status,
        "review_recommendation": _review_recommendation(status),
        "highest_operational_risk": operations_brief["highest_operational_risk"],
        "active_tasks": len(tasks),
        "open_tasks": task_kpis["open"],
        "in_progress_tasks": task_kpis["in_progress"],
        "blocked_tasks": task_kpis["blocked"],
        "critical_tasks": task_kpis["critical"],
        "high_tasks": task_kpis["high"],
        "medium_tasks": task_kpis["medium"],
        "low_tasks": task_kpis["low"],
        "escalations_detected": len(escalations),
        "tasks": tasks,
        "escalations": escalations,
        "commands": REVIEW_COMMANDS,
        "close_criteria": REVIEW_CLOSE_CRITERIA,
        "next_action": _next_action(status, tasks, escalations),
    }


def export_operations_area_review(conn):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_operations_area_review(conn)
    report_path = REPORTS_DIR / f"operations_area_review_{result['date']}.md"

    content = f"""# Operations Area Review v0.1

Date: {result['date']}

## Operations Area Summary

Review status: {result['review_status']}
Review recommendation: {result['review_recommendation']}
Highest operational risk: {result['highest_operational_risk']}
Active tasks: {result['active_tasks']}
Open tasks: {result['open_tasks']}
In-progress tasks: {result['in_progress_tasks']}
Blocked tasks: {result['blocked_tasks']}
Critical priority tasks: {result['critical_tasks']}
High priority tasks: {result['high_tasks']}
Medium priority tasks: {result['medium_tasks']}
Low priority tasks: {result['low_tasks']}
Escalations detected: {result['escalations_detected']}
Next action: {result['next_action']}

## Active Tasks

{_format_task_rows(result['tasks']) if result['tasks'] else 'No active operations tasks.'}

## Escalations

{_format_escalation_rows(result['escalations']) if result['escalations'] else 'No operations escalations detected.'}

## Review Commands

{_format_commands(result['commands'])}

## Close Criteria

{_format_bullets(result['close_criteria'])}

## Operator Note

This review is advisory and read-only. It does not complete, dismiss, or reassign operations tasks automatically. An operations task should only move to completed or dismissed when the owner has enough evidence to justify the status change.
"""

    report_path.write_text(content, encoding="utf-8")

    write_audit_log(
        conn,
        "operations_area_review_exported",
        "info" if result["review_status"] == "operations_clear" else "warning",
        "Operations area review exported.",
        {
            "report_path": str(report_path.relative_to(ROOT_DIR)),
            "review_status": result["review_status"],
            "active_tasks": result["active_tasks"],
            "highest_operational_risk": result["highest_operational_risk"],
            "escalations_detected": result["escalations_detected"],
        },
    )

    return result, str(report_path)


def print_operations_area_review(conn):
    result, report_path = export_operations_area_review(conn)

    print("Operations Area Review:")
    print(f"Date: {result['date']}")
    print(f"Review status: {result['review_status']}")
    print(f"Review recommendation: {result['review_recommendation']}")
    print(f"Highest operational risk: {result['highest_operational_risk']}")
    print(f"Active tasks: {result['active_tasks']}")
    print(f"Escalations detected: {result['escalations_detected']}")
    print(f"Next action: {result['next_action']}")
    print(f"Operations area review exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return result
