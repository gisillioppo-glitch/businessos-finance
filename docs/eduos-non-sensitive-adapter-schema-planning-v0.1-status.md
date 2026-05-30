# EduOS Non-Sensitive Adapter Schema Planning v0.1

Date: 2026-05-30

## Status

Closed for non-sensitive adapter schema planning.

## Purpose

This block defines the planning posture for a future EduOS non-sensitive adapter schema.

The goal is not to create an EduOS schema file, create EduOS runtime, create an EduOS repository, initialize Git in the skeleton, implement adapters, connect Classroom/LMS/SIS systems, create academic data, create `python cli.py adapter-schema-check`, implement validator code, create an `os-core` package, move BusinessOS code, or allow Public AI private runtime access. The goal is to document what a future EduOS schema may describe without requiring sensitive implementation.

## Current Inputs

Current posture:

```text
BusinessOS reference schema planning: closed
EduOS skeleton: local_only_ready
EduOS repository creation: blocked
EduOS runtime: blocked
EduOS database: blocked
EduOS dashboard: blocked
EduOS adapters: blocked
EduOS academic data: blocked
OS Core package creation: blocked
Adapter schema validator implementation: blocked
Public AI private runtime access: blocked
```

Relevant EduOS planning sources:

- EduOS Module Boundary Draft v0.1
- EduOS Data Contract Sketch v0.1
- EduOS Public Private Boundary Sketch v0.1
- EduOS Non-Sensitive Skeleton Scope v0.1
- EduOS Skeleton Approval Decision Revisit v0.1

## Planning Decision

```text
EduOS_non_sensitive_schema_posture_planned: yes
schema_file_created: no
schema_format_selected_for_future: json
future_schema_location_candidate: config/adapters/eduos.adapter.schema.json
schema_runtime_authority: none
validator_command_created: no
adapter_implementation: blocked
EduOS_runtime: blocked
EduOS_repository_creation: blocked
academic_data: blocked
Classroom_LMS_SIS_adapters: blocked
Public_AI_private_runtime_access: blocked
OS_Core_package_creation: blocked
```

The future EduOS schema should be a non-sensitive JSON configuration artifact.

The location is a planning target only. No file is created in this block.

## Future Root Fields

The future EduOS non-sensitive schema should include these root fields:

```text
adapter_name: eduos_non_sensitive
adapter_version: 0.1
branch_name: EduOS
branch_id: eduos
branch_visibility: private_future_branch
branch_owner: operator
branch_mode: local_only_skeleton
supported_core_families:
  - identity
  - dashboard
  - approvals
  - evidence
  - readiness
  - runtime
  - scheduler
  - notifications
  - governance
  - command_center
  - public_boundary
validation_profile: planning
rollback_rule: local_only_skeleton_no_runtime
```

These fields are conceptual configuration only. They do not create EduOS runtime or schema files.

## Future Registries

The future schema should define non-sensitive registry placeholders only.

```text
role_registry:
  conceptual_roles: administrator, teacher, guardian, student, counselor, support_specialist
  public_roles: none
  rule: roles remain conceptual until access enforcement is approved

page_registry:
  conceptual_pages: Academic Command Center, Academic Close, Academic Evidence, Guardian Communications, Student Support, Readiness
  rule: pages remain planning-only and must not create dashboard runtime

approval_policy:
  conceptual_approval_domains: assessment_release, guardian_communication, intervention_review, policy_exception
  rule: approval execution remains blocked

protected_source_policy:
  conceptual_sources: academic_governance, guardian_communications, student_support, assessment_review
  rule: sensitive source workflows require future approval gates

evidence_registry:
  conceptual_evidence_domains: academic_close, assessment_review, support_case, intervention_plan, guardian_communication, governance_finding
  rule: evidence references are conceptual and must not include raw records

notification_policy:
  conceptual_modes: queue_only, approval_required
  rule: delivery is blocked until implementation approval

readiness_check_registry:
  conceptual_checks: skeleton_scope, boundary_docs, non_sensitive_config, no_academic_data, no_adapters
  rule: readiness checks must run without private academic data

runtime_check_registry:
  conceptual_checks: no_runtime, no_database, no_dashboard, no_adapters, no_public_ai_private_access
  rule: runtime is blocked until explicit approval

scheduler_job_registry:
  conceptual_jobs: academic_close_future
  rule: scheduler execution remains blocked

governance_rule_pack:
  conceptual_rules: sensitivity_required, role_visibility_required, public_private_deny_by_default
  rule: governance remains planning-only

command_summary_adapter:
  conceptual_sources: academic_health, support_need, governance_risk, evidence_completeness
  rule: command synthesis remains conceptual and cannot execute actions

public_boundary_policy:
  source: EduOS Public Private Boundary Sketch v0.1
  rule: deny student records, teacher records, guardian records, grades, attendance, assessment content, private reports, CLI execution, workflow mutation, and live private status claims
```

## Explicitly Blocked Fields

The future EduOS non-sensitive schema must not include:

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

## Family Posture

```text
identity: conceptual_schema_only
dashboard: conceptual_schema_only
approvals: conceptual_schema_only
evidence: conceptual_schema_only
readiness: conceptual_schema_only
runtime: blocked
scheduler: conceptual_schema_only
notifications: conceptual_schema_only
governance: conceptual_schema_only
command_center: conceptual_schema_only
public_boundary: deny_by_default
```

No family is approved for EduOS implementation in this block.

## Academic Labels Remain EduOS-Owned

These labels remain EduOS-owned and must not become universal OS Core labels:

- Institution
- Academic People
- Courses
- Assignments
- Assessments
- Student Support
- Interventions
- Guardian Communications
- Academic Governance
- Academic Evidence
- Academic Close
- Academic Command Center
- Academic Readiness

OS Core may later define neutral slots, but EduOS owns academic meaning, visibility, sensitivity, and role semantics.

## Public Boundary Requirements

The future EduOS schema must enforce:

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

Public AI remains outside private runtime authority.

## Validation Expectations

When the validator is eventually implemented, the EduOS non-sensitive schema should pass only if:

- all required root fields are present
- supported families are explicit
- all registries are non-sensitive placeholders
- no student, teacher, guardian, grade, attendance, assessment, intervention, or academic evidence records are required
- Classroom/LMS/SIS adapters remain blocked
- dashboard runtime remains blocked
- notification delivery remains blocked
- Public AI private runtime access is denied
- BusinessOS private paths are not referenced
- rollback returns to local-only skeleton with no runtime

## Remaining Blockers

Still unresolved after this block:

```text
EduOS_schema_file_created: no
fixture_policy_approved: yes_for_future_synthetic_only
report_format_finalized: no
failure_semantics_finalized: no
adapter_schema_validator_implementation: no
EduOS_adapter_implementation: no
EduOS_repository_creation: no
EduOS_runtime: no
EduOS_database: no
EduOS_dashboard: no
Classroom_LMS_SIS_adapters: no
OS_Core_package_creation: no
code_extraction: no
```

## Extraction Gate Impact

This block satisfies:

```text
EduOS_non_sensitive_schema_posture_planned: yes
schema_format_selected_for_future: json
schema_location_candidate_selected: yes
academic_data_required_for_validation: no
```

It does not satisfy:

```text
EduOS_schema_file_created: no
Adapter schema validator implementation: no
EduOS adapter implementation: no
OS Core package creation: no
OS Core repository creation: no
EduOS repository creation: no
EduOS runtime implementation approval: no
Public AI runtime approval: no
```

## Recommended Next Blocks

Recommended sequence:

```text
Adapter Schema Validator Fixture Policy v0.1 (closed)
Adapter Schema Validator Report Format and Failure Semantics v0.1
Adapter Schema Validator Implementation Scope v0.1
```

Executable validator implementation should remain blocked until those planning gates are closed.

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: schema_planning_only
Notification delivery: blocked
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema validator implementation: blocked
Academic data: blocked
Reference schema posture: planned_not_created
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

This block gives EduOS a validator-ready planning posture without opening EduOS itself. It keeps the branch useful for future OS Core comparison while preserving every sensitive academic and repository boundary.
