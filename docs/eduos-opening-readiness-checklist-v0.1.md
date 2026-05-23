# EduOS Opening Readiness Checklist v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This checklist evaluates whether BusinessOS and the emerging OS Platform doctrine are ready to open EduOS as a future branch.

The goal is not to create EduOS yet. The goal is to decide what kind of EduOS work is safe now, what must wait, and what guardrails must be honored before implementation begins.

## Current Decision

```text
EduOS concept architecture: ready
EduOS repository/project opening: ready_with_conditions
EduOS implementation: not_ready_yet
```

BusinessOS is mature enough to support EduOS concept architecture work.

BusinessOS is not yet ready for direct EduOS implementation or code cloning.

## Readiness Summary

| Area | Status | Reason |
| --- | --- | --- |
| BusinessOS reference maturity | ready | Core operating loops, dashboard, reports, approvals, readiness, and validation are stable. |
| OS Core candidate mapping | ready | Major reusable layers have boundary readiness notes. |
| OS Platform map | ready | Parent architecture is documented. |
| Module stability matrix | ready | Stability and extraction risk are documented. |
| Public/private boundary | ready | Public AI and public surface limits are documented. |
| Domain adapter doctrine | ready | BusinessOS-specific logic is separated from reusable patterns. |
| Shared code extraction | not_ready | No shared package should be created until EduOS contracts are clearer. |
| EduOS domain model | not_ready | Student/course/teacher/assessment model is not documented yet. |
| EduOS dashboard registry | not_ready | Branch page registry pattern is not implemented. |
| EduOS command center adapter | not_ready | Academic synthesis adapter is not designed yet. |
| EduOS implementation | not_ready | Implementation would risk copying BusinessOS too directly. |

## Required Preconditions Before EduOS Implementation

Before implementing EduOS code:

- EduOS concept architecture must be documented.
- EduOS domain model must be documented separately from BusinessOS.
- EduOS role model must be documented separately from BusinessOS.
- Academic evidence requirements must be documented.
- Academic governance and assessment sensitivity rules must be mapped.
- EduOS dashboard page registry must be sketched.
- EduOS command center adapter shape must be sketched.
- Public/private boundary must be restated for EduOS.
- BusinessOS finance rules must not be copied into EduOS.
- Shared OS Core extraction must remain deferred until a real shared contract exists.

## Safe Work Now

The following EduOS-adjacent work is safe now:

- EduOS Concept Architecture v0.1
- EduOS Domain Model Sketch v0.1
- EduOS Governance Boundary Sketch v0.1
- EduOS Dashboard Surface Map v0.1
- EduOS Public/Private Boundary Sketch v0.1
- OS Core Contract Drafts v0.1

These are architecture and planning blocks only.

## Unsafe Work Now

The following should not happen yet:

- create EduOS runtime modules inside BusinessOS
- clone BusinessOS code into EduOS
- create shared OS Core package prematurely
- implement EduOS dashboard pages
- implement EduOS database schema
- implement EduOS AI behavior
- connect Public AI to private EduOS runtime
- create approval execution for EduOS
- reuse BusinessOS finance rules as academic rules

## Opening Modes

### Mode 1: Concept Only

Status: approved.

Allowed:

- architecture docs
- domain sketches
- boundary maps
- concept checklist
- future module list

Not allowed:

- runtime code
- database schema
- dashboard implementation
- workflow execution

### Mode 2: Separate Repo/Project Shell

Status: ready_with_conditions.

Allowed only if:

- it contains docs only
- no BusinessOS private files are copied
- no secrets, DB, reports, or dashboard artifacts are copied
- no implementation starts yet

### Mode 3: Implementation

Status: blocked for now.

Blocked until:

- EduOS concept architecture is closed
- EduOS domain model is closed
- EduOS governance model is closed
- branch adapter contracts are clearer
- BusinessOS remains stable after the planning blocks

## EduOS Guardrails

EduOS must:

- be a separate branch/project, not a module inside BusinessOS
- use academic domain language
- define its own data model
- define its own roles
- define its own governance sensitivity rules
- define its own evidence requirements
- inherit patterns, not BusinessOS content
- keep public AI outside private runtime
- keep approvals explicit and auditable
- keep dashboard actions read-only until governance gates exist

## BusinessOS Protection Rules

During EduOS planning:

- do not touch `finance.db`
- do not move BusinessOS private reports
- do not copy private dashboard state into public surfaces
- do not stage unrelated files
- do not touch `BussinessOS Avance.pdf`
- keep BusinessOS repo private
- keep landing/public surfaces separate
- validate BusinessOS after planning blocks

## Recommended Next Block

```text
EduOS Concept Architecture v0.1
```

Purpose:

- define EduOS as a separate future branch
- describe academic modules
- map BusinessOS patterns to EduOS analogs
- define what EduOS inherits and what it must own
- keep implementation deferred

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
