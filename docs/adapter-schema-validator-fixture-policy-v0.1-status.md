# Adapter Schema Validator Fixture Policy v0.1

Date: 2026-05-30

## Status

Closed for fixture policy planning.

## Purpose

This block defines the fixture policy for a future adapter schema validator.

The goal is not to create fixture files, create adapter schema files, implement `python cli.py adapter-schema-check`, add validator code, implement adapters, create an `os-core` package, create a repository, open EduOS runtime, copy BusinessOS private files, or allow Public AI private runtime access. The goal is to decide what fixture data may be used later without introducing sensitive data or runtime authority.

## Current Inputs

Current posture:

```text
BusinessOS reference schema planning: closed
EduOS non-sensitive schema posture planning: closed
Adapter schema validator implementation decision: closed_not_approved_yet
Fixture policy: planning_now
Fixture files: not_created
Validator implementation: blocked
Adapter implementation: blocked
OS Core package creation: blocked
Repository creation: blocked
EduOS runtime: blocked
Public AI private runtime access: blocked
```

## Policy Decision

```text
fixture_policy_approved: yes_for_future_synthetic_fixtures_only
fixture_files_created: no
fixture_runtime_authority: none
fixture_format_selected_for_future: json
future_fixture_location_candidate: tests/fixtures/adapter_schema/
BusinessOS_fixture_posture: synthetic_non_sensitive_only
EduOS_fixture_posture: synthetic_non_sensitive_only
negative_fixture_posture: allowed_for_boundary_tests
private_data_fixtures: blocked
academic_data_fixtures: blocked
credential_fixtures: blocked
```

Fixtures are approved only as future static, synthetic, non-sensitive validation inputs.

No fixture file is created in this block.

## Allowed Future Fixture Types

Future validator fixtures may include:

```text
valid_businessos_reference_schema
valid_eduos_non_sensitive_schema
missing_root_field_schema
missing_registry_schema
public_private_violation_schema
approval_gap_schema
domain_leakage_schema
sensitive_data_required_schema
repository_or_runtime_scope_violation_schema
rollback_missing_schema
invalid_json_schema
```

These fixtures must be synthetic and minimal. They should test validator behavior, not business data.

## Allowed Fixture Content

Allowed fixture content:

- branch ids such as `businessos` or `eduos`
- branch-owned labels already documented in planning artifacts
- synthetic role names
- synthetic page names
- conceptual registry names
- boolean boundary flags
- non-sensitive validation profiles
- explicit rollback rules
- placeholder source categories
- synthetic failure cases

Allowed examples:

```text
branch_id: businessos
branch_id: eduos
validation_profile: planning
public_private_boundary: deny_by_default
student_data_required: false
private_db_access: denied
rollback_rule: branch_only
```

## Blocked Fixture Content

Fixture content must not include:

- private database contents
- private report contents
- copied BusinessOS reports
- copied BusinessOS runtime files
- secrets
- tokens
- credentials
- Streamlit secrets
- email credentials
- notification credentials
- student names
- teacher names
- guardian names
- rosters
- attendance records
- grades
- assessment content
- support case details
- intervention details
- academic evidence contents
- LMS exports
- SIS exports
- Classroom exports
- public AI conversation payloads
- live dashboard state
- production URLs with secrets

## Negative Fixture Policy

Negative fixtures are allowed because the validator needs to prove it blocks unsafe schemas.

Negative fixtures may simulate:

```text
missing_required_root_field
missing_required_registry
public_ai_private_db_access_requested
public_route_private_report_access_requested
approval_gate_missing_for_action_family
dashboard_mutation_without_approval
external_delivery_without_approval
student_data_required_for_eduos_planning
businessos_finance_label_marked_universal
repository_creation_implied_by_schema
runtime_implementation_implied_by_schema
rollback_rule_missing
```

Negative fixtures must still use fake values and must not contain real private data.

## Fixture Naming Rules

Future fixture names should be explicit and boring:

```text
valid_businessos_reference.schema.json
valid_eduos_non_sensitive.schema.json
invalid_missing_root_field.schema.json
invalid_missing_registry.schema.json
invalid_public_private_violation.schema.json
invalid_approval_gap.schema.json
invalid_domain_leakage.schema.json
invalid_sensitive_data_required.schema.json
invalid_repository_runtime_scope.schema.json
invalid_missing_rollback.schema.json
invalid_json.schema.json
```

Names should describe the validator outcome and must not include customer, school, student, or operator names.

## Fixture Location Policy

The future location candidate is:

```text
tests/fixtures/adapter_schema/
```

This location is approved as a planning target only.

Before creating this folder or any fixture files:

- validator implementation scope must be approved
- report format and failure semantics must be approved
- fixture contents must be reviewed for non-sensitive posture
- no BusinessOS private artifacts may be copied
- no EduOS academic data may be introduced

## Fixture Review Checklist

Every future fixture must pass this review before commit:

```text
contains_secrets: no
contains_credentials: no
contains_private_reports: no
contains_database_rows: no
contains_academic_records: no
contains_student_teacher_guardian_data: no
contains_real_customer_or_school_data: no
contains_businessos_private_paths: no
contains_runtime_command_execution: no
contains_public_ai_private_access: no
synthetic_only: yes
purpose_is_validator_behavior: yes
safe_to_commit: yes
```

## Validator Impact

This fixture policy enables future validator implementation planning, but does not create executable validation.

Allowed future use:

- unit tests for schema loading
- unit tests for root field validation
- unit tests for registry presence
- unit tests for public/private denial
- unit tests for approval gate detection
- unit tests for domain leakage detection
- unit tests for sensitive-data requirement denial
- unit tests for rollback enforcement

Still blocked:

- validator CLI command
- validator runtime code
- schema file creation
- fixture file creation
- adapter implementation
- OS Core package creation
- repository creation
- EduOS runtime
- Public AI private runtime access

## Extraction Gate Impact

This block satisfies:

```text
fixture_policy_approved: yes
future_fixture_format_selected: json
future_fixture_location_candidate_selected: yes
negative_fixture_policy_defined: yes
safe_to_commit_rule_defined: yes
```

It does not satisfy:

```text
fixture_files_created: no
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
Adapter Schema Validator Report Format and Failure Semantics v0.1 (closed)
Adapter Schema Validator Implementation Scope v0.1 (closed)
Adapter Schema Validator Implementation Approval v0.1 (closed)
Adapter Schema Validator Module Implementation v0.1
```

Executable validator implementation should remain blocked until report format, failure semantics, and implementation scope are closed.

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: fixture_policy_only
Notification delivery: unchanged
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema validator implementation: blocked
Fixture files: not_created
Fixture policy: approved_for_future_synthetic_only
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

This block lets the future validator have tests without letting tests become a data leak. Fixtures may later prove boundary behavior, but only with synthetic, commit-safe content.
