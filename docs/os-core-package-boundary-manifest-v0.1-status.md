# OS Core Package Boundary Manifest v0.1

Date: 2026-05-28

## Status

Closed for contract planning.

## Purpose

This block defines the future OS Core package boundary without creating the package, moving code, opening a repository, or implementing EduOS.

The manifest exists so BusinessOS can continue as the stable reference branch while OS Core planning becomes explicit, reviewable, and constrained.

## Package Opening Posture

```text
package_name: os-core
package_status: not_created
planning_status: manifest_drafted
code_extraction: blocked
shared_runtime: blocked
remote_repository: blocked_pending_explicit_approval
BusinessOS_role: reference_branch
EduOS_role: future_consumer_not_implemented
Public_AI_role: denied_private_runtime_access
```

## Future Package Purpose

Future OS Core may own reusable operating primitives that are:

- branch-neutral
- private-by-default
- adapter-driven
- approval-aware
- evidence-aware
- audit-aware
- validation-friendly
- rollback-friendly

Future OS Core must not own branch meaning.

Branch meaning belongs to BusinessOS, EduOS, or another future OS branch through adapters and configuration.

## Allowed Package Families

The following families are allowed for contract planning only.

| Future Package Area | Current Source | Planning Status | Extraction Status |
| --- | --- | --- | --- |
| `os_core.audit` | `app/audit` | allowed | blocked |
| `os_core.identity` | `app/people`, `app/security` | allowed | blocked |
| `os_core.approvals` | `app/approvals` | allowed | blocked |
| `os_core.governance` | `app/governance` | allowed | blocked |
| `os_core.notifications` | `app/notifications` | allowed | blocked |
| `os_core.evidence` | `app/evidence` | allowed | blocked |
| `os_core.readiness` | `app/readiness` | allowed | blocked |
| `os_core.runtime` | `app/system` | allowed | blocked |
| `os_core.scheduler` | `app/scheduler` | allowed | blocked |
| `os_core.dashboard_shell` | `app/dashboard` | planning_only | blocked |
| `os_core.command_synthesis` | `app/command_center` | planning_only | blocked |
| `os_core.demo_pilot` | `app/demo` | planning_only | blocked |

## Branch-Owned Areas

The following remain branch-owned and must not enter OS Core as universal logic:

| Branch Area | Current Source | Owner |
| --- | --- | --- |
| Finance rules | `app/rules`, `app/actions`, `app/ingest` | BusinessOS |
| Business operations tasks | `app/operations` | BusinessOS |
| Business support incidents | `app/support` | BusinessOS |
| Business dashboard pages | `app/dashboard/main.py` page content | BusinessOS |
| Business demo copy | `app/demo` current copy and flow labels | BusinessOS |
| EduOS academic models | future EduOS modules | EduOS, not BusinessOS |
| Public AI copy and intake | public surface / future public assistant | Public surface adapter |

## Required Adapter Boundaries

Future OS Core package code, if ever approved, must require branch adapters for:

```text
roles
page registry
approval types
protected approval sources
evidence item registry
readiness check registry
runtime check registry
notification recipients
notification templates
governance rule packs
scheduler jobs
command center summaries
demo and pilot workflow labels
public-safe copy
```

No adapter, no branch execution.

## Proposed Package Layers

Future package layers should be separated like this:

```text
os_core/
  contracts/
  config/
  audit/
  identity/
  approvals/
  governance/
  notifications/
  evidence/
  readiness/
  runtime/
  scheduler/
  dashboard_shell/
  command_synthesis/
  demo_pilot/
  public_boundary/
```

This folder map is a planning target only. It must not be created as code in this block.

## Contract Requirements Per Family

Each package family must define:

```text
contract_name:
contract_version:
owner:
current_businessos_source:
branch_adapter_required:
input_schema:
output_schema:
private_data_rule:
public_surface_rule:
approval_rule:
audit_rule:
evidence_rule:
configuration_rule:
validation_command:
rollback_rule:
first_consumer:
extraction_status:
```

## Extraction Readiness Rules

A family may move from planning to extraction review only when:

- BusinessOS behavior is validated by targeted tests
- branch adapter boundary is documented
- config defaults are branch-owned
- private data access is denied by default
- Public AI runtime access is denied
- approval-gated actions cannot bypass approvals
- evidence behavior is explicit
- audit behavior is explicit
- rollback restores BusinessOS-only behavior
- future consumer is approved

## Package-Level Blockers

OS Core package creation remains blocked while any are true:

- EduOS implementation scope is not approved
- branch adapter contract is missing
- package ownership is not decided
- repository creation is not explicitly approved
- shared database schema is proposed before contracts
- BusinessOS domain logic is required by shared core
- Public AI requires private runtime access
- dashboard actions can mutate without approval
- scheduler can execute sensitive workflows without approval
- validation cannot run without sensitive data

## Public AI Boundary

Future OS Core may define public/private boundary rules.

Future OS Core must not give Public AI operational authority.

Allowed:

- public route separation doctrine
- public artifact allowlist shape
- public intake schema shape
- refusal and denial policy shape

Blocked:

- private DB access
- private report access
- private dashboard access
- CLI command execution
- approval decisions
- workflow mutation
- notification delivery
- live private status claims

## EduOS Boundary

EduOS remains a future consumer.

This manifest does not approve:

- EduOS repository creation
- EduOS runtime implementation
- EduOS database
- EduOS dashboard
- EduOS adapters
- EduOS approvals
- EduOS notification delivery
- academic data
- Classroom, LMS, or SIS integration

EduOS may use this manifest later to understand which BusinessOS patterns should become branch-neutral contracts.

## Approved Next Blocks

Recommended sequence:

```text
OS Core Branch Adapter Contract Draft v0.1 (drafted)
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
Approval behavior: manifest_only
Notification delivery: unchanged
Remote publish: blocked
Code extraction: blocked
Package creation: blocked
Manifest posture: planning_only
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

This manifest is the boundary line before any package work. It gives OS Core a shape without giving it runtime authority.
