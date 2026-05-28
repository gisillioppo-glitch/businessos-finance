# Approval Lifecycle Contract Tests v0.1

Date: 2026-05-27

## Status

Closed for MVP validation.

## Purpose

This block implements automated tests for the BusinessOS approval lifecycle contract.

The goal is not to change approval runtime behavior, extract code, create an OS Core package, open EduOS implementation, create shared approval tables, expose approval data publicly, or grant dashboard approval authority. The goal is to protect lifecycle behavior beyond config defaults.

## Scope

- Add `tests/test_approval_lifecycle_contract.py`.
- Use standard library `unittest`.
- Use in-memory SQLite fixtures.
- Use temporary report folders for report export checks.
- Avoid production database access.
- Avoid external network calls.
- Avoid EduOS academic data.

## Test Coverage

Implemented tests cover:

- first pending selection by priority
- protected source skip behavior
- demo approve transition
- demo reject transition and justification
- cancelled status summary
- list visibility does not approve
- summary visibility does not approve
- report export does not approve
- status update old/new status contract
- no-pending demo action writes no-op audit

## Test Command

Run:

```bash
python -m unittest tests.test_approval_lifecycle_contract
```

Expected result:

```text
Ran 10 tests
OK
```

## Behavior Preservation

The tests confirm current BusinessOS approval lifecycle behavior remains stable:

- priority order is respected
- protected pilot expansion requests are skipped by demo decisions
- demo approve/reject changes only the selected eligible request
- cancelled status counts in summary
- list, summary, and report visibility do not mutate approval status
- report export writes audit but does not grant authority
- no pending approvals produces no action and writes no-op audit

## Authority Boundary

This block reinforces:

```text
Dashboard visibility is not approval authority.
CLI visibility is not approval authority.
Report export is not approval authority.
Only an explicit status update can change approval state.
```

## Extraction Boundary

This test block improves safety for future OS Core review, but extraction remains blocked.

Still blocked:

- OS Core package creation
- shared approval schema
- shared database tables
- EduOS approval implementation
- Public AI approval access
- external approval authority
- dashboard approval authority changes

## Recommended Next Blocks

```text
Public AI Approval Denial Check v0.1 (closed)
OS Core Package Opening Decision v0.1
EduOS Skeleton Approval Decision Revisit v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: partially
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: tested_behavior_preserved
Approval behavior: lifecycle_contract_tested
Notification delivery: unchanged
Remote publish: none
Code extraction: blocked
```

## Validation

Validation for this block:

```text
python -m py_compile app/approvals/requests.py app/approvals/approval_status.py app/approvals/approval_views.py app/approvals/approval_report.py tests/test_approval_lifecycle_contract.py
python -m unittest tests.test_approval_config_boundary
python -m unittest tests.test_approval_lifecycle_contract
python cli.py approval-report
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected result:

```text
py_compile: passed
approval config tests: passed
approval lifecycle tests: passed
approval-report: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

Approvals now have config tests and lifecycle tests. The next safe move is Public AI denial checking, not extraction.
