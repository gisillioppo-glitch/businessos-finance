# Dashboard Demo Readiness Page v0.1

## Product meaning

This block adds a read-only private dashboard page for demo readiness. It turns the CLI dry run into an operator-facing screen so BusinessOS can be checked visually before a private presentation.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared private demo readiness candidate
- Private data touched: sanitized only
- Public surface touched: no
- Approval required: no
- Evidence generated: report only
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats private demo readiness pattern

## Why it matters

A private demo should not depend only on terminal output. Leaders and operators need a simple readiness view that shows whether the package, script, dry run, required pages, and safety boundaries are in place before presenting the system.

## Current capabilities

- Adds `Demo Readiness` to the private dashboard navigation.
- Reads the latest `reports/private_demo_dry_run_YYYY-MM-DD.md`.
- Shows KPIs for status, passed checks, warnings, failures, and run sequence size.
- Lists dry-run checks with filtering by status.
- Shows package/script/report evidence paths.
- Shows the operator run sequence and available demo pages.
- Keeps the page read-only; generation still happens through `python cli.py private-demo-dry-run`.

## Safety boundary

The page does not expose database internals, credentials, secrets, or local private files. It only surfaces the prepared demo readiness artifacts.

## Next step

Use this page before private demos. Later, it can become part of a broader presenter mode or private pilot onboarding flow.
