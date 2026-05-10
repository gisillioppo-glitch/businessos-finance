# Executive Alerts MVP v0.1

## Product meaning

Executive Alerts v0.1 turns cross-module BusinessOS signals into a single executive alert queue.

This block connects governance sensitivity, finance recommendations, support incidents, approvals, assistance, and operations risk into one private operating layer for leadership review.

## Why it matters

Before this block, each module could report its own state. With Executive Alerts, the operating system now consolidates what needs executive attention across modules instead of forcing leaders to inspect each page separately.

## Current capabilities

- Generate executive alerts from governance sensitivity findings.
- Include active finance recommendations as executive alerts.
- Include active support incidents as executive alerts.
- Rank alerts by severity.
- Print alert list through CLI.
- Print executive alert brief through CLI.
- Show Executive Alerts on the private dashboard home page.
- Add a dedicated Alerts page in the private dashboard.

## Files

```text
app/alerts/__init__.py
app/alerts/executive_alerts.py
app/dashboard/main.py
app/security/access_control.py
cli.py
scripts/smoke_test.py
```

## CLI commands

```bash
python cli.py executive-alerts
python cli.py executive-alerts-brief
```

## Dashboard

Run locally:

```bash
streamlit run app/dashboard/main.py
```

The dashboard now includes:

- Alerts navigation entry.
- Executive alert count.
- Critical alert count.
- High alert count.
- Alert queue with source module, owner, severity, and recommended action.
- Alert brief for executive review.

## Validation

This block should be validated with:

```bash
python -m py_compile app/alerts/executive_alerts.py app/dashboard/main.py cli.py
python cli.py executive-alerts
python cli.py executive-alerts-brief
python scripts/smoke_test.py
```

## Suggested tag

```text
businessos-executive-alerts-mvp-v0.1
```
