import uuid
from datetime import datetime

from app.audit.audit_log import write_audit_log
from app.notifications.schema import create_notification_outbox_table


VALID_STATUSES = {"queued", "sent", "dismissed", "failed"}


def queue_notification(
    conn,
    recipient_name,
    recipient_email,
    recipient_role,
    recipient_department,
    subject,
    body,
    source_module,
    source_reference_id,
    channel="email",
):
    create_notification_outbox_table(conn)

    existing = conn.execute(
        """
        SELECT id, status
        FROM notification_outbox
        WHERE channel = ?
          AND recipient_email = ?
          AND source_module = ?
          AND source_reference_id = ?
        LIMIT 1
        """,
        (channel, recipient_email, source_module, source_reference_id),
    ).fetchone()

    now = datetime.now().isoformat()

    if existing:
        notification_id, existing_status = existing
        next_status = existing_status if existing_status == "sent" else "queued"

        conn.execute(
            """
            UPDATE notification_outbox
            SET updated_at = ?,
                recipient_name = ?,
                recipient_role = ?,
                recipient_department = ?,
                subject = ?,
                body = ?,
                status = ?
            WHERE id = ?
            """,
            (
                now,
                recipient_name,
                recipient_role,
                recipient_department,
                subject,
                body,
                next_status,
                notification_id,
            ),
        )
        conn.commit()

        write_audit_log(
            conn,
            "notification_outbox_updated",
            "info",
            "Notification outbox item updated.",
            {
                "notification_id": notification_id,
                "recipient_email": recipient_email,
                "source_module": source_module,
                "source_reference_id": source_reference_id,
                "status": next_status,
            },
        )

        return {
            "id": notification_id,
            "status": next_status,
            "was_created": False,
        }

    notification_id = str(uuid.uuid4())

    conn.execute(
        """
        INSERT INTO notification_outbox (
            id,
            created_at,
            updated_at,
            channel,
            recipient_name,
            recipient_email,
            recipient_role,
            recipient_department,
            subject,
            body,
            status,
            source_module,
            source_reference_id,
            sent_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            notification_id,
            now,
            now,
            channel,
            recipient_name,
            recipient_email,
            recipient_role,
            recipient_department,
            subject,
            body,
            "queued",
            source_module,
            source_reference_id,
            None,
        ),
    )
    conn.commit()

    write_audit_log(
        conn,
        "notification_outbox_queued",
        "info",
        "Notification outbox item queued.",
        {
            "notification_id": notification_id,
            "recipient_email": recipient_email,
            "source_module": source_module,
            "source_reference_id": source_reference_id,
            "status": "queued",
        },
    )

    return {
        "id": notification_id,
        "status": "queued",
        "was_created": True,
    }


def get_notification_outbox(conn, limit=20):
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
            status,
            source_module,
            source_reference_id
        FROM notification_outbox
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
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
            "status": row[8],
            "source_module": row[9],
            "source_reference_id": row[10],
        }
        for row in rows
    ]


def get_notification_summary(conn):
    create_notification_outbox_table(conn)

    rows = conn.execute(
        """
        SELECT status, COUNT(*)
        FROM notification_outbox
        GROUP BY status
        """
    ).fetchall()

    summary = {
        "queued": 0,
        "sent": 0,
        "dismissed": 0,
        "failed": 0,
    }

    for status, count in rows:
        summary[status] = count

    summary["total"] = sum(summary.values())
    return summary


def print_notification_outbox(conn):
    notifications = get_notification_outbox(conn)

    if not notifications:
        print("Notification Outbox: No notifications queued.")
        return notifications

    print("Notification Outbox:")

    for notification in notifications:
        print(
            f"[{notification['status'].upper()}] "
            f"{notification['channel']} | "
            f"{notification['recipient_name']} <{notification['recipient_email']}> | "
            f"{notification['subject']}"
        )

    write_audit_log(
        conn,
        "notification_outbox_viewed",
        "info",
        "Notification outbox viewed.",
        {"count": len(notifications)},
    )

    return notifications


def print_notification_summary(conn):
    summary = get_notification_summary(conn)

    print("Notification Summary KPIs:")
    print(f"Total notifications: {summary['total']}")
    print(f"Queued notifications: {summary['queued']}")
    print(f"Sent notifications: {summary['sent']}")
    print(f"Dismissed notifications: {summary['dismissed']}")
    print(f"Failed notifications: {summary['failed']}")

    return summary
