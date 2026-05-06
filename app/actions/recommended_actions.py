import uuid
from datetime import datetime

from app.audit.audit_log import write_audit_log


def store_recommended_action(conn, action):
    existing = conn.execute(
        """
        SELECT id, status
        FROM recommended_actions
        WHERE risk_type = ?
          AND recommended_action = ?
          AND status IN ('open', 'in_progress')
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (
            action["risk_type"],
            action["recommended_action"],
        ),
    ).fetchone()

    if existing:
        action_id, status = existing

        write_audit_log(
            conn,
            "recommended_action_duplicate_skipped",
            "info",
            "Duplicate recommended action skipped.",
            {
                "existing_action_id": action_id,
                "existing_status": status,
                "risk_type": action["risk_type"],
                "recommended_action": action["recommended_action"],
            },
        )

        return action_id, status, False

    action_id = str(uuid.uuid4())

    conn.execute(
        """
        INSERT INTO recommended_actions (
            id,
            created_at,
            risk_type,
            risk_severity,
            recommended_action,
            owner_role,
            priority,
            deadline_days,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            action_id,
            datetime.now().isoformat(),
            action["risk_type"],
            action["risk_severity"],
            action["recommended_action"],
            action["owner_role"],
            action["priority"],
            action["deadline_days"],
            "open",
        ),
    )
    conn.commit()

    return action_id, "open", True


def generate_recommended_actions(conn, risks):
    actions = []

    action_map = {
        "no_income_detected": {
            "recommended_action": "Review revenue sources immediately and confirm whether income data is missing or the business has no active revenue.",
            "owner_role": "Finance Manager",
            "priority": "high",
            "deadline_days": 1,
        },
        "negative_cash_flow": {
            "recommended_action": "Reduce non-essential expenses and identify short-term revenue opportunities to restore positive cash flow.",
            "owner_role": "Finance Manager",
            "priority": "high",
            "deadline_days": 3,
        },
        "expense_ratio_warning": {
            "recommended_action": "Review discretionary expenses and reduce non-essential spending until the expense ratio improves.",
            "owner_role": "Finance Manager",
            "priority": "medium",
            "deadline_days": 7,
        },
        "expense_concentration": {
            "recommended_action": "Review the category with high expense concentration and confirm whether spending is justified by expected return.",
            "owner_role": "Finance Manager",
            "priority": "medium",
            "deadline_days": 7,
        },
    }

    if not risks:
        print("Recommended Actions: No actions required.")
        write_audit_log(
            conn,
            "recommended_actions_generated",
            "info",
            "No recommended actions were required.",
            {"actions_generated": 0},
        )
        return []

    print("Recommended Actions:")

    for risk in risks:
        action_template = action_map.get(
            risk["risk_type"],
            {
                "recommended_action": "Review this financial risk and define a corrective action.",
                "owner_role": "Finance Manager",
                "priority": risk["severity"],
                "deadline_days": 7,
            },
        )

        action = {
            "risk_type": risk["risk_type"],
            "risk_severity": risk["severity"],
            "recommended_action": action_template["recommended_action"],
            "owner_role": action_template["owner_role"],
            "priority": action_template["priority"],
            "deadline_days": action_template["deadline_days"],
        }

        action_id, status, was_created = store_recommended_action(conn, action)
        action["id"] = action_id
        action["status"] = status

        actions.append(action)

        if was_created:
            print(
                f"[{action['priority'].upper()}] "
                f"{action['recommended_action']} "
                f"(Owner: {action['owner_role']}, Deadline: {action['deadline_days']} days, Status: {action['status']})"
            )

            write_audit_log(
                conn,
                "recommended_action_generated",
                action["priority"],
                action["recommended_action"],
                action,
            )
        else:
            print(
                f"[SKIPPED] Duplicate action already exists "
                f"(Status: {action['status']}): {action['recommended_action']}"
            )

    write_audit_log(
        conn,
        "recommended_actions_generated",
        "info",
        "Recommended actions generated from financial risks.",
        {"actions_generated": len(actions)},
    )

    return actions
