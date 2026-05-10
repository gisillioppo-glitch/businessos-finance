import os
from datetime import date

from app.audit.audit_log import write_audit_log


def ensure_reports_folder():
    reports_path = "reports"

    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    return reports_path


def _format_alert_rows(alerts):
    if not alerts:
        return "No active executive alerts detected."

    rows = [
        "| Severity | Source | Owner | Alert | Recommended Action |",
        "| --- | --- | --- | --- | --- |",
    ]

    for alert in alerts:
        rows.append(
            "| "
            f"{alert['severity']} | "
            f"{alert['source_module']} | "
            f"{alert['owner_role']} | "
            f"{alert['title']} | "
            f"{alert['recommended_action']} |"
        )

    return "\n".join(rows)


def export_executive_alerts_report(conn, alerts, alert_brief):
    reports_path = ensure_reports_folder()
    report_date = date.today().isoformat()
    report_path = os.path.join(
        reports_path,
        f"executive_alerts_{report_date}.md",
    )

    alert_rows = _format_alert_rows(alerts)

    content = f"""# Executive Alerts Brief

Date: {report_date}

## Alert Summary

Total alerts: {alert_brief['total_alerts']}  
Critical alerts: {alert_brief['critical_alerts']}  
High alerts: {alert_brief['high_alerts']}  
Medium alerts: {alert_brief['medium_alerts']}  
Highest alert risk: {alert_brief['highest_alert_risk']}  

## Next Best Alert Move

{alert_brief['next_best_move']}

## Alert Queue

{alert_rows}
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Executive Alerts report exported: {report_path}")

    write_audit_log(
        conn,
        "executive_alerts_report_exported",
        "info",
        "Executive alerts report exported.",
        {"report_path": report_path},
    )

    return report_path
