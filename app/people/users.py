import uuid
from datetime import datetime

from app.audit.audit_log import write_audit_log


VALID_STATUSES = {"active", "inactive", "pending", "suspended"}
VALID_ACCESS_LEVELS = {"viewer", "operator", "manager", "executive", "admin"}


def create_business_user(
    conn,
    full_name,
    email,
    role,
    department,
    access_level="viewer",
    manager_id=None,
    status="active",
    source_module=None,
    source_reference_id=None,
):
    normalized_email = email.strip().lower()

    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid user status: {status}")

    if access_level not in VALID_ACCESS_LEVELS:
        raise ValueError(f"Invalid access level: {access_level}")

    existing = conn.execute(
        """
        SELECT id, status
        FROM business_users
        WHERE email = ?
        LIMIT 1
        """,
        (normalized_email,),
    ).fetchone()

    if existing:
        user_id, existing_status = existing

        write_audit_log(
            conn,
            "business_user_duplicate_skipped",
            "info",
            "Duplicate business user skipped.",
            {
                "user_id": user_id,
                "email": normalized_email,
                "status": existing_status,
            },
        )

        return {
            "id": user_id,
            "full_name": full_name,
            "email": normalized_email,
            "role": role,
            "department": department,
            "manager_id": manager_id,
            "status": existing_status,
            "access_level": access_level,
            "source_module": source_module,
            "source_reference_id": source_reference_id,
            "was_created": False,
        }

    user_id = str(uuid.uuid4())

    conn.execute(
        """
        INSERT INTO business_users (
            id,
            created_at,
            full_name,
            email,
            role,
            department,
            manager_id,
            status,
            access_level,
            source_module,
            source_reference_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            datetime.now().isoformat(),
            full_name,
            normalized_email,
            role,
            department,
            manager_id,
            status,
            access_level,
            source_module,
            source_reference_id,
        ),
    )
    conn.commit()

    write_audit_log(
        conn,
        "business_user_created",
        "info",
        "Business user created.",
        {
            "user_id": user_id,
            "full_name": full_name,
            "email": normalized_email,
            "role": role,
            "department": department,
            "access_level": access_level,
            "status": status,
            "source_module": source_module,
            "source_reference_id": source_reference_id,
        },
    )

    return {
        "id": user_id,
        "full_name": full_name,
        "email": normalized_email,
        "role": role,
        "department": department,
        "manager_id": manager_id,
        "status": status,
        "access_level": access_level,
        "source_module": source_module,
        "source_reference_id": source_reference_id,
        "was_created": True,
    }


def ensure_default_business_users(conn):
    default_users = [
        {
            "full_name": "Executive Owner",
            "email": "owner@businessos.local",
            "role": "Owner / CEO",
            "department": "Executive",
            "access_level": "admin",
            "source_module": "people",
            "source_reference_id": "people-mvp-v0.1",
        },
        {
            "full_name": "Finance Manager",
            "email": "finance.manager@businessos.local",
            "role": "Finance Manager",
            "department": "Finance",
            "access_level": "manager",
            "source_module": "people",
            "source_reference_id": "people-mvp-v0.1",
        },
        {
            "full_name": "Operations Manager",
            "email": "operations.manager@businessos.local",
            "role": "Operations Manager",
            "department": "Operations",
            "access_level": "manager",
            "source_module": "people",
            "source_reference_id": "people-mvp-v0.1",
        },
        {
            "full_name": "Support Manager",
            "email": "support.manager@businessos.local",
            "role": "Support Manager",
            "department": "Support",
            "access_level": "manager",
            "source_module": "people",
            "source_reference_id": "people-mvp-v0.1",
        },
    ]

    results = []

    for user in default_users:
        results.append(create_business_user(conn, **user))

    return results
