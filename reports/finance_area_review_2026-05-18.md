# Finance Area Review v0.1

Date: 2026-05-18

## Finance Area Summary

Review status: finance_review_high_risk
Review recommendation: resolve_high_financial_risk
Financial health: positive
Total income: $1000.00
Total expenses: $750.00
Net cash flow: $250.00
Expense ratio: 75.00%
Financial risks detected: 2
Highest financial risk: high
Active actions: 2
Open actions: 0
In-progress actions: 2
High priority actions: 0
Medium priority actions: 2
Low priority actions: 0
Next action: Review expense_ratio_warning with Finance Manager and confirm action progress.

## Financial Risks

| Severity | Type | Message |
| --- | --- | --- |
| medium | expense_ratio_warning | Expense ratio warning: 75.00% of income is being spent. |
| high | expense_concentration | Expense concentration risk: marketing represents 93.33% of expenses. |

## Active Recommended Actions

| ID | Status | Priority | Owner | Risk | Action |
| --- | --- | --- | --- | --- | --- |
| c8259958-5158-4f36-8934-049b35cf4061 | in_progress | medium | Finance Manager | expense_ratio_warning | Review discretionary expenses and reduce non-essential spending until the expense ratio improves. |
| 4a240520-31bb-4727-9de6-c741b7146c75 | in_progress | medium | Finance Manager | expense_concentration | Review the category with high expense concentration and confirm whether spending is justified by expected return. |

## Review Commands

| Purpose | Command |
| --- | --- |
| Run full finance workflow | `python cli.py run` |
| Review active finance actions | `python cli.py actions` |
| Review report history | `python cli.py reports` |
| Review command center impact | `python cli.py command-center` |
| Confirm release readiness | `python cli.py release-readiness` |

## Close Criteria

- No high financial risk remains without an owner action.
- Open recommended actions have an owner and execution path.
- In-progress actions have current owner progress evidence.
- Command Center no longer depends on finance actions for next best executive move.
- Daily Close can reference finance state without ambiguity.

## Operator Note

This review is advisory and read-only. It does not complete, dismiss, or mutate recommended actions automatically. Finance actions should only close when the owner has evidence for the status change.
