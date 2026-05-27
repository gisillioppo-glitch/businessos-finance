# OS Core Approval Contract Draft v0.1

Date: 2026-05-25

## Status

Drafted for architecture validation.

## Purpose

This document defines the first formal approval contract for future OS Core.

The goal is not to extract `app/approvals`, create an OS Core package, change BusinessOS approval behavior, open EduOS implementation, create shared database tables, or grant dashboard approval authority. The goal is to define the branch-neutral approval contract that future shared code would need to satisfy.

## Contract Identity

```text
contract_name: os_core_approval_lifecycle
contract_version: v0.1
owning_layer: future OS Core
source_reference: BusinessOS app/approvals
current_state: contract_draft_only
extraction_allowed: no
```

## Contract Purpose

The approval contract controls gated institutional action.

It should answer:

```text
Who requested action?
Who may approve action?
What action is gated?
What evidence supports the decision?
What status is current?
What audit event proves the lifecycle?
What branch owns the domain meaning?
```

## Branch-Neutral Record Shape

Future approval records should support this neutral shape:

```text
approval_id:
created_at:
title:
description:
approval_type:
priority:
requester_identity:
requester_role:
approver_role:
status:
status_justification:
source_module:
source_reference_id:
evidence_reference:
branch_id:
branch_context:
```

Current BusinessOS supports most of this shape, except:

- `evidence_reference`
- `branch_id`
- `branch_context`
- configurable role/type registry

These are future contract fields, not current migration requirements.

## Allowed Lifecycle

Minimum lifecycle:

```text
pending
approved
rejected
cancelled
```

Rules:

- new requests start as `pending`
- only valid statuses are accepted
- status changes require audit
- status changes may include justification
- branch adapters may display branch-specific copy
- branch adapters may not invent unregistered statuses

## Priority Contract

Minimum priority set:

```text
low
medium
high
critical
```

Rules:

- priority controls review ordering
- priority does not grant approval authority
- branch adapters may map domain urgency into this set
- branch adapters may not use priority to bypass required evidence

## Approval Type Contract

OS Core should not hard-code BusinessOS approval types as universal.

Shared core should support a branch registry:

```text
branch_id:
approval_types:
  - type_id:
    label:
    requires_evidence:
    required_approver_role:
    allowed_source_modules:
    action_gate:
```

BusinessOS may register:

- decision
- access
- budget
- policy
- incident
- pilot expansion
- notification delivery

Future EduOS may later register, only after approval:

- academic policy exception
- assessment change
- restricted student record access
- intervention plan
- guardian communication
- director acknowledgement

## Request Creation Contract

Request creation must:

- validate registered approval type
- validate priority
- normalize requester identity where appropriate
- record requester role
- record approver role
- record source module
- record source reference
- create audit event
- avoid duplicate active request creation for the same source reference

Duplicate behavior:

```text
If a matching request exists, return existing request and audit duplicate skip.
```

## Status Update Contract

Status update must:

- validate requested status
- require existing approval id
- preserve old status in audit metadata
- record new status
- record justification where provided
- create audit event
- return status transition summary

Status update must not:

- execute the gated action directly
- bypass branch evidence rules
- bypass branch approver rules
- expose private approval records publicly

## Approval Authority Contract

The authority rule is:

```text
Only an approved approval record can authorize a gated action.
```

Non-authorities:

- dashboard display
- CLI list/report output
- scheduler job visibility
- Public AI
- report generation
- notification outbox visibility
- pilot recommendation
- demo script wording

These surfaces may show or prepare approval context. They do not approve.

## Evidence Contract

Action-producing approval types should define evidence requirements.

Each branch approval type should specify:

```text
evidence_required:
evidence_source:
freshness_rule:
sensitivity_level:
dashboard_visibility:
public_visibility:
```

Default rule:

```text
If evidence is required and missing, approval may be requested but gated action remains blocked.
```

## Audit Contract

Required audit events:

```text
approval_request_created
approval_request_duplicate_skipped
approval_request_status_updated
```

Optional branch events:

```text
approval_request_viewed
approval_summary_viewed
approval_report_exported
approval_gate_checked
```

Audit metadata should include:

- approval id
- title
- approval type
- priority
- requester role
- approver role
- source module
- source reference id
- old status, when relevant
- new status, when relevant
- justification, when relevant

## Branch Adapter Boundary

OS Core may own:

- lifecycle statuses
- priority ordering
- request creation shape
- duplicate prevention shape
- status update shape
- audit event requirement
- authority rule
- dashboard visibility vs authority separation

Branch adapters must own:

- approval type registry
- branch roles
- source module registry
- evidence requirements
- report copy
- dashboard labels
- gated action execution
- branch-specific risk language

## BusinessOS Adapter Responsibilities

BusinessOS remains responsible for:

- finance approvals
- operations approvals
- support incident approvals
- pilot expansion approvals
- notification delivery approvals
- executive owner language
- BusinessOS report copy
- current SQLite table ownership
- current dashboard page behavior

## Future EduOS Adapter Responsibilities

EduOS may later define:

- academic approval types
- teacher/director/guardian role labels
- assessment and student-record evidence rules
- school-specific dashboard labels
- academic policy sensitivity

EduOS approval implementation is not opened by this contract.

## Public AI Boundary

Public AI may:

- explain that approval gates exist
- collect non-sensitive public interest
- route public requests inward

Public AI must not:

- read approval tables
- list approval requests
- change approval status
- approve, reject, or cancel requests
- trigger gated actions
- inspect private evidence
- expose private reports

## Validation Contract

Current BusinessOS validation:

```text
python cli.py approval-report
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Future contract validation should add targeted checks for:

- valid statuses
- invalid status rejection
- valid priorities
- invalid priority rejection
- duplicate source reference behavior
- audit on create
- audit on status update
- protected source module behavior
- dashboard read-only authority boundary
- Public AI denial boundary

## Rollback Rule

Until extraction is explicitly approved:

```text
Keep approval code inside BusinessOS.
Keep BusinessOS table ownership unchanged.
Keep EduOS approval implementation blocked.
Keep OS Core package creation blocked.
```

If future contract design creates instability, rollback by returning to:

```text
BusinessOS-only approval lifecycle
documentation-only OS Core approval contract
no shared package
no shared database
```

## Current Readiness

```text
BusinessOS approval lifecycle maturity: high
OS Core contract design readiness: ready
Approval config boundary readiness: next
Code extraction readiness: blocked
EduOS approval implementation readiness: blocked
Public AI approval authority: blocked
```

## Recommended Next Blocks

```text
Approval Config Boundary Prep v0.1 (closed)
Approval Config Boundary Implementation v0.1 (closed)
OS Core Approval Contract Test Plan v0.1 (drafted)
Approval Config Boundary Tests v0.1 (closed)
OS Core Candidate Contract Review - Evidence v0.1 (closed)
OS Core Approval Extraction Readiness Review v0.1 (closed)
OS Core Approval Branch Adapter Contract v0.1 (drafted)
Approval Lifecycle Contract Tests v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: partially
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none_changed
Approval behavior: contract_only
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

This contract gives approvals a reusable institutional shape without moving authority out of BusinessOS. The right next move is configuration boundary preparation, not extraction.
