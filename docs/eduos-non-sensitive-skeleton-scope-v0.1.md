# EduOS Non-Sensitive Skeleton Scope v0.1

Date: 2026-05-23

## Status

Closed for MVP validation.

## Purpose

This document defines the first safe implementation scope that EduOS may eventually open after docs-only planning.

The goal is not to implement the skeleton now. The goal is to define a narrow non-sensitive scope that can later be created without student data, guardian data, assessment content, database records, LMS/SIS adapters, Public AI, or workflow execution.

## Current Decision

```text
EduOS non-sensitive skeleton scope: defined
EduOS implementation: still not opened
EduOS runtime: still not opened
EduOS database: still not opened
EduOS dashboard: still not opened
EduOS adapters: still not opened
```

## Skeleton Doctrine

The first EduOS implementation must be boring on purpose.

It should prove folder structure, naming, docs/config posture, validation rhythm, and boundary discipline before any academic data or operational workflow exists.

## Allowed First Skeleton

The first non-sensitive skeleton may eventually include:

- README
- docs folder
- static configuration examples with synthetic labels only
- module registry document
- boundary registry document
- validation checklist
- no-op placeholder notes
- test plan document
- architecture index

If code is later allowed, the first code should be limited to:

- no-op health command
- static version metadata
- static docs index reader
- static config validation with synthetic values only

This code is not opened by this block.

## Explicitly Not Allowed

The first skeleton must not include:

- student records
- teacher records
- guardian records
- grades
- attendance
- assessment content
- intervention plans
- academic evidence records
- LMS/SIS exports
- database files
- database migrations
- real adapters
- Streamlit dashboard pages
- Public AI behavior
- approval execution
- notification delivery
- BusinessOS private reports
- BusinessOS private code copies
- secrets or credentials

## Allowed Folder Shape Later

If implementation is later approved, the first folder shape may be:

```text
eduos/
  README.md
  docs/
  config/
  app/
    __init__.py
  tests/
```

Only after explicit approval.

This shape must not be created by this block.

## Allowed Config Shape Later

Future static config may include:

```text
branch_name: EduOS
mode: non_sensitive_skeleton
implementation_status: skeleton_only
student_data_enabled: false
lms_adapters_enabled: false
dashboard_actions_enabled: false
public_ai_enabled: false
```

This is conceptual only.

## First Health Signal Later

Future no-op health output may say:

```text
EduOS skeleton health: ok
student data: disabled
lms/sis adapters: disabled
dashboard actions: disabled
public ai: disabled
```

This is conceptual only.

## Validation Requirements Before Skeleton Opens

Before creating implementation files:

- BusinessOS must be clean except known local artifacts.
- EduOS docs-only shell must remain free of sensitive files.
- Implementation gate must be refreshed.
- Non-sensitive skeleton scope must be approved.
- No BusinessOS private code should be copied blindly.
- No data files should be imported.
- No external integrations should be connected.

## Implementation Entry Criteria

The skeleton may be opened only when:

```text
implementation gate: ready_for_non_sensitive_skeleton
student data: disabled
database: not opened
dashboard actions: disabled
adapters: disabled
public ai: disabled
```

EduOS is not at this state yet.

The implementation gate refresh v0.2 later moved the gate to:

```text
implementation gate: ready_for_non_sensitive_skeleton
```

This still does not open implementation by itself.

The skeleton repository decision later approved this future local-only posture:

```text
future skeleton folder: C:\Users\fabia\OneDrive\Escritorio\OS\eduos-skeleton
initial git posture: local-only
remote repository: not opened yet
```

The skeleton opening checklist later moved the next step to:

```text
skeleton opening status: ready_to_open_non_sensitive_skeleton
```

## BusinessOS Separation

BusinessOS remains the private reference implementation.

EduOS skeleton must be separate and must not depend on BusinessOS runtime paths, database, reports, Streamlit dashboard, or private workflow state.

## Readiness Impact

This block moves EduOS from:

```text
first implementation scope: undefined
```

to:

```text
first implementation scope: non_sensitive_skeleton_defined
```

Implementation remains closed until the gate is refreshed.

## Recommended Next Blocks

```text
EduOS Non-Sensitive Skeleton Open v0.1
EduOS Skeleton Local Validation v0.1
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
