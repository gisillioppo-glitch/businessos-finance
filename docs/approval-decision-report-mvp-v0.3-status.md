# Approval Decision Report MVP v0.3

## Product meaning

BusinessOS now exports approval decisions into a timestamped Markdown report. This gives leadership and governance users a durable record of what was approved, rejected, pending, and why.

## Why it matters

Approvals are institutional decisions. Once BusinessOS can approve or reject sensitive requests, it also needs an evidence layer that can be reviewed, shared, audited, and compared over time.

## MVP scope

- Add Markdown export for approval decisions.
- Include pending, approved, rejected, cancelled, priority, and type KPIs.
- Include highest approval risk and next best approval move.
- Include approval table with status, approver, requester, source, and justification.
- Add `approval-report` CLI command.
- Add smoke test coverage.

## CLI commands

```bash
python cli.py approval-report
```

## Output

`reports/approval_decisions_YYYY-MM-DD.md`

## Files

- `app/approvals/approval_report.py`
- `cli.py`
- `scripts/smoke_test.py`
- `README.md`

## Suggested tag

`businessos-approval-decision-report-mvp-v0.3`
