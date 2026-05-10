def print_people_brief(conn, people_kpis):
    active_users = people_kpis["active_users"]
    suspended_users = people_kpis["suspended_users"]
    pending_users = people_kpis["pending_users"]
    admin_users = people_kpis["admin_users"]
    manager_users = people_kpis["manager_users"]

    if suspended_users > 0:
        highest_people_risk = "high"
        next_best_move = "Review suspended users and confirm access controls."
    elif pending_users > 0:
        highest_people_risk = "medium"
        next_best_move = "Review pending users and approve or reject access."
    elif admin_users == 0:
        highest_people_risk = "high"
        next_best_move = "Assign at least one admin user before scaling access."
    elif manager_users == 0 and active_users > 1:
        highest_people_risk = "medium"
        next_best_move = "Assign manager coverage for active users."
    else:
        highest_people_risk = "low"
        next_best_move = "Maintain current people access structure."

    brief = {
        "active_users": active_users,
        "pending_users": pending_users,
        "suspended_users": suspended_users,
        "admin_users": admin_users,
        "manager_users": manager_users,
        "highest_people_risk": highest_people_risk,
        "next_best_move": next_best_move,
    }

    print("People Brief:")
    print(f"Active users: {active_users}")
    print(f"Pending users: {pending_users}")
    print(f"Suspended users: {suspended_users}")
    print(f"Admin users: {admin_users}")
    print(f"Manager users: {manager_users}")
    print(f"Highest people risk: {highest_people_risk}")
    print(f"Next best people move: {next_best_move}")

    return brief
