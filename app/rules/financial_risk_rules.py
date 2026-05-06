import pandas as pd

from app.audit.audit_log import write_audit_log


def evaluate_financial_risk_rules(conn, cash_flow_summary):
    risks = []

    total_income = cash_flow_summary["total_income"]
    total_expenses = cash_flow_summary["total_expenses"]
    net_cash_flow = cash_flow_summary["net_cash_flow"]
    expense_ratio = cash_flow_summary["expense_ratio"]

    if total_income == 0 and total_expenses > 0:
        risks.append(
            {
                "risk_type": "no_income_detected",
                "severity": "high",
                "message": "No income detected while expenses exist.",
            }
        )

    if net_cash_flow < 0:
        risks.append(
            {
                "risk_type": "negative_cash_flow",
                "severity": "high",
                "message": f"Negative cash flow detected: ${net_cash_flow:.2f}.",
            }
        )

    if expense_ratio >= 0.9:
        risks.append(
            {
                "risk_type": "expense_ratio_warning",
                "severity": "high",
                "message": f"Expense ratio is very high: {expense_ratio * 100:.2f}% of income is being spent.",
            }
        )
    elif expense_ratio >= 0.7:
        risks.append(
            {
                "risk_type": "expense_ratio_warning",
                "severity": "medium",
                "message": f"Expense ratio warning: {expense_ratio * 100:.2f}% of income is being spent.",
            }
        )

    category_df = pd.read_sql_query(
        """
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category
        """,
        conn,
    )

    if total_expenses > 0 and not category_df.empty:
        for _, row in category_df.iterrows():
            category_share = float(row["total"]) / total_expenses

            if category_share >= 0.8:
                severity = "high"
            elif category_share >= 0.6:
                severity = "medium"
            else:
                continue

            risks.append(
                {
                    "risk_type": "expense_concentration",
                    "severity": severity,
                    "message": (
                        f"Expense concentration risk: {row['category']} represents "
                        f"{category_share * 100:.2f}% of expenses."
                    ),
                    "category": row["category"],
                    "category_share": category_share,
                }
            )

    if not risks:
        print("Financial Risk Rules: No financial risks detected.")
        write_audit_log(
            conn,
            "financial_risk_rules_evaluated",
            "info",
            "Financial risk rules evaluated with no risks detected.",
            {"risks_found": 0},
        )
        return []

    print("Financial Risk Rules:")

    for risk in risks:
        print(f"[{risk['severity'].upper()}] {risk['message']}")

        write_audit_log(
            conn,
            "financial_risk_detected",
            risk["severity"],
            risk["message"],
            risk,
        )

    write_audit_log(
        conn,
        "financial_risk_rules_evaluated",
        "info",
        "Financial risk rules evaluated.",
        {"risks_found": len(risks)},
    )

    return risks
