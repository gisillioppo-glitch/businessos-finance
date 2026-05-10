# System Integrity Check

Date: 2026-05-10

## Integrity Summary

Overall status: warning  
Total checks: 50
Passed checks: 49
Warning checks: 1  
Failed checks: 0  

## Checks

| Check | Status | Detail |
| --- | --- | --- |
| Repository root | passed | C:\Users\fabia\OneDrive\Escritorio\businessos-finance-module |
| Database file | passed | C:\Users\fabia\OneDrive\Escritorio\businessos-finance-module\finance.db |
| Reports folder | passed | C:\Users\fabia\OneDrive\Escritorio\businessos-finance-module\reports |
| Module: actions | passed | app\actions |
| Module: alerts | passed | app\alerts |
| Module: approvals | passed | app\approvals |
| Module: assistance | passed | app\assistance |
| Module: audit | passed | app\audit |
| Module: command_center | passed | app\command_center |
| Module: dashboard | passed | app\dashboard |
| Module: db | passed | app\db |
| Module: evidence | passed | app\evidence |
| Module: governance | passed | app\governance |
| Module: notifications | passed | app\notifications |
| Module: operations | passed | app\operations |
| Module: people | passed | app\people |
| Module: reports | passed | app\reports |
| Module: rules | passed | app\rules |
| Module: scheduler | passed | app\scheduler |
| Module: security | passed | app\security |
| Module: support | passed | app\support |
| Database table: audit_logs | passed | present |
| Database table: transactions | passed | present |
| Database table: recommended_actions | passed | present |
| Database table: operations_tasks | passed | present |
| Database table: support_incidents | passed | present |
| Database table: business_users | passed | present |
| Database table: assistance_requests | passed | present |
| Database table: approval_requests | passed | present |
| Database table: notification_outbox | passed | present |
| Database table: scheduled_daily_close | passed | present |
| Latest report: daily_brief | passed | reports\daily_brief_2026-05-10.md |
| Latest report: governance_brief | passed | reports\governance_brief_2026-05-10.md |
| Latest report: support_brief | passed | reports\support_brief_2026-05-10.md |
| Latest report: command_center | passed | reports\command_center_2026-05-10.md |
| Latest report: approval_decisions | passed | reports\approval_decisions_2026-05-10.md |
| Latest report: executive_alerts | passed | reports\executive_alerts_2026-05-10.md |
| Latest report: executive_evidence_index | passed | reports\executive_evidence_index_2026-05-10.md |
| Latest report: daily_close | passed | reports\daily_close_2026-05-10.md |
| Latest report: daily_close_distribution | passed | reports\daily_close_distribution_2026-05-10.md |
| Gitignore protects: finance.db | passed | protected |
| Gitignore protects: .env | passed | protected |
| Gitignore protects: .venv/ | passed | protected |
| Gitignore protects: .streamlit/secrets.toml | passed | protected |
| Public secret boundary: public/finance.db | passed | not present |
| Public secret boundary: public/.env | passed | not present |
| Public secret boundary: public/secrets.toml | passed | not present |
| Public secret boundary: public/.streamlit/secrets.toml | passed | not present |
| Notification statuses | passed | valid |
| Git working tree | warning | M README.md; M app/dashboard/main.py; M app/security/access_control.py; M reports/system_integrity_2026-05-10.md; ?? docs/dashboard-scheduled-close-page-v0.1-status.md |
