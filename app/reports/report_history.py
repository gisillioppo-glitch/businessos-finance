import os

from app.audit.audit_log import write_audit_log
from app.reports.report_export import ensure_reports_folder


def print_report_history(conn):
    reports_path = ensure_reports_folder()

    report_files = [
        file_name
        for file_name in os.listdir(reports_path)
        if file_name.endswith(".md")
    ]

    report_files.sort(reverse=True)

    if not report_files:
        print("Report History: No reports found.")
        write_audit_log(
            conn,
            "report_history_viewed",
            "info",
            "Report history viewed with no reports found.",
            {"reports_found": 0},
        )
        return []

    print("Report History:")

    for file_name in report_files[:5]:
        print(f"- {os.path.join(reports_path, file_name)}")

    latest_report = os.path.join(reports_path, report_files[0])
    print(f"Latest report: {latest_report}")

    write_audit_log(
        conn,
        "report_history_viewed",
        "info",
        "Report history viewed.",
        {
            "reports_found": len(report_files),
            "latest_report": latest_report,
        },
    )

    return report_files
