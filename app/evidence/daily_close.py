import os
from datetime import date

from app.audit.audit_log import write_audit_log


def ensure_reports_folder():
    reports_path = "reports"

    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    return reports_path


def _format_step_rows(close_steps):
    rows = [
        "| Step | Status | Detail |",
        "| --- | --- | --- |",
    ]

    for step in close_steps:
        rows.append(
            "| "
            f"{step['name']} | "
            f"{step['status']} | "
            f"{step['detail']} |"
        )

    return "\n".join(rows)


def export_daily_close_report(conn, close_steps, evidence_index):
    reports_path = ensure_reports_folder()
    report_date = date.today().isoformat()
    report_path = os.path.join(reports_path, f"daily_close_{report_date}.md")

    completed_steps = sum(1 for step in close_steps if step["status"] == "completed")

    content = f"""# Executive Daily Close

Date: {report_date}

## Close Summary

Completed close steps: {completed_steps}  
Total close steps: {len(close_steps)}  
Evidence available: {evidence_index['available_count']}  
Evidence missing: {evidence_index['missing_count']}  

## Close Steps

{_format_step_rows(close_steps)}

## Evidence Index

Evidence index report: `reports/executive_evidence_index_{report_date}.md`
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Executive Daily Close exported: {report_path}")

    write_audit_log(
        conn,
        "executive_daily_close_exported",
        "info",
        "Executive daily close exported.",
        {
            "report_path": report_path,
            "completed_steps": completed_steps,
            "total_steps": len(close_steps),
            "evidence_available": evidence_index["available_count"],
            "evidence_missing": evidence_index["missing_count"],
        },
    )

    return report_path
