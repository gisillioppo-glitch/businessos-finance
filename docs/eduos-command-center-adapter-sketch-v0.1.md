# EduOS Command Center Adapter Sketch v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This document sketches how a future EduOS Academic Command Center should adapt the BusinessOS command center pattern to academic institutions.

The goal is not to implement a command center, adapter code, dashboard page, database schema, or AI behavior. The goal is to define the academic inputs, synthesis rules, output shape, and governance boundaries before implementation begins.

## Current Decision

```text
EduOS command center adapter: sketched
EduOS command center implementation: not opened
EduOS runtime: not opened
EduOS repository: not opened
```

## Adapter Doctrine

The EduOS Academic Command Center should reuse the command synthesis pattern, not BusinessOS risk language.

BusinessOS asks:

```text
What is the enterprise operating risk and next executive move?
```

EduOS should ask:

```text
What is the academic operating risk and next institutional move?
```

The command center may recommend, prioritize, and route attention. It must not execute sensitive academic decisions without governance.

## Academic Input Domains

The future adapter may summarize these domains:

| Domain | Example Signals | Sensitivity |
| --- | --- | --- |
| Student support | active support incidents, high-risk students, intervention review dates | sensitive_student |
| Courses | course risk, missing assignment coverage, teacher workload signals | internal/restricted |
| Assignments | overdue work, missing submissions, completion trends | internal/sensitive_student |
| Assessments | grading status, integrity flags, assessment release status | sensitive_assessment |
| Governance | academic governance findings, approval queues, sensitivity review | confidential_governance |
| Guardian communications | pending approvals, communication sensitivity, delivery status | sensitive_guardian |
| Evidence | missing evidence, stale evidence, review status | restricted/sensitive_student |
| Academic close | daily/weekly close warnings, evidence completeness, readiness | restricted |
| Notifications | staff/guardian notification queue status | restricted/sensitive_guardian |

## Neutral Input Contract Sketch

Future branch adapters should convert academic data into neutral summaries before command synthesis.

Conceptual input shape:

```text
summary_id
domain
status
risk_level
sensitivity_level
owner_role
evidence_ref
approval_required
recommended_attention
```

The command center should consume these summaries instead of hard-coded source tables or branch-specific private records.

## Academic Health States

Initial conceptual health states:

- healthy
- watch
- needs_attention
- governance_review_required
- blocked

Meaning:

| State | Meaning |
| --- | --- |
| healthy | No immediate academic or governance concern requiring leadership attention. |
| watch | Signals exist but are not urgent. |
| needs_attention | Academic workflow, support, evidence, or communication needs owner review. |
| governance_review_required | Sensitive assessment, intervention, communication, or evidence decision needs governance. |
| blocked | Required evidence, approval, owner, or policy condition is missing. |

## Priority Model

The adapter should prioritize signals by:

1. student safety or support sensitivity
2. assessment integrity or grading sensitivity
3. governance approval requirement
4. missing required evidence
5. stale academic close or readiness artifact
6. high-risk course or assignment trend
7. guardian communication sensitivity
8. notification/delivery failure

This is conceptual only. Exact scoring should wait until EduOS implementation design.

## Output Shape

The Academic Command Center should eventually produce:

- overall academic health
- highest academic risk
- highest governance risk
- highest support/intervention need
- evidence completeness status
- pending approval count
- next institutional move
- private evidence references
- dashboard pages to review

Example output shape:

```text
Overall academic health: needs_attention
Highest academic risk: student_support
Highest governance risk: assessment_review
Evidence completeness: warnings
Pending approvals: 2
Next institutional move: Review sensitive assessment queue before guardian communication.
```

## Recommended Move Rules

The adapter may recommend moves such as:

- review high-risk student support cases
- confirm intervention evidence
- review assessment integrity queue
- complete academic close evidence
- approve or hold guardian communication
- review course missing-work trend
- assign owner to blocked academic workflow
- pause expansion of pilot until evidence is complete

These recommendations are advisory. Execution requires authorized human review and future approval gates.

## Governance Boundary

The command center must not:

- approve grade changes
- release assessments
- send guardian communications
- finalize academic integrity cases
- change student status
- expose private student evidence publicly
- bypass role-based access
- show sensitive evidence to unauthorized roles

## Dashboard Boundary

The future dashboard may show command center synthesis as read-only:

- health state
- risk summary
- recommended move
- links to private pages
- evidence references based on role

The dashboard must not use command center recommendations as executable buttons until governance gates exist.

## LMS/SIS Adapter Boundary

The command center should remain LMS-agnostic.

Future sources such as Google Classroom, Canvas, Moodle, Schoology, PowerSchool, SIS systems, Drive, Sheets, or manual imports should feed source adapters.

Source adapters should produce neutral academic summaries. The command center should not depend directly on a specific external platform.

## BusinessOS Analog Guardrail

| BusinessOS Command Center Concept | EduOS Adaptation |
| --- | --- |
| Finance risk | Academic risk or assessment integrity risk. |
| Operations task escalation | Academic workflow or course execution warning. |
| Support incident | Student/teacher/academic support need. |
| Governance finding | Academic governance or sensitivity finding. |
| Daily close | Academic daily/weekly close. |
| Executive next move | Institutional academic next move. |

EduOS should not copy BusinessOS wording, thresholds, module names, or enterprise operating assumptions.

## Implementation Guardrails

This sketch does not:

- create EduOS command center code
- create adapters
- create database schema
- create dashboard pages
- connect to Classroom, LMS, or SIS systems
- create student data
- execute approvals
- alter BusinessOS command center behavior

## Recommended Next Blocks

```text
EduOS Public Private Boundary Sketch v0.1
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
