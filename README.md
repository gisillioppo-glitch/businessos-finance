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

## Landing Website MVP

The BusinessOS Landing Website MVP is a public static product presentation page.

Files:

```text
public/index.html
public/styles.css
public/assets/dashboard-preview.png
```

The landing page is separate from the private dashboard. It does not connect to `finance.db`, import private modules, or expose internal logic.

Open locally:

```text
public/index.html
```

## Deployment Readiness MVP

The BusinessOS Deployment Readiness MVP defines the publication boundary between the public landing website and the private operating system runtime.

Public surface:

```text
public/
```

Private surface:

```text
app/
finance.db
.env
.streamlit/secrets.toml
reports/
data/
```

Before publishing anything externally, run:

```bash
python scripts/deployment_check.py
python scripts/smoke_test.py
```

Rules:

- Publish the landing website first.
- Keep the dashboard private until stronger authentication and deployment controls are ready.
- Never publish `finance.db`, `.env`, Streamlit secrets, or private module logic as a public website.

## Landing Publish MVP

The BusinessOS Landing Publish MVP prepares the public landing website for GitHub Pages.

Deployment workflow:

```text
.github/workflows/pages.yml
```

The workflow publishes only:

```text
public/
```

It runs the deployment readiness check before publishing.

GitHub Pages setting required:

```text
Repository → Settings → Pages → Build and deployment → Source → GitHub Actions
```

Expected public URL pattern:

```text
https://gisillioppo-glitch.github.io/businessos-finance/
```

## Lead Intake & Demo Request MVP

The BusinessOS Lead Intake & Demo Request MVP adds a structured demo request form to the public landing website.

Current status:

- Form UI is live on the landing page.
- Request Demo buttons now point to the form.
- Fields capture lead qualification details.
- Honeypot anti-spam field is included.
- Automatic email delivery requires connecting a real form endpoint.

Activation options:

- Formspree endpoint.
- Tally or Typeform.
- Netlify Forms.
- Future BusinessOS backend endpoint.

The public form remains separate from the private dashboard and does not expose internal runtime data.

## Repository Split & IP Protection MVP

BusinessOS now separates public presentation from private product runtime.

Public landing repository:

```text
https://github.com/gisillioppo-glitch/businessos-landing
```

Private product repository:

```text
https://github.com/gisillioppo-glitch/businessos-finance
```

The public repo contains only static landing files. The private repo contains the BusinessOS runtime, dashboard, modules, security layer, and internal documentation.

The GitHub Pages workflow was removed from this private repo so public deployment happens from `businessos-landing` only.

## People Layer MVP

The BusinessOS People Layer is the first internal user operating layer.

It tracks institutional users, departments, roles, statuses, access levels, people KPIs, and a People Brief for executive oversight.

### People Architecture

```text
app/people/
  __init__.py
  schema.py
  users.py
  people_views.py
  people_brief.py
```

### People CLI Commands

```bash
python cli.py people
python cli.py people-brief
```

### Current People Capabilities

- Create and seed business users.
- Deduplicate users by email.
- Track role, department, status, and access level.
- Generate People Directory output.
- Generate People Summary KPIs.
- Generate People Brief and next best people move.
- Write audit logs for people events.
- Validate People Layer through smoke test.

## Assistance Layer MVP

The BusinessOS Assistance Layer is the first internal request and escalation system.

It lets institutional users create structured help, approval, incident, access, and decision requests that can be routed to owners and reviewed by the operating system.

### Assistance Architecture

```text
app/assistance/
  __init__.py
  schema.py
  requests.py
  request_views.py
  assistance_brief.py
```

### Assistance CLI Commands

```bash
python cli.py assistance
python cli.py assistance-brief
```

### Current Assistance Capabilities

- Create and seed assistance requests.
- Deduplicate active requests by source.
- Track request type, severity, requester, owner, status, and source module.
- Generate Assistance Request List output.
- Generate Assistance Summary KPIs.
- Generate Assistance Brief and next best assistance move.
- Write audit logs for assistance events.
- Validate Assistance Layer through smoke test.

## Assistance Status v0.2

BusinessOS Assistance requests now support controlled status updates with audit logging and justification.

### Assistance Status CLI Command

```bash
python cli.py assistance-status
```

Current behavior:

- Finds the first open assistance request.
- Moves it to `triaged`.
- Stores a justification.
- Writes an audit log.
- Passes through the smoke test.

## Dashboard Assistance Page v0.1

The private BusinessOS dashboard now includes an Assistance page.

Current visual capabilities:

- Assistance navigation entry.
- Active request KPIs.
- High-severity assistance request count.
- Waiting approval count.
- Active assistance request list with owner, type, status, and severity.
- Assistance Brief panel for executive review.

Run locally:

```bash
streamlit run app/dashboard/main.py
```

## Dashboard People Page v0.1

The private BusinessOS dashboard now includes a People page.

Current visual capabilities:

- People navigation entry.
- Total users, active users, admin users, and manager users.
- People Directory with user, email, role, department, status, and access level.
- People Brief panel for executive review.

Run locally:

```bash
streamlit run app/dashboard/main.py
```

## Approval Layer MVP

The BusinessOS Approval Layer is the first institutional decision-control layer.

It captures sensitive requests that require explicit approval before dependent actions proceed.

### Approval Architecture

```text
app/approvals/
  __init__.py
  schema.py
  requests.py
  approval_views.py
  approval_brief.py
```

### Approval CLI Commands

```bash
python cli.py approvals
python cli.py approval-brief
```

### Current Approval Capabilities

- Create and seed approval requests.
- Deduplicate pending approvals by source.
- Track approval type, priority, requester, approver role, status, and source module.
- Generate Approval Request List output.
- Generate Approval Summary KPIs.
- Generate Approval Brief and next best approval move.
- Write audit logs for approval events.
- Validate Approval Layer through smoke test.

## Governance Sensitivity Rules v0.1

BusinessOS now includes a rule-based governance sensitivity layer.

It defines which institutional signals should be treated as sensitive and reviewed before action proceeds.

### Sensitivity CLI Commands

```bash
python cli.py gov-sensitivity
python cli.py gov-sensitivity-brief
```

Current sensitivity categories:

- Pending decision/access/budget/policy/incident approvals.
- High or critical approvals.
- Sensitive assistance requests.
- Privileged admin/executive users.
- Overdue operations tasks.
- High or critical support incidents.
- Critical/error audit events.
- Sensitive status updates missing justification.

## Dashboard Governance Sensitivity Page v0.1

The private BusinessOS dashboard now includes a Sensitivity page.

Current visual capabilities:

- Sensitivity navigation entry.
- Sensitive findings count.
- High and medium sensitivity finding counts.
- Highest sensitivity risk.
- Sensitivity Findings list with source, finding type, and severity.
- Sensitivity Brief panel for executive review.

Run locally:

```bash
streamlit run app/dashboard/main.py
```

## Executive Alerts MVP v0.1

BusinessOS now includes an Executive Alerts layer.

It consolidates cross-module signals into one executive alert queue for leadership review.

### Executive Alerts CLI Commands

```bash
python cli.py executive-alerts
python cli.py executive-alerts-brief
```

Current capabilities:

- Generate executive alerts from governance sensitivity findings.
- Include active finance recommendations.
- Include active support incidents.
- Rank alerts by severity.
- Display alerts on the private dashboard home page.
- Add a dedicated private dashboard Alerts page.
- Validate Executive Alerts through smoke test.

Run locally:

```bash
streamlit run app/dashboard/main.py
```

## Executive Alerts Report MVP v0.1

BusinessOS can now export the Executive Alerts queue as a Markdown report.

### Executive Alerts Report CLI Command

```bash
python cli.py executive-alerts-report
```

Current capabilities:

- Export alert summary to `reports/executive_alerts_YYYY-MM-DD.md`.
- Include total, critical, high, and medium alert counts.
- Include highest alert risk and next best alert move.
- Include a Markdown table of active alerts.
- Write audit log on export.
- Validate report export through smoke test.

## Executive Alert Status MVP v0.1

BusinessOS Executive Alerts now support controlled status tracking.

### Executive Alert Status CLI Command

```bash
python cli.py executive-alert-status
```

Current capabilities:

- Create and maintain `executive_alert_statuses`.
- Generate stable alert keys for derived executive alerts.
- Track `open`, `acknowledged`, `in_review`, `resolved`, and `dismissed` alert states.
- Store owner role and status justification.
- Write audit logs for alert status updates.
- Show status in Executive Alerts CLI output.
- Show open, acknowledged, and in-review alert KPIs in the private dashboard.
- Include status in Executive Alerts reports.
- Validate alert status through smoke test.

## Executive Alert Resolution MVP v0.2

BusinessOS Executive Alerts now support a basic resolution lifecycle.

### Executive Alert Resolution CLI Commands

```bash
python cli.py executive-alert-status
python cli.py executive-alert-review
python cli.py executive-alert-resolve
```

Current capabilities:

- Move executive alerts from `open` to `acknowledged`.
- Move acknowledged alerts to `in_review`.
- Resolve in-review alerts with justification.
- Keep resolved alerts out of the active queue.
- Track resolved alert count in the private dashboard.
- Include status-aware alert queue in Executive Alerts reports.
- Validate the resolution lifecycle through smoke test.

## Approval Decision MVP v0.2

BusinessOS approvals now support executive decision outcomes.

### Approval Decision CLI Commands

```bash
python cli.py approvals
python cli.py approval-brief
python cli.py approval-approve
python cli.py approval-reject
```

Current capabilities:

- Move pending approvals to `approved` with justification.
- Move pending approvals to `rejected` with justification.
- Write audit logs for approval decision updates.
- Prevent closed default approvals from being recreated as pending duplicates.
- Show pending, approved, rejected, and high-priority approval counts in the private dashboard.
- Add a dedicated private dashboard Approvals page.
- Validate approval decisions through smoke test.

## Approval Decision Report MVP v0.3

BusinessOS can now export approval decisions as a Markdown governance record.

### Approval Decision Report CLI Command

```bash
python cli.py approval-report
```

Current capabilities:

- Export approval decision summary to `reports/approval_decisions_YYYY-MM-DD.md`.
- Include pending, approved, rejected, cancelled, priority, and type KPIs.
- Include highest approval risk and next best approval move.
- Include approval rows with approver, requester, source, status, and justification.
- Write audit log on report export.
- Validate export through smoke test.

## Executive Evidence Index MVP v0.1

BusinessOS can now generate an executive evidence index for the operating day.

### Executive Evidence Index CLI Command

```bash
python cli.py evidence-index
```

Current capabilities:

- Track expected daily evidence reports.
- Show available and missing evidence items.
- Export `reports/executive_evidence_index_YYYY-MM-DD.md`.
- Include Command Center, Executive Alerts, Approval Decisions, Governance, Support, and Daily Finance evidence.
- Write audit logs when the evidence index is viewed/exported.
- Validate evidence indexing through smoke test.

## Executive Daily Close MVP v0.1

BusinessOS can now run a one-command executive daily close.

### Executive Daily Close CLI Command

```bash
python cli.py daily-close
```

Current capabilities:

- Generate the daily finance brief.
- Generate Governance, Support, Command Center, Approval Decision, and Executive Alerts reports.
- Generate the Executive Evidence Index after reports are refreshed.
- Export `reports/daily_close_YYYY-MM-DD.md`.
- Write audit logs for the daily close report.
- Validate the close flow through smoke test.

## Dashboard Daily Close Page v0.1

The private BusinessOS dashboard now includes a Daily Close page.

Current visual capabilities:

- Show completed close steps versus total close steps.
- Show available and missing evidence counts.
- Show latest daily close and evidence index report paths.
- List close step statuses from the latest daily close report.
- List evidence register items from the latest executive evidence index.
- Include Daily Close in role-based dashboard navigation.

Run locally:

```bash
streamlit run app/dashboard/main.py
```

## Daily Close Distribution MVP v0.1

BusinessOS can now prepare an email-ready daily close distribution package for leadership and department owners.

CLI commands:

```bash
python cli.py daily-close
python cli.py daily-close-distribution
```

Current capabilities:

- Automatically prepares daily close distribution after the executive daily close.
- Builds recipient packages from active BusinessOS users.
- Routes the full evidence package to the Executive Owner / CEO.
- Routes scoped evidence packages to Finance, Operations, and Support managers.
- Exports `reports/daily_close_distribution_YYYY-MM-DD.md`.
- Keeps real email sending out of MVP code until protected SMTP/API credentials are ready.
- Validates the command through smoke test.

## Scheduled Daily Close MVP v0.1

BusinessOS can now expose a controlled daily close runner for external schedulers.

CLI commands:

```bash
python cli.py daily-close-schedule
python cli.py scheduled-daily-close
```

Current capabilities:

- Initialize a default `executive_daily_close` schedule.
- Show schedule status, today's close report status, and next action.
- Run the daily close only when due.
- Skip safely if today's close report already exists.
- Record scheduler outcomes in the database and audit log.
- Keep external delivery and operating system scheduler setup outside this MVP.

## Dashboard Scheduled Close Page v0.1

The private BusinessOS dashboard now includes a Scheduled Close page.

Current visual capabilities:

- Show schedule enabled status and configured local run time.
- Show whether today's daily close report already exists.
- Show last scheduler status and next action.
- Display last run date, start timestamp, completion timestamp, and latest scheduler message.
- Keep the dashboard page read-only; execution remains in CLI or an external scheduler.

## Notification Outbox MVP v0.1

BusinessOS now has a safe internal notification queue for prepared executive and manager messages.

CLI command:

```bash
python cli.py notifications
```

Current capabilities:

- Queue Daily Close Distribution messages for CEO and department owners.
- Store recipient, subject, body, source, channel, and status.
- Track queued, sent, dismissed, and failed notification counts.
- Prevent duplicate daily close notifications for the same recipient/source/date.
- Keep real email sending out of MVP code until protected delivery credentials are ready.
- Validate notification outbox through smoke test.

## Notification Status MVP v0.2

BusinessOS now tracks the lifecycle of notification outbox messages.

CLI commands:

```bash
python cli.py notification-sent
python cli.py notification-dismiss
python cli.py notification-fail
python cli.py notifications
```

Current capabilities:

- Move queued notifications into sent, dismissed, or failed states.
- Record sent timestamp for sent notifications.
- Keep notification outcomes auditable.
- Validate notification lifecycle through smoke test.
- Preserve the safety boundary: no external email is sent yet.

## Notification Delivery Approval MVP v0.1

BusinessOS now requires governance approval before queued notifications can be marked as sent.

CLI command:

```bash
python cli.py notification-delivery-approval
```

Current capabilities:

- Create approval requests for queued notification outbox items.
- Deduplicate delivery approvals by notification ID.
- Export `reports/notification_delivery_approval_YYYY-MM-DD.md`.
- Block `notification-sent` unless the matching delivery approval is approved.
- Keep real email delivery out of scope until protected SMTP/API credentials are ready.

## Secure Email Delivery Adapter v0.1

BusinessOS can now run a protected email delivery adapter.

CLI command:

```bash
python cli.py secure-email-delivery
```

Current capabilities:

- Read SMTP configuration from environment variables.
- Default to disabled and dry-run mode.
- Only process queued email notifications with approved delivery approvals.
- Export `reports/secure_email_delivery_YYYY-MM-DD.md`.
- Mark notifications sent or failed only after an enabled SMTP attempt.
- Keep credentials out of code, reports, and Git.

## System Integrity Check MVP v0.1

BusinessOS now includes a structural self-check command.

CLI command:

```bash
python cli.py system-check
```

Current capabilities:

- Validate required app modules.
- Validate required database tables.
- Validate latest critical reports.
- Validate notification status integrity.
- Validate `.gitignore` protection for local DB, env, virtual environment, and Streamlit secrets.
- Validate that sensitive files are not present in the public website surface.
- Export `reports/system_integrity_YYYY-MM-DD.md`.
- Validate system-check through smoke test.

## Dashboard System Integrity Page v0.1

The private BusinessOS dashboard now includes a System Integrity page.

Current visual capabilities:

- Show latest system-check overall status.
- Show total, passed, warning, and failed check counts.
- List individual integrity checks with status and detail.
- Filter checks by status.
- Keep the dashboard page read-only; refresh the artifact with `python cli.py system-check`.

## Dashboard Delivery Approval Page v0.1

The private BusinessOS dashboard now includes a Delivery Approval page.

Current visual capabilities:

- Show queued notifications, pending delivery approvals, approved delivery approvals, ready-to-deliver count, and blocked notification count.
- Filter delivery approval rows by approval status.
- List notification subject, recipient, notification status, approver, and approval state.
- Keep the dashboard page read-only; refresh approval artifacts with `python cli.py notification-delivery-approval`.

## Dashboard Secure Email Page v0.1

The private BusinessOS dashboard now includes a Secure Email page.

Current visual capabilities:

- Show secure email adapter mode, dry-run status, SMTP configuration status, ready-to-deliver count, and latest failures.
- Show latest secure email delivery report path and delivery outcomes.
- List latest delivery result rows when available.
- Keep the dashboard page read-only; run delivery only through `python cli.py secure-email-delivery`.

## Release Readiness MVP v0.1

BusinessOS can now generate a private demo readiness report.

CLI command:

```bash
python cli.py release-readiness
```

Current capabilities:

- Check system integrity, deployment boundary, dashboard response, landing files, lead intake markers, sensitive file protections, daily close, notifications, scheduled close, dashboard readiness pages, and Git working tree.
- Export `reports/release_readiness_YYYY-MM-DD.md`.
- Report `ready`, `ready_with_warnings`, or `blocked` for controlled demo readiness.

## Private Demo Package MVP v0.1

BusinessOS can now generate a controlled private demo package.

CLI command:

```bash
python cli.py private-demo-package
```

Current capabilities:

- Export `reports/private_demo_package_YYYY-MM-DD.md`.
- Include system summary, release readiness status, demo commands, dashboard pages, recommended demo flow, known risks, and pre-demo checklist.
- Define what is safe to show and what should remain private.
- Keep local artifacts such as `BussinessOS Avance.pdf` outside the package.

## Private Demo Script / Sketch MVP v0.1

BusinessOS now has a guided private demo script.

CLI command:

```bash
python cli.py private-demo-script
```

Current capabilities:

- Export `reports/private_demo_script_YYYY-MM-DD.md`.
- Define demo arc, timeboxes, screen order, and talk track.
- List demo commands and dashboard pages to show.
- Define what not to show during a controlled private demo.
- Include known risks and closing discovery questions.
- Validate the script through smoke test.

## Private Demo Dry Run MVP v0.1

BusinessOS now includes a controlled pre-demo rehearsal gate for private product presentations.

Run:

```bash
python cli.py private-demo-dry-run
```

The dry run validates release readiness, demo package, demo script, required dashboard pages, and private safety boundaries before a presentation. It exports `reports/private_demo_dry_run_YYYY-MM-DD.md` and keeps the demo inside the protected BusinessOS boundary.

## Dashboard Demo Readiness Page v0.1

The private Streamlit dashboard now includes a read-only `Demo Readiness` page.

It reads the latest `reports/private_demo_dry_run_YYYY-MM-DD.md` artifact and shows:

- private demo status
- passed, warning, and failed checks
- generated demo package and script paths
- operator run sequence
- available demo pages

Generate the backing artifact with:

```bash
python cli.py private-demo-dry-run
```

## Private Pilot Intake MVP v0.1

BusinessOS includes a private pilot intake artifact for moving from demo to controlled pilot.

Run:

```bash
python cli.py private-pilot-intake
```

The intake uses release readiness and private demo dry run status to recommend a starting pilot module, list diagnostic questions, define pilot boundaries, and export `reports/private_pilot_intake_YYYY-MM-DD.md`.

## Private Pilot Plan MVP v0.1

BusinessOS can now turn private pilot intake into a 14-day pilot plan.

Run:

```bash
python cli.py private-pilot-plan
```

The plan defines pilot owner, primary workflow, 14-day timeline, daily operating rhythm, success criteria, exit decisions, and protected boundaries. It exports `reports/private_pilot_plan_YYYY-MM-DD.md`.

## Dashboard Pilot Plan Page v0.1

The private dashboard now includes a read-only `Pilot Plan` page.

It reads the latest `reports/private_pilot_plan_YYYY-MM-DD.md` artifact and shows:

- pilot plan status
- pilot owner and primary workflow
- 14-day timeline
- daily operating rhythm
- pilot roles
- success criteria
- exit decisions
- protected boundaries

Generate the backing artifact with:

```bash
python cli.py private-pilot-plan
```

## Private Pilot Daily Tracker MVP v0.1

BusinessOS can now generate a daily pilot tracker for controlled private pilot execution.

Run:

```bash
python cli.py private-pilot-tracker
```

The tracker reads the private pilot plan and current evidence artifacts, classifies the pilot day as `on_track`, `needs_attention`, or `blocked`, lists missing required/optional evidence, and exports `reports/private_pilot_tracker_YYYY-MM-DD.md`.

## Dashboard Pilot Tracker Page v0.1

The private dashboard now includes a read-only `Pilot Tracker` page.

It reads the latest `reports/private_pilot_tracker_YYYY-MM-DD.md` artifact and shows:

- tracker status
- available evidence
- missing required evidence
- missing optional evidence
- daily operator steps
- evidence checklist
- pilot owner and workflow
- next action and operator note

Generate the backing artifact with:

```bash
python cli.py private-pilot-tracker
```

## Private Pilot Exit Decision MVP v0.1

BusinessOS can now generate a controlled exit decision artifact for a private pilot.

Run:

```bash
python cli.py private-pilot-exit-decision
```

The exit decision reads the private pilot tracker, recommends an outcome such as `extend_pilot`, `expand_pilot`, `convert_to_implementation`, `pause_pilot`, or `close_no_fit`, and exports `reports/private_pilot_exit_decision_YYYY-MM-DD.md`. It is advisory only; the executive owner must confirm the final decision.

## Dashboard Pilot Exit Page v0.1

The private dashboard now includes a read-only `Pilot Exit` page.

It reads the latest `reports/private_pilot_exit_decision_YYYY-MM-DD.md` artifact and shows:

- decision status
- recommended exit decision
- highest exit risk
- evidence counts
- decision rationale
- conditions before execution
- evidence summary
- allowed exit options
- operator note

Generate the backing artifact with:

```bash
python cli.py private-pilot-exit-decision
```
