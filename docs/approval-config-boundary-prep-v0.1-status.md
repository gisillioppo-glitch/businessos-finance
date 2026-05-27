# Approval Config Boundary Prep v0.1

Date: 2026-05-25

## Status

Closed for architecture validation.

## Purpose

This block prepares the configuration boundary for the BusinessOS approval layer.

The goal is not to change approval runtime behavior, extract code, create an OS Core package, open EduOS implementation, create shared database tables, or introduce a new configuration loader. The goal is to identify which approval constants and branch-specific meanings must become configurable before approvals can move toward shared OS Core.

## Current Hard-Coded Approval Inputs

Current BusinessOS approval constants:

```text
VALID_APPROVAL_TYPES = decision, access, budget, policy, incident
VALID_PRIORITIES = low, medium, high, critical
ACTIVE_STATUSES = pending
VALID_APPROVAL_STATUSES = pending, approved, rejected, cancelled
DEMO_PROTECTED_SOURCE_MODULES = pilot_expansion
```

Current BusinessOS branch-owned values also include:

- Executive Owner role wording
- Operations Manager role wording
- Support Manager role wording
- notification delivery source context
- pilot expansion source context
- BusinessOS report copy
- BusinessOS dashboard labels

## Config Boundary Decision

Approvals should move toward config boundary before extraction.

Decision:

```text
approval lifecycle statuses: future OS Core default
approval priorities: future OS Core default
approval types: branch config
protected source modules: branch config
role labels: branch config
evidence requirements: branch config
dashboard labels: branch config
report copy: branch config
gated action execution: branch adapter
```

## Proposed Future Config Shape

Future branch config may use a shape like:

```text
branch_id: businessos
approval:
  statuses:
    - pending
    - approved
    - rejected
    - cancelled
  priorities:
    - low
    - medium
    - high
    - critical
  active_statuses:
    - pending
  protected_source_modules:
    - pilot_expansion
  approval_types:
    - type_id: decision
      label: Decision
      requires_evidence: false
      default_approver_role: Executive Owner
      allowed_source_modules:
        - assistance
        - pilot_expansion
    - type_id: policy
      label: Policy
      requires_evidence: true
      default_approver_role: Executive Owner
      allowed_source_modules:
        - notifications
```

This shape is not implemented in this block.

## Migration Order

Future safe order:

1. Document config shape.
2. Add BusinessOS-only config module or file.
3. Keep current constants as compatibility defaults.
4. Add read-only config accessor.
5. Add targeted tests for defaults.
6. Move validation lookups behind config accessor.
7. Move protected source module lookups behind config accessor.
8. Keep database schema unchanged.
9. Keep dashboard behavior unchanged.
10. Validate with approval-report, system-check, release-readiness, runtime-stability, and quick smoke.

## Do Not Move Yet

Do not move these in the next code block without explicit approval:

- approval database schema
- approval status update behavior
- demo approval commands
- dashboard approval pages
- notification delivery approval behavior
- pilot expansion approval behavior
- EduOS approval analogs
- OS Core shared package

## Required Future Tests

Future config boundary tests should prove:

- default BusinessOS approval types remain accepted
- invalid approval types remain rejected
- default BusinessOS priorities remain accepted
- invalid priorities remain rejected
- default statuses remain accepted
- invalid statuses remain rejected
- protected source modules remain protected
- duplicate source reference behavior is unchanged
- audit events are unchanged
- approval-report output remains stable

## Extraction Impact

This prep reduces extraction risk by separating:

- OS Core lifecycle mechanics
- BusinessOS approval meaning
- future EduOS approval meaning
- Public AI denial boundary

It does not make extraction ready yet.

## Current Readiness

```text
approval contract readiness: drafted
config boundary readiness: prepared
runtime config implementation: not_started
code extraction readiness: blocked
EduOS approval implementation: blocked
Public AI approval authority: blocked
```

## Recommended Next Blocks

```text
Approval Config Boundary Implementation v0.1 (closed)
OS Core Approval Contract Test Plan v0.1
OS Core Candidate Contract Review - Evidence v0.1
Approval Config Boundary Tests v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: partially
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none_changed
Approval behavior: config_boundary_prep_only
Notification delivery: none
Remote publish: none
Code extraction: blocked
```

## Validation

Expected validation for this block:

```text
documentation ASCII check
python cli.py approval-report
system-check
release-readiness
runtime-stability
quick smoke
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

This block prepares the next engineering move. The next safe implementation would add a BusinessOS-only approval config boundary while keeping current behavior exactly the same.
