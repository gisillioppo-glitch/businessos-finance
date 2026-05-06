from app.audit.audit_log import write_audit_log


def print_daily_executive_brief(conn, cash_flow_summary, risks, action_kpis):
    print("Daily Executive Brief:")
    print(f"Financial health: {cash_flow_summary['financial_health']}")
    print(f"Net cash flow: ${cash_flow_summary['net_cash_flow']:.2f}")
    print(f"Expense ratio: {cash_flow_summary['expense_ratio'] * 100:.2f}%")
    print(f"Financial risks detected: {len(risks)}")
    print(f"Open actions: {action_kpis['open']}")
    print(f"In-progress actions: {action_kpis['in_progress']}")

    if risks:
        highest_risk = "high" if any(risk["severity"] == "high" for risk in risks) else risks[0]["severity"]
        print(f"Highest risk level: {highest_risk}")
    else:
        highest_risk = "none"
        print("Highest risk level: none")

    if action_kpis["open"] > 0:
        next_best_move = "Review and start the highest-priority open financial action."
    elif action_kpis["in_progress"] > 0:
        next_best_move = "Follow up on in-progress financial actions and confirm owner progress."
    elif risks:
        next_best_move = "Review detected financial risks and assign corrective actions."
    else:
        next_best_move = "Maintain current monitoring and review financial data again in the next cycle."

    print(f"Next best move: {next_best_move}")

    write_audit_log(
        conn,
        "daily_executive_brief_generated",
        "info",
        "Daily executive brief generated.",
        {
            "financial_health": cash_flow_summary["financial_health"],
            "net_cash_flow": cash_flow_summary["net_cash_flow"],
            "expense_ratio": cash_flow_summary["expense_ratio"],
            "risks_detected": len(risks),
            "open_actions": action_kpis["open"],
            "in_progress_actions": action_kpis["in_progress"],
            "highest_risk": highest_risk,
            "next_best_move": next_best_move,
        },
    )

    return {
        "financial_health": cash_flow_summary["financial_health"],
        "net_cash_flow": cash_flow_summary["net_cash_flow"],
        "expense_ratio": cash_flow_summary["expense_ratio"],
        "risks_detected": len(risks),
        "open_actions": action_kpis["open"],
        "in_progress_actions": action_kpis["in_progress"],
        "highest_risk": highest_risk,
        "next_best_move": next_best_move,
    }
