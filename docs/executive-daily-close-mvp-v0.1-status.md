# Executive Daily Close MVP v0.1

## Product meaning

BusinessOS now has a single daily close command that generates the core executive report set and then indexes the resulting evidence. This creates an operating ritual for ending the day with a clean institutional record.

## Why it matters

The platform now produces many reports across Finance, Governance, Support, Command Center, Approvals, Executive Alerts, and Evidence. A daily close command prevents fragmented reporting and gives leadership one repeatable close process.

## MVP scope

- Add `daily-close` CLI command.
- Generate the daily finance brief.
- Generate Governance, Support, Command Center, Approval Decision, and Executive Alerts reports.
- Generate the Executive Evidence Index after reports are created.
- Export an Executive Daily Close Markdown report.
- Add smoke test coverage.

## CLI command

```bash
python cli.py daily-close
```

## Output

`reports/daily_close_YYYY-MM-DD.md`

## Files

- `app/evidence/daily_close.py`
- `cli.py`
- `scripts/smoke_test.py`
- `README.md`

## Suggested tag

`businessos-executive-daily-close-mvp-v0.1`
