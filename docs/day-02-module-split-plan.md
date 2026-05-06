# Day 02 - Module Split Plan

Date: 2026-05-04

## Objective

Plan how to split the current main.py file into clean internal modules without breaking the working BusinessOS Finance Module MVP.

## Current Problem

The current MVP works, but main.py now contains too many responsibilities:

- CSV ingestion.
- Database table creation.
- Transaction insertion.
- Cash flow summary.
- Financial risk rules.
- Recommended action generation.
- Action storage.
- Action status updates.
- Action list view.
- Action KPI summary.
- Daily executive brief.
- Report export.
- Report history.
- Expense anomaly detection.
- Audit logging.
- Application orchestration.

Keeping everything inside main.py is acceptable for the first MVP, but it will become hard to maintain as the system grows.

## Current Working Flow

CSV -> SQLite -> Duplicate Transaction Check -> Cash Flow Summary -> Financial Risk Rules -> Recommended Actions -> Action Storage -> Action Deduplication -> Action Status Update -> Action List View -> Action Summary KPIs -> Daily Executive Brief -> Report Export -> Report History -> Anomaly Detection -> Audit Log

## Proposed Module Structure

```text
app/
  db/
    connection.py
    schema.py

  ingest/
    csv_loader.py

  audit/
    audit_log.py

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

main.py
## Completed Split Block

DB Module Split MVP was completed.

## Moved Into app/db/connection.py

- DB_PATH
- create_connection

## Moved Into app/db/schema.py

- create_transactions_table
- create_audit_logs_table
- create_recommended_actions_table

## Updated main.py

main.py now imports database connection and schema functions from app/db.

## Verified Output After Split

The application still runs successfully and preserves the full workflow:

- CSV ingestion.
- Duplicate transaction check.
- Cash flow summary.
- Financial risk rules.
- Recommended actions.
- Action status update.
- Action list view.
- Action summary KPIs.
- Daily executive brief.
- Report export.
- Report history.
- Anomaly detection.
- Audit logging.

## Why This Matters

The first architecture split was completed without breaking the working MVP. This reduces main.py responsibility and prepares the system for a cleaner production-ready module structure.

## Next Recommended Split

Audit Module Split MVP:

- Move write_audit_log into app/audit/audit_log.py.
- Update imports in main.py.
- Verify python main.py still works.
## Completed Split Block

Ingest Module Split MVP was completed.

## Moved Into app/ingest/csv_loader.py

- create_transaction_hash
- load_csv
- insert_transactions

## Updated main.py

main.py now imports CSV ingestion and transaction insertion from app/ingest/csv_loader.py.

## Verified Output After Split

The application still runs successfully and preserves the full workflow:

- CSV ingestion.
- Duplicate transaction check.
- Cash flow summary.
- Financial risk rules.
- Recommended actions.
- Action status update.
- Action list view.
- Action summary KPIs.
- Daily executive brief.
- Report export.
- Report history.
- Anomaly detection.
- Audit logging.

## Why This Matters

The ingestion logic is now isolated from the orchestration layer. This makes the system easier to maintain, test, and extend with future data sources such as QuickBooks, Xero, bank exports, APIs, and uploaded files.

## Next Recommended Split

Rules Module Split MVP:

- Move cash flow summary into app/rules/cash_flow.py.
- Move financial risk rules into app/rules/financial_risk_rules.py.
- Move anomaly detection into app/rules/anomaly_rules.py.
- Update main.py imports.
- Verify python main.py still works.
## Completed Split Block

Rules Module Split MVP was completed in three safe steps.

## Moved Into app/rules/cash_flow.py

- generate_cash_flow_summary

## Moved Into app/rules/financial_risk_rules.py

- evaluate_financial_risk_rules

## Moved Into app/rules/anomaly_rules.py

- calculate_expense_anomaly_severity
- detect_expense_anomalies

## Updated main.py

main.py now imports financial rule functions from app/rules instead of defining them directly.

## Verified Output After Split

The application still runs successfully and preserves the full workflow:

- Cash flow summary.
- Financial risk rules.
- Recommended actions.
- Action status update.
- Action list view.
- Action summary KPIs.
- Daily executive brief.
- Report export.
- Report history.
- Expense anomaly detection.
- Audit logging.

## Why This Matters

The finance rule logic is now isolated from orchestration. This makes the system easier to test, expand, and adapt to future rule types such as runway, margin compression, vendor risk, revenue concentration, and cash flow forecasting.

## Next Recommended Split

Actions Module Split MVP:

- Move recommended action generation.
- Move action storage.
- Move action status update.
- Move action list view.
- Move action KPI summary.
## Completed Split Block

Actions Module Split MVP was completed in three safe parts.

## Moved Into app/actions/recommended_actions.py

- store_recommended_action
- generate_recommended_actions

## Moved Into app/actions/action_status.py

- update_recommended_action_status
- demo_update_first_open_action

## Moved Into app/actions/action_views.py

- print_recommended_actions_list
- print_action_summary_kpis

## Updated main.py

main.py now imports action generation, action status, and action view functions from app/actions.

## Verified Output After Split

The application still runs successfully and preserves the full workflow:

- Recommended actions.
- Action deduplication.
- Action status update.
- Action list view.
- Action summary KPIs.
- Daily executive brief.
- Report export.
- Report history.
- Anomaly detection.
- Audit logging.

## Why This Matters

Action logic is now isolated from orchestration. This prepares BusinessOS for real task workflows, ownership assignment, status management, escalation rules, dashboards, and future integrations with tools like ClickUp, Notion, Slack, Teams, or internal workflow systems.

## Next Recommended Split

Reports Module Split MVP:

- Move ensure_reports_folder.
- Move print_daily_executive_brief.
- Move export_daily_brief_report.
- Move print_report_history.
## Completed Split Block

Reports Module Split MVP was completed.

## Moved Into app/reports/executive_brief.py

- print_daily_executive_brief

## Moved Into app/reports/report_export.py

- ensure_reports_folder
- export_daily_brief_report

## Moved Into app/reports/report_history.py

- print_report_history

## Updated main.py

main.py now imports reporting functions from app/reports and acts more clearly as an orchestration layer.

## Verified Output After Split

The application still runs successfully and preserves the full workflow:

- Daily executive brief.
- Report export.
- Report history.
- Financial rules.
- Recommended actions.
- Action views.
- Anomaly detection.
- Audit logging.

## Why This Matters

Reporting logic is now isolated from orchestration. This prepares BusinessOS for future email delivery, dashboard integration, report archives, PDF export, and executive notification workflows.

## Current Architecture After Splits

```text
app/
  actions/
  audit/
  db/
  ingest/
  reports/
  rules/

main.py
## Completed Review Block

Architecture Review And Smoke Test was completed.

## Verified Architecture Modules

The BusinessOS Finance Module now uses the following modular structure:

- app/db
- app/audit
- app/ingest
- app/rules
- app/actions
- app/reports

## Verified Smoke Test

Command executed:

python main.py

Result:

BusinessOS Finance Module MVP finished successfully.

## Preserved Workflow

The full workflow still works after modularization:

- CSV ingestion.
- SQLite storage.
- Duplicate transaction check.
- Cash flow summary.
- Financial risk rules.
- Recommended actions.
- Action deduplication.
- Action status update.
- Action list view.
- Action summary KPIs.
- Daily executive brief.
- Report export.
- Report history.
- Expense anomaly detection.
- Audit logging.

## Stable Architecture Baseline

main.py is now primarily an orchestration layer. Core responsibilities have been moved into dedicated modules.

## Next Recommended Block

README Architecture Update:

- Update README.md with current module structure.
- Explain how to run the system.
- Explain current MVP capabilities.
- Document the current architecture baseline for future development.
