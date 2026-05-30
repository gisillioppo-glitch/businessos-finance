# OS Core Adapter Schema Validator Plan v0.1

Date: 2026-05-29

## Status

Closed for validator planning.

## Purpose

This block defines how a future OS Core adapter schema validator should behave before any validator code is created.

The goal is not to implement `python cli.py adapter-schema-check`, create an `os-core` package, move BusinessOS code, create a new repository, open EduOS runtime, or allow Public AI private runtime access. The goal is to make the future validator reviewable before it becomes executable.

## Validator Position

```text
BusinessOS: reference branch
EduOS: local-only skeleton and future consumer
OS Core package: not created
Branch adapter contract: drafted
Adapter schema checklist: closed
Adapter schema validator plan: closed
Adapter schema validator implementation: blocked
Adapter implementation: blocked
Code extraction: blocked
Repository creation: blocked
Public AI runtime access: blocked
```

## Future Command Shape

The future validator may eventually be exposed as:

```text
python cli.py adapter-schema-check
```

Optional future profiles may include:

```text
python cli.py adapter-schema-check --adapter businessos
python cli.py adapter-schema-check --adapter eduos
python cli.py adapter-schema-check --profile planning
python cli.py adapter-schema-check --profile release
```

These commands are planning targets only. They are not created in this block.

## Validator Inputs

The future validator should read only non-sensitive adapter configuration.

Allowed future inputs:

| Input | Required | Rule |
| --- | --- | --- |
| adapter schema file | yes | Non-sensitive config only. |
| branch label | yes | Branch-owned and explicit. |
| supported families | yes | No implicit enablement. |
| registry definitions | yes | Required per supported family. |
| public boundary policy | yes | Deny-by-default required. |
| rollback rule | yes | Must return to branch-only behavior. |
| validation profile | yes | Must run without sensitive data. |

Blocked future inputs:

- private database contents
- private reports
- credentials
- Streamlit secrets
- academic records
- student, teacher, guardian, grade, attendance, or assessment data
- live dashboard session data
- external delivery credentials
- Public AI runtime state

## Validation Phases

The future validator should run in deterministic phases:

| Phase | Purpose | Failure Type |
| --- | --- | --- |
| `load_schema` | Read non-sensitive schema input. | block |
| `root_field_check` | Confirm required root fields. | block |
| `family_registry_check` | Confirm registries for supported families. | block |
| `public_boundary_check` | Confirm private runtime denial. | block |
| `approval_gate_check` | Confirm action families are approval-aware. | block |
| `evidence_visibility_check` | Confirm visibility and sensitivity rules. | block |
| `runtime_validation_check` | Confirm validation can run without sensitive data. | block |
| `domain_leakage_check` | Confirm branch labels remain adapter-owned. | block |
| `rollback_check` | Confirm branch-only fallback. | block |
| `report_export` | Export non-sensitive validator report. | warning or pass |

## Required Result Model

The future validator should return a structured result:

```text
adapter_name:
adapter_version:
branch_name:
validation_profile:
overall_status:
total_checks:
passed_checks:
warning_checks:
failed_checks:
blocking_reasons:
warnings:
report_path:
```

Allowed future `overall_status` values:

```text
adapter_schema_valid_for_design
adapter_schema_valid_with_warnings
adapter_schema_blocked
adapter_schema_invalid_input
```

Only `adapter_schema_valid_for_design` may allow continued contract design.

It must not allow implementation, extraction, repository creation, or EduOS runtime work.

## Mapping to Checklist Outcomes

The validator should map checklist outcomes into executable status:

| Checklist Outcome | Validator Status | Meaning |
| --- | --- | --- |
| `adapter_schema_pass_for_design` | `adapter_schema_valid_for_design` | Continue design only. |
| `adapter_schema_defer_missing_registry` | `adapter_schema_blocked` | Registry gap. |
| `adapter_schema_defer_missing_validation` | `adapter_schema_blocked` | Validation gap. |
| `adapter_schema_block_public_private_risk` | `adapter_schema_blocked` | Public/private violation. |
| `adapter_schema_block_approval_gap` | `adapter_schema_blocked` | Missing approval gate. |
| `adapter_schema_block_domain_leakage` | `adapter_schema_blocked` | Branch meaning leaked into core. |
| `adapter_schema_block_sensitive_data_requirement` | `adapter_schema_blocked` | Sensitive data required. |
| `adapter_schema_block_repository_or_runtime_scope` | `adapter_schema_blocked` | Scope exceeds planning gate. |

## Minimum Checks

The first future validator implementation should include these checks:

```text
required_root_fields_present
supported_core_families_explicit
required_registries_present
registry_names_branch_neutral
private_runtime_denied_to_public_ai
public_routes_deny_private_db
public_routes_deny_private_reports
approval_gates_required_for_actions
external_delivery_disabled_or_approval_gated
dashboard_mutations_disabled_or_approval_gated
scheduler_jobs_observable
evidence_visibility_explicit
validation_profile_non_sensitive
rollback_rule_present
branch_labels_adapter_owned
eduos_sensitive_data_not_required
businessos_domain_logic_not_universal
repository_creation_not_implied
package_creation_not_implied
```

## Future Report Path

The future command should export a report like:

```text
reports/adapter_schema_check_YYYY-MM-DD.md
```

The report must be safe to commit and must not include:

- secrets
- private data rows
- private report contents
- database snapshots
- credentials
- student or academic records
- public AI conversation payloads

## BusinessOS Validation Posture

For BusinessOS, the future validator should prove:

- BusinessOS can act as reference branch without becoming universal core
- finance, operations, support, and pilot labels remain branch-owned
- approval gates remain explicit
- evidence visibility remains private by default
- dashboard mutations remain blocked unless approval-gated
- public surface cannot read private runtime state

BusinessOS adapter implementation remains blocked.

## EduOS Validation Posture

For EduOS, the future validator should prove:

- local-only skeleton planning can be evaluated without academic data
- student, teacher, guardian, grade, attendance, assessment, LMS, SIS, or Classroom data are not required
- academic labels remain EduOS-owned
- public/private boundary is deny-by-default
- repository creation and runtime implementation are not implied

EduOS runtime implementation remains blocked.

## Public AI Validation Posture

For Public AI, the future validator should prove:

- Public AI cannot read private DB
- Public AI cannot read private reports
- Public AI cannot execute CLI commands
- Public AI cannot approve, reject, cancel, deliver, schedule, or mutate workflows
- public claims are allowlisted
- private runtime claims are denylisted
- intake handoff is sanitized

Public AI private runtime access remains blocked.

## Integration With Existing Checks

Future validation should fit into the existing validation stack like this:

```text
adapter-schema-check
system-check
release-readiness
runtime-stability
quick smoke
```

The adapter schema check should not replace existing checks. It should become an additional gate before adapter implementation or package extraction.

## Implementation Blockers

Validator implementation remains blocked until:

- schema file location is approved
- schema format is selected
- branch adapter ownership is decided
- package ownership is decided
- report format is approved
- failure semantics are approved
- test fixture policy is approved
- BusinessOS reference schema is approved
- EduOS non-sensitive schema posture is approved

## Extraction Gate Impact

This plan satisfies one planning gate:

```text
Adapter schema validator plan drafted: yes
```

It does not satisfy:

```text
Adapter schema validator implementation: no
Adapter implementation: no
OS Core package creation: no
code extraction approval: no
EduOS runtime implementation approval: no
repository creation approval: no
Public AI runtime approval: no
```

## Approved Next Blocks

Recommended sequence:

```text
OS Core Package Ownership and Repository Decision v0.1 (closed)
EduOS Skeleton Approval Decision Revisit v0.1
OS Core Adapter Schema Validator Implementation Decision v0.1 (closed)
BusinessOS Reference Adapter Schema Planning v0.1 (closed)
EduOS Non-Sensitive Adapter Schema Planning v0.1 (closed)
Adapter Schema Validator Fixture Policy v0.1 (closed)
Adapter Schema Validator Report Format and Failure Semantics v0.1 (closed)
Adapter Schema Validator Implementation Scope v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: validator_plan_only
Notification delivery: unchanged
Remote publish: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema validator implementation: blocked
Checklist posture: planned
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

This validator plan keeps the project moving toward reusable OS Core without accidentally turning a checklist into runtime authority. It defines the gate before the gate gets code.
