def get_people_summary_kpis(conn):
    rows = conn.execute(
        """
        SELECT status, COUNT(*)
        FROM business_users
        GROUP BY status
        """
    ).fetchall()

    access_rows = conn.execute(
        """
        SELECT access_level, COUNT(*)
        FROM business_users
        GROUP BY access_level
        """
    ).fetchall()

    kpis = {
        "total_users": 0,
        "active_users": 0,
        "inactive_users": 0,
        "pending_users": 0,
        "suspended_users": 0,
        "admin_users": 0,
        "executive_users": 0,
        "manager_users": 0,
        "operator_users": 0,
        "viewer_users": 0,
    }

    for status, count in rows:
        kpis["total_users"] += count
        kpis[f"{status}_users"] = count

    for access_level, count in access_rows:
        kpis[f"{access_level}_users"] = count

    return kpis


def print_people_list(conn):
    rows = conn.execute(
        """
        SELECT full_name, email, role, department, status, access_level
        FROM business_users
        ORDER BY
            CASE access_level
                WHEN 'admin' THEN 1
                WHEN 'executive' THEN 2
                WHEN 'manager' THEN 3
                WHEN 'operator' THEN 4
                ELSE 5
            END,
            department,
            full_name
        """
    ).fetchall()

    if not rows:
        print("People Directory: No users found.")
        return []

    print("People Directory:")

    for full_name, email, role, department, status, access_level in rows:
        print(
            f"[{access_level.upper()}] Status: {status} | Department: {department} | Role: {role} | User: {full_name} <{email}>"
        )

    return rows


def print_people_summary_kpis(conn):
    kpis = get_people_summary_kpis(conn)

    print("People Summary KPIs:")
    print(f"Total users: {kpis['total_users']}")
    print(f"Active users: {kpis['active_users']}")
    print(f"Inactive users: {kpis['inactive_users']}")
    print(f"Pending users: {kpis['pending_users']}")
    print(f"Suspended users: {kpis['suspended_users']}")
    print(f"Admin users: {kpis['admin_users']}")
    print(f"Executive users: {kpis['executive_users']}")
    print(f"Manager users: {kpis['manager_users']}")
    print(f"Operator users: {kpis['operator_users']}")
    print(f"Viewer users: {kpis['viewer_users']}")

    return kpis
