# Approval Config Boundary Tests v0.1

Date: 2026-05-27

## Status

Closed for MVP validation.

## Purpose

This block implements the first automated tests for the BusinessOS approval config boundary.

The goal is to protect the approval configuration and lifecycle behavior introduced by `Approval Config Boundary Implementation v0.1`. This block does not change approval runtime behavior, extract code, create an OS Core package, open EduOS implementation, create shared database tables, or change dashboard approval authority.

## Scope

- Add `tests/test_approval_config_boundary.py`.
- Use standard library `unittest` to avoid adding new dependencies.
- Use in-memory SQLite fixtures.
- Create only the audit and approval tables needed by the tests.
- Avoid production database access.
- Avoid external network calls.
- Avoid EduOS academic data.

## Test Coverage

Implemented tests cover:

- approval config accessors
- read-only config behavior
- compatibility aliases
- valid request creation
- invalid approval type rejection
- invalid priority rejection
- duplicate request handling
- audit event creation
- valid status update
- invalid status rejection
- missing approval id rejection
- protected `pilot_expansion` source behavior

## Test Command

Run:

```bash
python -m unittest tests.test_approval_config_boundary
```

Result:

```text
Ran 11 tests
OK
```

## Behavior Preservation

The tests confirm the current BusinessOS approval boundary remains stable:

- default approval types stay unchanged
- priorities stay unchanged
- statuses stay unchanged
- protected source modules stay unchanged
- duplicate request behavior stays unchanged
- audit behavior stays present
- protected pilot expansion requests are not selected for demo approval decisions

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
OS Core Candidate Contract Review - Evidence v0.1
OS Core Approval Extraction Readiness Review v0.1 (closed)
Approval Lifecycle Contract Tests v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: partially
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: tested_behavior_preserved
Approval behavior: config_boundary_tested
Notification delivery: unchanged
Remote publish: none
Code extraction: blocked
```

## Validation

Validation for this block:

```text
python -m py_compile app/approvals/config.py app/approvals/requests.py app/approvals/approval_status.py tests/test_approval_config_boundary.py
python -m unittest tests.test_approval_config_boundary
python cli.py approval-report
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected result:

```text
approval tests: passed
approval-report: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

Approvals now have both a config boundary and a test boundary. The next architectural move can safely shift to another OS Core candidate, especially evidence.
