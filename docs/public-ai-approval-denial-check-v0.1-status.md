# Public AI Approval Denial Check v0.1

Date: 2026-05-27

## Status

Closed for MVP validation.

## Purpose

This block adds an explicit approval denial check to the public/private surface audit.

The goal is not to create Public AI, expose approvals publicly, change approval runtime behavior, extract OS Core code, open EduOS implementation, create public routes, or mutate approval data. The goal is to ensure the public surface cannot reference private approval runtime paths, commands, reports, tables, or audit events.

## Scope

- Add `public_ai_approval_denial` to `app/security/surface_audit.py`.
- Block precise private approval runtime references under `public/`.
- Allow safe public concept copy such as "approval gates".
- Add `tests/test_public_ai_approval_denial.py`.
- Keep landing behavior unchanged.
- Keep dashboard and approval runtime unchanged.

## Blocked Public References

The denial check blocks:

```text
approval_requests
app/approvals
app\approvals
approval-report
approval-approve
approval-reject
approval_decisions_
approval_request_status_updated
approval_request_created
```

These are private runtime/table/command/report/audit references, not public product copy.

## Public AI Boundary

Public AI may:

- explain that approval gates exist
- collect non-sensitive public interest
- route public requests inward

Public AI must not:

- read approval tables
- reference approval runtime modules
- expose approval reports
- call approval CLI commands
- reveal approval audit events
- approve, reject, or cancel requests
- infer private approval state

## Behavior Preservation

Preserved behavior:

- public landing remains static
- lead intake remains static client-side MVP behavior
- approval runtime remains private
- dashboard behavior is unchanged
- `public-private-surface-audit` still exports its report
- publish checklist benefits from the stricter surface audit

## Extraction Boundary

This check strengthens the Public AI denial boundary, but extraction remains blocked.

Still blocked:

- Public AI runtime
- approval public routes
- approval data exposure
- OS Core package creation
- EduOS approval implementation
- shared approval tables

## Recommended Next Blocks

```text
OS Core Package Opening Decision v0.1
EduOS Skeleton Approval Decision Revisit v0.1
Public AI Boundary Contract Tests v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: partially
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: public_surface_guard_added
Approval behavior: public_denial_checked
Notification delivery: unchanged
Remote publish: none
Code extraction: blocked
```

## Validation

Validation for this block:

```text
python -m py_compile app/security/surface_audit.py tests/test_public_ai_approval_denial.py
python -m unittest tests.test_public_ai_approval_denial
python cli.py public-private-surface-audit
python cli.py public-surface-publish-checklist
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected result:

```text
py_compile: passed
public AI approval denial tests: passed
public-private-surface-audit: surface_ready
public-surface-publish-checklist: safe
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

Public AI approval denial is now enforced at the static public surface audit layer. This keeps approval authority private even if future public AI copy or intake grows.
