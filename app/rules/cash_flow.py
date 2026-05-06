import pandas as pd

from app.audit.audit_log import write_audit_log


def generate_cash_flow_summary(conn):
    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    if df.empty:
        summary = {
            "total_income": 0.0,
            "total_expenses": 0.0,
            "net_cash_flow": 0.0,
            "expense_ratio": 0.0,
            "financial_health": "warning",
        }
    else:
        income_df = df[df["type"] == "income"]
        expense_df = df[df["type"] == "expense"]

        total_income = float(income_df["amount"].sum())
        total_expenses = float(expense_df["amount"].sum())
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
