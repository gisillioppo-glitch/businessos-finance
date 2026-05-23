# EduOS Module Boundary Draft v0.1

Date: 2026-05-23

## Status

Closed for MVP validation.

## Purpose

This document drafts the future EduOS module boundaries before any runtime, database schema, dashboard, API, LMS/SIS adapter, or Public AI implementation begins.

The goal is to define what each future EduOS module should own, what it must not own, and where governance, evidence, role access, and public/private boundaries must be enforced.

## Current Decision

```text
EduOS module boundaries: drafted
EduOS runtime modules: not opened
EduOS database schema: not opened
EduOS dashboard modules: not opened
EduOS adapters: not opened
```

## Boundary Doctrine

EduOS modules should be academic-domain modules, not renamed BusinessOS modules.

OS Core patterns may inform workflows, approvals, evidence, notifications, people, command synthesis, and readiness. EduOS must define its own academic contracts before implementation.

## Proposed Future Modules

| Module | Owns | Must Not Own |
| --- | --- | --- |
| Institution | school profile, term structure, academic year, policy profile, boundary profile | student records, course execution, private evidence content |
| Academic People | role identities, student/teacher/guardian/admin/counselor role links | authentication runtime, unrelated private records |
| Courses | subjects, course sections, rosters by reference, course health | grades, support interventions, guardian communication execution |
| Assignments | assignment status, due dates, submission coverage, missing work signals | final grades, disciplinary outcomes, guardian messaging |
| Assessments | assessment status, grading sensitivity, release state, integrity review references | automatic grade changes, final integrity decisions |
| Student Support | support incidents, support status, intervention needs, assigned support owners | assessment release, disciplinary outcomes, public evidence |
| Interventions | intervention plan status, review dates, owner tracking, evidence references | medical/legal judgments, automatic disclosure |
| Guardian Communications | communication readiness, consent state, approval requirement, delivery status | unapproved message sending, private evidence publication |
| Academic Governance | policy findings, sensitivity findings, approval needs, review queues | operational execution without approval |
| Academic Evidence | evidence packets, sensitivity, source category, visibility roles, review status | raw LMS/SIS ingestion, public exposure, unauthorized details |
| Academic Close | daily/weekly/term close summaries, evidence completeness, warnings | source system ownership, sensitive details outside role scope |
| Academic Command Center | cross-module synthesis, health state, next institutional move | execution of actions, approvals, grade changes, communications |
| Notifications | staff/guardian notification queue state and delivery status | sending sensitive communications without approval |
| Readiness | implementation readiness, validation posture, demo/pilot readiness | bypassing system integrity or governance checks |
| System Integrity | private system health once runtime exists | public status claims from private checks |
| Adapters | normalized summaries from LMS/SIS/source systems | direct public access, raw credential handling in public surfaces |

## Module Dependency Direction

Conceptual direction:

```text
Institution
-> Academic People
-> Courses / Assignments / Assessments
-> Student Support / Interventions
-> Guardian Communications
-> Governance / Approvals
-> Evidence
-> Academic Close
-> Command Center
-> Readiness / System Integrity
```

Adapters feed normalized summaries into domain modules and evidence. Public surfaces do not feed private modules directly.

## Cross-Cutting Boundaries

Every future module must respect:

- role access matrix
- sensitivity classification
- evidence visibility rules
- approval state
- auditability
- public/private separation
- docs-only shell until implementation is explicitly opened

## Module Boundary Details

### Institution

Owns:

- institution profile
- term/academic year structure
- school type
- governance policy profile
- public/private boundary profile

Does not own:

- student evidence
- grades
- assessments
- support incidents
- communications

### Academic People

Owns:

- academic role concepts
- role-to-person links
- student/teacher/guardian/admin/counselor identity classification
- guardian-student relationship references

Does not own:

- authentication implementation
- sensitive academic evidence
- final access enforcement code

### Courses, Assignments, And Assessments

Owns:

- course structure
- assignment workflow status
- assessment workflow status
- academic risk signals
- grading/release sensitivity references

Does not own:

- support interventions
- guardian communication delivery
- governance decisions
- public proof publication

### Student Support And Interventions

Owns:

- support incidents
- intervention plan status
- assigned owners
- review dates
- support evidence references

Does not own:

- assessment integrity decisions
- public disclosure
- medical/legal conclusions
- unapproved guardian messaging

### Governance And Approvals

Owns:

- sensitivity findings
- policy findings
- approval requirements
- review queues
- approval status references

Does not own:

- raw academic content
- automatic execution of sensitive decisions
- LMS/SIS connectors

### Evidence

Owns:

- academic evidence packet metadata
- sensitivity classification
- source category
- role visibility references
- decision supported
- review status

Does not own:

- source system raw exports
- public asset publication without approval
- final academic decisions

### Academic Close And Command Center

Owns:

- close summaries
- evidence completeness
- warnings
- cross-domain health
- recommended institutional move

Does not own:

- mutation of workflows
- approvals
- communications
- direct source ingestion

### Notifications And Guardian Communications

Owns:

- notification queue state
- delivery readiness
- guardian communication approval requirement
- delivery status

Does not own:

- unapproved sensitive delivery
- evidence publication
- Public AI communication generation

### Adapters

Owns:

- normalized summaries from Classroom/LMS/SIS/source systems
- source category identification
- private ingestion boundary

Does not own:

- public credential collection
- public raw data access
- module decisions
- approval execution

## Implementation Boundary

This draft does not:

- create EduOS code
- create folders for runtime modules
- create database tables
- create APIs
- create dashboard pages
- create LMS/SIS adapters
- create Public AI behavior
- create sample student data
- copy BusinessOS modules
- extract OS Core packages
- alter BusinessOS runtime

## Readiness Impact

This block moves EduOS from:

```text
module boundaries: missing
```

to:

```text
module boundaries: drafted
```

Implementation remains blocked until data contracts and initial non-sensitive skeleton scope are explicitly defined.

## Recommended Next Blocks

```text
EduOS Data Contract Sketch v0.1
EduOS Dashboard Read-Only Interaction Rules v0.1
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
