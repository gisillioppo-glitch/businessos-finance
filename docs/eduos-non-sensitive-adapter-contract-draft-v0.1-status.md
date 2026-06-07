# EduOS Non-Sensitive Adapter Contract Draft v0.1

Date: 2026-06-06

## Status

Drafted for adapter contract design.

## Purpose

This block drafts the EduOS non-sensitive adapter contract for future OS Core comparison.

The goal is not to implement an EduOS adapter, create EduOS runtime, create an EduOS repository, create an EduOS database, create an EduOS dashboard, introduce academic data, connect Classroom/LMS/SIS systems, create an `os-core` package, create a repository, move BusinessOS code, or allow Public AI private runtime access. The goal is to define what EduOS may describe as a branch-owned adapter contract while remaining non-sensitive and planning-only.

## Contract Position

```text
EduOS: future consumer
EduOS skeleton: local_only_ready
EduOS adapter contract: drafted
EduOS adapter implementation: blocked
EduOS runtime: blocked
EduOS repository creation: blocked
EduOS database: blocked
EduOS dashboard: blocked
academic data: blocked
Classroom_LMS_SIS_integration: blocked
OS Core package: not created
OS Core repository: not created
Public AI private runtime access: blocked
```

EduOS may be described for contract comparison.

EduOS may not run.

## Contract Decision Source

This contract is allowed by:

```text
docs/adapter-schema-validator-adapter-contract-decision-v0.1-status.md
```

That decision allows adapter contract drafting only.

It does not allow EduOS implementation or runtime.

## Adapter Identity

Future EduOS adapter identity:

```text
adapter_name: eduos_non_sensitive
adapter_version: 0.1
branch_name: EduOS
branch_id: eduos
branch_visibility: private_future_branch
branch_owner: operator
branch_role: future_consumer
branch_mode: local_only_skeleton
domain_owner: education
validation_profile: planning
rollback_rule: local_only_skeleton_no_runtime
runtime_authority: none
implementation_authority: none
```

## Supported Core Families

EduOS may describe these families for contract design:

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
public_boundary
```

Each family remains conceptual and non-sensitive until separate implementation approval.

## Root Field Contract

A future EduOS non-sensitive adapter schema must include:

| Field | Required | Contract Rule |
| --- | --- | --- |
| `adapter_name` | yes | Must be `eduos_non_sensitive` unless explicitly versioned later. |
| `adapter_version` | yes | Must be explicit and reviewable. |
| `branch_name` | yes | Must identify EduOS as a future branch, not BusinessOS or universal core. |
| `branch_id` | yes | Must be stable and branch-owned. |
| `branch_visibility` | yes | Must remain private future branch. |
| `branch_owner` | yes | Must identify responsible operator or owner role. |
| `branch_mode` | yes | Must remain `local_only_skeleton` until implementation approval. |
| `supported_core_families` | yes | Must be explicit, no implicit enablement. |
| `validation_profile` | yes | Must run without academic records or secrets. |
| `rollback_rule` | yes | Must return to local-only skeleton with no runtime. |

## Role Registry Contract

EduOS owns its conceptual academic roles.

Required role registry posture:

```text
conceptual_roles:
  - administrator
  - teacher
  - guardian
  - student
  - counselor
  - support_specialist
public_roles: none
private_access_enforcement: blocked_until_runtime_approval
public_dashboard_access: denied
```

Contract rules:

- roles remain conceptual
- role enforcement is not implemented
- Public AI is not a private EduOS user
- student, guardian, and teacher visibility rules require future sensitive implementation approval
- academic roles must not become universal OS Core roles

## Page Registry Contract

EduOS dashboard pages remain conceptual.

Required page posture:

```text
conceptual_pages:
  - Academic Command Center
  - Academic Close
  - Academic Evidence
  - Guardian Communications
  - Student Support
  - Readiness
dashboard_runtime: blocked
page_labels: eduos_owned
mutation_default: disabled
public_page_access: denied
```

The adapter may describe page concepts and visibility.

It must not create dashboard files, routes, Streamlit pages, UI controls, mutations, or shared OS Core UI behavior.

## Approval Policy Contract

EduOS approval policy remains planning-only.

Required approval posture:

```text
conceptual_approval_domains:
  - assessment_release
  - guardian_communication
  - intervention_review
  - policy_exception
approval_execution: blocked
approval_mutation: blocked
public_approval_authority: denied
```

Contract rules:

- sensitive academic actions require future approval gates
- approval execution is not implemented
- Public AI cannot approve, reject, cancel, or mutate approvals
- no real student, teacher, guardian, grade, attendance, assessment, or intervention records may be required

## Protected Source Policy Contract

EduOS protected sources remain conceptual.

Protected source candidates:

```text
academic_governance
guardian_communications
student_support
assessment_review
intervention_review
policy_exception
```

Contract rules:

- protected sources require future approval policy
- protected source labels remain EduOS-owned
- protected source handling must not become universal OS Core logic
- no protected source may reference real academic records in this stage

## Evidence Registry Contract

EduOS evidence remains conceptual and non-sensitive.

Required evidence posture:

```text
conceptual_evidence_domains:
  - academic_close
  - assessment_review
  - support_case
  - intervention_plan
  - guardian_communication
  - governance_finding
evidence_contents: blocked
raw_records: denied
public_evidence_access: denied
private_report_embedding_in_schema: denied
```

Contract rules:

- adapter may name evidence domains
- adapter must not include raw evidence contents
- adapter must not require academic records
- public exposure requires future allowlisted sanitized copy only

## Notification Policy Contract

EduOS notification behavior remains blocked or queue-only in planning.

Required notification posture:

```text
conceptual_modes:
  - queue_only
  - approval_required
delivery_execution: blocked
guardian_delivery: blocked
credentials_in_schema: denied
public_delivery_authority: denied
```

Contract rules:

- guardian communication delivery requires future approval
- external delivery cannot be enabled by default
- notification templates remain EduOS-owned
- Public AI cannot trigger delivery

## Readiness Contract

EduOS readiness checks must prove non-sensitive posture.

Required readiness posture:

```text
skeleton_scope_check: required
boundary_docs_check: required
non_sensitive_config_check: required
no_academic_data_check: required
no_adapters_check: required
no_runtime_check: required
no_repository_creation_check: required
```

Contract rules:

- readiness checks must not require academic records
- readiness may only evaluate docs/config/no-op skeleton posture
- public surfaces cannot claim live EduOS runtime readiness

## Runtime Contract

EduOS runtime remains blocked.

Required runtime posture:

```text
runtime_status: blocked
database_status: blocked
dashboard_status: blocked
adapter_status: blocked
public_ai_private_access: denied
```

Contract rules:

- adapter validation does not execute EduOS workflows
- runtime checks remain conceptual inputs only
- runtime authority remains none

## Scheduler Contract

EduOS scheduled work remains conceptual.

Required scheduler posture:

```text
conceptual_jobs:
  - academic_close_future
scheduler_execution: blocked
sensitive_scheduled_actions: approval_required_before_future_execution
public_scheduler_execution: denied
```

Contract rules:

- scheduled academic work cannot run
- scheduler jobs may be named only as future concepts
- Public AI cannot trigger scheduler jobs

## Governance Rule Pack Contract

EduOS governance rules remain planning-only.

Required governance posture:

```text
conceptual_rules:
  - sensitivity_required
  - role_visibility_required
  - public_private_deny_by_default
student_privacy_policy: planning_only
assessment_sensitivity_policy: planning_only
guardian_communication_policy: planning_only
```

Contract rules:

- governance severity mapping must be explicit in future implementation
- academic governance labels remain EduOS-owned
- no BusinessOS governance labels become EduOS runtime behavior

## Command Summary Adapter Contract

EduOS command synthesis remains conceptual and advisory.

Required command posture:

```text
conceptual_sources:
  - academic_health
  - support_need
  - governance_risk
  - evidence_completeness
next_action_authority: advisory_only
workflow_mutation_from_summary: denied
public_command_center_access: denied
```

Contract rules:

- command center concepts cannot execute actions
- summaries cannot create authority
- Public AI cannot claim live private EduOS command status

## Public Boundary Contract

EduOS public boundary is deny-by-default.

Required public boundary posture:

```text
public_student_data_access: denied
public_teacher_data_access: denied
public_guardian_data_access: denied
public_grade_access: denied
public_attendance_access: denied
public_assessment_content_access: denied
public_private_report_access: denied
public_cli_execution: denied
public_workflow_mutation: denied
public_guardian_delivery: denied
public_live_private_status_claims: denied
public_intake_handoff: sanitized_only
```

Public AI remains outside private EduOS runtime authority.

## Explicitly Blocked Data

The EduOS contract must not require or include:

- student names
- student records
- teacher records
- guardian records
- rosters
- attendance
- grades
- assessment content
- intervention details
- academic evidence contents
- raw LMS exports
- raw SIS exports
- Classroom credentials
- LMS credentials
- SIS credentials
- tokens
- private files
- BusinessOS private reports
- BusinessOS database paths
- runtime commands
- dashboard mutations
- notification delivery instructions

## Validation Contract

A future EduOS non-sensitive adapter contract should validate with:

```text
python cli.py adapter-schema-check --schema config/adapters/eduos.adapter.schema.json
python cli.py adapter-schema-fixture-run
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

The EduOS schema path is a future target.

No schema file is created in this block.

## Rollback Contract

Rollback rule:

```text
local_only_skeleton_no_runtime
```

Rollback must mean:

- no EduOS adapter execution
- no EduOS runtime
- no EduOS database
- no EduOS dashboard
- no EduOS repository creation
- no academic records
- no Classroom/LMS/SIS integration
- no Public AI private runtime access
- skeleton remains local-only and non-sensitive

## Explicitly Blocked

Still blocked:

```text
EduOS adapter implementation
EduOS adapter runtime execution
EduOS schema file creation
EduOS repository creation
EduOS runtime
EduOS database
EduOS dashboard
EduOS approvals
EduOS notification delivery
academic data
Classroom/LMS/SIS integration
OS Core package creation
OS Core repository creation
BusinessOS code extraction
Public AI private runtime access
```

## Extraction Gate Impact

This block satisfies:

```text
EduOS non-sensitive adapter contract drafted: yes
EduOS conceptual branch-owned labels identified: yes
EduOS public/private denial contract drafted: yes
EduOS validation contract drafted: yes
academic data remains blocked: yes
```

It does not satisfy:

```text
EduOS adapter implementation: no
EduOS schema file creation: no
EduOS runtime implementation approval: no
EduOS repository creation: no
OS Core package creation: no
OS Core repository creation: no
BusinessOS code extraction: no
Public AI runtime approval: no
```

## Recommended Next Blocks

Recommended sequence:

```text
Adapter Contract Cross-Branch Comparison v0.1 (closed)
BusinessOS Reference Adapter Schema File Decision v0.1
EduOS Non-Sensitive Adapter Schema File Decision v0.1
Adapter Schema File Cross-Validation Plan v0.1
```

Adapter execution, OS Core packaging, EduOS runtime, and Public AI private runtime access remain separate and blocked.

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: contract_draft_only
Notification delivery: blocked
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema file creation: blocked
Academic data: blocked
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

This contract gives EduOS a comparable adapter shape without opening EduOS. It is useful because it lets BusinessOS and EduOS be compared at the OS Core boundary while keeping all sensitive academic implementation blocked.
