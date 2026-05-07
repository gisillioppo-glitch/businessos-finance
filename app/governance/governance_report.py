import os
from datetime import date

from app.audit.audit_log import write_audit_log


def ensure_reports_folder():
    reports_path = "reports"

    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    return reports_path


def export_governance_report(conn, governance_brief):
    reports_path = ensure_reports_folder()
    report_date = date.today().isoformat()
    report_path = os.path.join(
        reports_path,
        f"governance_brief_{report_date}.md",
    )

    content = f"""# Governance Brief

Date: {report_date}

## Governance Summary

Governance findings detected: {governance_brief['findings_detected']}  
Highest governance risk: {governance_brief['highest_governance_risk']}  
Audit trail health: {governance_brief['audit_trail_health']}  

## Next Best Governance Move

{governance_brief['next_best_move']}
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Governance report exported: {report_path}")

    write_audit_log(
        conn,
        "governance_report_exported",
        "info",
        "Governance report exported.",
        {"report_path": report_path},
    )

    return report_path
