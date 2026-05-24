# EduOS Skeleton Repository Decision v0.1

Date: 2026-05-24

## Status

Closed for MVP validation.

## Purpose

This document decides the repository and folder posture for the first future EduOS non-sensitive skeleton.

The goal is not to create the skeleton in this block. The goal is to decide where it may live, what it may be called, what it may contain, and what remains blocked before any files are created.

## Current Decision

```text
EduOS skeleton decision: approved_with_conditions
EduOS skeleton opening checklist: passed_with_conditions
EduOS skeleton creation: not opened in this block
EduOS sensitive implementation: blocked
```

EduOS may proceed to a future skeleton opening checklist.

EduOS must not create runtime, database, dashboard, adapters, Public AI, approvals, notification delivery, or academic records in this block.

## Repository Posture

The first EduOS skeleton should begin as a local project folder under the existing OS workspace:

```text
C:\Users\fabia\OneDrive\Escritorio\OS\eduos-skeleton
```

Initial posture:

```text
local-only
non-sensitive
docs-config-no-op
not connected to BusinessOS runtime
not connected to public surfaces
not connected to LMS/SIS/Classroom
```

The skeleton should not become a separate GitHub repository until it passes its own opening checklist and a later publish decision.

## Why Local-Only First

Local-only first is preferred because it:

- avoids publishing premature structure
- avoids copying private BusinessOS code
- keeps EduOS separate from BusinessOS runtime
- allows guardrails to be validated before repo creation
- keeps naming, docs, config, and validation flexible
- prevents accidental data, secrets, or dashboard exposure

## Naming Decision

Recommended folder name:

```text
eduos-skeleton
```

Reason:

- clear purpose
- no implication of production readiness
- separate from `eduos-docs-shell`
- separate from BusinessOS
- easy to promote later if approved

Not recommended:

```text
eduos
eduos-production
eduos-platform
eduos-live
```

These names imply more maturity than the skeleton has.

## Relationship To Existing Shell

Existing shell:

```text
C:\Users\fabia\OneDrive\Escritorio\OS\eduos-docs-shell
```

Future skeleton:

```text
C:\Users\fabia\OneDrive\Escritorio\OS\eduos-skeleton
```

The docs-only shell remains a planning artifact.

The future skeleton may reference shell decisions, but must not copy private BusinessOS runtime files, database files, reports, dashboard state, secrets, or generated artifacts.

## Allowed First Skeleton Contents

If opened in a later block, the first skeleton may contain only:

- `README.md`
- `docs/`
- `config/` with non-sensitive example labels only
- module registry document
- boundary registry document
- validation checklist
- no-op health metadata document
- no-op architecture index

Optional code remains blocked unless explicitly approved by a later block.

## Blocked Contents

The skeleton must not include:

- student records
- teacher records
- guardian records
- grades
- attendance
- assessments
- academic evidence records
- intervention plans
- LMS/SIS/Classroom exports
- database files
- database migrations
- Streamlit dashboard pages
- API routes
- CLI commands
- Public AI behavior
- approval execution
- notification delivery
- BusinessOS private code copies
- BusinessOS private reports
- `finance.db`
- `.env`
- `.venv`
- Streamlit secrets

## Git Decision

Initial skeleton git posture:

```text
git repository: not opened yet
remote repository: not created yet
publish status: blocked
```

The skeleton should become its own repository only after:

- opening checklist passes
- sensitive scan passes
- BusinessOS remains clean
- folder boundaries are stable
- no private artifacts are present
- a publish decision block explicitly approves it

## Validation Decision

Before any skeleton files are created, validate:

```text
BusinessOS system-check
BusinessOS release-readiness
BusinessOS runtime-stability
BusinessOS quick smoke
EduOS docs shell sensitive-file scan
```

After skeleton files are created in a future block, validate:

```text
no non-Markdown or approved config files unless explicitly allowed
no database files
no secrets
no private BusinessOS files
no real academic records
ASCII docs check
BusinessOS quick smoke
```

## BusinessOS Protection

During future skeleton opening:

- do not move active BusinessOS workspace
- do not stage unrelated files
- do not touch `BussinessOS Avance.pdf`
- do not copy `finance.db`
- do not copy reports into EduOS
- do not copy BusinessOS dashboard state
- do not create shared OS Core package
- do not use `git add .`

## Decision Result

```text
EduOS skeleton repository decision: approved_with_conditions
Recommended skeleton location: C:\Users\fabia\OneDrive\Escritorio\OS\eduos-skeleton
Recommended git posture: local-only, no remote yet
Recommended next step: EduOS Skeleton Opening Checklist v0.1
```

## What This Opens

This opens only the next planning block:

```text
EduOS Skeleton Opening Checklist v0.1
```

It does not create the skeleton.

It does not open EduOS implementation.

## Recommended Next Blocks

```text
EduOS Non-Sensitive Skeleton Open v0.1
EduOS Skeleton Local Validation v0.1
```

## Validation

Validation expected for this block:

```text
docs ASCII check
EduOS docs shell sensitive-file scan
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
