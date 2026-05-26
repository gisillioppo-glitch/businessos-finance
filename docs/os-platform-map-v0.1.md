# OS Platform Map v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This document maps the future OS Platform as the parent architecture above BusinessOS, future EduOS, Public AI, OS Core candidates, and branch-specific domain adapters.

The goal is not to create a new repository, extract code, or implement EduOS yet. The goal is to define the platform shape before another OS branch is opened.

## Platform Position

The OS Platform is the future parent layer that should coordinate multiple institutional operating systems without merging their private data, domain models, or operational authority.

Current doctrine:

```text
BusinessOS -> harden -> identify reusable core -> design OS Platform -> design EduOS -> implement EduOS
```

BusinessOS remains the live reference implementation.

EduOS remains a future branch.

OS Platform remains an architecture map, not an active runtime in this block.

## Platform Shape

```text
OS Platform
|-- OS Core candidates
|   |-- audit
|   |-- security
|   |-- people
|   |-- approvals
|   |-- governance
|   |-- notifications
|   |-- evidence
|   |-- readiness
|   |-- runtime/system checks
|   |-- scheduler
|   |-- dashboard shell
|   |-- command synthesis pattern
|   `-- demo/pilot methodology
|
|-- Branches
|   |-- BusinessOS
|   |   |-- finance domain adapter
|   |   |-- operations domain adapter
|   |   |-- support domain adapter
|   |   |-- business rules
|   |   `-- business reports
|   |
|   `-- EduOS future
|       |-- academic domain adapter
|       |-- student/course/teacher models
|       |-- assessment governance
|       |-- academic support
|       `-- academic evidence
|
|-- Public AI boundary
|   |-- explanation
|   |-- public intake
|   |-- lead qualification
|   `-- private handoff
|
`-- Platform governance
    |-- branch registry
    |-- shared policy contracts
    |-- validation contracts
    |-- extraction rules
    `-- release gates
```

## Platform Responsibilities

The future OS Platform should provide:

- branch registry
- shared OS Core contracts
- branch-specific domain adapter contracts
- public/private boundary rules
- shared validation profile expectations
- release/readiness status comparison across branches
- governance policy contract shape
- evidence packet contract shape
- approval gate contract shape
- notification/delivery control contract shape
- dashboard shell and navigation contract shape
- public AI permission boundaries

## Platform Non-Responsibilities

The OS Platform should not:

- own BusinessOS finance logic
- own EduOS academic logic
- merge private branch databases
- bypass branch-level access control
- execute approvals without branch governance
- expose private reports publicly
- force one branch data model onto another
- make Public AI operational over private runtime
- treat BusinessOS wording as universal OS wording

## BusinessOS Role

BusinessOS is the first live branch and reference implementation.

BusinessOS currently proves:

- private institutional runtime
- dashboard protected surface
- command center synthesis
- release readiness and system integrity
- approval-gated decisions
- notification outbox and delivery controls
- evidence index and daily close
- demo and pilot methodology
- public/private repository split
- boundary classification discipline

BusinessOS should keep its enterprise domain logic inside the BusinessOS branch.

## EduOS Future Role

EduOS should become a separate branch only after enough platform contracts are clear.

EduOS should inherit:

- OS Core contracts
- governance patterns
- approval gates
- evidence packet patterns
- readiness checks
- dashboard shell patterns
- public/private boundary rules
- demo/pilot methodology shape

EduOS should define its own:

- academic domain adapters
- student/course/teacher data model
- assessment governance rules
- academic risk semantics
- teacher/director/guardian roles
- academic evidence requirements
- school/district demo and pilot language

EduOS is not opened in this block.

## Public AI Role

Public AI remains outside private branch runtimes.

Public AI may:

- explain branches
- qualify interest
- collect safe public intake
- route to private handoff
- explain public/private boundaries

Public AI must not:

- access private branch data
- execute branch workflows
- mutate approvals
- read private reports
- expose private dashboards
- present private live status publicly

## OS Core Contract Candidates

The current BusinessOS extraction map suggests these contract families:

| Contract Family | Current Readiness | Platform Direction |
| --- | --- | --- |
| Audit | L2 | Shared event timeline with domain metadata. |
| Security | L2 | Shared role/session/access boundary. |
| People | L2 | Shared institutional identity with branch roles. |
| Approvals | L2 | Shared approval lifecycle with branch approval types. |
| Governance | L2 | Shared policy engine with branch rule packs. |
| Notifications | L2 | Shared outbox/delivery gate with branch adapters. |
| Evidence | L2 | Shared evidence packet structure with branch registries. |
| Readiness | L2 | Shared validation framework with branch check registries. |
| System/runtime | L2 | Shared integrity/runtime checks with branch registries. |
| Scheduler | L2 | Shared recurring job status model. |
| Dashboard | L1 | Shared shell and read-only page patterns. |
| Command center | L1 | Shared synthesis pattern with branch adapters. |
| Demo/pilot | L1 | Shared methodology with branch-specific language. |
| Domain adapters | L0/L1 | Branch-owned data, rules, thresholds, and copy. |
| Public AI | Planning | Public boundary and intake layer only. |

## Extraction Guardrails

Before code moves into shared OS Core:

- extraction contract must be documented
- at least one branch must have a clear consumer need
- branch-specific copy must be removed from shared contracts
- branch-specific data models must stay in branch adapters
- public/private access must be enforced by design
- approvals must remain explicit and auditable
- evidence behavior must be policy-driven
- readiness checks must be configurable
- dashboard pages must use a branch registry
- command center must consume neutral branch summaries
- Public AI must remain deny-by-default

## Current Platform Readiness

BusinessOS reference maturity: high

OS Core candidate mapping: high

OS Core extraction contract readiness: draft

OS Core contract checklist readiness: draft

Shared code extraction readiness: medium-low

Branch adapter doctrine: medium-high

Public AI boundary doctrine: high

EduOS opening readiness: medium-high for concept architecture, not implementation.

## Recommended Next Blocks

```text
BusinessOS Module Stability Matrix v0.1
EduOS Opening Readiness Checklist v0.1
EduOS Concept Architecture v0.1
```

## Operator Note

This map is architectural. It does not create OS Platform runtime, create EduOS, split repositories, or extract shared packages. It defines the parent shape so future branches can be opened deliberately.
