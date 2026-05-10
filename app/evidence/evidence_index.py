import os
from datetime import date

from app.audit.audit_log import write_audit_log


EVIDENCE_REPORTS = [
    {
        "label": "Command Center",
        "file_prefix": "command_center",
        "purpose": "Unified executive system summary.",
    },
    {
        "label": "Executive Alerts",
        "file_prefix": "executive_alerts",
        "purpose": "Cross-module executive alert queue.",
    },
    {
        "label": "Approval Decisions",
        "file_prefix": "approval_decisions",
        "purpose": "Approval outcomes, decisions, and justifications.",
    },
    {
        "label": "Governance Brief",
        "file_prefix": "governance_brief",
        "purpose": "Governance posture and audit trail health.",
    },
    {
        "label": "Support Brief",
        "file_prefix": "support_brief",
        "purpose": "Support incident status and next move.",
    },
    {
        "label": "Daily Finance Brief",
        "file_prefix": "daily_brief",
        "purpose": "Finance health, risks, and recommended actions.",
    },
]


def ensure_reports_folder():
    reports_path = "reports"

    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    return reports_path


def get_executive_evidence_index(report_date=None):
    reports_path = ensure_reports_folder()
    resolved_date = report_date or date.today().isoformat()
    evidence_items = []

    for report in EVIDENCE_REPORTS:
        file_name = f"{report['file_prefix']}_{resolved_date}.md"
        report_path = os.path.join(reports_path, file_name)
        exists = os.path.exists(report_path)

        evidence_items.append(
            {
                "label": report["label"],
                "purpose": report["purpose"],
                "file_name": file_name,
                "report_path": report_path,
                "status": "available" if exists else "missing",
            }
        )

    available_count = sum(1 for item in evidence_items if item["status"] == "available")

    return {
        "date": resolved_date,
        "available_count": available_count,
        "missing_count": len(evidence_items) - available_count,
        "total_count": len(evidence_items),
        "items": evidence_items,
    }


def print_executive_evidence_index(conn, report_date=None):
    evidence_index = get_executive_evidence_index(report_date)

    print("Executive Evidence Index:")
    print(f"Date: {evidence_index['date']}")
    print(f"Available evidence: {evidence_index['available_count']}")
    print(f"Missing evidence: {evidence_index['missing_count']}")

    for item in evidence_index["items"]:
        print(
            f"[{item['status'].upper()}] "
            f"{item['label']} | {item['report_path']} | {item['purpose']}"
        )

    write_audit_log(
        conn,
        "executive_evidence_index_viewed",
        "info",
        "Executive evidence index viewed.",
        {
            "date": evidence_index["date"],
            "available_count": evidence_index["available_count"],
            "missing_count": evidence_index["missing_count"],
            "total_count": evidence_index["total_count"],
        },
    )

    return evidence_index


def _format_evidence_rows(evidence_index):
    rows = [
        "| Evidence | Status | Report Path | Purpose |",
        "| --- | --- | --- | --- |",
    ]

    for item in evidence_index["items"]:
        rows.append(
            "| "
            f"{item['label']} | "
            f"{item['status']} | "
            f"{item['report_path']} | "
            f"{item['purpose']} |"
        )

    return "\n".join(rows)


def export_executive_evidence_index(conn, report_date=None):
    reports_path = ensure_reports_folder()
    evidence_index = print_executive_evidence_index(conn, report_date)
    report_path = os.path.join(
        reports_path,
        f"executive_evidence_index_{evidence_index['date']}.md",
    )

    content = f"""# Executive Evidence Index

Date: {evidence_index['date']}

## Evidence Summary

Available evidence: {evidence_index['available_count']}  
Missing evidence: {evidence_index['missing_count']}  
Total expected evidence items: {evidence_index['total_count']}  

## Evidence Register

{_format_evidence_rows(evidence_index)}
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Executive Evidence Index exported: {report_path}")

    write_audit_log(
        conn,
        "executive_evidence_index_exported",
        "info",
        "Executive evidence index exported.",
        {"report_path": report_path},
    )

    return report_path
