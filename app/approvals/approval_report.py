import os
from datetime import date

from app.audit.audit_log import write_audit_log


def ensure_reports_folder():
    reports_path = "reports"

    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    return reports_path


def get_approval_requests_for_report(conn):
    return conn.execute(
        """
        SELECT title,
               approval_type,
               priority,
               status,
               approver_role,
               requester_role,
               source_module,
               status_justification
        FROM approval_requests
        ORDER BY
            CASE status
                WHEN 'pending' THEN 1
                WHEN 'approved' THEN 2
                WHEN 'rejected' THEN 3
                WHEN 'cancelled' THEN 4
                ELSE 5
            END,
            CASE priority
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            created_at DESC
        """
    ).fetchall()


def _format_approval_rows(rows):
    if not rows:
        return "No approval requests found."

    table = [
        "| Priority | Status | Type | Approver | Requester | Source | Approval | Justification |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        (
            title,
            approval_type,
            priority,
            status,
            approver_role,
            requester_role,
            source_module,
            status_justification,
        ) = row

        table.append(
            "| "
            f"{priority} | "
            f"{status} | "
            f"{approval_type} | "
            f"{approver_role} | "
            f"{requester_role or 'n/a'} | "
            f"{source_module or 'n/a'} | "
            f"{title} | "
            f"{status_justification or 'n/a'} |"
        )

    return "\n".join(table)


def export_approval_report(conn, approval_kpis, approval_brief):
    reports_path = ensure_reports_folder()
    report_date = date.today().isoformat()
    report_path = os.path.join(
        reports_path,
        f"approval_decisions_{report_date}.md",
    )

    approval_rows = _format_approval_rows(get_approval_requests_for_report(conn))

    content = f"""# Approval Decision Brief

Date: {report_date}

## Approval Summary

Pending approvals: {approval_kpis['pending']}  
Approved approvals: {approval_kpis['approved']}  
Rejected approvals: {approval_kpis['rejected']}  
Cancelled approvals: {approval_kpis['cancelled']}  
Critical approvals: {approval_kpis['critical']}  
High approvals: {approval_kpis['high']}  
Medium approvals: {approval_kpis['medium']}  
Low approvals: {approval_kpis['low']}  
Decision approvals: {approval_kpis['decision']}  
Incident approvals: {approval_kpis['incident']}  

## Risk Summary

Highest approval risk: {approval_brief['highest_approval_risk']}  

## Next Best Approval Move

{approval_brief['next_best_move']}

## Approval Decision Queue

{approval_rows}
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Approval Decision report exported: {report_path}")

    write_audit_log(
        conn,
        "approval_decision_report_exported",
        "info",
        "Approval decision report exported.",
        {"report_path": report_path},
    )

    return report_path
