from app.audit.audit_log import write_audit_log
from app.approvals.config import (
    get_demo_protected_source_modules,
    get_valid_approval_statuses,
)
from app.approvals.schema import create_approval_requests_table


VALID_APPROVAL_STATUSES = get_valid_approval_statuses()
DEMO_PROTECTED_SOURCE_MODULES = get_demo_protected_source_modules()


def update_approval_request_status(conn, approval_id, new_status, justification=None):
    if new_status not in get_valid_approval_statuses():
        raise ValueError(f"Invalid approval request status: {new_status}")

    create_approval_requests_table(conn)

    row = conn.execute(
        """
        SELECT title, status, approver_role
        FROM approval_requests
        WHERE id = ?
        """,
        (approval_id,),
    ).fetchone()

    if not row:
        raise ValueError(f"Approval request not found: {approval_id}")

    title, old_status, approver_role = row

    conn.execute(
        """
        UPDATE approval_requests
        SET status = ?,
            status_justification = ?
        WHERE id = ?
        """,
        (new_status, justification, approval_id),
    )
    conn.commit()

    write_audit_log(
        conn,
        "approval_request_status_updated",
        "info",
        "Approval request status updated.",
        {
            "approval_id": approval_id,
            "title": title,
            "old_status": old_status,
            "new_status": new_status,
            "justification": justification,
            "approver_role": approver_role,
        },
    )

    return {
        "approval_id": approval_id,
        "title": title,
        "old_status": old_status,
        "new_status": new_status,
        "justification": justification,
        "approver_role": approver_role,
    }


def get_first_pending_approval_request(conn):
    create_approval_requests_table(conn)
    protected_source_modules = sorted(get_demo_protected_source_modules())
    protected_placeholders = ", ".join("?" for _ in protected_source_modules)

    return conn.execute(
        f"""
        SELECT id, title
        FROM approval_requests
        WHERE status = 'pending'
          AND (
              source_module IS NULL
              OR source_module NOT IN ({protected_placeholders})
          )
        ORDER BY
            CASE priority
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            created_at ASC
        LIMIT 1
        """,
        tuple(protected_source_modules),
    ).fetchone()


def demo_approve_first_pending_approval_request(conn):
    row = get_first_pending_approval_request(conn)

    if not row:
        print("Approval Decision Update: No pending approval requests found.")
        write_audit_log(
            conn,
            "approval_request_approve_demo",
            "info",
            "No pending approval requests found for approve demo.",
            {},
        )
        return None

    approval_id, title = row
    result = update_approval_request_status(
        conn,
        approval_id,
        "approved",
        "Demo mode approved the first pending approval request after executive review.",
    )

    print(
        "Approval Decision Update: "
        f"{title} changed from {result['old_status']} to {result['new_status']}."
    )

    return result


def demo_reject_first_pending_approval_request(conn):
    row = get_first_pending_approval_request(conn)

    if not row:
        print("Approval Rejection Update: No pending approval requests found.")
        write_audit_log(
            conn,
            "approval_request_reject_demo",
            "info",
            "No pending approval requests found for reject demo.",
            {},
        )
        return None

    approval_id, title = row
    result = update_approval_request_status(
        conn,
        approval_id,
        "rejected",
        "Demo mode rejected the first pending approval request pending a better resolution path.",
    )

    print(
        "Approval Rejection Update: "
        f"{title} changed from {result['old_status']} to {result['new_status']}."
    )

    return result


def get_approval_decision_summary(conn):
    create_approval_requests_table(conn)

    rows = conn.execute(
        """
        SELECT status, COUNT(*) AS count
        FROM approval_requests
        GROUP BY status
        """
    ).fetchall()

    summary = {
        "pending": 0,
        "approved": 0,
        "rejected": 0,
        "cancelled": 0,
    }

    for status, count in rows:
        if status in summary:
            summary[status] = count

    return summary
