# BusinessOS Finance Module MVP

BusinessOS Finance Module is a local Python MVP for financial intelligence, operational actions, auditability, and executive reporting.

The current module loads transaction data from CSV, stores it in SQLite, evaluates financial rules, generates recommended actions, exports daily reports, and records audit logs for traceability.

## Current Architecture

The project is organized as a modular Python application.

```text
businessos-finance-module/
  main.py
  finance.db
  data/
    raw/
      sample.csv
  reports/
    daily_brief_YYYY-MM-DD.md
  app/
    audit/
      audit_log.py
    db/
      connection.py
      schema.py
    ingest/
      csv_loader.py
    rules/
      cash_flow.py
      financial_risk_rules.py
      anomaly_rules.py
    actions/
      recommended_actions.py
      action_status.py
      action_views.py
    reports/
      executive_brief.py
      report_export.py
      report_history.py
## Demo Mode

The system includes a demo mode flag in `main.py`:

```python
DEMO_MODE = False
## Health Check

The project includes a quick health check script:

```bash
python scripts/health_check.py
## CLI Commands

The project includes a small CLI entry point:

```bash
python cli.py <command>
## CLI Commands

The project includes a small CLI entry point:

```bash
python cli.py <command>
```

Available commands:

```bash
python cli.py run
python cli.py health
python cli.py actions
python cli.py reports
```

### Command Details

- `run`
  - Runs the full Finance MVP workflow.
- `health`
  - Runs the Finance health check.
- `actions`
  - Shows active recommended actions and action KPIs.
- `reports`
  - Shows report history.

### Recommended Daily Check

```bash
python cli.py health
python cli.py actions
python cli.py reports
```
## Smoke Test

The project includes a smoke test script:

```bash
python scripts/smoke_test.py
```

The smoke test verifies the main CLI commands:

```bash
python cli.py health
python cli.py actions
python cli.py reports
python cli.py run
```

Expected final output:

```text
Smoke test completed successfully.
```
## Action Status Justification

Recommended action status changes support an optional justification.

The database table `recommended_actions` includes:

```text
status_justification
```

When an action status is updated, the audit log records:

- Action ID.
- Old status.
- New status.
- Justification.
- Recommended action.

This improves traceability for governance workflows.
## Architecture Diagram

The current Finance MVP architecture diagram is documented in:

```text
docs/finance-mvp-status.md
## Operations Module MVP

The BusinessOS Operations Module is active as the second core MVP block.

It converts operational work into trackable tasks with owners, priorities, deadlines, statuses, justifications, escalations, KPIs, and an operations brief.

### Operations Architecture

```text
app/operations/
  __init__.py
  schema.py
  tasks.py
  task_status.py
  task_views.py
  escalation_rules.py
  operations_brief.py
```

### Operations Database Table

```text
operations_tasks
```

Current fields:

```text
id
created_at
title
description
owner_role
priority
deadline_date
status
status_justification
source_module
source_reference_id
```

### Operations CLI Commands

```bash
python cli.py ops-tasks
python cli.py ops-escalations
python cli.py ops-brief
```

### Current Operations Capabilities

- Create operations tasks.
- Track owners.
- Track priorities.
- Track deadlines.
- Track status.
- Store status justification.
- List active operations tasks.
- Generate operations KPIs.
- Evaluate escalation rules.
- Generate operations brief.
- Write audit logs for operations events.
- Validate operations commands through smoke test.
