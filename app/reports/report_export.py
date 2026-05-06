import os
from datetime import date

from app.audit.audit_log import write_audit_log


def ensure_reports_folder():
    reports_path = "reports"
    if not os.path.exists(reports_path):
        os.makedirs(reports_path)
    return reports_path


def export_daily_brief_report(conn, executive_brief):
    reports_path = ensure_reports_folder()
    report_date = date.today().isoformat()
    report_path = os.path.join(reports_path, f"daily_brief_{report_date}.md")

    content = f"""# Daily Executive Brief

Date: {report_date}

## Financial Summary

Financial health: {executive_brief['financial_health']}  
Net cash flow: ${executive_brief['net_cash_flow']:.2f}  
Expense ratio: {executive_brief['expense_ratio'] * 100:.2f}%  

## Risk Summary

Financial risks detected: {executive_brief['risks_detected']}  
Highest risk level: {executive_brief['highest_risk']}  

## Action Summary

Open actions: {executive_brief['open_actions']}  
In-progress actions: {executive_brief['in_progress_actions']}  

## Next Best Move

{executive_brief['next_best_move']}
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Report exported: {report_path}")

    write_audit_log(
        conn,
        "daily_brief_report_exported",
        "info",
        "Daily executive brief report exported.",
        {"report_path": report_path},
    )

    return report_path
