# EduOS Concept Architecture v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This document defines EduOS as a future institutional operating system branch for education.

The goal is not to implement EduOS yet. The goal is to define the branch concept, domain modules, boundaries, OS Core inheritance candidates, BusinessOS analogs, and implementation guardrails before any EduOS code, database, dashboard, or public AI surface is created.

## Current Decision

```text
EduOS concept architecture: opened
EduOS implementation: not opened
EduOS repository/runtime: not opened
```

EduOS is now conceptually defined as a future branch.

EduOS is not implemented in BusinessOS.

## Strategic Position

EduOS should be a separate OS branch under the future OS Platform.

BusinessOS remains the reference implementation. EduOS should learn from BusinessOS patterns without copying BusinessOS domain logic.

Target doctrine:

```text
BusinessOS proves institutional OS patterns.
OS Platform defines shared contracts.
EduOS adapts those contracts to academic institutions.
```

## EduOS Mission

EduOS should help educational institutions operate with governed academic intelligence.

The system should support:

- academic visibility
- student support coordination
- course and assignment workflow awareness
- assessment governance
- academic integrity protection
- director/administrator decision support
- teacher workload visibility
- guardian communication governance
- academic evidence and daily/weekly close
- public/private separation for school-facing surfaces

EduOS should assist and recommend. It should not bypass teachers, directors, academic governance, or institutional authority.

## Future EduOS Branch Shape

```text
EduOS
|-- academic_command_center
|-- students
|-- teachers
|-- courses
|-- assignments
|-- assessments
|-- academic_governance
|-- academic_support
|-- academic_evidence
|-- academic_close
|-- guardian_communications
|-- learning_assistance
|-- approvals
|-- notifications
|-- dashboard
|-- readiness
|-- security
`-- system
```

This is a conceptual module map only.

## OS Core Patterns EduOS May Inherit

EduOS may eventually inherit or adapt these OS Core candidates:

- audit trail
- people and roles
- security/access boundary
- approval lifecycle
- governance policy engine
- sensitivity classification
- notification outbox and delivery approval
- evidence packet structure
- readiness framework
- system integrity checks
- runtime stability profiles
- scheduler status model
- dashboard shell
- command center synthesis pattern
- demo/pilot methodology
- public/private boundary doctrine

These patterns should be consumed through future contracts, not copied directly from BusinessOS code.

## EduOS-Owned Domain Areas

EduOS must define its own domain model for:

- students
- teachers
- directors/administrators
- guardians/families
- courses
- subjects
- assignments
- assessments
- grades or evaluation outcomes
- attendance or participation signals
- learning support needs
- academic incidents
- academic integrity events
- intervention plans
- school/district operating context

These are not BusinessOS finance, operations, or support objects.

## BusinessOS Pattern Analogs

| BusinessOS Pattern | EduOS Analog | Reuse Rule |
| --- | --- | --- |
| Finance rules | Academic risk and assessment integrity rules | Reuse rule shape, not finance thresholds. |
| Operations tasks | Academic workflows | Reuse workflow lifecycle, not BusinessOS task categories. |
| Support incidents | Student/teacher/academic support incidents | Reuse incident shape, not support categories. |
| Command Center | Academic Command Center | Reuse synthesis pattern, not business risk wording. |
| Daily Close | Academic Daily or Weekly Close | Reuse close packet shape, not business report content. |
| Evidence Index | Academic Evidence Index | Reuse evidence structure, not BusinessOS artifacts. |
| Approvals | Academic approvals | Reuse approval lifecycle with academic approval types. |
| Notifications | Guardian/staff/admin communications | Reuse outbox/delivery gate with education adapters. |
| Demo/pilot | School pilot methodology | Reuse methodology shape with academic language. |
| Public AI boundary | EduOS public explainer/intake | Reuse boundary doctrine, not private runtime. |

## EduOS Governance Concepts

EduOS governance must account for:

- student privacy
- assessment sensitivity
- academic integrity
- guardian communication controls
- intervention decisions
- teacher/admin role boundaries
- school policy enforcement
- auditability for academic decisions
- separation between recommendation and authority

EduOS should never make hidden academic decisions that bypass institutional review.

## EduOS Dashboard Concept

The future EduOS dashboard should be private and role-aware.

Possible read-only pages:

- Academic Dashboard
- Academic Command Center
- Students
- Courses
- Assignments
- Assessments
- Academic Governance
- Academic Support
- Evidence
- Academic Close
- Guardian Communications
- Approvals
- Notifications
- Readiness
- System Integrity

Dashboard implementation is not part of this block.

## EduOS Public Boundary Concept

Future EduOS public surfaces may:

- explain EduOS
- collect school demo interest
- qualify institution type and need
- route to private intake
- describe safe demo boundaries

Future EduOS public surfaces must not:

- access student records
- expose teacher data
- expose assessment data
- access private academic evidence
- execute approvals
- mutate academic workflows
- provide private live status publicly
- connect Public AI to private EduOS runtime

## EduOS Implementation Guardrails

Before implementation begins:

- create a separate project or repository when appropriate
- do not add EduOS runtime modules inside BusinessOS
- do not copy `finance.db`
- do not copy private BusinessOS reports
- do not copy BusinessOS dashboard state
- do not reuse BusinessOS finance rules
- document EduOS domain model first
- document EduOS governance model first
- document EduOS role model first
- sketch EduOS dashboard registry first
- sketch EduOS command center adapter first
- keep Public AI deny-by-default

## Current Readiness

```text
Concept architecture: ready
Domain model: sketched
Governance model: sketched
Dashboard registry: mapped
Command center adapter: sketched
Public/private boundary: sketched
Docs-only shell: opened
Academic evidence model: sketched
Implementation readiness gate: blocked_with_clear_path
Academic role access matrix: sketched
Implementation: blocked
```

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
