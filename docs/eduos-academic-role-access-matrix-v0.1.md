# EduOS Academic Role Access Matrix v0.1

Date: 2026-05-23

## Status

Closed for MVP validation.

## Purpose

This document sketches the future EduOS academic role access matrix before any runtime, dashboard, database, LMS/SIS adapter, or Public AI implementation begins.

The goal is to define which academic roles may see which categories of information, what remains blocked, and what requires approval.

## Current Decision

```text
EduOS academic role access matrix: sketched
EduOS role enforcement implementation: not opened
EduOS dashboard permissions: not opened
EduOS database permissions: not opened
EduOS Public AI permissions: not opened
```

## Access Doctrine

EduOS access must be role-aware, evidence-aware, sensitivity-aware, and approval-aware.

Default rule:

```text
deny by default
allow by explicit role, scope, sensitivity, and approval state
```

No role should receive private academic data merely because it exists in the system.

## Core Roles

Initial conceptual roles:

| Role | Meaning |
| --- | --- |
| Director/Administrator | Institution leadership responsible for academic oversight and governance. |
| Teacher | Educator responsible for assigned courses, assignments, assessments, and students. |
| Counselor/Support Specialist | Staff responsible for assigned student support, intervention, and wellbeing workflows. |
| Governance Reviewer | Authorized reviewer for policy, privacy, assessment, or approval-sensitive matters. |
| Guardian | Family or guardian participant with approved communication scope. |
| Student | Learner with approved personal academic visibility. |
| Public User | Unauthenticated or public visitor. |

## Sensitivity Access Matrix

| Sensitivity | Director/Admin | Teacher | Counselor/Support | Governance Reviewer | Guardian | Student | Public |
| --- | --- | --- | --- | --- | --- | --- | --- |
| public | yes | yes | yes | yes | yes | yes | yes |
| internal | yes | scoped | scoped | scoped | no | no | no |
| restricted | yes | scoped | scoped | scoped | no | no | no |
| sensitive_student | scoped | assigned/scoped | assigned/scoped | review/scoped | approved summary only | own approved summary only | no |
| sensitive_assessment | scoped | owned/scoped | no by default | review/scoped | no by default | approved feedback only | no |
| sensitive_guardian | scoped | assigned/scoped | assigned/scoped | review/scoped | own approved communications only | no by default | no |
| confidential_governance | scoped | no by default | no by default | review/scoped | no | no | no |

Meaning of `scoped`:

```text
access is limited by institution, assignment, ownership, policy, and approval state
```

## Domain Access Matrix

| Domain | Director/Admin | Teacher | Counselor/Support | Governance Reviewer | Guardian | Student | Public |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Institution summary | yes | limited | limited | yes | no | no | public-only |
| Course | yes | owned | support context only | review context only | approved summary only | enrolled/approved | no |
| Assignment | yes | owned | support context only | review context only | approved summary only | own/approved | no |
| Assessment | scoped | owned/scoped | no by default | review/scoped | no by default | own approved feedback | no |
| Evaluation outcome | scoped | owned/scoped | assigned support context | review/scoped | approved summary only | own approved outcome | no |
| Student support | scoped | assigned context | assigned | review/scoped | approved communication only | own approved summary | no |
| Intervention plan | scoped | assigned context | assigned | review/scoped | approved communication only | own approved summary | no |
| Guardian communication | scoped | assigned context | assigned context | review/scoped | own approved communication | no by default | no |
| Governance finding | scoped | no by default | no by default | review/scoped | no | no | no |
| Academic evidence | scoped | owned/assigned/scoped | assigned/scoped | review/scoped | approved summary only | own approved summary only | public proof only |
| Academic close | yes | limited | limited | yes | no | no | no |
| Public proof | yes | yes | yes | yes | yes | yes | yes |

## Approval Requirements

Approval should be required before:

- guardian-facing communication involving academic risk
- sensitive assessment release
- grade-change visibility beyond normal policy
- academic integrity case visibility
- restricted evidence access outside normal scope
- public proof publication
- intervention plan disclosure
- cross-role access to sensitive student evidence

## Public User Boundary

Public users may see only:

- product explanation
- approved public proof
- synthetic examples
- non-sensitive public FAQ
- public contact/demo request surfaces

Public users must not see:

- student records
- teacher records
- guardian records
- grades
- attendance
- assessment content
- intervention plans
- academic evidence
- academic close
- live dashboard status

## Dashboard Boundary

Future dashboards must be read-only until implementation gates are opened.

Dashboard actions must not:

- approve sensitive decisions
- send guardian communications
- expose evidence outside scope
- mutate workflows
- change student status
- publish public proof

## Public AI Boundary

Future Public AI must inherit the Public User boundary.

It may explain EduOS and collect non-sensitive interest.

It must not use private role context, private evidence, academic records, assessment records, or guardian communication context.

## Implementation Guardrails

This matrix does not:

- create EduOS code
- create permissions middleware
- create database access policies
- create dashboard permissions
- create Public AI permissions
- create student data
- connect to LMS/SIS systems
- execute approvals
- alter BusinessOS runtime

## Readiness Impact

This block moves EduOS from:

```text
academic role access matrix: missing
```

to:

```text
academic role access matrix: sketched
```

Implementation is still blocked, but one key blocker has been reduced.

## Recommended Next Blocks

```text
EduOS Module Boundary Draft v0.1
EduOS Data Contract Sketch v0.1
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
