# EduOS Dashboard Surface Map v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This document maps the future private EduOS dashboard surface before any implementation begins.

The goal is not to build EduOS dashboard pages yet. The goal is to define the page set, role visibility, sensitivity boundaries, read-only posture, and governance guardrails for the future EduOS private operating surface.

## Current Decision

```text
EduOS dashboard surface: mapped
EduOS dashboard implementation: not opened
EduOS runtime: not opened
EduOS repository: not opened
```

## Dashboard Doctrine

The EduOS dashboard should be a protected private operating surface for academic leadership and authorized staff.

The first EduOS dashboard should be read-only by default.

It may surface evidence, status, queues, risks, and recommendations. It must not execute sensitive academic actions until explicit governance gates exist.

## Private Dashboard Surface

Proposed future pages:

| Page | Purpose | Primary Roles | Sensitivity | Initial Posture |
| --- | --- | --- | --- | --- |
| Academic Dashboard | Top-level health, risks, and priorities. | Director, administrator | internal/restricted | read-only |
| Academic Command Center | Cross-domain synthesis and next best academic move. | Director, administrator | restricted | read-only |
| Students | Student status, support signals, and risk summary. | Director, teacher, counselor | sensitive_student | read-only |
| Teachers | Teacher workload and assigned course visibility. | Director, administrator | restricted | read-only |
| Courses | Course health, assignment coverage, and academic risk. | Director, teacher | internal/restricted | read-only |
| Assignments | Assignment status, missing work, and completion coverage. | Teacher, director | internal/sensitive_student | read-only |
| Assessments | Assessment status, sensitivity, grading, and integrity review queues. | Teacher, director | sensitive_assessment | read-only |
| Academic Governance | Governance findings, sensitivity queues, and policy review status. | Director, governance reviewer | confidential_governance | read-only |
| Academic Support | Support incidents, intervention plans, and owner status. | Counselor, director, teacher | sensitive_student | read-only |
| Intervention Plans | Active interventions and review dates. | Counselor, teacher, director | sensitive_student | read-only |
| Guardian Communications | Communication approvals, delivery status, and sensitivity. | Director, teacher, counselor | sensitive_guardian | read-only |
| Academic Evidence | Evidence packets and review visibility. | Director, teacher, counselor | restricted/sensitive_student | read-only |
| Academic Close | Daily/weekly close, evidence completeness, and warnings. | Director, administrator | restricted | read-only |
| Approvals | Academic approval requests and status. | Director, approver | restricted/confidential_governance | read-only until gates exist |
| Notifications | Internal/staff/guardian notification queue visibility. | Director, administrator | restricted/sensitive_guardian | read-only |
| Readiness | EduOS readiness checks when implementation exists. | Director, operator | internal | read-only |
| System Integrity | EduOS system health when implementation exists. | Operator, administrator | internal | read-only |

## Navigation Groups

Initial navigation grouping:

```text
Overview
- Academic Dashboard
- Academic Command Center

Academic Operations
- Students
- Teachers
- Courses
- Assignments
- Assessments

Support and Governance
- Academic Support
- Intervention Plans
- Academic Governance
- Guardian Communications
- Approvals

Evidence and Close
- Academic Evidence
- Academic Close
- Notifications

System
- Readiness
- System Integrity
```

## Role Visibility Sketch

| Role | Likely Visible Pages | Notes |
| --- | --- | --- |
| Director/Administrator | All leadership pages, governance, close, command center, approvals. | May see institution-level summaries and high-risk queues. |
| Teacher | Own courses, assignments, assessments, relevant student signals, approved communications. | Must not see unrelated teacher or student details. |
| Counselor/Support Specialist | Academic Support, Intervention Plans, assigned students, relevant evidence. | Visibility must be case-based and policy-bound. |
| Governance Reviewer | Academic Governance, Approvals, restricted evidence. | Must see only governance-scoped evidence. |
| Guardian | Not part of the private staff dashboard. | Future guardian portal would be separate and approval-aware. |
| Student | Not part of the private staff dashboard. | Future student view would be separate and policy-bound. |
| Public User | No private dashboard access. | Public AI/landing remains separate. |

## Read-Only Action Boundary

The first dashboard concept may show:

- status
- risk levels
- evidence references
- approval status
- notification status
- intervention review dates
- academic close warnings
- command center summaries

The first dashboard concept must not:

- approve or reject academic decisions
- change grades
- release assessments
- send guardian communications
- mutate student status
- create interventions
- finalize academic integrity findings
- expose private evidence publicly
- trigger workflows from the UI

## Evidence Boundary

Dashboard evidence visibility must be:

- role-aware
- sensitivity-aware
- student privacy-aware
- assessment privacy-aware
- guardian communication-aware
- excluded from public surfaces
- auditable when used for decisions

Evidence references may be shown before full evidence content when sensitivity is high.

## Public/Private Boundary

The EduOS dashboard must remain private.

Public EduOS surfaces may describe dashboard capabilities at a high level, but must not show live or private dashboard data.

Public surfaces must not expose:

- student records
- teacher workload records
- assessment status
- academic evidence
- support incidents
- intervention plans
- guardian communications
- approvals
- private close artifacts

## Relationship to Classroom/LMS/SIS

EduOS should be LMS-agnostic.

Future external systems such as Google Classroom, Canvas, Moodle, Schoology, PowerSchool, or a SIS should be treated as adapters or evidence sources.

The dashboard should not assume one source platform. It should show EduOS academic operating state after data is safely ingested, normalized, approved, or reviewed through future adapters.

## Implementation Guardrails

This map does not:

- create EduOS dashboard code
- create Streamlit pages
- create database schema
- create integrations with Classroom, LMS, or SIS systems
- create student data
- create approval execution
- create Public AI behavior
- alter BusinessOS dashboard behavior

## Recommended Next Blocks

```text
EduOS Docs-Only Shell v0.1
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
