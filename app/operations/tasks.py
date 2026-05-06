import uuid
from datetime import datetime

from app.audit.audit_log import write_audit_log


def create_operations_task(
    conn,
    title,
    description,
    owner_role,
    priority,
    deadline_date=None,
    source_module=None,
    source_reference_id=None,
):
    valid_priorities = {"low", "medium", "high", "critical"}

    if priority not in valid_priorities:
        raise ValueError(f"Invalid task priority: {priority}")

    task_id = str(uuid.uuid4())

    conn.execute(
        """
        INSERT INTO operations_tasks (
            id,
            created_at,
            title,
            description,
            owner_role,
            priority,
            deadline_date,
            status,
            status_justification,
            source_module,
            source_reference_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            task_id,
            datetime.now().isoformat(),
            title,
            description,
            owner_role,
            priority,
            deadline_date,
            "open",
            None,
            source_module,
            source_reference_id,
        ),
    )
    conn.commit()

    write_audit_log(
        conn,
        "operations_task_created",
        priority,
        "Operations task created.",
        {
            "task_id": task_id,
            "title": title,
            "owner_role": owner_role,
            "priority": priority,
            "deadline_date": deadline_date,
            "source_module": source_module,
            "source_reference_id": source_reference_id,
        },
    )

    return {
        "id": task_id,
        "title": title,
        "description": description,
        "owner_role": owner_role,
        "priority": priority,
        "deadline_date": deadline_date,
        "status": "open",
        "source_module": source_module,
        "source_reference_id": source_reference_id,
    }

