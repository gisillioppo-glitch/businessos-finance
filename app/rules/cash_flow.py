from app.audit.audit_log import write_audit_log


def generate_cash_flow_summary(conn):
    rows = conn.execute(
        """
        SELECT type, COALESCE(SUM(amount), 0)
        FROM transactions
        GROUP BY type
        """
    ).fetchall()

    if not rows:
        summary = {
            "total_income": 0.0,
            "total_expenses": 0.0,
            "net_cash_flow": 0.0,
            "expense_ratio": 0.0,
            "financial_health": "warning",
        }
    else:
        totals = {row[0]: float(row[1] or 0) for row in rows}
        total_income = totals.get("income", 0.0)
        total_expenses = totals.get("expense", 0.0)
        net_cash_flow = total_income - total_expenses

        if total_income > 0:
            expense_ratio = total_expenses / total_income
        else:
            expense_ratio = 0.0

        if net_cash_flow > 0:
            financial_health = "positive"
        elif net_cash_flow == 0:
            financial_health = "warning"
        else:
            financial_health = "negative"

        summary = {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_cash_flow": net_cash_flow,
            "expense_ratio": expense_ratio,
            "financial_health": financial_health,
        }

    print("Cash Flow Summary:")
    print(f"Total income: ${summary['total_income']:.2f}")
    print(f"Total expenses: ${summary['total_expenses']:.2f}")
    print(f"Net cash flow: ${summary['net_cash_flow']:.2f}")
    print(f"Expense ratio: {summary['expense_ratio'] * 100:.2f}%")
    print(f"Financial health: {summary['financial_health']}")

    write_audit_log(
        conn,
        "cash_flow_summary_generated",
        summary["financial_health"],
        "Cash flow summary generated.",
        summary,
    )

    return summary
