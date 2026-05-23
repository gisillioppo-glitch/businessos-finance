# EduOS Data Contract Sketch v0.1

Date: 2026-05-23

## Status

Closed for MVP validation.

## Purpose

This document sketches future EduOS data contracts before any database schema, runtime module, API, dashboard, LMS/SIS adapter, Public AI behavior, or student data is created.

The goal is to define neutral conceptual shapes that future modules may exchange without binding EduOS to BusinessOS internals, raw LMS/SIS exports, public surfaces, or premature OS Core packages.

## Current Decision

```text
EduOS data contracts: sketched
EduOS database schema: not opened
EduOS APIs: not opened
EduOS runtime models: not opened
EduOS adapters: not opened
EduOS sample data: not opened
```

## Contract Doctrine

EduOS data contracts should be:

- academic-domain first
- sensitivity-aware
- role-aware
- evidence-aware
- approval-aware
- source-agnostic
- private by default
- independent from BusinessOS private data

Contracts are conceptual. They are not tables, migrations, Pydantic models, API endpoints, or adapter implementations.

## Cross-Cutting Contract Fields

Future private EduOS contracts should usually include:

```text
record_id
institution_ref
academic_domain
status
sensitivity_level
owner_role
visibility_roles
approval_required
evidence_refs
source_system_category
created_at
updated_at
```

These fields keep records traceable without forcing a specific database or source platform.

## Institution Contract

Conceptual shape:

```text
institution_id
institution_type
academic_year
term_structure
governance_profile_ref
public_private_boundary_profile
status
```

Boundary:

- may identify institution-level configuration
- must not include student records
- must not include private evidence content
- must not include LMS/SIS credentials

## Academic Person Contract

Conceptual shape:

```text
person_id
institution_ref
role_type
role_scope
status
linked_person_refs
visibility_scope
sensitivity_level
```

Boundary:

- role_type may describe student, teacher, guardian, administrator, counselor, or support specialist
- linked_person_refs may describe relationships without exposing private details
- must not include raw contact data in public or unclassified contexts
- must not become authentication implementation

## Course Contract

Conceptual shape:

```text
course_id
institution_ref
subject_ref
teacher_refs
term_ref
course_status
risk_level
evidence_refs
visibility_roles
```

Boundary:

- may summarize course health
- must not own grades
- must not include raw roster data in public contexts
- must not send communications

## Assignment Contract

Conceptual shape:

```text
assignment_id
course_ref
status
due_context
completion_signal
missing_work_signal
risk_level
sensitivity_level
evidence_refs
```

Boundary:

- may describe completion and missing work signals
- must not expose individual student details outside role scope
- must not create disciplinary outcomes

## Assessment Contract

Conceptual shape:

```text
assessment_id
course_ref
assessment_type
review_status
release_status
integrity_signal
grading_sensitivity
sensitivity_level
approval_required
evidence_refs
```

Boundary:

- may surface review and release status
- must not approve grade changes
- must not finalize integrity decisions
- must not expose assessment content publicly

## Student Support Contract

Conceptual shape:

```text
support_case_id
student_ref
assigned_owner_role
support_status
risk_level
intervention_required
next_review_date
sensitivity_level
evidence_refs
```

Boundary:

- may summarize support need and owner status
- must not expose sensitive student details outside scope
- must not produce medical/legal conclusions

## Intervention Contract

Conceptual shape:

```text
intervention_id
student_ref
support_case_ref
plan_status
owner_role
review_date
approval_required
visibility_roles
evidence_refs
```

Boundary:

- may track intervention workflow
- must not disclose intervention details to guardians without approval
- must not change student status automatically

## Guardian Communication Contract

Conceptual shape:

```text
communication_id
student_ref
guardian_ref
communication_type
readiness_status
approval_required
delivery_status
sensitivity_level
evidence_refs
```

Boundary:

- may prepare and track communication readiness
- must not send sensitive communication without approval
- must not expose internal governance notes

## Governance Finding Contract

Conceptual shape:

```text
finding_id
institution_ref
domain_ref
finding_type
severity
sensitivity_level
approval_required
review_status
evidence_refs
```

Boundary:

- may describe policy, privacy, assessment, or academic process findings
- must not execute decisions
- must not publish confidential governance evidence

## Academic Evidence Contract

Conceptual shape:

```text
evidence_id
evidence_type
academic_domain
source_system_category
source_reference
evidence_summary
sensitivity_level
visibility_roles
decision_supported
approval_required
review_status
retention_policy
```

Boundary:

- may reference evidence
- must not expose raw private evidence outside role scope
- must not ingest raw exports into public surfaces

## Academic Close Contract

Conceptual shape:

```text
academic_close_id
institution_ref
close_period
overall_health
evidence_completeness
highest_academic_risk
highest_governance_risk
pending_approval_count
recommended_institutional_move
evidence_refs
```

Boundary:

- may summarize academic operating health
- must not expose sensitive details to unauthorized roles
- must not mutate workflows

## Academic Command Center Contract

Conceptual shape:

```text
command_summary_id
institution_ref
overall_academic_health
highest_academic_risk
highest_support_need
highest_governance_risk
blocked_domain_count
next_institutional_move
dashboard_refs
evidence_refs
```

Boundary:

- may synthesize and recommend
- must not execute approvals
- must not send communications
- must not change grades, student status, or assessment state

## Adapter Summary Contract

Conceptual shape:

```text
adapter_summary_id
source_system_category
institution_ref
domain
summary_status
normalized_signal
sensitivity_level
evidence_ref
ingestion_status
review_required
```

Boundary:

- may normalize source summaries from Classroom, LMS, SIS, Drive, Sheets, or manual imports
- must not expose credentials
- must not feed public surfaces directly
- must not bypass review and classification

## Public Handoff Contract

Conceptual shape:

```text
request_id
institution_type
size_band
requester_role
high_level_need
current_system_category
demo_interest
contact_channel
consent_to_contact
created_at
```

Boundary:

- public-safe only
- no student records
- no teacher records
- no guardian records
- no grades
- no assessment content
- no private files
- no secrets

## Contract Validation Rules

Future implementation should validate:

- sensitivity_level is present
- visibility_roles are explicit
- approval_required is explicit
- evidence_refs are references, not raw private content
- source_system_category does not imply direct platform coupling
- public contracts cannot include private fields
- contracts do not include BusinessOS finance concepts

## Implementation Guardrails

This sketch does not:

- create EduOS code
- create database tables
- create migrations
- create APIs
- create runtime models
- create dashboard pages
- create LMS/SIS adapters
- create sample data
- create Public AI behavior
- copy BusinessOS data
- alter BusinessOS runtime

## Readiness Impact

This block moves EduOS from:

```text
data contracts: missing
```

to:

```text
data contracts: sketched
```

Implementation remains blocked until dashboard interaction rules and a non-sensitive implementation skeleton scope are explicitly defined.

## Recommended Next Blocks

```text
EduOS Dashboard Read-Only Interaction Rules v0.1
EduOS Non-Sensitive Skeleton Scope v0.1
```

## Validation

Validation expected for this block:

```text
docs ASCII check
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected result:

```text
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```
