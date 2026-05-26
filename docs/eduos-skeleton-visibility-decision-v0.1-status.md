# EduOS Skeleton Visibility Decision v0.1

Date: 2026-05-25

## Status

Closed for MVP validation.

## Purpose

This block decides the future visibility posture for the EduOS skeleton if it later becomes a repository.

The goal is not to create a repository. The goal is to decide whether a future repo should start public or private, while keeping Git initialization, remote creation, publishing, runtime, database, dashboard, adapters, Public AI, approvals, delivery, and academic data blocked.

## Decision

```text
EduOS skeleton visibility decision: private_when_created
recommended_repo_name: eduos-skeleton
git_repository: not opened
remote_repository: blocked
public_repository: not approved
sensitive_implementation: blocked
```

If the skeleton later becomes a repository, it should start private.

Public visibility is not approved.

## Reason

Private-first visibility is required because:

- EduOS is still a skeleton
- public claims are not reviewed
- license/proprietary notice is not decided
- publish approval is missing
- Public AI boundaries remain blocked
- sensitive implementation is still blocked

## Local Skeleton Update

Added local visibility decision:

```text
C:\Users\fabia\OneDrive\Escritorio\OS\eduos-skeleton\docs\visibility-decision.md
```

No `.git` folder was created.

No remote repository was created.

No runtime, database, dashboard, adapter, Public AI, approval, notification delivery, or academic data files were created.

## Readiness Checklist Update

This resolves:

```text
Visibility decision: private_when_created
```

Still unresolved:

```text
License decision: missing
Public claim review: missing
Publish approval: missing
```

## Visibility Not Approved

Do not create:

- public GitHub repository
- public package
- public demo
- public docs site
- public AI surface
- public live status

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
visibility decision: missing
```

to:

```text
visibility decision: private_when_created
```

Remote publish and sensitive implementation remain blocked.

## Recommended Next Blocks

```text
EduOS Skeleton License Notice Decision v0.1
EduOS Skeleton Public Claims Review v0.1
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
