# EduOS Docs-Only Shell v0.1

Date: 2026-05-23

## Status

Closed for MVP validation.

## Purpose

This block opens the first visible EduOS project shell as documentation-only work.

The shell exists outside the BusinessOS private repo as:

```text
C:\Users\fabia\OneDrive\Escritorio\OS\eduos-docs-shell
```

The shell is not an EduOS implementation repo. It is a planning container that keeps EduOS separate from BusinessOS while avoiding runtime, database, dashboard, AI, or adapter work.

## Current Decision

```text
EduOS docs-only shell: opened
EduOS implementation: not opened
EduOS runtime: not opened
EduOS database: not opened
EduOS dashboard: not opened
EduOS Public AI: not opened
```

## Shell Contents

The shell currently contains:

```text
README.md
docs/guardrails.md
docs/index.md
```

These are docs-only files.

The shell was later organized under the local `OS` folder alongside other OS assets. BusinessOS remains in its active workspace and was not moved during this session.

## What Was Not Copied

The shell does not contain:

- `finance.db`
- BusinessOS private reports
- Streamlit dashboard files
- CLI runtime files
- secrets or credentials
- `.env`
- `.venv`
- private evidence packets
- student records
- teacher records
- guardian records
- LMS/SIS exports
- BusinessOS private workflow state

## Boundary Classification

Classification: docs-only future branch shell.

Data exposure:

```text
public conceptual docs only
no private BusinessOS data
no private EduOS data
no runtime access
```

Approval behavior:

```text
no approvals executed
no approval queues created
no governance decisions executed
```

Evidence behavior:

```text
no private evidence copied
no academic evidence created
no report evidence copied
```

Audit behavior:

```text
BusinessOS records this shell opening as a validated planning block.
The EduOS shell itself remains documentation-only.
```

Extraction timing:

```text
implementation extraction remains blocked.
OS Core extraction remains deferred.
EduOS code extraction remains not opened.
```

## Integration

BusinessOS remains the private reference system.

EduOS now has a separate visible docs-only shell for future planning, but no operating surface.

The shell supports the sequence:

```text
BusinessOS stable reference
OS Platform doctrine
EduOS concept docs
EduOS docs-only shell
future EduOS implementation gate
```

## Validation

Validation performed:

```text
docs shell created
shell docs ASCII OK
no private files copied
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

## Recommended Next Blocks

```text
EduOS Academic Evidence Model Sketch v0.1
EduOS Implementation Readiness Gate v0.1
```
