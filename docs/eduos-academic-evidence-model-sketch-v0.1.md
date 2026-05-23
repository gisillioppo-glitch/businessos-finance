# EduOS Academic Evidence Model Sketch v0.1

Date: 2026-05-23

## Status

Closed for MVP validation.

## Purpose

This document sketches the future EduOS academic evidence model before any implementation, database schema, dashboard page, LMS/SIS adapter, or student data is created.

The goal is to define what academic evidence means in EduOS, how evidence should be classified, where it may come from, who may see it, and how it should support academic decisions without exposing protected records.

## Current Decision

```text
EduOS academic evidence model: sketched
EduOS academic evidence implementation: not opened
EduOS evidence database: not opened
EduOS LMS/SIS evidence adapters: not opened
EduOS private runtime: not opened
```

## Evidence Doctrine

EduOS evidence should support academic review, not replace institutional judgment.

Evidence may help directors, teachers, counselors, and authorized support staff understand academic workflows, student support needs, assessment reviews, guardian communications, and institutional closes.

Evidence must be classified, role-aware, approval-aware, and private by default.

## Evidence Categories

Future EduOS evidence may include:

| Category | Meaning | Example Sources | Default Sensitivity |
| --- | --- | --- | --- |
| Course evidence | Course workflow, coverage, assignments, and execution context. | LMS summaries, teacher notes, course plans. | internal/restricted |
| Assignment evidence | Submission, missing work, feedback, or completion context. | LMS assignment exports, manual teacher review. | sensitive_student |
| Assessment evidence | Grading, integrity, review, and release context. | assessment systems, teacher review, audit notes. | sensitive_assessment |
| Student support evidence | Support need, intervention context, and follow-up status. | counselor notes, support logs, intervention plans. | sensitive_student |
| Guardian communication evidence | Approved communication context and delivery status. | communication logs, approval records. | sensitive_guardian |
| Governance evidence | Policy, privacy, integrity, or approval review context. | governance findings, approvals, audit notes. | confidential_governance |
| Academic close evidence | Daily, weekly, or term close support packet. | command center summaries, area reviews, readiness checks. | restricted |
| Public proof evidence | Sanitized proof suitable for public storytelling. | approved mockups, synthetic metrics, public case notes. | public |

## Evidence Packet Shape

Future academic evidence packets should be neutral and branch-owned.

Conceptual packet fields:

```text
evidence_id
evidence_type
academic_domain
institution_ref
owner_role
subject_ref
sensitivity_level
source_system_category
source_reference
evidence_summary
decision_supported
approval_required
visibility_roles
retention_policy
created_at
review_status
```

The packet should not require a direct dependency on Google Classroom, Canvas, Moodle, SIS, or BusinessOS internals.

## Source Boundary

Potential future source categories:

- manual institutional note
- LMS summary
- SIS summary
- assessment system summary
- support workflow summary
- guardian communication summary
- governance finding
- approval decision
- academic close summary
- synthetic demo artifact

Source adapters should sanitize and classify data before evidence is indexed.

EduOS should not ingest raw private exports into public or unclassified surfaces.

## Sensitivity Classification

Evidence must map to the EduOS sensitivity levels:

| Level | Evidence Rule |
| --- | --- |
| public | Only approved, synthetic, or sanitized proof assets. |
| internal | General institutional context without protected records. |
| restricted | Operational academic context limited to authorized staff. |
| sensitive_student | Student-specific evidence requiring protected access. |
| sensitive_assessment | Assessment, grading, integrity, or release-sensitive evidence. |
| sensitive_guardian | Guardian or family communication-sensitive evidence. |
| confidential_governance | Leadership or governance-only review evidence. |

Default posture:

```text
unknown evidence sensitivity: restricted
student-linked evidence: sensitive_student
assessment-linked evidence: sensitive_assessment
guardian-linked evidence: sensitive_guardian
governance-linked evidence: confidential_governance
```

## Role Visibility

Conceptual role visibility:

| Role | May See |
| --- | --- |
| Director/Administrator | Institution-level evidence, governance evidence, academic close, approved summaries. |
| Teacher | Evidence for owned courses, assignments, assessments, and assigned students. |
| Counselor/Support Specialist | Assigned support and intervention evidence. |
| Guardian | Only approved guardian-facing summaries and communications. |
| Student | Only approved student-facing academic feedback and personal records. |
| Public User | Public proof assets only. |

Role visibility must be enforced before dashboard or Public AI implementation.

## Approval Boundary

Evidence access or use may require approval when it involves:

- assessment release
- grade-change review
- academic integrity review
- intervention plan review
- guardian communication
- restricted evidence access
- public proof publication
- school pilot expansion

EduOS evidence may support approvals. It must not execute approvals.

## Evidence Lifecycle

Conceptual statuses:

- draft
- collected
- classified
- in_review
- approved_for_internal_use
- approved_for_guardian_use
- approved_for_public_use
- rejected
- archived

Evidence should not move into public, guardian, or executive-facing use without the required classification and approval state.

## Academic Close Use

Academic close packets may include:

- course workflow status
- assessment review warnings
- student support summary counts
- guardian communication readiness
- governance findings
- evidence completeness status
- pending approval count
- recommended institutional move

Academic close must reference protected evidence without exposing sensitive details to unauthorized roles.

## Public Boundary

Public EduOS surfaces may reference only:

- approved public proof evidence
- synthetic examples
- high-level product explanations
- sanitized demo narratives

Public surfaces must not expose:

- raw academic evidence
- student-linked evidence
- assessment evidence
- guardian communication evidence
- governance evidence
- private academic close packets
- LMS/SIS source references

## BusinessOS Analog Guardrail

EduOS should reuse the evidence pattern, not BusinessOS evidence content.

| BusinessOS Evidence Concept | EduOS Adaptation |
| --- | --- |
| Executive evidence index | Academic evidence index. |
| Daily close evidence packet | Academic close evidence packet. |
| Approval decision support | Academic approval evidence support. |
| Public/private boundary | Student, assessment, guardian, and governance privacy boundary. |

EduOS must not copy BusinessOS private reports, finance evidence, recipients, or operating assumptions.

## Implementation Guardrails

This sketch does not:

- create EduOS code
- create evidence database tables
- create academic evidence records
- connect to LMS/SIS systems
- create dashboard pages
- create Public AI behavior
- create approvals
- copy BusinessOS reports
- copy private files
- alter BusinessOS runtime

## Readiness Impact

This block moves EduOS from:

```text
academic evidence requirements: not defined
```

to:

```text
academic evidence requirements: sketched
```

EduOS implementation remains blocked until evidence contracts, role access, and approval gates are implementation-ready.

## Recommended Next Blocks

```text
EduOS Implementation Readiness Gate v0.1
EduOS Academic Role Access Matrix v0.1
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
