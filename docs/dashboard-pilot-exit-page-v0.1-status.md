# Dashboard Pilot Exit Page v0.1

## Product Meaning

This block makes the private pilot exit decision visible in the private dashboard. It gives the executive owner a read-only view of BusinessOS' recommended exit path and the evidence behind it.

## What Changed

- Added `load_private_pilot_exit_decision_status()` to `app/dashboard/main.py`.
- Added `Pilot Exit` to the dashboard navigation.
- Added the page to access control roles.
- Added the page to release readiness dashboard page checks.
- Added the page to the private demo package dashboard page list.
- Updated README documentation.

## Page Behavior

The page reads the latest `reports/private_pilot_exit_decision_YYYY-MM-DD.md` artifact and displays:

- decision status
- recommended decision
- highest exit risk
- available evidence
- missing required evidence
- decision rationale
- conditions before execution
- evidence summary
- allowed exit options
- operator note

The page is read-only. It does not execute the exit decision or mutate pilot state.

## Validation

- `py_compile`
- dashboard loader probe
- `python cli.py release-readiness`
- `python scripts\smoke_test.py`

## Status

Closed as MVP v0.1 after validation, commit, push, and tag.
