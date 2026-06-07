# BusinessOS Reference Adapter Contract Draft v0.1

Date: 2026-06-06

## Status

Drafted for adapter contract design.

## Purpose

This block drafts the BusinessOS reference adapter contract for future OS Core comparison.

The goal is not to implement an adapter, create an `os-core` package, create a repository, move BusinessOS code, change runtime behavior, expose private reports, create shared imports, open EduOS runtime, or allow Public AI private runtime access. The goal is to define what BusinessOS would have to provide as a branch-owned adapter contract before any shared core could consume BusinessOS behavior.

## Contract Position

```text
BusinessOS: reference branch
BusinessOS adapter contract: drafted
BusinessOS adapter implementation: blocked
BusinessOS code extraction: blocked
OS Core package: not created
OS Core repository: not created
EduOS runtime: blocked
Public AI private runtime access: blocked
```

BusinessOS is the reference branch.

BusinessOS is not the universal core.

## Contract Decision Source

This contract is allowed by:

```text
docs/adapter-schema-validator-adapter-contract-decision-v0.1-status.md
```

That decision allows adapter contract drafting only.

It does not allow runtime adapter implementation.

## Adapter Identity

Future BusinessOS adapter identity:

```text
adapter_name: businessos_reference
adapter_version: 0.1
branch_name: BusinessOS
branch_id: businessos
branch_visibility: private
branch_owner: operator
branch_role: reference_branch
domain_owner: business_operations
validation_profile: planning
rollback_rule: branch_only_businessos_runtime
runtime_authority: none
implementation_authority: none
```

## Supported Core Families

BusinessOS may describe these families for contract design:

```text
identity
dashboard
approvals
evidence
readiness
runtime
scheduler
notifications
governance
command_center
demo_pilot
public_boundary
```

Each family remains design-only until separate implementation approval.

## Root Field Contract

A future BusinessOS adapter schema must include:

| Field | Required | Contract Rule |
| --- | --- | --- |
| `adapter_name` | yes | Must be `businessos_reference` unless explicitly versioned later. |
| `adapter_version` | yes | Must be explicit and reviewable. |
| `branch_name` | yes | Must identify BusinessOS as a branch, not universal core. |
| `branch_id` | yes | Must be stable and branch-owned. |
| `branch_visibility` | yes | Must remain private. |
| `branch_owner` | yes | Must identify responsible operator or owner role. |
| `supported_core_families` | yes | Must be explicit, no implicit enablement. |
| `validation_profile` | yes | Must run without private data rows or secrets. |
| `rollback_rule` | yes | Must return to branch-only BusinessOS runtime. |

## Role Registry Contract

BusinessOS owns its roles.

Required role registry posture:

```text
roles: admin, executive, viewer
public_roles: none
default_private_role: viewer
private_dashboard_access: role_bound
public_dashboard_access: denied
```

Contract rules:

- roles remain BusinessOS-owned
- Public AI is not a private user
- private dashboard access is denied by default
- role meanings must not become universal OS Core meanings

## Page Registry Contract

BusinessOS owns dashboard pages and page labels.

Required page posture:

```text
dashboard_surface: private
page_labels: branch_owned
mutation_default: disabled
action_pages: approval_gated_or_read_only
public_page_access: denied
```

The adapter may describe page groups and visibility.

It must not implement dashboard routing, page rendering, mutation controls, or shared OS Core UI behavior.

## Approval Policy Contract

BusinessOS approval policy must remain explicit and branch-owned.

Required approval posture:

```text
approval_statuses: pending, approved, rejected, cancelled
approval_priorities: low, medium, high, critical
protected_source_modules: pilot_expansion, notification_delivery, sensitive_assistance, privileged_access
action_authority_without_approval: denied
public_approval_authority: denied
```

Contract rules:

- approval-producing flows must be approval-aware
- protected sources cannot bypass approval gates
- demo and pilot commands cannot approve protected requests
- Public AI cannot approve, reject, cancel, or mutate approvals

## Protected Source Policy Contract

BusinessOS protected sources must remain branch-owned.

Protected source candidates:

```text
pilot_expansion
notification_delivery
secure_email_delivery
sensitive_assistance_request
privileged_access
overdue_sensitive_operation
```

Contract rules:

- protected sources require explicit approval policy
- protected source labels remain BusinessOS-owned
- protected source handling must not become universal OS Core logic

## Evidence Registry Contract

BusinessOS evidence remains private, report-backed, and branch-owned.

Required evidence posture:

```text
evidence_sources:
  - Command Center
  - Executive Alerts
  - Approval Decisions
  - Governance Brief
  - Support Brief
  - Daily Finance Brief
distribution_mode: email_ready_queue
public_evidence_access: denied
private_report_embedding_in_schema: denied
```

Contract rules:

- adapter may name evidence categories
- adapter must not embed private report contents
- evidence visibility must be explicit
- public exposure requires allowlisted sanitized copy only

## Notification Policy Contract

BusinessOS notifications remain queued or approval-gated.

Required notification posture:

```text
delivery_default: queued
external_delivery_default: disabled_or_approval_gated
credentials_in_schema: denied
public_delivery_authority: denied
```

Contract rules:

- notification recipients remain branch-owned
- templates remain branch-owned
- external delivery cannot be enabled by default
- Public AI cannot trigger delivery

## Readiness Contract

BusinessOS readiness checks remain BusinessOS-local.

Required readiness posture:

```text
system_check: required
release_readiness: required
dashboard_response_check: required
area_review_freshness: required
boundary_classification_coverage: required
git_working_tree_policy: clean_except_known_local_artifacts
```

Contract rules:

- readiness checks must not require private data rows
- readiness reports must remain private
- public surfaces cannot claim live private readiness unless explicitly allowlisted and sanitized

## Runtime Contract

BusinessOS runtime stability remains branch-local.

Required runtime posture:

```text
runtime_stability: required
quick_smoke: required
standard_smoke_limit: explicit
full_smoke_reserved_for_deep_checkpoints: yes
heavy_pilot_commands_default: blocked_from_standard_profile
```

Contract rules:

- adapter validation does not execute runtime workflows
- runtime checks remain evidence inputs only
- runtime authority remains blocked

## Scheduler Contract

BusinessOS scheduled work must remain observable and non-public.

Required scheduler posture:

```text
scheduled_daily_close: observable
scheduled_execution_visibility: required
sensitive_scheduled_actions: approval_aware
public_scheduler_execution: denied
```

Contract rules:

- scheduler jobs must be observable
- scheduled sensitive work requires approval-aware posture
- Public AI cannot trigger scheduler jobs

## Governance Rule Pack Contract

BusinessOS governance rules remain branch-owned.

Required governance posture:

```text
sensitivity_rules: branch_owned
approval_required_findings: supported
privileged_access_findings: supported
public_private_boundary_findings: supported
finance_or_operations_policy_as_core: denied
```

Contract rules:

- governance severity mapping must be explicit
- protected sources must be explicit
- BusinessOS governance labels must not become universal core labels

## Command Summary Adapter Contract

BusinessOS command synthesis remains summary-only.

Required command posture:

```text
summary_sources: reports_and_status_artifacts
next_action_authority: advisory_only
workflow_mutation_from_summary: denied
public_command_center_access: denied
```

Contract rules:

- command center can summarize branch status
- summaries cannot create action authority
- Public AI cannot claim live private command status

## Demo and Pilot Adapter Contract

BusinessOS demo and pilot methodology remains branch-owned.

Required demo/pilot posture:

```text
demo_copy: branch_owned
pilot_methodology: branch_owned
pilot_expansion: approval_gated
demo_command_authority: read_only_or_evidence_only
public_pilot_evidence_access: denied
```

Contract rules:

- demo copy is not runtime truth
- pilot expansion cannot be approved by advisory output
- private pilot evidence remains private

## Public Boundary Contract

BusinessOS public boundary is deny-by-default.

Required public boundary posture:

```text
public_db_access: denied
public_report_access: denied
public_cli_execution: denied
public_approval_mutation: denied
public_notification_delivery: denied
public_scheduler_execution: denied
public_live_private_status_claims: denied
public_intake_handoff: sanitized_only
```

Public AI remains outside private runtime authority.

## Validation Contract

A future BusinessOS reference adapter contract should validate with:

```text
python cli.py adapter-schema-check --schema config/adapters/businessos.adapter.schema.json
python cli.py adapter-schema-fixture-run
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

The BusinessOS schema path is a future target.

No schema file is created in this block.

## Rollback Contract

Rollback rule:

```text
branch_only_businessos_runtime
```

Rollback must mean:

- no adapter execution
- no shared OS Core import
- no package dependency
- no public runtime access
- BusinessOS continues using current branch-local modules
- reports and dashboard remain private

## Explicitly Blocked

Still blocked:

```text
BusinessOS adapter implementation
BusinessOS adapter runtime execution
BusinessOS code extraction
OS Core package creation
OS Core repository creation
shared database schema
shared dashboard runtime
shared scheduler runtime
shared notification delivery
EduOS runtime
EduOS repository creation
academic data
Classroom/LMS/SIS integration
Public AI private runtime access
```

## Extraction Gate Impact

This block satisfies:

```text
BusinessOS reference adapter contract drafted: yes
BusinessOS branch-owned labels identified: yes
BusinessOS public/private denial contract drafted: yes
BusinessOS validation contract drafted: yes
```

It does not satisfy:

```text
BusinessOS adapter implementation: no
BusinessOS schema file creation: no
BusinessOS code extraction: no
OS Core package creation: no
OS Core repository creation: no
EduOS runtime implementation approval: no
Public AI runtime approval: no
```

## Recommended Next Blocks

Recommended sequence:

```text
EduOS Non-Sensitive Adapter Contract Draft v0.1
Adapter Contract Cross-Branch Comparison v0.1
BusinessOS Reference Adapter Schema File Decision v0.1
```

Adapter execution, OS Core packaging, EduOS runtime, and Public AI private runtime access remain separate and blocked.

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: yes
EduOS-specific: no
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: contract_draft_only
Notification delivery: unchanged
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema file creation: blocked
Implementation authority: none
Runtime authority: none
```

## Validation

Validation for this block:

```text
documentation ASCII check
python cli.py adapter-schema-fixture-run
py_compile
unittest tests.test_adapter_schema_validator
unittest tests.test_adapter_schema_cli
system-check
release-readiness
runtime-stability
quick smoke
```

Expected result:

```text
adapter-schema-fixture-run: passed
unittest: passed
py_compile: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

This contract protects BusinessOS from being mistaken for OS Core. BusinessOS can teach the platform pattern, but its finance, operations, support, demo, pilot, and executive language remain branch-owned.
