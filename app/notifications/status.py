from datetime import datetime

from app.audit.audit_log import write_audit_log
from app.notifications.delivery_approval import get_notification_delivery_approval_status
from app.notifications.schema import create_notification_outbox_table


VALID_NOTIFICATION_STATUSES = {"queued", "sent", "dismissed", "failed"}


def update_notification_status(conn, notification_id, new_status):
    create_notification_outbox_table(conn)

    if new_status not in VALID_NOTIFICATION_STATUSES:
        raise ValueError(f"Invalid notification status: {new_status}")

    existing = conn.execute(
        """
        SELECT id, status, recipient_email, subject
        FROM notification_outbox
        WHERE id = ?
        LIMIT 1
        """,
        (notification_id,),
    ).fetchone()

    if not existing:
        return None

    _, old_status, recipient_email, subject = existing

    if new_status == "sent":
        approval = get_notification_delivery_approval_status(conn, notification_id)
        if approval["status"] != "approved":
            write_audit_log(
                conn,
                "notification_delivery_blocked_pending_approval",
                "warning",
                "Notification delivery blocked because approval is not approved.",
                {
                    "notification_id": notification_id,
                    "recipient_email": recipient_email,
                    "subject": subject,
                    "approval_status": approval["status"],
                    "approval_id": approval["approval_id"],
                },
            )

            return {
                "id": notification_id,
                "recipient_email": recipient_email,
                "subject": subject,
                "old_status": old_status,
                "new_status": old_status,
                "blocked": True,
                "approval_status": approval["status"],
            }

    now = datetime.now().isoformat()
    sent_at = now if new_status == "sent" else None

    conn.execute(
        """
        UPDATE notification_outbox
        SET status = ?,
            updated_at = ?,
            sent_at = ?
        WHERE id = ?
        """,
        (new_status, now, sent_at, notification_id),
    )
    conn.commit()

    write_audit_log(
        conn,
        "notification_status_updated",
        "info",
        "Notification status updated.",
        {
            "notification_id": notification_id,
            "recipient_email": recipient_email,
            "subject": subject,
            "old_status": old_status,
            "new_status": new_status,
        },
    )

    return {
        "id": notification_id,
        "recipient_email": recipient_email,
        "subject": subject,
        "old_status": old_status,
        "new_status": new_status,
        "blocked": False,
    }


def _update_first_notification_by_status(conn, current_status, new_status):
    create_notification_outbox_table(conn)

    existing = conn.execute(
        """
        SELECT id
        FROM notification_outbox
        WHERE status = ?
        ORDER BY created_at ASC
        LIMIT 1
        """,
        (current_status,),
    ).fetchone()

    if not existing:
        print(f"Notification Status Update: No {current_status} notifications found.")
        return None

    result = update_notification_status(conn, existing[0], new_status)

    if result and result.get("blocked"):
        print(
            "Notification Delivery Blocked: "
            f"{result['subject']} for {result['recipient_email']} "
            f"requires approved delivery approval. "
            f"Current approval status: {result['approval_status']}."
        )
        return result

    print(
        "Notification Status Update: "
        f"{result['subject']} for {result['recipient_email']} "
        f"changed from {result['old_status']} to {result['new_status']}."
    )

    return result


def demo_mark_first_queued_notification_sent(conn):
    return _update_first_notification_by_status(conn, "queued", "sent")


def demo_dismiss_first_queued_notification(conn):
    return _update_first_notification_by_status(conn, "queued", "dismissed")


def demo_fail_first_queued_notification(conn):
    return _update_first_notification_by_status(conn, "queued", "failed")
