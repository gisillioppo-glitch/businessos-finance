# EduOS Governance Boundary Sketch v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This document sketches the future EduOS governance boundary before any implementation begins.

The goal is not to create EduOS rules, runtime modules, approval code, or dashboard pages. The goal is to define the academic governance areas EduOS must protect, what requires approval, what remains advisory, and how public/private boundaries should behave.

## Current Decision

```text
EduOS governance boundary: sketched
EduOS governance implementation: not opened
EduOS approval execution: not opened
EduOS repository/runtime: not opened
```

## Governance Doctrine

EduOS may assist, summarize, recommend, and route academic decisions.

EduOS must not replace institutional authority.

Academic governance belongs to the school, district, director, teacher, and authorized support staff. EduOS should make governance visible and auditable, not invisible and automated.

## Protected Governance Areas

EduOS governance must protect:

- student privacy
- assessment sensitivity
- academic integrity
- guardian communication boundaries
- intervention decisions
- academic support escalation
- role-based access between teachers, directors, counselors, guardians, and students
- evidence visibility
- academic close integrity
- public/private separation

## Sensitivity Levels

Initial conceptual levels:

| Level | Meaning | Example |
| --- | --- | --- |
| public | Safe for public explanation or marketing. | EduOS product description. |
| internal | School-internal operational information. | Course workflow status. |
| restricted | Limited to authorized staff. | Teacher workload concerns. |
| sensitive_student | Student-specific protected information. | Academic risk, support incident, intervention plan. |
| sensitive_assessment | Assessment integrity or grading-sensitive information. | Exam review, grade-change request, integrity flag. |
| sensitive_guardian | Guardian/family communication-sensitive information. | Consent status, guardian contact, communication history. |
| confidential_governance | Governance review or leadership-only information. | Policy breach, high-risk academic integrity case. |

## Approval Candidates

Future EduOS approval types may include:

- assessment release approval
- grade-change review approval
- academic integrity review approval
- student intervention approval
- guardian communication approval
- restricted evidence access approval
- academic support escalation approval
- school pilot expansion approval
- public proof asset approval

These are conceptual approval types only.

## Advisory vs Executable Boundary

EduOS may advise:

- a student appears to need support
- an assessment may require review
- a course has missing evidence
- a guardian communication may require approval
- an intervention plan should be reviewed
- an academic close has warning context

EduOS must not execute without governance:

- approve grade changes
- disclose student information
- send sensitive guardian communications
- finalize assessment integrity decisions
- change student status
- assign disciplinary outcomes
- publish private evidence
- expose private academic dashboards

## Role Boundary Sketch

| Role | May See | Must Not See |
| --- | --- | --- |
| Director/Administrator | Institution-level summaries, governance queues, academic close, high-risk escalations. | Private details outside policy scope or without authorization. |
| Teacher | Own courses, own assignments, own student workflow signals, relevant support needs. | Other teachers' private course records unless delegated. |
| Counselor/Support Specialist | Assigned student support cases, intervention plans, relevant evidence. | Unrelated assessment or teacher records. |
| Guardian | Approved communications and allowed student-facing summaries. | Internal governance notes, other students, private teacher data. |
| Student | Approved personal academic feedback and assignments. | Internal governance, staff notes, other students. |
| Public User | Public product information only. | Any private school, student, teacher, guardian, or assessment data. |

## Evidence Governance

Academic evidence should be:

- linked to a clear academic decision or review
- classified by sensitivity
- visible only to authorized roles
- included in academic close only when policy allows
- auditable when used for intervention or assessment decisions
- excluded from public surfaces by default

Evidence packets may support:

- student intervention review
- assessment review
- academic close
- guardian communication approval
- academic support escalation
- school pilot review

## Guardian Communication Boundary

Guardian communication must be approval-aware when it includes:

- academic risk
- intervention plans
- assessment concerns
- conduct or integrity concerns
- sensitive support context
- attendance or participation risk

Public AI must not generate or send guardian communication from private data.

## Assessment Governance Boundary

Assessment governance should protect:

- grading integrity
- assessment release timing
- grade-change review
- academic integrity flags
- sensitive feedback visibility
- restricted assessment evidence

EduOS may surface review queues and evidence. EduOS must not make final academic judgments without authorized review.

## Public/Private Boundary

Public EduOS surfaces may:

- explain EduOS
- collect school interest
- qualify needs at a non-sensitive level
- route to private intake

Public EduOS surfaces must not:

- access student records
- access teacher records
- access assessment data
- access private evidence
- execute approvals
- send guardian communications
- mutate workflows
- expose private live status

## Implementation Guardrails

This sketch does not:

- create EduOS code
- create governance rules in runtime
- create approval execution
- create database schema
- create dashboard pages
- create Public AI behavior
- copy BusinessOS governance rules
- alter BusinessOS runtime

## Recommended Next Blocks

```text
EduOS Dashboard Surface Map v0.1
EduOS Command Center Adapter Sketch v0.1
EduOS Public Private Boundary Sketch v0.1
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
