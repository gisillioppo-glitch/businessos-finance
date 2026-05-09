import os
from datetime import date

from app.audit.audit_log import write_audit_log


def ensure_reports_folder():
    reports_path = "reports"

    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    return reports_path


def export_command_center_report(conn, command_brief):
    reports_path = ensure_reports_folder()
    report_date = date.today().isoformat()
    report_path = os.path.join(
        reports_path,
        f"command_center_{report_date}.md",
    )

    content = f"""# BusinessOS Command Center Brief

Date: {report_date}

## Executive Summary

Overall health: {command_brief['overall_health']}  
Highest system risk: {command_brief['highest_system_risk']}  

## Module Snapshot

Transactions: {command_brief['transactions_count']}  
Active finance actions: {command_brief['active_finance_actions']}  
Active operations tasks: {command_brief['active_operations_tasks']}  
Active support incidents: {command_brief['active_support_incidents']}  
Governance findings: {command_brief['governance_findings_recent']}  
Error/Critical events: {command_brief['error_events']}  

## Next Best Executive Move

{command_brief['next_best_move']}
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Command Center report exported: {report_path}")

    write_audit_log(
        conn,
        "command_center_report_exported",
        "info",
        "Command center report exported.",
        {"report_path": report_path},
    )

    return report_path
