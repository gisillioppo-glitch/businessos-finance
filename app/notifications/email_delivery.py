import smtplib
from datetime import date
from email.message import EmailMessage
from pathlib import Path

from app.approvals.schema import create_approval_requests_table
from app.audit.audit_log import write_audit_log
from app.notifications.schema import create_notification_outbox_table
from app.notifications.status import update_notification_status
from app.security.config import settings


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"


def _get_ready_notifications(conn):
    create_notification_outbox_table(conn)
    create_approval_requests_table(conn)

    rows = conn.execute(
        """
        SELECT
            notification.id,
            notification.channel,
            notification.recipient_name,
            notification.recipient_email,
            notification.subject,
            notification.body,
            approval.id,
            approval.status
        FROM notification_outbox AS notification
        INNER JOIN approval_requests AS approval
            ON approval.source_module = 'notifications'
           AND approval.source_reference_id = notification.id
        WHERE notification.status = 'queued'
          AND notification.channel = 'email'
          AND approval.status = 'approved'
        ORDER BY notification.created_at ASC
        """
    ).fetchall()

    return [
        {
            "id": row[0],
            "channel": row[1],
            "recipient_name": row[2],
            "recipient_email": row[3],
            "subject": row[4],
            "body": row[5],
            "approval_id": row[6],
            "approval_status": row[7],
        }
        for row in rows
    ]


def _get_queued_email_count(conn):
    create_notification_outbox_table(conn)

    return conn.execute(
        """
        SELECT COUNT(*)
        FROM notification_outbox
        WHERE status = 'queued'
          AND channel = 'email'
        """
    ).fetchone()[0]


def _build_email_message(notification):
    message = EmailMessage()
    message["From"] = settings.smtp_from_email
    message["To"] = notification["recipient_email"]
    message["Subject"] = notification["subject"]
    message.set_content(notification["body"])
    return message


def _send_email(notification):
    message = _build_email_message(notification)

    with smtplib.SMTP(
        settings.smtp_host,
        settings.smtp_port,
        timeout=settings.smtp_timeout_seconds,
    ) as smtp:
        if settings.smtp_use_tls:
            smtp.starttls()

        smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(message)


def _delivery_mode():
    if not settings.email_delivery_enabled:
        return "disabled"

    if settings.email_delivery_dry_run:
        return "dry_run"

    if not settings.email_delivery_configured:
        return "configuration_error"

    return "smtp"


def get_secure_email_delivery_status(conn):
    return {
        "delivery_mode": _delivery_mode(),
        "delivery_enabled": settings.email_delivery_enabled,
        "dry_run": settings.email_delivery_dry_run,
        "smtp_configured": settings.email_delivery_configured,
        "smtp_host_configured": bool(settings.smtp_host),
        "smtp_from_email_configured": bool(settings.smtp_from_email),
        "queued_email_notifications": _get_queued_email_count(conn),
        "ready_to_deliver": len(_get_ready_notifications(conn)),
    }


def get_latest_secure_email_delivery_report():
    if not REPORTS_DIR.exists():
        return None

    reports = sorted(
        REPORTS_DIR.glob("secure_email_delivery_*.md"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    return reports[0] if reports else None


def parse_secure_email_delivery_report(report_path=None):
    if report_path is None:
        report_path = get_latest_secure_email_delivery_report()

    if not report_path or not report_path.exists():
        return {
            "exists": False,
            "report_path": None,
            "date": None,
            "delivery_mode": "missing",
            "queued_email_notifications": 0,
            "ready_to_deliver": 0,
            "sent": 0,
            "failed": 0,
            "blocked_or_skipped": 0,
            "results": [],
        }

    content = report_path.read_text(encoding="utf-8")

    def metric(label, default="0"):
        for line in content.splitlines():
            if line.startswith(f"{label}:"):
                return line.split(":", 1)[1].strip()
        return default

    results = []
    for line in content.splitlines():
        if not line.startswith("|") or line.startswith("| ---") or line.startswith("| Recipient"):
            continue

        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) == 4:
            results.append(
                {
                    "recipient_email": parts[0],
                    "delivery_status": parts[1],
                    "subject": parts[2],
                    "message": parts[3],
                }
            )

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "date": metric("Date", None),
        "delivery_mode": metric("Delivery mode", "unknown"),
        "queued_email_notifications": int(metric("Queued email notifications")),
        "ready_to_deliver": int(metric("Ready to deliver")),
        "sent": int(metric("Sent")),
        "failed": int(metric("Failed")),
        "blocked_or_skipped": int(metric("Blocked or skipped")),
        "results": results,
    }


def run_secure_email_delivery(conn):
    ready_notifications = _get_ready_notifications(conn)
    queued_email_count = _get_queued_email_count(conn)
    mode = _delivery_mode()

    results = []

    for notification in ready_notifications:
        result = {
            "notification_id": notification["id"],
            "recipient_email": notification["recipient_email"],
            "subject": notification["subject"],
            "approval_id": notification["approval_id"],
            "delivery_status": mode,
            "message": "",
        }

        if mode == "disabled":
            result["message"] = "Email delivery disabled by BUSINESSOS_EMAIL_DELIVERY_ENABLED."
        elif mode == "dry_run":
            result["message"] = "Dry run enabled; no external email sent."
        elif mode == "configuration_error":
            result["message"] = "SMTP configuration incomplete; no external email sent."
        else:
            try:
                _send_email(notification)
                status_update = update_notification_status(conn, notification["id"], "sent")
                if status_update and not status_update.get("blocked"):
                    result["delivery_status"] = "sent"
                    result["message"] = "Email sent through configured SMTP adapter."
                else:
                    result["delivery_status"] = "blocked"
                    result["message"] = "Delivery approval gate blocked status update."
            except Exception as error:
                update_notification_status(conn, notification["id"], "failed")
                result["delivery_status"] = "failed"
                result["message"] = f"{type(error).__name__}: {error}"

        results.append(result)

    summary = {
        "date": date.today().isoformat(),
        "delivery_mode": mode,
        "queued_email_notifications": queued_email_count,
        "ready_to_deliver": len(ready_notifications),
        "sent": sum(1 for result in results if result["delivery_status"] == "sent"),
        "failed": sum(1 for result in results if result["delivery_status"] == "failed"),
        "blocked_or_skipped": sum(
            1
            for result in results
            if result["delivery_status"] in {"disabled", "dry_run", "configuration_error", "blocked"}
        ),
        "results": results,
    }

    write_audit_log(
        conn,
        "secure_email_delivery_run",
        "info" if summary["failed"] == 0 else "warning",
        "Secure email delivery adapter run.",
        {
            "delivery_mode": summary["delivery_mode"],
            "queued_email_notifications": summary["queued_email_notifications"],
            "ready_to_deliver": summary["ready_to_deliver"],
            "sent": summary["sent"],
            "failed": summary["failed"],
            "blocked_or_skipped": summary["blocked_or_skipped"],
        },
    )

    return summary


def _format_result_rows(results):
    if not results:
        return "No approved queued email notifications were ready for secure delivery."

    rows = [
        "| Recipient | Status | Subject | Message |",
        "| --- | --- | --- | --- |",
    ]

    for result in results:
        subject = result["subject"].replace("|", "\\|")
        message = result["message"].replace("|", "\\|")
        rows.append(
            f"| {result['recipient_email']} | "
            f"{result['delivery_status']} | "
            f"{subject} | "
            f"{message} |"
        )

    return "\n".join(rows)


def export_secure_email_delivery_report(conn):
    REPORTS_DIR.mkdir(exist_ok=True)
    summary = run_secure_email_delivery(conn)
    report_path = REPORTS_DIR / f"secure_email_delivery_{summary['date']}.md"

    content = f"""# Secure Email Delivery Adapter MVP v0.1

Date: {summary['date']}

## Delivery Summary

Delivery mode: {summary['delivery_mode']}
Queued email notifications: {summary['queued_email_notifications']}
Ready to deliver: {summary['ready_to_deliver']}
Sent: {summary['sent']}
Failed: {summary['failed']}
Blocked or skipped: {summary['blocked_or_skipped']}

## Delivery Results

{_format_result_rows(summary['results'])}

## Safety Boundary

Email delivery only sends externally when `BUSINESSOS_EMAIL_DELIVERY_ENABLED=true`, `BUSINESSOS_EMAIL_DELIVERY_DRY_RUN=false`, SMTP configuration is complete, the notification is queued, and delivery approval is approved. Credentials are read from environment variables and are never written to this report.
"""

    report_path.write_text(content, encoding="utf-8")

    write_audit_log(
        conn,
        "secure_email_delivery_report_exported",
        "info" if summary["failed"] == 0 else "warning",
        "Secure email delivery report exported.",
        {
            "report_path": str(report_path.relative_to(ROOT_DIR)),
            "delivery_mode": summary["delivery_mode"],
            "sent": summary["sent"],
            "failed": summary["failed"],
        },
    )

    return summary, str(report_path)


def print_secure_email_delivery(conn):
    summary, report_path = export_secure_email_delivery_report(conn)

    print("Secure Email Delivery:")
    print(f"Delivery mode: {summary['delivery_mode']}")
    print(f"Queued email notifications: {summary['queued_email_notifications']}")
    print(f"Ready to deliver: {summary['ready_to_deliver']}")
    print(f"Sent: {summary['sent']}")
    print(f"Failed: {summary['failed']}")
    print(f"Blocked or skipped: {summary['blocked_or_skipped']}")
    print(f"Secure email delivery report exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return summary
