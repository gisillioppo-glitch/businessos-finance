# EduOS Dashboard Read-Only Interaction Rules v0.1

Date: 2026-05-23

## Status

Closed for MVP validation.

## Purpose

This document sketches future EduOS dashboard interaction rules before any dashboard implementation, runtime module, database schema, API, LMS/SIS adapter, Public AI behavior, or student data is created.

The goal is to define what a future private EduOS dashboard may allow users to see, filter, inspect, and navigate without executing sensitive academic actions.

## Current Decision

```text
EduOS dashboard interaction rules: sketched
EduOS dashboard implementation: not opened
EduOS dashboard actions: blocked
EduOS runtime: not opened
EduOS database: not opened
```

## Interaction Doctrine

The first EduOS dashboard should be read-only by default.

It may support:

- viewing summaries
- filtering records
- sorting queues
- opening detail views
- viewing evidence references
- reviewing approval status
- navigating to related pages

It must not execute sensitive academic actions until governance gates, permissions, audit, and approval execution contracts exist.

## Allowed Read-Only Interactions

Future dashboard pages may allow:

- filter by status
- filter by risk level
- filter by sensitivity level when role permits
- filter by owner role
- sort by due/review date
- open read-only detail panels
- view sanitized summaries
- view evidence references
- view approval state
- view notification delivery state
- navigate to related private pages
- copy non-sensitive reference IDs
- export only approved non-sensitive summaries when policy allows

## Blocked Interactions

The dashboard must not allow:

- approve/reject academic decisions
- change grades
- release assessments
- send guardian communications
- create or update intervention plans
- change student status
- finalize academic integrity findings
- publish public proof
- ingest LMS/SIS files
- connect external systems
- edit evidence classification
- bypass role access
- execute Public AI actions
- mutate workflows

## Button And Action Rules

Until implementation gates open:

```text
action buttons: not implemented
mutation controls: not implemented
approval controls: not implemented
send controls: not implemented
import controls: not implemented
```

If future UI prototypes need action affordances, they must be visibly disabled and documented as non-functional.

## Page Interaction Matrix

| Page | Allowed | Blocked |
| --- | --- | --- |
| Academic Dashboard | view KPIs, risks, summaries, navigation | mutate workflow, approve decisions |
| Academic Command Center | view health, next move, evidence refs | execute next move |
| Students | view scoped summaries | edit student records, change status |
| Teachers | view workload summaries | expose private teacher data outside scope |
| Courses | view course health | edit course setup |
| Assignments | view completion/missing work signals | alter submissions or outcomes |
| Assessments | view review/release status | release assessments, change grades |
| Academic Governance | view findings and review queues | finalize findings |
| Academic Support | view support cases | create clinical/legal decisions |
| Intervention Plans | view plan status | change plan or disclose without approval |
| Guardian Communications | view readiness and approval state | send communications |
| Academic Evidence | view references and permitted summaries | expose raw restricted evidence |
| Academic Close | view close summary | finalize or alter close state |
| Approvals | view approval queue/status | approve/reject |
| Notifications | view queue and delivery status | send/retry/dismiss |
| Readiness | view readiness checks | bypass gates |
| System Integrity | view health | execute repair actions |

## Evidence Interaction Rules

Evidence should be shown in tiers:

```text
tier 1: evidence exists / missing / stale
tier 2: evidence reference and summary
tier 3: evidence details only when role, sensitivity, and approval state allow
```

The dashboard may show evidence references before showing evidence details.

The dashboard must not show raw sensitive evidence to unauthorized roles.

## Approval Interaction Rules

Approvals may be visible as:

- pending
- approved
- rejected
- cancelled
- required
- not required

The first dashboard must not perform approval decisions.

Approval execution belongs to a later governed implementation block.

## Guardian Communication Interaction Rules

Guardian communications may show:

- readiness status
- approval required
- delivery status
- sensitivity level
- evidence reference

The dashboard must not send, retry, dismiss, generate, or edit guardian communications until governance gates exist.

## Adapter Interaction Rules

Adapter status may be visible as:

- not connected
- summary available
- review required
- ingestion blocked
- classification required

The dashboard must not collect credentials, import files, connect LMS/SIS systems, or trigger ingestion from UI in the first implementation scope.

## Export Rules

Exports are blocked by default.

If a future export is allowed, it must be:

- non-sensitive
- role-scoped
- approved by policy
- auditable
- stripped of private evidence
- separated from public surfaces

## Public Boundary

The private EduOS dashboard must not be accessible from public EduOS surfaces.

Public EduOS may describe dashboard capabilities at a high level, but must not expose live status, screenshots with real data, evidence references, student data, teacher data, guardian communication, assessment state, or governance state.

## Implementation Guardrails

This sketch does not:

- create EduOS dashboard code
- create Streamlit pages
- create UI components
- create database queries
- create APIs
- create permissions enforcement
- create approvals
- create notification delivery
- create LMS/SIS adapters
- create Public AI behavior
- create student data
- alter BusinessOS dashboard behavior

## Readiness Impact

This block moves EduOS from:

```text
dashboard interaction rules: missing
```

to:

```text
dashboard interaction rules: sketched
```

Implementation remains blocked until non-sensitive skeleton scope is defined.

## Recommended Next Blocks

```text
EduOS Non-Sensitive Skeleton Scope v0.1
EduOS Implementation Gate Refresh v0.2
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
