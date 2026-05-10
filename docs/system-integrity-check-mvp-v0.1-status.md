# System Integrity Check MVP v0.1

## Product Meaning

The System Integrity Check MVP gives BusinessOS a self-check command for structural readiness.

Instead of relying only on smoke tests, BusinessOS can now inspect whether its core modules, database tables, reports, notification states, and public/private safety boundaries are intact.

## Why It Matters

As BusinessOS grows, it needs a fast way to confirm that the operating system is still healthy before adding production automations such as scheduled daily close, secure email delivery, or dashboard-driven operations.

## Current Capabilities

- Adds `python cli.py system-check`.
- Checks required application modules.
- Checks required SQLite tables.
- Checks latest critical reports.
- Checks notification outbox statuses.
- Checks `.gitignore` protection for local DB, env, venv, and Streamlit secrets.
- Checks that sensitive files are not present in the public website surface.
- Checks Git working tree status and treats local artifacts as non-critical.
- Exports `reports/system_integrity_YYYY-MM-DD.md`.
- Writes audit logs when the check is viewed/exported.
- Adds smoke test coverage.

## Current Safety Boundary

This command is read-only for system state except for exporting its own report and audit log. It does not mutate alerts, approvals, notifications, or operational records.

## Next Step

Future versions can add scoring, dashboard visualization, CI integration, and deployment gates before production releases.
