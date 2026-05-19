from datetime import date
from pathlib import Path

from app.actions.action_views import print_action_summary_kpis
from app.audit.audit_log import write_audit_log
from app.reports.executive_brief import print_daily_executive_brief
from app.rules.cash_flow import generate_cash_flow_summary
from app.rules.financial_risk_rules import evaluate_financial_risk_rules


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

REVIEW_COMMANDS = [
    ("Run full finance workflow", "python cli.py run"),
    ("Review active finance actions", "python cli.py actions"),
    ("Review report history", "python cli.py reports"),
    ("Review command center impact", "python cli.py command-center"),
    ("Confirm release readiness", "python cli.py release-readiness"),
]

REVIEW_CLOSE_CRITERIA = [
    "No high financial risk remains without an owner action.",
    "Open recommended actions have an owner and execution path.",
    "In-progress actions have current owner progress evidence.",
    "Command Center no longer depends on finance actions for next best executive move.",
    "Daily Close can reference finance state without ambiguity.",
]


def _active_actions(conn):
    rows = conn.execute(
        """
        SELECT id, created_at, status, priority, owner_role, risk_type,
               recommended_action, COALESCE(status_justification, '')
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
        ORDER BY
            CASE priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                WHEN 'low' THEN 3
                ELSE 4
            END,
            created_at ASC
        """
    ).fetchall()

    return [
        {
            "id": row[0],
            "created_at": row[1],
            "status": row[2],
            "priority": row[3],
            "owner_role": row[4],
            "risk_type": row[5],
            "recommended_action": row[6],
            "status_justification": row[7],
        }
        for row in rows
    ]


def _review_status(cash_flow_summary, risks, action_kpis):
    if cash_flow_summary["financial_health"] == "negative":
        return "finance_review_negative_cash_flow"

    if any(risk["severity"] == "high" for risk in risks):
        return "finance_review_high_risk"

    if action_kpis["high"] > 0:
        return "finance_review_high_priority_actions"

    if action_kpis["open"] > 0:
        return "finance_review_triage_required"

    if action_kpis["in_progress"] > 0:
        return "finance_review_monitoring_required"

    if risks:
        return "finance_review_risk_monitoring"

    return "finance_clear"


def _review_recommendation(status):
    if status == "finance_review_negative_cash_flow":
        return "stabilize_cash_flow"

    if status == "finance_review_high_risk":
        return "resolve_high_financial_risk"

    if status == "finance_review_high_priority_actions":
        return "prioritize_high_finance_actions"

    if status == "finance_review_triage_required":
        return "start_open_finance_actions"

    if status == "finance_review_monitoring_required":
        return "confirm_owner_progress"

    if status == "finance_review_risk_monitoring":
        return "monitor_financial_risks"

    return "maintain_finance_cadence"


def _next_action(status, actions, risks):
    if actions:
        first = actions[0]
        return f"Review {first['risk_type']} with {first['owner_role']} and confirm action progress."

    if risks:
        first = risks[0]
        return f"Review {first['risk_type']} and assign corrective action if needed."

    if status != "finance_clear":
        return "Review finance state and confirm owner path."

    return "Maintain finance monitoring cadence."


def _format_action_rows(actions):
    rows = [
        "| ID | Status | Priority | Owner | Risk | Action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for action in actions:
        rows.append(
            f"| {action['id']} | {action['status']} | {action['priority']} | {action['owner_role']} | {action['risk_type']} | {action['recommended_action']} |"
        )

    return "\n".join(rows)


def _format_risk_rows(risks):
    rows = [
        "| Severity | Type | Message |",
        "| --- | --- | --- |",
    ]

    for risk in risks:
        rows.append(f"| {risk['severity']} | {risk['risk_type']} | {risk['message']} |")

    return "\n".join(rows)


def _format_bullets(items):
    if not items:
        return "- None."

    return "\n".join(f"- {item}" for item in items)


def _format_commands(commands):
    rows = [
        "| Purpose | Command |",
        "| --- | --- |",
    ]

    for purpose, command in commands:
        rows.append(f"| {purpose} | `{command}` |")

    return "\n".join(rows)


def generate_finance_area_review(conn):
    cash_flow_summary = generate_cash_flow_summary(conn)
    risks = evaluate_financial_risk_rules(conn, cash_flow_summary)
    action_kpis = print_action_summary_kpis(conn)
    executive_brief = print_daily_executive_brief(
        conn,
        cash_flow_summary,
        risks,
        action_kpis,
    )
    actions = _active_actions(conn)
    status = _review_status(cash_flow_summary, risks, action_kpis)

    return {
        "date": date.today().isoformat(),
        "review_status": status,
        "review_recommendation": _review_recommendation(status),
        "financial_health": cash_flow_summary["financial_health"],
        "total_income": cash_flow_summary["total_income"],
        "total_expenses": cash_flow_summary["total_expenses"],
        "net_cash_flow": cash_flow_summary["net_cash_flow"],
        "expense_ratio": cash_flow_summary["expense_ratio"],
        "risks_detected": len(risks),
        "highest_financial_risk": executive_brief["highest_risk"],
        "active_actions": len(actions),
        "open_actions": action_kpis["open"],
        "in_progress_actions": action_kpis["in_progress"],
        "high_priority_actions": action_kpis["high"],
        "medium_priority_actions": action_kpis["medium"],
        "low_priority_actions": action_kpis["low"],
        "risks": risks,
        "actions": actions,
        "commands": REVIEW_COMMANDS,
        "close_criteria": REVIEW_CLOSE_CRITERIA,
        "next_action": _next_action(status, actions, risks),
    }


def export_finance_area_review(conn):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_finance_area_review(conn)
    report_path = REPORTS_DIR / f"finance_area_review_{result['date']}.md"

    content = f"""# Finance Area Review v0.1

Date: {result['date']}

## Finance Area Summary

Review status: {result['review_status']}
Review recommendation: {result['review_recommendation']}
Financial health: {result['financial_health']}
Total income: ${result['total_income']:.2f}
Total expenses: ${result['total_expenses']:.2f}
Net cash flow: ${result['net_cash_flow']:.2f}
Expense ratio: {result['expense_ratio'] * 100:.2f}%
Financial risks detected: {result['risks_detected']}
Highest financial risk: {result['highest_financial_risk']}
Active actions: {result['active_actions']}
Open actions: {result['open_actions']}
In-progress actions: {result['in_progress_actions']}
High priority actions: {result['high_priority_actions']}
Medium priority actions: {result['medium_priority_actions']}
Low priority actions: {result['low_priority_actions']}
Next action: {result['next_action']}

## Financial Risks

{_format_risk_rows(result['risks']) if result['risks'] else 'No financial risks detected.'}

## Active Recommended Actions

{_format_action_rows(result['actions']) if result['actions'] else 'No active finance actions.'}

## Review Commands

{_format_commands(result['commands'])}

## Close Criteria

{_format_bullets(result['close_criteria'])}

## Operator Note

This review is advisory and read-only. It does not complete, dismiss, or mutate recommended actions automatically. Finance actions should only close when the owner has evidence for the status change.
"""

    report_path.write_text(content, encoding="utf-8")

    write_audit_log(
        conn,
        "finance_area_review_exported",
        "info" if result["review_status"] == "finance_clear" else "warning",
        "Finance area review exported.",
        {
            "report_path": str(report_path.relative_to(ROOT_DIR)),
            "review_status": result["review_status"],
            "financial_health": result["financial_health"],
            "risks_detected": result["risks_detected"],
            "active_actions": result["active_actions"],
            "highest_financial_risk": result["highest_financial_risk"],
        },
    )

    return result, str(report_path)


def print_finance_area_review(conn):
    result, report_path = export_finance_area_review(conn)

    print("Finance Area Review:")
    print(f"Date: {result['date']}")
    print(f"Review status: {result['review_status']}")
    print(f"Review recommendation: {result['review_recommendation']}")
    print(f"Financial health: {result['financial_health']}")
    print(f"Net cash flow: ${result['net_cash_flow']:.2f}")
    print(f"Highest financial risk: {result['highest_financial_risk']}")
    print(f"Active actions: {result['active_actions']}")
    print(f"Next action: {result['next_action']}")
    print(f"Finance area review exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return result
