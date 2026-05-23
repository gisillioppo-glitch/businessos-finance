# EduOS Domain Model Sketch v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This document sketches the future EduOS academic domain model before any implementation begins.

The goal is not to create database tables, runtime modules, or dashboard pages. The goal is to define the education-specific entities and relationships that EduOS must own separately from BusinessOS.

## Current Decision

```text
EduOS domain model: sketched
EduOS database schema: not opened
EduOS implementation: not opened
EduOS repository/runtime: not opened
```

## Domain Doctrine

EduOS is not BusinessOS with renamed finance objects.

EduOS must model academic institutions directly:

- students, not customers
- teachers, not operators
- courses and subjects, not departments alone
- assignments and assessments, not finance actions
- academic support, not business support
- academic evidence, not business evidence
- academic governance, not finance governance

OS Core patterns may shape the lifecycle, but EduOS owns the academic meaning.

## Core Academic Entities

| Entity | Meaning | Notes |
| --- | --- | --- |
| Institution | School, campus, district, academy, or education organization. | Owns academic year, term structure, governance profile, and public/private boundary profile. |
| Academic Person | Base identity for students, teachers, guardians, administrators, counselors, and support specialists. | Extends future OS Core people pattern with education-specific roles. |
| Student | Learner under academic responsibility. | Owns grade level, cohort, enrollment status, support status, academic risk, and guardian links. |
| Teacher | Educator responsible for courses, assignments, assessments, and interventions. | Owns subject areas, assigned courses, workload status, and support needs. |
| Guardian | Family or guardian communication participant. | Owns communication permissions, contact preferences, consent status, and linked students. |
| Course | Class, subject instance, or academic section. | Connects subject, teacher, term, roster, and academic risk. |
| Subject | Curriculum area or subject domain. | Owns grade band, assessment policy, and academic integrity profile. |
| Assignment | Student work assigned by course or teacher. | Tracks due date, submission coverage, missing work, and risk. |
| Assessment | Exam, quiz, project, standardized assessment, or governed evaluation. | Tracks sensitivity, integrity, grading, and review status. |
| Evaluation Outcome | Grade, score, mastery level, feedback status, or evaluation result. | Connects student work to review and visibility state. |

## Academic Operations Entities

| Entity | Meaning | Notes |
| --- | --- | --- |
| Attendance Signal | Attendance, participation, or engagement signal. | May inform academic risk or intervention. |
| Academic Workflow | Trackable academic task or workflow. | Reuses workflow lifecycle shape, not BusinessOS task categories. |
| Academic Support Incident | Student, teacher, guardian, or academic support need. | Reuses incident lifecycle shape with education-specific taxonomy. |
| Intervention Plan | Structured support plan for a student, course, or academic risk. | May require approval and evidence. |
| Guardian Communication | Governed communication with guardians or families. | Must respect consent, sensitivity, and approval rules. |
| Staff Notification | Internal school staff notification. | Uses notification pattern with education-specific recipients and content. |

## Governance and Evidence Entities

| Entity | Meaning | Notes |
| --- | --- | --- |
| Academic Governance Finding | Policy, integrity, privacy, or academic process finding. | May require approval or restricted visibility. |
| Academic Evidence Packet | Evidence supporting academic decisions, reviews, closes, or interventions. | Reuses evidence packet pattern with education-specific registries. |
| Academic Close | Daily, weekly, or term close summary for the institution. | Reuses close packet shape, not BusinessOS close content. |
| Academic Approval Request | Approval request for sensitive academic action. | Reuses approval lifecycle with academic approval types. |

## Relationship Map

```text
Institution
|-- Academic Person
|   |-- Student
|   |-- Teacher
|   |-- Guardian
|   `-- Director/Administrator
|
|-- Subject
|   `-- Course
|       |-- Assignment
|       |-- Assessment
|       |-- Attendance Signal
|       `-- Academic Workflow
|
|-- Student
|   |-- Evaluation Outcome
|   |-- Academic Support Incident
|   |-- Intervention Plan
|   |-- Guardian Communication
|   `-- Academic Evidence Packet
|
|-- Academic Governance Finding
|-- Academic Close
`-- Staff Notification
```

## Status and Severity Drafts

Reusable status concepts:

- active
- inactive
- pending
- in_review
- approved
- rejected
- completed
- blocked
- archived

Reusable severity concepts:

- none
- low
- medium
- high
- critical

EduOS must define academic meaning for each status and severity before implementation.

## Privacy and Sensitivity Levels

Initial conceptual levels:

- public
- internal
- restricted
- sensitive_student
- sensitive_assessment
- sensitive_guardian
- confidential_governance

These labels are conceptual. A future governance boundary sketch must define how they are enforced.

## BusinessOS Analog Guardrail

| BusinessOS Object | EduOS Should Not Do | EduOS Should Do |
| --- | --- | --- |
| Transaction | Rename as student record. | Define student/course/assessment entities directly. |
| Finance rule | Copy as academic rule. | Define academic risk rules separately. |
| Operations task | Copy task categories. | Define academic workflow types. |
| Support incident | Copy support categories. | Define academic support incident taxonomy. |
| Daily close | Copy business close content. | Define academic close content. |
| Notification outbox | Copy recipients and subjects. | Define school staff/guardian communication adapters. |

## Implementation Guardrails

This sketch does not:

- create EduOS code
- create database schema
- create dashboard pages
- create Public AI behavior
- create student data
- copy BusinessOS private data
- alter BusinessOS runtime

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
