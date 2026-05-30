# Adapter Schema Validator Report Format and Failure Semantics v0.1

Date: 2026-05-30

## Status

Closed for report format and failure semantics planning.

## Purpose

This block defines the future report format and failure semantics for the adapter schema validator.

The goal is not to create `python cli.py adapter-schema-check`, implement validator code, create adapter schemas, create fixture files, export an adapter schema report, create an `os-core` package, create a repository, implement adapters, open EduOS runtime, or allow Public AI private runtime access. The goal is to define what a future report must contain and how validator failures must behave.

## Current Inputs

Current posture:

```text
BusinessOS reference schema planning: closed
EduOS non-sensitive schema posture planning: closed
Fixture policy: closed_for_future_synthetic_only
Report format: planning_now
Failure semantics: planning_now
Validator implementation: blocked
Adapter implementation: blocked
OS Core package creation: blocked
Repository creation: blocked
EduOS runtime: blocked
Public AI private runtime access: blocked
```

## Report Decision

```text
report_format_approved: yes_for_future_validator
failure_semantics_approved: yes_for_future_validator
report_file_created: no
validator_command_created: no
validator_runtime_code_created: no
future_report_path_pattern: reports/adapter_schema_check_YYYY-MM-DD.md
future_report_format: markdown
future_machine_result_format: structured_dict
report_commit_posture: safe_if_non_sensitive
```

The future validator may export a commit-safe Markdown report and return a structured result.

No report file is created in this block.

## Future Report Sections

The future report should include:

```text
# Adapter Schema Check

Date:
Adapter:
Adapter version:
Branch:
Validation profile:
Overall status:

## Summary

Total checks:
Passed checks:
Warning checks:
Failed checks:
Blocking failures:

## Schema Input

Schema path:
Schema format:
Schema source:
Sensitive input required:

## Checks

| Check | Status | Severity | Detail |

## Blocking Reasons

## Warnings

## Boundary Classification

## Operator Note
```

The report must summarize validator behavior only. It must not embed private source data.

## Structured Result Model

The future validator should return a structured result with these fields:

```text
date
adapter_name
adapter_version
branch_name
validation_profile
overall_status
total_checks
passed_checks
warning_checks
failed_checks
blocking_failures
blocking_reasons
warnings
report_path
safe_to_commit
runtime_authority
implementation_authority
```

Required constant values:

```text
runtime_authority: none
implementation_authority: none
```

The result must never authorize runtime, implementation, repository creation, package creation, adapter execution, Public AI private runtime access, or EduOS runtime.

## Overall Status Values

Allowed future overall status values:

```text
adapter_schema_valid_for_design
adapter_schema_valid_with_warnings
adapter_schema_blocked
adapter_schema_invalid_input
```

Meaning:

| Overall Status | Meaning | Allows |
| --- | --- | --- |
| `adapter_schema_valid_for_design` | Schema passes planning checks. | Continued design only. |
| `adapter_schema_valid_with_warnings` | Schema passes with non-blocking warnings. | Review and continued design only. |
| `adapter_schema_blocked` | Schema has one or more blocking failures. | Nothing beyond remediation. |
| `adapter_schema_invalid_input` | Schema could not be parsed or loaded safely. | Nothing beyond input repair. |

No status allows implementation.

## Check Status Values

Allowed future check status values:

```text
passed
warning
failed
blocked
invalid_input
not_applicable
```

Severity values:

```text
info
warning
blocker
critical
```

Rules:

- `critical` means unsafe validator input or unsafe report export.
- `blocker` means design cannot continue until fixed.
- `warning` means design may continue only with operator review.
- `info` means informational pass or non-applicable context.

## Blocking Failure Semantics

The future validator must block when any of these are true:

```text
required_root_fields_missing
schema_parse_failed
schema_format_unsupported
supported_core_families_missing
required_registry_missing
public_ai_private_runtime_access_requested
public_route_private_db_access_requested
public_route_private_report_access_requested
approval_gate_missing_for_action_family
external_delivery_enabled_without_approval
dashboard_mutation_enabled_without_approval
scheduler_execution_enabled_without_observability
evidence_visibility_missing
sensitive_data_required_for_validation
student_teacher_guardian_data_required_for_eduos_planning
businessos_domain_logic_marked_universal
eduos_academic_logic_marked_businessos_runtime
repository_creation_implied
package_creation_implied
runtime_implementation_implied
rollback_rule_missing
report_not_safe_to_commit
```

Any blocking failure should produce:

```text
overall_status: adapter_schema_blocked
blocking_failures: count greater than 0
runtime_authority: none
implementation_authority: none
```

## Invalid Input Semantics

The future validator should return `adapter_schema_invalid_input` when:

- the schema file cannot be read
- the schema content is not valid JSON
- the schema root is not an object
- required metadata cannot be interpreted safely
- the schema attempts to load external resources
- the schema path is outside approved locations

Invalid input should not export sensitive detail.

## Warning Semantics

Warnings are allowed only for non-blocking design issues, such as:

```text
optional_registry_detail_missing
non_blocking_description_missing
future_family_marked_planning_only
fixture_coverage_not_yet_created
report_export_skipped_in_dry_run
```

Warnings must not hide sensitive-data, public/private, approval, runtime, repository, package, or rollback problems. Those remain blockers.

## Safe Report Rules

Future reports must be safe to commit.

The report must not contain:

- secrets
- credentials
- private database rows
- private report contents
- private report excerpts
- student, teacher, guardian, roster, grade, attendance, assessment, support, intervention, or academic evidence data
- Streamlit secrets
- email credentials
- LMS/SIS/Classroom exports
- Public AI conversation payloads
- live private dashboard state

If safe report export cannot be guaranteed, the validator must return:

```text
overall_status: adapter_schema_blocked
blocking_reason: report_not_safe_to_commit
```

## Boundary Classification

Every future report should include:

```text
OS Core candidate: yes
BusinessOS-specific: adapter_owned_if_businessos
EduOS-specific: adapter_owned_if_eduos
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: validation_only
Notification delivery: none
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema validator implementation authority: none
```

## Extraction Gate Impact

This block satisfies:

```text
report_format_approved: yes
failure_semantics_approved: yes
future_report_path_pattern_selected: yes
safe_report_rules_defined: yes
overall_status_values_defined: yes
blocking_failure_semantics_defined: yes
```

It does not satisfy:

```text
adapter_schema_report_created: no
Adapter schema validator implementation: no
Adapter implementation: no
OS Core package creation: no
OS Core repository creation: no
EduOS repository creation: no
EduOS runtime implementation approval: no
Public AI runtime approval: no
```

## Recommended Next Blocks

Recommended sequence:

```text
Adapter Schema Validator Implementation Scope v0.1 (closed)
Adapter Schema Validator Implementation Approval v0.1
```

Executable validator implementation should remain blocked until implementation scope is closed.

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: report_semantics_only
Notification delivery: unchanged
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema validator implementation: blocked
Report file: not_created
Failure semantics: approved_for_future_validator
```

## Validation

Validation for this block:

```text
documentation ASCII check
py_compile
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

This block keeps the future validator honest: a report can support design decisions, but it cannot grant runtime authority. Failures should be boring, explicit, and safe to commit.
