# Approval Config Boundary Implementation v0.1

Date: 2026-05-27

## Status

Closed for MVP validation.

## Purpose

This block implements the first BusinessOS-only approval configuration boundary.

The goal is to move approval constants behind a read-only config accessor while preserving current BusinessOS behavior. This block does not extract approval code, create an OS Core package, create shared database tables, open EduOS implementation, change dashboard approval authority, or change approval runtime outcomes.

## Scope

- Add `app/approvals/config.py`.
- Keep existing approval constants available as compatibility aliases.
- Route approval type validation through config accessors.
- Route priority validation through config accessors.
- Route status validation through config accessors.
- Route demo protected source module lookup through config accessors.
- Keep database schema unchanged.
- Keep approval-report output unchanged.
- Keep notification delivery and pilot expansion approval behavior unchanged.

## Implemented Config Boundary

Current BusinessOS config is now centralized as:

```text
BUSINESSOS_APPROVAL_CONFIG
```

It contains:

```text
branch_id: businessos
statuses: pending, approved, rejected, cancelled
priorities: low, medium, high, critical
active_statuses: pending
protected_source_modules: pilot_expansion
approval_types: decision, access, budget, policy, incident
```

Read-only accessors:

```text
get_approval_config
get_valid_approval_types
get_valid_priorities
get_active_statuses
get_valid_approval_statuses
get_demo_protected_source_modules
```

## Behavior Preservation

Current behavior is preserved:

- valid approval types are unchanged
- valid priorities are unchanged
- valid statuses are unchanged
- active statuses are unchanged
- demo protected source modules are unchanged
- approval request creation behavior is unchanged
- approval status update behavior is unchanged
- duplicate request behavior is unchanged
- audit event behavior is unchanged
- report output remains stable

## Extraction Boundary

This block prepares future extraction work but does not approve it.

Still blocked:

- OS Core package creation
- shared approval schema
- shared database tables
- EduOS approval implementation
- Public AI approval access
- external approval authority
- dashboard approval authority changes

## Future Work

Recommended next steps:

```text
OS Core Approval Contract Test Plan v0.1 (drafted)
Approval Config Boundary Tests v0.1 (implemented)
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
Runtime behavior: behavior_preserved
Approval behavior: config_boundary_implemented
Notification delivery: unchanged
Remote publish: none
Code extraction: blocked
```

## Validation

Validation for this block:

```text
py_compile approvals files
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

This is the first small code step from approval contract doctrine toward a reusable approval boundary. It deliberately keeps BusinessOS as the only runtime owner.
