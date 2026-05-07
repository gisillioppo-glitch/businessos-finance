import os
from datetime import date

from app.audit.audit_log import write_audit_log


def ensure_reports_folder():
    reports_path = "reports"

    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    return reports_path


def export_support_report(conn, support_brief):
    reports_path = ensure_reports_folder()
    report_date = date.today().isoformat()
    report_path = os.path.join(
        reports_path,
        f"support_brief_{report_date}.md",
    )

    content = f"""# Support Brief

Date: {report_date}

## Support Summary

Open incidents: {support_brief['open_incidents']}  
Investigating incidents: {support_brief['investigating_incidents']}  
Waiting incidents: {support_brief['waiting_incidents']}  
Resolved incidents: {support_brief['resolved_incidents']}  
Dismissed incidents: {support_brief['dismissed_incidents']}  

## Risk Summary

Critical incidents: {support_brief['critical_incidents']}  
High incidents: {support_brief['high_incidents']}  
Highest support risk: {support_brief['highest_support_risk']}  

## Next Best Support Move

{support_brief['next_best_move']}
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Support report exported: {report_path}")

    write_audit_log(
        conn,
        "support_report_exported",
        "info",
        "Support report exported.",
        {"report_path": report_path},
    )

    return report_path
