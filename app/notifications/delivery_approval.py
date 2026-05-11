from datetime import date
from pathlib import Path

from app.approvals.requests import create_approval_request
from app.approvals.schema import create_approval_requests_table
from app.audit.audit_log import write_audit_log
from app.notifications.schema import create_notification_outbox_table


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"


def _delivery_priority(notification):
    if notification["recipient_role"] in {"Owner / CEO", "Executive Owner"}:
        return "high"

    return "medium"


def _get_queued_notifications(conn):
    create_notification_outbox_table(conn)

    rows = conn.execute(
        """
        SELECT
            id,
            created_at,
            channel,
            recipient_name,
            recipient_email,
            recipient_role,
            recipient_department,
            subject,
            source_module,
            source_reference_id
        FROM notification_outbox
        WHERE status = 'queued'
        ORDER BY created_at ASC
        """
    ).fetchall()

    return [
        {
            "id": row[0],
            "created_at": row[1],
            "channel": row[2],
            "recipient_name": row[3],
            "recipient_email": row[4],
            "recipient_role": row[5],
            "recipient_department": row[6],
            "subject": row[7],
            "source_module": row[8],
            "source_reference_id": row[9],
        }
        for row in rows
    ]


def get_notification_delivery_approval_status(conn, notification_id):
    create_approval_requests_table(conn)

    row = conn.execute(
        """
        SELECT id, status, approver_role, status_justification
        FROM approval_requests
        WHERE source_module = 'notifications'
          AND source_reference_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (notification_id,),
    ).fetchone()

    if not row:
        return {
            "approval_id": None,
            "status": "missing",
            "approver_role": None,
            "status_justification": None,
        }

    return {
        "approval_id": row[0],
        "status": row[1],
        "approver_role": row[2],
        "status_justification": row[3],
    }


def notification_delivery_is_approved(conn, notification_id):
    approval = get_notification_delivery_approval_status(conn, notification_id)
    return approval["status"] == "approved"


def ensure_notification_delivery_approvals(conn):
    create_notification_outbox_table(conn)
    create_approval_requests_table(conn)

    queued_notifications = _get_queued_notifications(conn)
    results = []

    for notification in queued_notifications:
        title = f"Approve notification delivery to {notification['recipient_name']}"
        description = (
            "Approval is required before this queued notification can be delivered "
            f"through a secure external adapter. Subject: {notification['subject']}. "
            f"Recipient: {notification['recipient_name']} <{notification['recipient_email']}>."
        )

        approval = create_approval_request(
            conn,
            title=title,
            description=description,
            approval_type="policy",
            priority=_delivery_priority(notification),
            approver_role="Executive Owner",
            requester_email="system@businessos.local",
            requester_role="BusinessOS System",
            source_module="notifications",
            source_reference_id=notification["id"],
        )

        results.append(
            {
                "notification": notification,
                "approval": approval,
            }
        )

    write_audit_log(
        conn,
        "notification_delivery_approvals_checked",
        "info",
        "Notification delivery approvals checked.",
        {
            "queued_notifications": len(queued_notifications),
            "approval_requests_created": sum(1 for result in results if result["approval"]["was_created"]),
            "approval_requests_existing": sum(1 for result in results if not result["approval"]["was_created"]),
        },
    )

    return results


def get_notification_delivery_approval_summary(conn):
    create_notification_outbox_table(conn)
    create_approval_requests_table(conn)

    queued_count = conn.execute(
        """
        SELECT COUNT(*)
        FROM notification_outbox
        WHERE status = 'queued'
        """
    ).fetchone()[0]

    rows = conn.execute(
        """
        SELECT status, COUNT(*)
        FROM approval_requests
        WHERE source_module = 'notifications'
        GROUP BY status
        """
    ).fetchall()

    approval_counts = {
        "pending": 0,
        "approved": 0,
        "rejected": 0,
        "cancelled": 0,
    }

    for status, count in rows:
        if status in approval_counts:
            approval_counts[status] = count

    ready_to_deliver = conn.execute(
        """
        SELECT COUNT(*)
        FROM notification_outbox AS notification
        INNER JOIN approval_requests AS approval
            ON approval.source_module = 'notifications'
           AND approval.source_reference_id = notification.id
        WHERE notification.status = 'queued'
          AND approval.status = 'approved'
        """
    ).fetchone()[0]

    blocked_count = max(queued_count - ready_to_deliver, 0)

    return {
        "queued_notifications": queued_count,
        "pending_delivery_approvals": approval_counts["pending"],
        "approved_delivery_approvals": approval_counts["approved"],
        "rejected_delivery_approvals": approval_counts["rejected"],
        "cancelled_delivery_approvals": approval_counts["cancelled"],
        "ready_to_deliver": ready_to_deliver,
        "blocked_notifications": blocked_count,
    }


def get_notification_delivery_approval_rows(conn):
    create_notification_outbox_table(conn)
    create_approval_requests_table(conn)

    rows = conn.execute(
        """
        SELECT
            notification.id,
            notification.recipient_name,
            notification.recipient_email,
            notification.recipient_role,
            notification.subject,
            notification.status,
            approval.id,
            approval.status,
            approval.priority,
            approval.approver_role
        FROM notification_outbox AS notification
        LEFT JOIN approval_requests AS approval
            ON approval.source_module = 'notifications'
           AND approval.source_reference_id = notification.id
        WHERE notification.status = 'queued'
           OR approval.source_module = 'notifications'
        ORDER BY notification.created_at DESC
        """
    ).fetchall()

    return [
        {
            "notification_id": row[0],
            "recipient_name": row[1],
            "recipient_email": row[2],
            "recipient_role": row[3],
            "subject": row[4],
            "notification_status": row[5],
            "approval_id": row[6],
            "approval_status": row[7] or "missing",
            "approval_priority": row[8] or "medium",
            "approver_role": row[9] or "Executive Owner",
        }
        for row in rows
    ]


def _format_delivery_rows(rows):
    if not rows:
        return "No queued notification delivery approvals found."

    table_rows = [
        "| Recipient | Notification status | Approval status | Approver | Subject |",
        "| --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        subject = row["subject"].replace("|", "\\|")
        table_rows.append(
            f"| {row['recipient_name']} <{row['recipient_email']}> | "
            f"{row['notification_status']} | "
            f"{row['approval_status']} | "
            f"{row['approver_role']} | "
            f"{subject} |"
        )

    return "\n".join(table_rows)


def export_notification_delivery_approval_report(conn):
    REPORTS_DIR.mkdir(exist_ok=True)
    approvals = ensure_notification_delivery_approvals(conn)
    summary = get_notification_delivery_approval_summary(conn)
    rows = get_notification_delivery_approval_rows(conn)
    today = date.today().isoformat()
    report_path = REPORTS_DIR / f"notification_delivery_approval_{today}.md"

    content = f"""# Notification Delivery Approval MVP v0.1

Date: {today}

## Delivery Approval Summary

Queued notifications: {summary['queued_notifications']}
Pending delivery approvals: {summary['pending_delivery_approvals']}
Approved delivery approvals: {summary['approved_delivery_approvals']}
Rejected delivery approvals: {summary['rejected_delivery_approvals']}
Cancelled delivery approvals: {summary['cancelled_delivery_approvals']}
Ready to deliver: {summary['ready_to_deliver']}
Blocked notifications: {summary['blocked_notifications']}
Approval requests created this run: {sum(1 for result in approvals if result['approval']['was_created'])}

## Delivery Approval Queue

{_format_delivery_rows(rows)}

## Safety Boundary

This report does not send email or deliver messages externally. It prepares governance approvals required before a future secure delivery adapter can mark queued notifications as sent.
"""

    report_path.write_text(content, encoding="utf-8")

    write_audit_log(
        conn,
        "notification_delivery_approval_report_exported",
        "info",
        "Notification delivery approval report exported.",
        {
            "report_path": str(report_path.relative_to(ROOT_DIR)),
            "queued_notifications": summary["queued_notifications"],
            "pending_delivery_approvals": summary["pending_delivery_approvals"],
            "ready_to_deliver": summary["ready_to_deliver"],
            "blocked_notifications": summary["blocked_notifications"],
        },
    )

    return summary, str(report_path)


def print_notification_delivery_approval(conn):
    summary, report_path = export_notification_delivery_approval_report(conn)

    print("Notification Delivery Approval:")
    print(f"Queued notifications: {summary['queued_notifications']}")
    print(f"Pending delivery approvals: {summary['pending_delivery_approvals']}")
    print(f"Approved delivery approvals: {summary['approved_delivery_approvals']}")
    print(f"Ready to deliver: {summary['ready_to_deliver']}")
    print(f"Blocked notifications: {summary['blocked_notifications']}")
    print(f"Notification delivery approval report exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return summary
