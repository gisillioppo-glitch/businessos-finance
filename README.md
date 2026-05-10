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
## Finance To Operations Handoff

Finance recommended actions now create an Operations follow-up task.

The handoff is deduplicated, so repeated runs do not create duplicate active Operations tasks.

Expected duplicate-safe output:

```text
[SKIPPED] Duplicate operations task already exists
```

This connects Finance intelligence to Operations execution.
## Governance Layer MVP

The BusinessOS Governance Layer is active as the third core MVP block.

Governance reads audit logs, evaluates control signals, detects missing justification or critical events, and generates a governance brief.

### Governance Architecture

```text
app/governance/
  __init__.py
  findings.py
  governance_brief.py
```

### Governance CLI Commands

```bash
python cli.py gov-findings
python cli.py gov-brief
```

### Current Governance Capabilities

- Read recent audit logs.
- Detect critical or error audit events.
- Detect status updates missing justification.
- Generate governance findings.
- Generate governance brief.
- Report audit trail health.
- Recommend next best governance move.
- Write governance audit events.
- Validate governance commands through smoke test.
## Governance Reports

Governance can export a Markdown governance brief report.

Command:

```bash
python cli.py gov-report
```

Output example:

```text
reports/governance_brief_YYYY-MM-DD.md
```

The report includes:

- Governance findings detected.
- Highest governance risk.
- Audit trail health.
- Next best governance move.
## Support / Incident Module MVP

The BusinessOS Support / Incident Module is active as the fourth core MVP block.

Support manages incidents generated from governance, operations, or other modules. It tracks severity, owner, status, justification, KPIs, briefs, and report exports.

### Support Architecture

```text
app/support/
  __init__.py
  schema.py
  incidents.py
  incident_status.py
  incident_views.py
  support_brief.py
  support_report.py
```

### Support CLI Commands

```bash
python cli.py support-incidents
python cli.py support-brief
python cli.py support-report
```

### Current Support Capabilities

- Create support incidents.
- Deduplicate active support incidents.
- Track severity.
- Track owner role.
- Track status.
- Store status justification.
- Update incident status with justification.
- List active support incidents.
- Generate support incident KPIs.
- Generate support brief.
- Export support brief report.
- Write support audit events.
- Validate support commands through smoke test.
## Command Center / Executive Dashboard MVP

The BusinessOS Command Center is active as the unified executive view across Finance, Operations, Governance, and Support.

It summarizes module health, identifies the highest system risk, recommends the next best executive move, and exports a Markdown executive report.

### Command Center Architecture

```text
app/command_center/
  __init__.py
  command_center_summary.py
  command_center_brief.py
  command_center_report.py
```

### Command Center CLI Commands

```bash
python cli.py command-center
python cli.py command-report
```

### Current Command Center Capabilities

- Read cross-module data from SQLite.
- Summarize Finance state.
- Summarize Operations state.
- Summarize Governance state.
- Summarize Support state.
- Calculate overall system health.
- Identify highest system risk.
- Generate next best executive move.
- Export Command Center Markdown report.
- Write Command Center audit events.
- Validate Command Center through smoke test.

### Current Operating Cycle

```text
Finance intelligence
→ Operations execution
→ Governance oversight
→ Support incident management
→ Command Center synthesis
```

## Dashboard MVP

The BusinessOS Dashboard MVP provides the first visual Command Center through Streamlit.

Run locally:

```bash
streamlit run app/dashboard/main.py
```

Local URL:

```text
http://localhost:8501
```

### Dashboard Security

The dashboard now requires local sign-in before showing BusinessOS data.

Local MVP credentials:

```text
Username: admin
Password: businessos-local
```

Before any external deployment, replace the local password with a private environment variable:

```text
BUSINESSOS_ADMIN_PASSWORD
```

Do not commit `.env`, Streamlit secrets, or local database files.

## Security Foundation MVP

The BusinessOS Security Foundation MVP is the first protection layer for the visual dashboard.

### Security Architecture

```text
app/security/
  __init__.py
  config.py
  access_control.py
```

### Current Security Capabilities

- Protect Streamlit dashboard with login.
- Track local session state.
- Assign a basic role context.
- Keep local secrets out of Git.
- Provide `.env.example` for safe configuration.
- Document remaining requirements before public deployment.

## Dashboard UI Upgrade v0.2

The Dashboard UI Upgrade v0.2 applies the first premium visual pass to the Streamlit Command Center.

Current visual capabilities:

- Dark executive interface.
- BusinessOS red accent system.
- Sidebar navigation.
- Protected login flow.
- Executive metric cards.
- Cash flow overview chart.
- Executive brief panel.
- Operations, incidents, and alerts panels.
- Module pages for Finance, Operations, Governance, and Support.

Run locally:

```bash
streamlit run app/dashboard/main.py
```
