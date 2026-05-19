from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.support.incident_views import print_support_incident_summary_kpis
from app.support.support_brief import print_support_brief


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

REVIEW_COMMANDS = [
    ("Review active support incidents", "python cli.py support-incidents"),
    ("Refresh support brief", "python cli.py support-brief"),
    ("Export support report", "python cli.py support-report"),
    ("Review command center impact", "python cli.py command-center"),
    ("Confirm release readiness", "python cli.py release-readiness"),
]

REVIEW_CLOSE_CRITERIA = [
    "Incident has a documented root cause or reason for dismissal.",
    "Owner confirms no unresolved action remains.",
    "No high or critical support incident is open.",
    "Command Center no longer depends on the incident for next best executive move.",
    "Daily Close can reference the resolution without ambiguity.",
]


def _active_incidents(conn):
    rows = conn.execute(
        """
        SELECT id, created_at, title, description, severity, owner_role, status,
               COALESCE(status_justification, ''), COALESCE(source_module, ''),
               COALESCE(source_reference_id, '')
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

    return [
        {
            "id": row[0],
            "created_at": row[1],
            "title": row[2],
            "description": row[3] or "",
            "severity": row[4],
            "owner_role": row[5],
            "status": row[6],
            "status_justification": row[7],
            "source_module": row[8],
            "source_reference_id": row[9],
        }
        for row in rows
    ]


def _review_status(kpis, incidents):
    if kpis["critical"] > 0 or kpis["high"] > 0:
        return "support_review_escalated"

    if kpis["waiting"] > 0:
        return "support_review_waiting"

    if kpis["investigating"] > 0:
        return "support_review_monitoring_required"

    if kpis["open"] > 0:
        return "support_review_triage_required"

    if incidents:
        return "support_review_active"

    return "support_clear"


def _review_recommendation(status):
    if status == "support_review_escalated":
        return "prioritize_escalated_incidents"

    if status == "support_review_waiting":
        return "follow_up_waiting_incidents"

    if status == "support_review_monitoring_required":
        return "continue_investigation"

    if status == "support_review_triage_required":
        return "start_triage"

    if status == "support_review_active":
        return "confirm_owner_resolution_path"

    return "maintain_monitoring"


def _next_action(status, incidents):
    if not incidents:
        return "Maintain support monitoring cadence."

    first = incidents[0]

    if status == "support_review_escalated":
        return f"Prioritize {first['title']} with {first['owner_role']} before expanding workload."

    if status == "support_review_waiting":
        return f"Follow up with {first['owner_role']} and confirm what is blocking {first['title']}."

    if status == "support_review_monitoring_required":
        return f"Continue investigation for {first['title']} and capture resolution evidence before closing."

    return f"Confirm owner and next action for {first['title']}."


def _format_incident_rows(incidents):
    rows = [
        "| ID | Status | Severity | Owner | Title | Source |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for incident in incidents:
        source = incident["source_module"] or "n/a"
        if incident["source_reference_id"]:
            source = f"{source}:{incident['source_reference_id']}"
        rows.append(
            f"| {incident['id']} | {incident['status']} | {incident['severity']} | {incident['owner_role']} | {incident['title']} | {source} |"
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


def generate_support_area_review(conn):
    kpis = print_support_incident_summary_kpis(conn)
    support_brief = print_support_brief(conn, kpis)
    incidents = _active_incidents(conn)
    status = _review_status(kpis, incidents)

    return {
        "date": date.today().isoformat(),
        "review_status": status,
        "review_recommendation": _review_recommendation(status),
        "highest_support_risk": support_brief["highest_support_risk"],
        "active_incidents": len(incidents),
        "open_incidents": kpis["open"],
        "investigating_incidents": kpis["investigating"],
        "waiting_incidents": kpis["waiting"],
        "critical_incidents": kpis["critical"],
        "high_incidents": kpis["high"],
        "medium_incidents": kpis["medium"],
        "low_incidents": kpis["low"],
        "incidents": incidents,
        "commands": REVIEW_COMMANDS,
        "close_criteria": REVIEW_CLOSE_CRITERIA,
        "next_action": _next_action(status, incidents),
    }


def export_support_area_review(conn):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_support_area_review(conn)
    report_path = REPORTS_DIR / f"support_area_review_{result['date']}.md"

    content = f"""# Support Area Review v0.1

Date: {result['date']}

## Support Area Summary

Review status: {result['review_status']}
Review recommendation: {result['review_recommendation']}
Highest support risk: {result['highest_support_risk']}
Active incidents: {result['active_incidents']}
Open incidents: {result['open_incidents']}
Investigating incidents: {result['investigating_incidents']}
Waiting incidents: {result['waiting_incidents']}
Critical incidents: {result['critical_incidents']}
High incidents: {result['high_incidents']}
Medium incidents: {result['medium_incidents']}
Low incidents: {result['low_incidents']}
Next action: {result['next_action']}

## Active Incidents

{_format_incident_rows(result['incidents']) if result['incidents'] else 'No active support incidents.'}

## Review Commands

{_format_commands(result['commands'])}

## Close Criteria

{_format_bullets(result['close_criteria'])}

## Operator Note

This review is advisory and read-only. It does not resolve incidents automatically. A support incident should only move to resolved or dismissed when the owner has enough evidence to justify the status change.
"""

    report_path.write_text(content, encoding="utf-8")

    write_audit_log(
        conn,
        "support_area_review_exported",
        "info" if result["review_status"] == "support_clear" else "warning",
        "Support area review exported.",
        {
            "report_path": str(report_path.relative_to(ROOT_DIR)),
            "review_status": result["review_status"],
            "active_incidents": result["active_incidents"],
            "highest_support_risk": result["highest_support_risk"],
        },
    )

    return result, str(report_path)


def print_support_area_review(conn):
    result, report_path = export_support_area_review(conn)

    print("Support Area Review:")
    print(f"Date: {result['date']}")
    print(f"Review status: {result['review_status']}")
    print(f"Review recommendation: {result['review_recommendation']}")
    print(f"Highest support risk: {result['highest_support_risk']}")
    print(f"Active incidents: {result['active_incidents']}")
    print(f"Investigating incidents: {result['investigating_incidents']}")
    print(f"Next action: {result['next_action']}")
    print(f"Support area review exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return result
