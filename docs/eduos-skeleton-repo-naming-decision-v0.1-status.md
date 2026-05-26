# EduOS Skeleton Repo Naming Decision v0.1

Date: 2026-05-25

## Status

Closed for MVP validation.

## Purpose

This block decides the recommended future repository name for the local-only EduOS skeleton.

The goal is not to create a repository. The goal is to approve a name that does not imply production readiness, live academic data, shared OS Core, platform maturity, or public availability.

## Decision

```text
EduOS skeleton repo naming decision: approved_with_conditions
recommended_repo_name: eduos-skeleton
git_repository: not opened
remote_repository: blocked
sensitive_implementation: blocked
```

Recommended future repository name:

```text
eduos-skeleton
```

## Reason

This name is intentionally limited.

It communicates:

- EduOS branch context
- skeleton-only maturity
- no production claim
- no live academic data
- no platform/core claim

## Names Not Approved

Do not use:

- `eduos`
- `eduos-platform`
- `eduos-production`
- `eduos-live`
- `eduos-core`
- `os-platform-eduos`

These names imply runtime, production, shared core, or platform maturity that does not exist yet.

## Local Skeleton Update

Added local repo naming decision:

```text
C:\Users\fabia\OneDrive\Escritorio\OS\eduos-skeleton\docs\repo-naming-decision.md
```

No `.git` folder was created.

No remote repository was created.

No runtime, database, dashboard, adapter, Public AI, approval, notification delivery, or academic data files were created.

## Readiness Checklist Update

This resolves:

```text
Repo naming decision: approved_with_conditions
```

Still unresolved:

```text
Visibility decision: missing
License decision: missing
Public claim review: missing
Publish approval: missing
```

## Still Blocked

Still blocked:

- `git init`
- GitHub repository creation
- remote push
- runtime code
- CLI commands
- dashboard pages
- API routes
- database files
- database migrations
- data imports
- student records
- teacher records
- guardian records
- grades
- attendance
- assessments
- academic evidence records
- LMS/SIS/Classroom adapters
- Public AI behavior
- approvals
- notification delivery
- shared OS Core package
- BusinessOS private copies

## BusinessOS Protection

BusinessOS remains private and separate.

No BusinessOS private files were copied into EduOS.

`BussinessOS Avance.pdf` remains untouched and untracked.

## Readiness Impact

This moves EduOS from:

```text
repo naming decision: missing
```

to:

```text
repo naming decision: approved_with_conditions
```

Remote publish and sensitive implementation remain blocked.

## Recommended Next Blocks

```text
EduOS Skeleton Visibility Decision v0.1
EduOS Skeleton License Notice Decision v0.1
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
