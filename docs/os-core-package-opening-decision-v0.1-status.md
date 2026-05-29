# OS Core Package Opening Decision v0.1

Date: 2026-05-28

## Status

Closed for architecture decision.

## Purpose

This block records whether BusinessOS is ready to open an OS Core package path before EduOS implementation.

The goal is not to extract code, create a shared runtime, move BusinessOS modules, open an EduOS implementation, publish a repository, or create public AI access. The goal is to make the operating decision explicit so the next blocks can proceed without ambiguity.

## Decision

```text
OS Core package opening: conditionally_approved_for_contract_planning_only
Shared code package: blocked
Code extraction: blocked
Repository creation: blocked_pending_explicit_approval
BusinessOS remains reference branch: yes
EduOS implementation remains blocked: yes
```

BusinessOS is now stable enough to define the OS Core package shape, boundaries, and adapter expectations.

BusinessOS is not yet approved to move runtime code into a shared package.

## What Is Approved

Approved now:

- document package boundaries
- document module families
- document adapter contracts
- document validation gates
- document rollback rules
- document branch registry expectations
- identify first package candidates
- keep all work inside BusinessOS docs unless a separate local-only planning folder is explicitly approved

## What Remains Blocked

Still blocked:

- moving `app/` code into `os-core`
- creating shared Python package code
- creating shared database schemas
- creating shared migrations
- creating shared runtime commands
- creating Public AI runtime access
- creating an OS Core remote repository
- publishing OS Core
- creating an EduOS runtime
- creating EduOS database, dashboard, adapters, approvals, or academic data
- copying BusinessOS private artifacts into EduOS or OS Core

## Required Gates Before Code Extraction

Before any code can move into a shared OS Core package, all of these must be true:

```text
1. Package boundary manifest drafted.
2. Branch adapter contract drafted.
3. At least one candidate family has extraction-ready contract status.
4. BusinessOS behavior has targeted contract tests.
5. Rollback plan is documented.
6. EduOS consumer scope is approved or another branch consumer is named.
7. Sensitive data remains denied by default.
8. Public AI runtime access remains blocked.
9. Approval-gated actions stay approval-gated.
10. Repository/package creation receives explicit approval.
```

## Initial Package Families

Eligible for contract planning:

| Family | Status | Reason |
| --- | --- | --- |
| Audit | planning_allowed | Strong branch-neutral event pattern. |
| Approvals | planning_allowed | Lifecycle, config, and contract tests already exist. |
| Evidence | planning_allowed | Registry and contract tests already exist. |
| Readiness/System | planning_allowed | Validation patterns are stable and repeated. |
| Security/People | planning_allowed | Strong shared pattern, needs branch role adapter. |
| Notifications | planning_allowed | Outbox and delivery approval shape is reusable. |
| Dashboard shell | planning_only | Runtime now stable, but pages remain BusinessOS-specific. |
| Demo/Pilot | planning_only | Methodology reusable, copy and workflow remain branch-specific. |

Not eligible for package extraction:

| Family | Status | Reason |
| --- | --- | --- |
| Finance rules | blocked | BusinessOS-specific domain logic. |
| CSV ingest | blocked | BusinessOS finance sample/data path. |
| Operations rules | blocked | BusinessOS workflow domain. |
| Support incidents | blocked | BusinessOS support domain. |
| Command Center implementation | blocked | Needs branch summary adapter first. |

## Approved Next Step

The next approved OS Core step is:

```text
OS Core Package Boundary Manifest v0.1
```

That block should define the future package map without moving code.

The next EduOS step remains:

```text
EduOS Skeleton Approval Decision Revisit v0.1
```

That block should revisit whether the local-only EduOS skeleton can move toward repository creation, still without implementation unless explicitly approved.

## Decision Rationale

BusinessOS has strong evidence of reusable operating patterns:

- approvals lifecycle and tests
- evidence registry and tests
- public/private denial checks
- readiness and runtime checks
- dashboard runtime stability
- boundary classification coverage
- daily close and evidence packaging

But code extraction now would still be premature because:

- only BusinessOS is implemented as runtime
- EduOS remains local-only and non-sensitive
- branch adapters are not fully drafted
- shared package ownership is not defined
- remote repository creation has not been explicitly approved

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: decision_only
Notification delivery: unchanged
Remote publish: blocked
Code extraction: blocked
Package opening posture: contract_planning_only
```

## Validation

Validation for this block:

```text
documentation ASCII check
system-check
release-readiness
runtime-stability
quick smoke
```

Expected result:

```text
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

This decision moves OS Core from vague future idea to controlled planning track. It does not create the package yet. BusinessOS remains the operating reference branch.
