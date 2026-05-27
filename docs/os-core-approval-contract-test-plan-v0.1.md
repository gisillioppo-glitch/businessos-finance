# OS Core Approval Contract Test Plan v0.1

Date: 2026-05-27

## Status

Drafted for QA planning.

## Purpose

This document defines the approval contract test plan that should protect the BusinessOS approval layer before any further config work, extraction planning, or future OS Core package discussion.

The goal is not to implement tests in this block, change runtime behavior, extract code, create an OS Core package, open EduOS implementation, create shared database tables, or alter dashboard approval authority. The goal is to define the test coverage required to keep approval behavior stable.

## Test Plan Position

This plan follows:

- `docs/os-core-approval-contract-draft-v0.1.md`
- `docs/approval-config-boundary-prep-v0.1-status.md`
- `docs/approval-config-boundary-implementation-v0.1-status.md`

It prepares:

- `Approval Config Boundary Tests v0.1`
- future approval contract tests
- future extraction readiness review

## Required Test Groups

### Config Boundary Tests

Required checks:

- `get_approval_config` returns `branch_id` as `businessos`
- `get_valid_approval_types` returns `decision`, `access`, `budget`, `policy`, `incident`
- `get_valid_priorities` returns `low`, `medium`, `high`, `critical`
- `get_valid_approval_statuses` returns `pending`, `approved`, `rejected`, `cancelled`
- `get_active_statuses` returns `pending`
- `get_demo_protected_source_modules` returns `pilot_expansion`
- config values are read-only
- compatibility aliases still match config values

### Request Creation Tests

Required checks:

- valid approval request can be created
- invalid approval type raises `ValueError`
- invalid priority raises `ValueError`
- requester email is normalized
- created request starts as `pending`
- duplicate request returns existing id
- duplicate request reports `was_created` as false
- duplicate skip writes audit event
- request creation writes audit event

### Status Update Tests

Required checks:

- pending approval can move to `approved`
- pending approval can move to `rejected`
- pending approval can move to `cancelled`
- invalid status raises `ValueError`
- missing approval id raises `ValueError`
- status update preserves old status in result
- status update records justification
- status update writes audit event

### Protected Source Tests

Required checks:

- demo approve does not select `pilot_expansion` source requests
- demo reject does not select `pilot_expansion` source requests
- protected source module list comes from config accessor
- non-protected pending requests remain eligible for demo commands

### Report Stability Tests

Required checks:

- `python cli.py approval-report` exits successfully
- approval summary contains pending, approved, rejected, cancelled counts
- approval report exports `reports/approval_decisions_YYYY-MM-DD.md`
- current approval KPIs remain stable for the sample DB unless fixtures change intentionally

### Authority Boundary Tests

Required checks:

- approval list/report does not execute gated action
- dashboard visibility does not approve requests
- scheduler visibility does not approve requests
- notification outbox visibility does not send delivery
- pilot expansion recommendation does not approve expansion

These may start as documentation checks if runtime hooks are not yet isolated.

### Public AI Denial Tests

Required checks:

- no public route reads `approval_requests`
- no public route changes approval status
- no public route exposes private approval report content
- public landing remains separate from approval runtime

These may start as system/public-boundary checks.

## Minimum Test Implementation Order

Recommended order:

1. Config boundary unit tests.
2. Request creation unit tests with temporary SQLite connection.
3. Status update unit tests with temporary SQLite connection.
4. Protected source behavior tests.
5. Approval report command smoke.
6. Authority boundary documentation checks.
7. Public AI denial checks.

## Test Data Rules

Tests should use:

- temporary in-memory SQLite where possible
- current schema creation helpers
- non-sensitive sample approvals
- BusinessOS local roles only
- no EduOS academic data
- no real external delivery
- no public/private cross-access

Tests must not use:

- production credentials
- external SMTP
- private customer data
- real student records
- GitHub/API network calls
- public AI calls

## Validation Commands

Current validation before test implementation:

```text
python -m py_compile app/approvals/config.py app/approvals/requests.py app/approvals/approval_status.py
python cli.py approval-report
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Future validation after tests exist:

```text
python -m pytest tests/test_approval_config_boundary.py
python -m pytest tests/test_approval_lifecycle_contract.py
python cli.py approval-report
python scripts/smoke_test.py quick
```

## Exit Criteria For Future Test Block

`Approval Config Boundary Tests v0.1` should be complete when:

- config accessors are directly tested
- valid and invalid approval types are tested
- valid and invalid priorities are tested
- valid and invalid statuses are tested
- protected source behavior is tested
- duplicate request behavior is tested
- audit event creation is tested
- approval-report still passes
- quick smoke still passes

## Extraction Impact

This test plan improves extraction readiness by defining the safety net around:

- config defaults
- branch-specific meaning
- lifecycle behavior
- audit behavior
- approval authority
- public/private denial

It does not approve extraction.

## Recommended Next Blocks

```text
Approval Config Boundary Tests v0.1
OS Core Candidate Contract Review - Evidence v0.1
OS Core Approval Extraction Readiness Review v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: partially
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: test_plan_only
Notification delivery: none
Remote publish: none
Code extraction: blocked
```

## Validation

Expected validation for this block:

```text
documentation ASCII check
python cli.py approval-report
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected result:

```text
approval-report: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

The next code block should be tests, not more approval behavior changes. The approval boundary is now important enough to guard before we continue reshaping it.
