# Executive Alerts Report MVP v0.1

## Product meaning

Executive Alerts Report v0.1 turns the executive alert queue into a timestamped Markdown artifact.

This gives leadership a durable record of cross-module risks, owners, and next recommended actions.

## Why it matters

Executive alerts are useful in the dashboard, but institutions also need records. This block preserves the alert state as a report that can be reviewed, shared internally, or attached to operating cadence notes.

## Current capabilities

- Export Executive Alerts summary to Markdown.
- Include total, critical, high, and medium alert counts.
- Include highest alert risk.
- Include next best alert move.
- Include a Markdown table of active alerts with severity, source, owner, title, and recommended action.
- Write audit log on report export.
- Validate through smoke test.

## Files

```text
app/alerts/executive_alerts_report.py
cli.py
scripts/smoke_test.py
README.md
```

## CLI command

```bash
python cli.py executive-alerts-report
```

## Report output

```text
reports/executive_alerts_YYYY-MM-DD.md
```

## Suggested tag

```text
businessos-executive-alerts-report-mvp-v0.1
```
