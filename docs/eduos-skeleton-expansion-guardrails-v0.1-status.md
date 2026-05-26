# EduOS Skeleton Expansion Guardrails v0.1

Date: 2026-05-25

## Status

Closed for MVP validation.

## Purpose

This block defines what may and may not be added to the local-only EduOS skeleton before any implementation begins.

The goal is to allow safe documentation/config growth while keeping runtime code, database files, dashboard implementation, adapters, Public AI, approvals, notification delivery, sensitive academic data, and remote repository creation blocked.

## Result

```text
EduOS skeleton expansion guardrails: defined
EduOS skeleton publish decision: keep_local_only
location: C:\Users\fabia\OneDrive\Escritorio\OS\eduos-skeleton
mode: non_sensitive_skeleton
remote_repository: not opened
sensitive implementation: blocked
```

## Allowed Without New Approval

Allowed:

- Markdown documentation
- JSON example config with disabled flags
- architecture indexes
- boundary notes
- validation notes
- no-op status descriptions
- synthetic labels with no real academic records

## Requires Explicit Approval

Requires a future approved block:

- Python files
- CLI commands
- app folders
- tests with executable code
- dashboard mock pages
- schema files
- adapters
- sample datasets
- Git repository initialization
- remote repository creation

## Always Blocked

Always blocked until a future sensitive implementation gate:

- real student data
- real teacher data
- real guardian data
- grades
- attendance
- assessment content
- academic evidence records
- database files
- migrations
- LMS/SIS/Classroom exports
- secrets
- credentials
- Public AI behavior
- approval execution
- notification delivery
- BusinessOS private code copies
- BusinessOS private reports

## Local Skeleton Update

Added local guardrail document:

```text
C:\Users\fabia\OneDrive\Escritorio\OS\eduos-skeleton\docs\expansion-guardrails.md
```

No runtime, database, dashboard, adapter, Public AI, approval, notification delivery, or remote repository files were created.

## Expansion Decision Rule

Every future expansion must answer:

```text
Does this add runtime behavior?
Does this add data?
Does this add integration?
Does this expose private state?
Does this copy BusinessOS internals?
Does this require approval?
```

If any answer is yes, stop and create a separate approval block before proceeding.

## BusinessOS Protection

BusinessOS remains private and separate.

No BusinessOS private files were copied into EduOS.

`BussinessOS Avance.pdf` remains untouched and untracked.

## Readiness Impact

This moves EduOS from:

```text
skeleton local validation: passed
```

to:

```text
skeleton expansion guardrails: defined
```

EduOS sensitive implementation remains blocked.

## Recommended Next Blocks

```text
EduOS Skeleton Branch Boundary Review v0.1
EduOS Skeleton Publish Readiness Checklist v0.1
```

## Boundary Classification

```text
OS Core candidate: no
BusinessOS-specific: no
EduOS-specific: yes
Public AI boundary: blocked
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: none
Notification delivery: none
Remote publish: blocked
```

## Validation

Validation expected for this block:

```text
EduOS skeleton sensitive-file scan
EduOS skeleton allowed-extension scan
EduOS skeleton ASCII docs/config check
EduOS skeleton Git repository check
BusinessOS system-check
BusinessOS release-readiness
BusinessOS runtime-stability
BusinessOS quick smoke
```

Expected result:

```text
skeleton scan: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```
