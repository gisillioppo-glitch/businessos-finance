# OS Core Extraction Contract Draft v0.1

Date: 2026-05-25

## Status

Drafted for architecture validation.

## Purpose

This document defines the first contract rules for future OS Core extraction.

The goal is not to move code out of BusinessOS, create an `os-core` package, open EduOS implementation, create a shared runtime, or publish public surfaces. The goal is to define what must be true before any BusinessOS capability can become shared OS Core.

## Contract Position

BusinessOS remains the live reference branch.

EduOS remains local-only and not implemented.

OS Core remains a future shared layer.

This contract sits between:

- `docs/institutional-core-extraction-map-v0.1.md`
- `docs/os-core-boundary-checklist-v0.1.md`
- `docs/os-platform-map-v0.1.md`
- future OS Core package work

## Extraction Rule

No capability should be extracted into shared OS Core until it satisfies all of these:

- branch-neutral purpose
- branch-neutral input contract
- branch-neutral output contract
- branch-owned domain adapter boundary
- private-by-default access rule
- explicit approval behavior, if action can occur
- evidence and audit behavior defined
- public/private boundary defined
- configuration path defined
- validation path defined
- rollback path defined
- at least one future consumer identified

If any item is unclear, the capability stays inside BusinessOS as a named pattern.

## Contract Families

| Family | Current Source | Contract Shape | Extraction State |
| --- | --- | --- | --- |
| Audit | `app/audit` | append-only event contract | draft_only |
| Security | `app/security` | branch-aware access contract | draft_only |
| People | `app/people` | institutional identity contract | draft_only |
| Approvals | `app/approvals` | approval lifecycle contract | draft_only |
| Governance | `app/governance` | policy and sensitivity contract | draft_only |
| Notifications | `app/notifications` | outbox and delivery gate contract | draft_only |
| Evidence | `app/evidence` | evidence packet contract | draft_only |
| Readiness | `app/readiness` | validation checkpoint contract | draft_only |
| Runtime/System | `app/system` | integrity and runtime health contract | draft_only |
| Scheduler | `app/scheduler` | controlled recurring job contract | draft_only |
| Dashboard shell | `app/dashboard` | protected read-only surface contract | draft_only |
| Command synthesis | `app/command_center` | branch summary synthesis contract | draft_only |
| Demo/Pilot | `app/demo` | adoption methodology contract | draft_only |
| Domain adapters | branch modules | branch-owned domain contract | branch_owned |
| Public AI | external/public surface | deny-by-default public contract | blocked |

## Branch-Neutral Contract Requirements

Every future OS Core candidate should define:

```text
contract_name:
contract_version:
owning_layer:
consumer_branches:
input_schema:
output_schema:
branch_adapter_required:
private_data_touched:
public_surface_touched:
approval_required:
audit_required:
evidence_required:
configuration_required:
validation_command:
rollback_rule:
```

The contract must not include:

- finance-only terminology
- BusinessOS-only role names as universal roles
- EduOS academic data before EduOS implementation is approved
- private file paths as platform defaults
- database table names as shared requirements unless abstracted
- public claims based on private runtime state
- delivery behavior without approval gates

## Branch Adapter Boundary

Shared OS Core should own the operating pattern.

Branch adapters should own domain meaning.

Examples:

| Shared Pattern | BusinessOS Adapter Owns | Future EduOS Adapter Would Own |
| --- | --- | --- |
| approval lifecycle | finance, pilot, delivery approval types | academic, guardian, assessment approval types |
| evidence packet | daily close, finance evidence, pilot evidence | course, progress, assessment evidence |
| governance policy | sensitivity rules for business operations | student privacy and academic policy rules |
| notification outbox | executive and operational notification copy | teacher, guardian, academic notification copy |
| command synthesis | enterprise operating health | academic operating health |
| readiness checks | demo/pilot/release checks | school/pilot/readiness checks |

The shared contract can define shape and control. It should not define branch meaning.

## Approval Contract

Any extracted capability that can trigger action must define:

- who can request action
- who can approve action
- what states are allowed
- what evidence is required before approval
- what audit event is created
- what happens if approval is missing
- what cannot be bypassed by dashboard, CLI, scheduler, Public AI, or adapter code

Default rule:

```text
No approval, no action.
```

## Evidence Contract

Any extracted capability that produces institutional conclusions must define:

- source artifact
- freshness rule
- branch owner
- sensitivity level
- retention expectation
- dashboard visibility
- export visibility
- public visibility

Default rule:

```text
Private evidence remains private unless explicitly sanitized and allowlisted.
```

## Public AI Contract

Public AI is not OS Core runtime.

Public AI may explain, qualify, and route.

Public AI must not:

- read private branch databases
- read private reports
- execute branch commands
- approve decisions
- mutate workflows
- trigger delivery
- expose private dashboards
- claim live private status as public truth

Default rule:

```text
Public AI routes interest inward; it does not operate the private OS.
```

## Extraction Gates

Before any code extraction:

1. Contract documented.
2. Boundary classification documented.
3. BusinessOS source behavior validated.
4. Future branch consumer named.
5. Domain adapter boundary documented.
6. Sensitive data denied by default.
7. Approval behavior documented.
8. Evidence behavior documented.
9. Audit behavior documented.
10. Config shape drafted.
11. Validation command identified.
12. Rollback plan identified.

If the future consumer is EduOS, EduOS implementation approval must exist first.

## Prohibited Moves

Do not:

- move BusinessOS finance logic into OS Core
- move EduOS academic assumptions into BusinessOS
- create shared database tables before branch contracts are approved
- create an OS Core package before extraction gates pass
- create Public AI access to private runtime
- treat dashboard display as approval authority
- treat scheduler execution as approval authority
- create external delivery without secure approval gates
- publish private branch status as public proof

## Current Readiness Assessment

```text
Contract doctrine: drafted
Shared code extraction: not_started
BusinessOS reference stability: high
EduOS implementation approval: not_granted
Public AI operational authority: blocked
OS Core package creation: blocked
```

## Recommended Next Blocks

```text
OS Core Contract Checklist v0.1 (drafted)
OS Core Candidate Contract Review - Approvals v0.1
EduOS Skeleton Approval Decision Revisit v0.1
OS Core Package Opening Decision v0.1
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

This contract is intentionally conservative. It keeps BusinessOS moving while preventing premature platform extraction, accidental EduOS implementation, or public/private boundary drift.
