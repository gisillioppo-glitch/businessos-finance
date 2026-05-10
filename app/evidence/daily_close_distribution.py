import os
from datetime import date

from app.audit.audit_log import write_audit_log
from app.evidence.evidence_index import get_executive_evidence_index
from app.notifications.outbox import queue_notification
from app.people.schema import create_business_users_table
from app.people.users import ensure_default_business_users


DEPARTMENT_REPORTS = {
    "Executive": [
        "Command Center",
        "Executive Alerts",
        "Approval Decisions",
        "Governance Brief",
        "Support Brief",
        "Daily Finance Brief",
    ],
    "Finance": ["Daily Finance Brief", "Command Center", "Executive Alerts"],
    "Operations": ["Command Center", "Executive Alerts", "Approval Decisions"],
    "Governance": ["Governance Brief", "Approval Decisions", "Executive Alerts"],
    "Support": ["Support Brief", "Executive Alerts", "Command Center"],
}


def ensure_reports_folder():
    reports_path = "reports"

    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    return reports_path


def _get_active_recipients(conn):
    create_business_users_table(conn)
    ensure_default_business_users(conn)

    rows = conn.execute(
        """
        SELECT full_name, email, role, department, access_level
        FROM business_users
        WHERE status = 'active'
          AND access_level IN ('admin', 'executive', 'manager')
        ORDER BY
            CASE access_level
                WHEN 'admin' THEN 1
                WHEN 'executive' THEN 2
                WHEN 'manager' THEN 3
                ELSE 4
            END,
            department,
            full_name
        """
    ).fetchall()

    return [
        {
            "full_name": row[0],
            "email": row[1],
            "role": row[2],
            "department": row[3],
            "access_level": row[4],
        }
        for row in rows
    ]


def _select_reports_for_recipient(recipient, evidence_items):
    if recipient["access_level"] in {"admin", "executive"}:
        allowed_labels = DEPARTMENT_REPORTS["Executive"]
    else:
        allowed_labels = DEPARTMENT_REPORTS.get(
            recipient["department"],
            ["Command Center", "Executive Alerts"],
        )

    return [item for item in evidence_items if item["label"] in allowed_labels]


def _format_report_list(reports):
    lines = []

    for report in reports:
        lines.append(
            f"- {report['label']}: {report['status']} | {report['report_path']}"
        )

    return "\n".join(lines)


def _format_package_rows(packages):
    rows = [
        "| Recipient | Role | Department | Reports | Status |",
        "| --- | --- | --- | --- | --- |",
    ]

    for package in packages:
        report_labels = ", ".join(report["label"] for report in package["reports"])
        rows.append(
            "| "
            f"{package['recipient']['full_name']} | "
            f"{package['recipient']['role']} | "
            f"{package['recipient']['department']} | "
            f"{report_labels} | "
            f"{package['status']} |"
        )

    return "\n".join(rows)


def _build_email_subject(evidence_index):
    return f"BusinessOS Daily Close - {evidence_index['date']}"


def _build_email_body(recipient, reports, evidence_index):
    return f"""BusinessOS completed the executive daily close for {evidence_index['date']}.

Evidence available: {evidence_index['available_count']}
Evidence missing: {evidence_index['missing_count']}
Total evidence items: {evidence_index['total_count']}

Recommended review:
{_format_report_list(reports)}

Next action: Review the attached/linked evidence for your area and confirm any required follow-up.
"""


def _format_email_ready_messages(packages, evidence_index):
    sections = []

    for package in packages:
        recipient = package["recipient"]
        subject = package["subject"]
        body = f"""### {recipient['full_name']}

To: {recipient['email']}  
Role: {recipient['role']}  
Department: {recipient['department']}  
Subject: {subject}

{package['body']}"""
        sections.append(body)

    return "\n".join(sections)


def get_daily_close_distribution(conn, report_date=None):
    resolved_date = report_date or date.today().isoformat()
    evidence_index = get_executive_evidence_index(resolved_date)
    recipients = _get_active_recipients(conn)
    packages = []

    for recipient in recipients:
        reports = _select_reports_for_recipient(recipient, evidence_index["items"])
        missing_count = sum(1 for report in reports if report["status"] == "missing")
        packages.append(
            {
                "recipient": recipient,
                "reports": reports,
                "subject": _build_email_subject(evidence_index),
                "body": _build_email_body(recipient, reports, evidence_index),
                "status": "ready" if missing_count == 0 else "needs_attention",
                "missing_count": missing_count,
            }
        )

    return {
        "date": resolved_date,
        "delivery_mode": "email_ready_queue",
        "recipients_count": len(recipients),
        "packages": packages,
        "evidence_index": evidence_index,
    }


def print_daily_close_distribution(conn, report_date=None):
    distribution = get_daily_close_distribution(conn, report_date)

    print("Daily Close Distribution:")
    print(f"Date: {distribution['date']}")
    print(f"Delivery mode: {distribution['delivery_mode']}")
    print(f"Recipients prepared: {distribution['recipients_count']}")
    print(f"Evidence available: {distribution['evidence_index']['available_count']}")
    print(f"Evidence missing: {distribution['evidence_index']['missing_count']}")

    for package in distribution["packages"]:
        recipient = package["recipient"]
        print(
            f"[{package['status'].upper()}] "
            f"{recipient['full_name']} | {recipient['department']} | "
            f"{recipient['email']} | reports: {len(package['reports'])}"
        )

    write_audit_log(
        conn,
        "daily_close_distribution_viewed",
        "info",
        "Daily close distribution viewed.",
        {
            "date": distribution["date"],
            "delivery_mode": distribution["delivery_mode"],
            "recipients_count": distribution["recipients_count"],
        },
    )

    return distribution


def queue_daily_close_distribution_notifications(conn, distribution):
    queued_items = []
    source_reference_id = f"daily-close-distribution-{distribution['date']}"

    for package in distribution["packages"]:
        recipient = package["recipient"]
        queued_items.append(
            queue_notification(
                conn,
                recipient_name=recipient["full_name"],
                recipient_email=recipient["email"],
                recipient_role=recipient["role"],
                recipient_department=recipient["department"],
                subject=package["subject"],
                body=package["body"],
                source_module="daily_close_distribution",
                source_reference_id=source_reference_id,
                channel="email",
            )
        )

    print(f"Daily Close notifications queued: {len(queued_items)}")
    return queued_items


def export_daily_close_distribution(conn, report_date=None):
    reports_path = ensure_reports_folder()
    distribution = print_daily_close_distribution(conn, report_date)
    report_path = os.path.join(
        reports_path,
        f"daily_close_distribution_{distribution['date']}.md",
    )

    content = f"""# Daily Close Distribution

Date: {distribution['date']}

## Distribution Summary

Delivery mode: {distribution['delivery_mode']}  
Recipients prepared: {distribution['recipients_count']}  
Evidence available: {distribution['evidence_index']['available_count']}  
Evidence missing: {distribution['evidence_index']['missing_count']}  

## Recipient Packages

{_format_package_rows(distribution['packages'])}

## Email-Ready Messages

{_format_email_ready_messages(distribution['packages'], distribution['evidence_index'])}
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Daily Close Distribution exported: {report_path}")
    queued_items = queue_daily_close_distribution_notifications(conn, distribution)

    write_audit_log(
        conn,
        "daily_close_distribution_exported",
        "info",
        "Daily close distribution exported.",
        {
            "report_path": report_path,
            "date": distribution["date"],
            "recipients_count": distribution["recipients_count"],
            "queued_notifications": len(queued_items),
        },
    )

    return report_path
