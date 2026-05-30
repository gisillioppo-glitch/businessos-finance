# OS Core Branch Adapter Contract Draft v0.1

Date: 2026-05-29

## Status

Drafted for contract planning.

## Purpose

This block defines the first branch adapter contract for a future OS Core package.

The goal is not to create `os-core`, move code, create an adapter module, open EduOS implementation, create an OS Core repository, or publish shared runtime. The goal is to define the contract that every future branch must satisfy before it can consume shared OS Core behavior.

## Contract Position

```text
BusinessOS: reference branch
EduOS: future consumer, not implemented
OS Core package: not created
Branch adapter contract: drafted
Code extraction: blocked
Repository creation: blocked
Public AI runtime access: blocked
```

OS Core may own reusable operating patterns only after extraction approval.

Branch adapters must own branch meaning.

## Adapter Rule

```text
No adapter, no branch execution.
```

Future OS Core must not run against a branch unless that branch supplies an explicit adapter contract.

The adapter must provide configuration, labels, policies, registries, and validation hooks without leaking private data into public surfaces or forcing branch-specific domain logic into OS Core.

## Required Adapter Sections

Each branch adapter must define:

```text
adapter_name:
adapter_version:
branch_name:
branch_visibility:
branch_owner:
supported_core_families:
role_registry:
access_policy:
page_registry:
approval_policy:
protected_source_policy:
evidence_registry:
governance_rule_pack:
notification_policy:
readiness_check_registry:
runtime_check_registry:
scheduler_job_registry:
command_summary_adapter:
demo_pilot_adapter:
public_boundary_policy:
validation_profile:
rollback_rule:
```

## Required Adapter Families

### Identity and Access

Adapter must define:

- branch roles
- access levels
- private dashboard page visibility
- default role
- blocked public roles
- role-to-capability mapping

Adapter must not:

- treat BusinessOS roles as universal
- expose private dashboard access publicly
- make Public AI a private user

### Dashboard

Adapter must define:

- page registry
- page groups
- role allowlists
- read-only page status
- action-enabled page status

Adapter must not:

- add mutation controls without approval gates
- expose private data to public routes
- assume BusinessOS page names apply to EduOS

### Approvals

Adapter must define:

- approval types
- requester roles
- approver roles
- protected sources
- evidence requirements
- terminal states
- audit event names or mappings

Adapter must not:

- bypass approval gates
- allow demo commands to approve protected requests
- allow Public AI to approve, reject, or cancel requests

### Evidence

Adapter must define:

- evidence item registry
- source artifact rules
- freshness rules
- branch owner roles
- sensitivity levels
- dashboard visibility
- public visibility

Adapter must not:

- expose private evidence publicly
- treat BusinessOS daily close items as universal
- require EduOS academic evidence before EduOS is approved

### Governance

Adapter must define:

- branch rule packs
- sensitivity levels
- privileged role mappings
- protected tables or sources
- escalation labels
- evidence requirements

Adapter must not:

- hard-code BusinessOS finance/operations policy into core
- make EduOS academic policies part of BusinessOS
- allow sensitive actions without approval behavior

### Notifications

Adapter must define:

- recipient registry
- notification templates
- delivery modes
- approval requirements
- dry-run behavior
- failure policy

Adapter must not:

- enable external delivery by default
- expose credentials
- send external messages without approval

### Readiness and Runtime

Adapter must define:

- required modules
- required tables or abstract storage checks
- required reports
- required dashboard pages
- known local artifacts
- smoke profile limits
- runtime warning thresholds

Adapter must not:

- require sensitive data for validation
- publish private readiness as public proof
- assume one branch's report set is universal

### Scheduler

Adapter must define:

- scheduled jobs
- approval requirements for scheduled actions
- observability fields
- retry and failure policy
- disable policy

Adapter must not:

- execute sensitive work without approval
- hide scheduled execution from readiness/runtime checks

### Command Synthesis

Adapter must define:

- branch summary sources
- severity mapping
- next-action synthesis input
- domain labels
- blocked public summaries

Adapter must not:

- make BusinessOS finance health universal
- expose private command center status publicly
- create action authority from summary text

### Demo and Pilot

Adapter must define:

- demo audiences
- demo command list
- demo page list
- pilot intake fields
- pilot evidence requirements
- expansion approval policy

Adapter must not:

- treat demo copy as runtime truth
- approve expansion without approval gates
- publish private pilot evidence publicly

### Public Boundary

Adapter must define:

- public-safe claims
- public artifact allowlist
- private runtime denylist
- public intake schema
- refusal rules

Adapter must not:

- allow Public AI private DB access
- allow Public AI private report access
- allow Public AI CLI command execution
- allow Public AI approval decisions
- allow live private status claims

## BusinessOS Adapter Posture

BusinessOS may later provide an adapter with:

```text
branch_name: BusinessOS
branch_role: reference_branch
domain_owner: business_operations
finance_rules: branch_owned
operations_rules: branch_owned
support_incidents: branch_owned
approval_policy: partially_configured
evidence_registry: partially_configured
readiness_registry: implicit_current_behavior
dashboard_pages: branch_owned
public_boundary: deny_by_default
```

BusinessOS adapter creation is not approved in this block.

## EduOS Adapter Posture

EduOS may later provide an adapter with:

```text
branch_name: EduOS
branch_role: future_consumer
domain_owner: education
academic_models: blocked_until_approved
student_data: blocked
teacher_data: blocked
guardian_data: blocked
assessment_data: blocked
approval_policy: planning_only
evidence_registry: planning_only
dashboard_pages: planning_only
public_boundary: deny_by_default
```

EduOS adapter creation is not approved in this block.

## Minimal Adapter Validation

A future adapter must pass:

```text
adapter schema validation
required registry presence check
private data denylist check
public boundary denylist check
approval gate check
evidence visibility check
readiness registry check
runtime registry check
rollback rule check
branch-specific copy scan
```

## Extraction Gate Impact

This contract satisfies one required planning gate:

```text
Branch adapter contract drafted: yes
```

It does not satisfy:

```text
Adapter implementation: no
OS Core package creation: no
code extraction approval: no
EduOS implementation approval: no
repository creation approval: no
```

## Approved Next Blocks

Recommended sequence:

```text
OS Core Adapter Schema Checklist v0.1 (closed)
OS Core Adapter Schema Validator Plan v0.1 (closed)
OS Core Package Ownership and Repository Decision v0.1
EduOS Skeleton Approval Decision Revisit v0.1
OS Core Adapter Schema Validator Implementation Decision v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: contract_only
Notification delivery: unchanged
Remote publish: blocked
Code extraction: blocked
Adapter implementation: blocked
Contract posture: drafted
```

## Validation

Validation for this block:

```text
documentation ASCII check
system-check
release-readiness
runtime-stability
quick smoke
```

Expected result:

```text
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

This contract is the bridge between a future OS Core package and branch-specific meaning. It keeps the future core reusable by refusing to let any branch's domain become universal by accident.
