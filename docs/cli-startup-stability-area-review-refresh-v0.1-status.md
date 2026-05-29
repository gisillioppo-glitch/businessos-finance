# CLI Startup Stability and Area Review Refresh v0.1

Date: 2026-05-28

## Status

Closed for opening validation.

## Purpose

This block keeps BusinessOS opening checks responsive when optional finance data tooling is slow to import.

The opening check found that `python cli.py health` and other non-finance commands were blocked by eager imports that eventually reached `pandas`. The fix keeps the CLI lightweight at startup and moves finance-heavy imports to the commands that actually need them.

## Scope

- Make `main.py` import lazy inside `run_main()`.
- Make Finance area review import lazy inside `run_finance_area_review()`.
- Make area review bundle import lazy inside `run_area_review_bundle()`.
- Replace pandas usage in cash flow summary with direct SQLite aggregation.
- Replace pandas usage in financial risk category aggregation with direct SQLite queries.
- Refresh 2026-05-28 area review reports and index.

## Behavior Preserved

- `python cli.py run` still routes to the Finance MVP runner.
- `python cli.py daily-close` still routes through the Finance run step.
- Area review outputs keep the same review fields and report names.
- Financial risk rules keep the same thresholds and risk messages.
- No database schema changed.
- No Public AI runtime was created.
- No EduOS implementation was opened.

## Opening Issue Found

```text
python cli.py health: timed out
python cli.py system-check: failed because area_review_index was stale
root cause: eager CLI imports reached pandas before command dispatch
```

## Resolution

```text
CLI import: responsive
health: responsive
finance-area-review: responsive
area-review-bundle: responsive
area review freshness: 2026-05-28
```

## Validation

Validation for this block:

```text
python -m py_compile cli.py app/rules/cash_flow.py app/rules/financial_risk_rules.py
python -c "import cli"
python cli.py health
python cli.py finance-area-review
python cli.py area-review-bundle
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected result:

```text
py_compile: passed
cli import: passed
health: passed
finance-area-review: passed
area-review-bundle: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Boundary Classification

```text
OS Core candidate: partially
BusinessOS-specific: yes
EduOS-specific: no
Public AI boundary: unchanged
Sensitive data exposure: none
Runtime behavior: cli_startup_stabilized
Approval behavior: unchanged
Notification delivery: unchanged
Remote publish: none
Code extraction: blocked
```

## Operator Note

This is a stability refresh, not a product expansion. It protects daily checks and opening routines while keeping finance-heavy execution inside explicit finance commands.
