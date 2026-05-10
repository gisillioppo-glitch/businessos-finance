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

def demo_review_first_acknowledged_executive_alert(conn):
    from app.alerts.executive_alerts import get_executive_alerts

    alerts = get_executive_alerts(conn)
    acknowledged_alerts = [alert for alert in alerts if alert["status"] == "acknowledged"]

    if not acknowledged_alerts:
        print("Executive Alert Review Update: No acknowledged executive alerts found.")
        write_audit_log(
            conn,
            "executive_alert_review_demo",
            "info",
            "No acknowledged executive alerts found for review demo.",
            {},
        )
        return None

    alert = acknowledged_alerts[0]

    result = update_executive_alert_status(
        conn,
        alert["alert_key"],
        "in_review",
        "Demo mode moved the first acknowledged executive alert into review.",
        alert["owner_role"],
    )

    print(
        "Executive Alert Review Update: "
        f"{alert['title']} changed from "
        f"{result['old_status']} to {result['new_status']}."
    )

    return result


def demo_resolve_first_in_review_executive_alert(conn):
    from app.alerts.executive_alerts import get_executive_alerts

    alerts = get_executive_alerts(conn)
    in_review_alerts = [alert for alert in alerts if alert["status"] == "in_review"]

    if not in_review_alerts:
        print("Executive Alert Resolution Update: No in-review executive alerts found.")
        write_audit_log(
            conn,
            "executive_alert_resolution_demo",
            "info",
            "No in-review executive alerts found for resolution demo.",
            {},
        )
        return None

    alert = in_review_alerts[0]

    result = update_executive_alert_status(
        conn,
        alert["alert_key"],
        "resolved",
        "Demo mode resolved the first in-review executive alert after owner follow-up.",
        alert["owner_role"],
    )

    print(
        "Executive Alert Resolution Update: "
        f"{alert['title']} changed from "
        f"{result['old_status']} to {result['new_status']}."
    )

    return result


def get_executive_alert_status_summary(conn):
    from app.alerts.schema import create_executive_alert_statuses_table

    create_executive_alert_statuses_table(conn)

    rows = conn.execute(
        """
        SELECT status, COUNT(*) AS count
        FROM executive_alert_statuses
        GROUP BY status
        """
    ).fetchall()

    summary = {
        "open": 0,
        "acknowledged": 0,
        "in_review": 0,
        "resolved": 0,
        "dismissed": 0,
    }

    for status, count in rows:
        if status in summary:
            summary[status] = count

    return summary
