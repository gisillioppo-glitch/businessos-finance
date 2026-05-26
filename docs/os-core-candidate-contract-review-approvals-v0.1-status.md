# OS Core Candidate Contract Review - Approvals v0.1

Date: 2026-05-25

## Status

Closed for architecture validation.

## Purpose

This block applies `docs/os-core-contract-checklist-v0.1.md` to the current BusinessOS approval layer.

The goal is not to extract approval code, create an OS Core package, change approval behavior, open EduOS implementation, create shared database tables, or change dashboard approval authority. The goal is to decide whether approvals can move from general OS Core candidate into detailed contract design.

## Candidate

```text
candidate_name: approvals
source_module: app/approvals
contract_family: approval_lifecycle
current_readiness_level: L2
proposed_outcome: pass_for_contract_design
consumer_branch: future EduOS, after approval
businessos_behavior_validated: yes
eduos_implementation_required: no
public_surface_involved: no
private_data_touched: yes
branch_adapter_required: yes
approval_required: yes
audit_required: yes
evidence_required: yes for action-producing approvals
config_required: yes
validation_command: python cli.py approval-report
rollback_rule: keep approvals BusinessOS-only
```

## Review Outcome

```text
Outcome: pass_for_contract_design
Extraction allowed now: no
```

Approvals pass the checklist for detailed contract design because the current BusinessOS layer already has a reusable approval lifecycle shape:

- request creation
- deduplication by source reference
- pending, approved, rejected, cancelled statuses
- requester and approver role fields
- approval type and priority
- source module and source reference linkage
- status justification
- audit log on creation
- audit log on status update
- reporting and dashboard visibility patterns

Approvals do not pass for code extraction yet because branch configuration is not complete.

## Fast Gate

| Question | Result | Notes |
| --- | --- | --- |
| Branch-neutral purpose | pass | Approval-gated institutional action is reusable. |
| BusinessOS language removable | pass_with_work | Defaults and reports still include business/demo wording. |
| Branch-specific meaning adapter-owned | partial | Approval types and protected source modules are still code-level constants. |
| Private data denied by default | pass | No public surface is involved. |
| Public AI operational access blocked | pass | Public AI has no approval authority. |
| Approval behavior defined | pass | Lifecycle and state changes exist. |
| Validation without new sensitive data | pass | Existing CLI/report checks validate behavior. |
| Rollback path clear | pass | Keep approval code inside BusinessOS. |

## Contract Strengths

Current strengths:

- `approval_requests` table has a clear lifecycle record.
- `create_approval_request` validates type and priority.
- duplicate request creation is skipped and audited.
- status updates validate allowed statuses.
- status updates are audited.
- report output summarizes queue state and risk.
- demo approval commands avoid protected pilot expansion requests.
- notification delivery and pilot expansion already use approval requests as gates.

## Contract Gaps

The following gaps block extraction:

- approval types are hard-coded in `VALID_APPROVAL_TYPES`
- priority values are hard-coded in `VALID_PRIORITIES`
- protected demo source modules are hard-coded in `DEMO_PROTECTED_SOURCE_MODULES`
- role labels are branch text, not branch configuration
- report copy is still BusinessOS-oriented
- database table name is BusinessOS runtime specific
- evidence requirements are implied by source modules, not contract-defined
- dashboard approval authority is not represented as a contract rule
- validation exists through CLI/smoke, but not as approval-contract tests

## Required Contract Design

Before approvals can move toward shared OS Core, define:

```text
approval_contract_name:
approval_contract_version:
allowed_statuses:
allowed_priorities:
branch_approval_types:
branch_role_labels:
protected_source_modules:
source_reference_schema:
request_creation_audit_event:
status_update_audit_event:
evidence_requirements_by_type:
dashboard_visibility_rule:
dashboard_authority_rule:
public_ai_denial_rule:
validation_profile:
rollback_rule:
```

## Branch Adapter Boundary

Shared OS Core should own:

- lifecycle statuses
- request creation shape
- request deduplication shape
- status update shape
- audit event requirement
- approval authority rule
- dashboard visibility vs authority separation

BusinessOS should own:

- finance, operations, support, pilot, and delivery approval types
- executive-owner wording
- business role labels
- pilot expansion source modules
- notification delivery business copy
- BusinessOS report language

Future EduOS should own only after approval:

- academic policy exception approval types
- assessment or grade change approval types
- guardian/director acknowledgement language
- school role labels
- academic evidence requirements

## Approval Authority Rule

The future contract should preserve this rule:

```text
Dashboard visibility is not approval authority.
CLI visibility is not approval authority.
Scheduler execution is not approval authority.
Public AI is never approval authority.
Only an approved approval record can authorize a gated action.
```

## Recommended Follow-Up

```text
OS Core Approval Contract Draft v0.1
OS Core Candidate Contract Review - Evidence v0.1
Approval Config Boundary Prep v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: partially
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none_new
Runtime behavior: none_changed
Approval behavior: review_only
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

This review is a platform maturity step, not a refactor. The approval layer is strong enough to draft a formal OS Core contract, but not ready to leave BusinessOS.
