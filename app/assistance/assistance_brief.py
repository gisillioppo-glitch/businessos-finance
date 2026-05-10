def print_assistance_brief(conn, request_kpis):
    critical_requests = request_kpis["critical"]
    high_requests = request_kpis["high"]
    waiting_approval = request_kpis["waiting_approval"]
    open_requests = request_kpis["open"]
    decision_requests = request_kpis["decision"]

    if critical_requests > 0:
        highest_assistance_risk = "critical"
        next_best_move = "Resolve critical assistance requests immediately."
    elif high_requests > 0:
        highest_assistance_risk = "high"
        next_best_move = "Review high-severity assistance requests and assign ownership."
    elif waiting_approval > 0:
        highest_assistance_risk = "medium"
        next_best_move = "Review pending approvals and unblock responsible teams."
    elif open_requests > 0:
        highest_assistance_risk = "medium"
        next_best_move = "Triage open assistance requests and confirm routing."
    else:
        highest_assistance_risk = "low"
        next_best_move = "Maintain current assistance coverage and monitor requests."

    brief = {
        "open_requests": open_requests,
        "waiting_approval_requests": waiting_approval,
        "critical_requests": critical_requests,
        "high_requests": high_requests,
        "decision_requests": decision_requests,
        "highest_assistance_risk": highest_assistance_risk,
        "next_best_move": next_best_move,
    }

    print("Assistance Brief:")
    print(f"Open requests: {open_requests}")
    print(f"Waiting approval requests: {waiting_approval}")
    print(f"Critical requests: {critical_requests}")
    print(f"High requests: {high_requests}")
    print(f"Decision requests: {decision_requests}")
    print(f"Highest assistance risk: {highest_assistance_risk}")
    print(f"Next best assistance move: {next_best_move}")

    return brief
