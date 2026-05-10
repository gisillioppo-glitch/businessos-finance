# Approval Decision MVP v0.2

## Product meaning

BusinessOS now supports an explicit approval decision lifecycle. The system can move sensitive approval requests from pending into approved or rejected states with status justification and audit logging.

This turns governance from detection-only into controlled institutional decision execution.

## Why it matters

The Governance Sensitivity and Executive Alerts layers can identify what requires control. This block adds the next institutional step: an executive can approve or reject pending decisions, and BusinessOS preserves that decision as part of the operating record.

## MVP scope

- Add approval decision status helpers.
- Add CLI commands for approve and reject demo flows.
- Keep approved/rejected default approvals from being recreated as pending duplicates.
- Add approval decision KPIs to the private dashboard.
- Add an Approvals dashboard page.
- Add smoke test coverage for approval decisions.

## CLI commands

```bash
python cli.py approvals
python cli.py approval-brief
python cli.py approval-approve
python cli.py approval-reject
```

## Decision states

- `pending`: waiting for executive decision.
- `approved`: reviewed and accepted with justification.
- `rejected`: reviewed and stopped or returned with justification.
- `cancelled`: reserved for future cancellation flows.

## Files

- `app/approvals/approval_status.py`
- `app/approvals/requests.py`
- `cli.py`
- `scripts/smoke_test.py`
- `app/dashboard/main.py`
- `app/security/access_control.py`

## Suggested tag

`businessos-approval-decision-mvp-v0.2`
