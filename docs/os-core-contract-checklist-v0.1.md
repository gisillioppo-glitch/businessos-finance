# OS Core Contract Checklist v0.1

Date: 2026-05-25

## Status

Drafted for operating use.

## Purpose

This checklist converts `docs/os-core-extraction-contract-draft-v0.1.md` into a practical review tool.

Use it before extracting, preparing, or proposing any capability as shared OS Core.

This block does not extract code, create an OS Core package, open EduOS implementation, create a remote repository, create shared runtime, or publish any public surface.

## Decision Outcomes

Each review must end with one of these outcomes:

```text
pass_for_contract_design
defer_as_businessos_pattern
defer_until_eduos_approved
block_due_to_public_private_risk
block_due_to_domain_leakage
block_due_to_approval_gap
block_due_to_validation_gap
```

Only `pass_for_contract_design` allows the next step of drafting a detailed contract. It does not allow code extraction.

## Fast Gate

Answer these first:

| Question | Required Answer |
| --- | --- |
| Does it have a branch-neutral purpose? | yes |
| Can BusinessOS domain language be removed? | yes |
| Is branch-specific meaning owned by adapters? | yes |
| Is private data denied by default? | yes |
| Is Public AI operational access blocked? | yes |
| Is approval behavior defined if action is possible? | yes |
| Is validation possible without new sensitive data? | yes |
| Is rollback path clear? | yes |

If any answer is no, do not extract.

## Contract Checklist

For each candidate, fill this:

```text
candidate_name:
source_module:
contract_family:
current_readiness_level:
proposed_outcome:
consumer_branch:
businessos_behavior_validated:
eduos_implementation_required:
public_surface_involved:
private_data_touched:
branch_adapter_required:
approval_required:
audit_required:
evidence_required:
config_required:
validation_command:
rollback_rule:
```

## Required Pass Conditions

A candidate can move toward contract design only when all are true:

- purpose is branch-neutral
- input/output shape can be written without finance-specific terms
- BusinessOS data tables are not required as shared defaults
- branch adapter owns domain labels, statuses, thresholds, and copy
- private data remains inaccessible from public surfaces
- approval gates are explicit for action-producing behavior
- evidence rules exist for institutional conclusions
- audit rules exist for material state changes
- configuration can replace hard-coded branch assumptions
- validation command exists
- rollback can return behavior to BusinessOS-only
- EduOS implementation is not required unless separately approved

## Block Conditions

Block extraction planning when any are true:

- the candidate depends on finance, operations, support, or pilot language as its core meaning
- the candidate requires EduOS academic data before EduOS is approved
- the candidate needs public AI to read private reports or runtime state
- the candidate can mutate workflows without approval
- the candidate sends external delivery without delivery approval
- the candidate needs shared database tables before branch contracts exist
- the candidate has no targeted validation path
- the candidate would make BusinessOS less stable for a speculative platform benefit

## Family Review Prompts

### Audit

- Is the event shape branch-neutral?
- Can event metadata carry domain details without changing the core schema?
- Is append-only behavior preserved?

### Security and People

- Are universal access concepts separate from branch roles?
- Can BusinessOS roles remain branch-owned?
- Is private dashboard access still protected by branch configuration?

### Approvals

- Are requester, approver, state, evidence, and audit rules explicit?
- Can approval types be branch-owned?
- Is dashboard visibility separate from approval authority?

### Governance

- Are policies branch-configurable?
- Can sensitivity levels remain neutral?
- Are BusinessOS rules kept out of shared core?

### Notifications

- Is outbox shape separate from message copy?
- Is delivery adapter behavior behind approval gates?
- Is external delivery off by default?

### Evidence

- Is evidence structure separate from branch evidence content?
- Are freshness, sensitivity, and visibility rules defined?
- Is public exposure denied unless sanitized and allowlisted?

### Readiness and Runtime

- Can checks be registered by branch?
- Is the validation profile branch-neutral?
- Does runtime stability avoid branch-specific claims?

### Scheduler

- Is the job status model generic?
- Are scheduled actions approval-aware?
- Is automatic execution observable and reversible?

### Dashboard and Command Center

- Is shell behavior separate from branch pages?
- Is command synthesis based on neutral summaries?
- Is UI read-only unless approval gates exist?

### Demo and Pilot

- Is methodology separate from BusinessOS sales copy?
- Can pilot rhythms be adapted by branch?
- Are public claims separated from private runtime truth?

## Review Record Template

Use this record in future status docs:

```text
OS Core contract review:
- Candidate:
- Source:
- Family:
- Outcome:
- Reason:
- Blocking conditions:
- Required follow-up:
- Extraction allowed now: no
```

## Current Application

Current BusinessOS modules remain in their branch.

This checklist allows contract review only. It does not allow:

- shared package creation
- code movement
- database migration
- EduOS implementation
- external delivery
- Public AI runtime access
- public publication

## Recommended Next Blocks

```text
OS Core Candidate Contract Review - Approvals v0.1 (closed)
OS Core Approval Contract Draft v0.1 (drafted)
Approval Config Boundary Prep v0.1 (closed)
Approval Config Boundary Implementation v0.1 (closed)
OS Core Approval Contract Test Plan v0.1 (drafted)
Approval Config Boundary Tests v0.1 (closed)
OS Core Candidate Contract Review - Evidence v0.1 (closed)
OS Core Evidence Contract Draft v0.1 (drafted)
Evidence Config Boundary Prep v0.1 (closed)
Evidence Config Boundary Implementation v0.1
EduOS Skeleton Approval Decision Revisit v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: checklist_only
Notification delivery: none
Remote publish: none
Code extraction: blocked
```

## Validation

Expected validation for this block:

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

This checklist is intentionally strict. Passing it means a candidate can be documented more deeply, not extracted. BusinessOS remains the live reference branch until repeated branch patterns prove the shared core.
