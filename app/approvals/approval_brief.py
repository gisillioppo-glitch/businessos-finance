def print_approval_brief(conn, approval_kpis):
    pending_approvals = approval_kpis["pending"]
    critical_approvals = approval_kpis["critical"]
    high_approvals = approval_kpis["high"]
    decision_approvals = approval_kpis["decision"]
    access_approvals = approval_kpis["access"]

    if critical_approvals > 0:
        highest_approval_risk = "critical"
        next_best_move = "Review critical approvals before any dependent action proceeds."
    elif high_approvals > 0:
        highest_approval_risk = "high"
        next_best_move = "Review high-priority approvals and confirm executive decision."
    elif pending_approvals > 0:
        highest_approval_risk = "medium"
        next_best_move = "Review pending approvals to prevent operational blockage."
    else:
        highest_approval_risk = "low"
        next_best_move = "Maintain current approval controls and continue monitoring."

    brief = {
        "pending_approvals": pending_approvals,
        "critical_approvals": critical_approvals,
        "high_approvals": high_approvals,
        "decision_approvals": decision_approvals,
        "access_approvals": access_approvals,
        "highest_approval_risk": highest_approval_risk,
        "next_best_move": next_best_move,
    }

    print("Approval Brief:")
    print(f"Pending approvals: {pending_approvals}")
    print(f"Critical approvals: {critical_approvals}")
    print(f"High approvals: {high_approvals}")
    print(f"Decision approvals: {decision_approvals}")
    print(f"Access approvals: {access_approvals}")
    print(f"Highest approval risk: {highest_approval_risk}")
    print(f"Next best approval move: {next_best_move}")

    return brief
