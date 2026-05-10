from datetime import datetime

from app.alerts.schema import VALID_EXECUTIVE_ALERT_STATUSES, create_executive_alert_statuses_table
from app.audit.audit_log import write_audit_log


def update_executive_alert_status(
    conn,
    alert_key,
    new_status,
    justification=None,
    owner_role=None,
):
    if new_status not in VALID_EXECUTIVE_ALERT_STATUSES:
        raise ValueError(f"Invalid executive alert status: {new_status}")

    create_executive_alert_statuses_table(conn)

    row = conn.execute(
        """
        SELECT status, owner_role
        FROM executive_alert_statuses
        WHERE alert_key = ?
        """,
        (alert_key,),
    ).fetchone()

    old_status = row[0] if row else "open"
    previous_owner = row[1] if row else None
    resolved_owner = owner_role or previous_owner

    conn.execute(
        """
        INSERT INTO executive_alert_statuses (
            alert_key,
            status,
            status_justification,
            owner_role,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(alert_key) DO UPDATE SET
            status = excluded.status,
            status_justification = excluded.status_justification,
            owner_role = excluded.owner_role,
            updated_at = excluded.updated_at
        """,
        (
            alert_key,
            new_status,
            justification,
            resolved_owner,
            datetime.now().isoformat(),
        ),
    )
    conn.commit()

    write_audit_log(
        conn,
        "executive_alert_status_updated",
        "info",
        "Executive alert status updated.",
        {
            "alert_key": alert_key,
            "old_status": old_status,
            "new_status": new_status,
            "justification": justification,
            "owner_role": resolved_owner,
        },
    )

    return {
        "alert_key": alert_key,
        "old_status": old_status,
        "new_status": new_status,
        "justification": justification,
        "owner_role": resolved_owner,
    }


def demo_acknowledge_first_open_executive_alert(conn):
    from app.alerts.executive_alerts import get_executive_alerts

    alerts = get_executive_alerts(conn)
    open_alerts = [alert for alert in alerts if alert["status"] == "open"]

    if not open_alerts:
        print("Executive Alert Status Update: No open executive alerts found.")
        write_audit_log(
            conn,
            "executive_alert_status_demo",
            "info",
            "No open executive alerts found for status update demo.",
            {},
        )
        return None

    alert = open_alerts[0]

    result = update_executive_alert_status(
        conn,
        alert["alert_key"],
        "acknowledged",
        "Demo mode acknowledged the first open executive alert.",
        alert["owner_role"],
    )

    print(
        "Executive Alert Status Update: "
        f"{alert['title']} changed from "
        f"{result['old_status']} to {result['new_status']}."
    )

    return result
