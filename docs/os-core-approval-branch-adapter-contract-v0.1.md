# OS Core Approval Branch Adapter Contract v0.1

Date: 2026-05-27

## Status

Drafted for architecture validation.

## Purpose

This document defines the first branch adapter contract for future OS Core approvals.

The goal is not to extract `app/approvals`, create an OS Core package, change BusinessOS approval behavior, open EduOS implementation, create shared approval tables, expose approval data publicly, or grant dashboard approval authority. The goal is to define what each branch must own before approval lifecycle code can ever move closer to shared OS Core.

## Contract Identity

```text
contract_name: os_core_approval_branch_adapter
contract_version: v0.1
owning_layer: future branch adapter
source_reference: BusinessOS app/approvals/config.py
current_state: contract_draft_only
extraction_allowed: no
```

## Adapter Purpose

The approval branch adapter owns domain meaning.

It should answer:

```text
Which approval types exist in this branch?
Which source modules can request approvals?
Which source modules are protected from demo automation?
Which roles request and approve each type?
Which evidence is required?
Which action is gated?
Which UI/report labels are branch-specific?
Which public surfaces are denied?
```

OS Core may eventually own lifecycle mechanics. The branch adapter owns the meaning and limits of those mechanics.

## Minimum Adapter Shape

Future branch adapters should define:

```text
branch_id:
approval_types:
  - type_id:
    label:
    description:
    requires_evidence:
    required_evidence:
      - evidence_id:
        freshness_rule:
        sensitivity_level:
    requester_roles:
      - role_id:
    approver_roles:
      - role_id:
    allowed_source_modules:
      - source_module:
    protected_from_demo_actions:
      - source_module:
    action_gate:
      action_id:
      execution_owner:
      approval_required:
      audit_event:
statuses:
priorities:
active_statuses:
dashboard_visibility_rule:
dashboard_authority_rule:
public_ai_denial_rule:
rollback_rule:
```

This shape is not implemented in this block.

## OS Core-Owned Responsibilities

Future OS Core may own:

- approval lifecycle statuses
- priority validation
- request record shape
- source reference deduplication shape
- status update shape
- audit event requirement
- authority rule
- dashboard visibility vs authority separation
- validation hook shape
- rollback rule shape

OS Core must not own:

- BusinessOS approval type meaning
- EduOS academic approval meaning
- branch role labels
- branch source module names
- branch report copy
- branch dashboard labels
- branch evidence sensitivity rules
- branch action execution

## Branch-Owned Responsibilities

Each branch must own:

- approval type registry
- role labels and role authority
- source module registry
- protected source modules
- evidence requirements by type
- sensitivity and visibility rules
- report copy
- dashboard labels
- action execution adapter
- public/private denial rules
- branch-specific validation fixtures

## Current BusinessOS Adapter Draft

Current BusinessOS config already supports:

```text
branch_id: businessos
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
  - decision
  - access
  - budget
  - policy
  - incident
```

Current BusinessOS adapter still needs future detail for:

- per-type labels
- per-type required evidence
- requester roles
- approver roles
- allowed source modules
- action gate identifiers
- sensitivity rules
- dashboard visibility rules
- dashboard authority rules
- Public AI denial checks
- branch-specific validation fixtures

## BusinessOS Type Mapping Draft

Draft only:

```text
decision:
  branch_meaning: executive or operational decision approval
  evidence_required: optional_by_source
  default_approver_role: Executive Owner
  possible_sources:
    - assistance
    - pilot_expansion

access:
  branch_meaning: access or permission approval
  evidence_required: yes
  default_approver_role: Executive Owner
  possible_sources:
    - people
    - security

budget:
  branch_meaning: finance spend or budget exception approval
  evidence_required: yes
  default_approver_role: Finance Manager
  possible_sources:
    - finance
    - operations

policy:
  branch_meaning: governance, notification delivery, or policy approval
  evidence_required: yes
  default_approver_role: Executive Owner
  possible_sources:
    - governance
    - notifications
    - daily_close_distribution

incident:
  branch_meaning: incident response or escalation approval
  evidence_required: yes
  default_approver_role: Executive Owner
  possible_sources:
    - support
    - alerts
```

This mapping is not implemented in runtime.

## Future EduOS Adapter Draft

EduOS may later define, only after approval:

```text
branch_id: eduos
approval_types:
  - academic_policy_exception
  - assessment_change
  - restricted_student_record_access
  - intervention_plan
  - guardian_communication
  - director_acknowledgement
roles:
  - teacher
  - academic_director
  - guardian
  - counselor
  - institution_admin
```

EduOS approval implementation remains blocked.

Do not create:

- EduOS approval runtime
- EduOS database tables
- EduOS dashboard approval pages
- EduOS Public AI approval behavior
- EduOS sample academic records

## Authority Rule

The branch adapter must preserve this rule:

```text
Dashboard visibility is not approval authority.
CLI visibility is not approval authority.
Scheduler execution is not approval authority.
Public AI is never approval authority.
Only an approved approval record can authorize a gated action.
Only the branch action adapter can execute an approved action.
```

## Evidence Rule

The branch adapter must define evidence requirements before action execution.

Default rule:

```text
If evidence is required and missing, the approval may be recorded but the gated action remains blocked.
```

Evidence requirements should reference branch evidence IDs, not private file paths as universal defaults.

## Public AI Boundary

Public AI may:

- explain that approval gates exist
- collect non-sensitive public interest
- route public requests inward

Public AI must not:

- read approval records
- list pending approvals
- infer private approval status
- change approval status
- trigger gated actions
- inspect private evidence
- expose branch approval reports

## Validation Contract

Current BusinessOS validation:

```text
python -m unittest tests.test_approval_config_boundary
python cli.py approval-report
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Future branch adapter validation should add:

- per-type adapter registry tests
- evidence requirement tests
- protected source module tests
- dashboard authority denial tests
- Public AI denial checks
- rollback checks

## Rollback Rule

Until extraction is explicitly approved:

```text
Keep approval config inside BusinessOS.
Keep BusinessOS approval runtime unchanged.
Keep EduOS approval implementation blocked.
Keep OS Core package creation blocked.
```

If future adapter design creates instability, rollback by returning to:

```text
BusinessOS-only approval config
documentation-only branch adapter contract
no shared package
no shared database
no EduOS approval runtime
```

## Current Readiness

```text
approval lifecycle contract readiness: ready
approval config boundary readiness: implemented
approval test boundary readiness: implemented
branch adapter contract readiness: drafted
code extraction readiness: blocked
EduOS approval implementation readiness: blocked
Public AI approval authority: blocked
```

## Recommended Next Blocks

```text
Approval Lifecycle Contract Tests v0.1 (closed)
Public AI Approval Denial Check v0.1
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
Runtime behavior: none_changed
Approval behavior: adapter_contract_only
Notification delivery: unchanged
Remote publish: none
Code extraction: blocked
```

## Validation

Expected validation for this block:

```text
documentation ASCII check
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

This contract makes the branch adapter boundary explicit. It moves approvals closer to platform clarity without moving approvals out of BusinessOS.
