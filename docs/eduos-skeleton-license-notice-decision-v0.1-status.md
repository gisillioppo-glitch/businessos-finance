# EduOS Skeleton License Notice Decision v0.1

Date: 2026-05-25

## Status

Closed for MVP validation.

## Purpose

This block decides the license and ownership posture for the local-only EduOS skeleton before any future repository creation or publication.

The goal is not to create a `LICENSE` file, publish the skeleton, create a repository, or approve external distribution. The goal is to prevent the skeleton from being interpreted as public or open source while EduOS remains private, local-only, and non-sensitive.

## Decision

```text
EduOS skeleton license decision: proprietary_notice_required
recommended_repo_name: eduos-skeleton
visibility_decision: private_when_created
license_file: not created
open_source_license: not approved
public_distribution: blocked
git_repository: not opened
remote_repository: blocked
sensitive_implementation: blocked
```

If the skeleton later becomes a private repository, it should include a proprietary/confidential notice before any remote push.

No open source license is approved.

## Reason

The skeleton must remain proprietary because:

- EduOS is still local-only
- public claims are not reviewed
- publish approval is missing
- OS Core ownership is not separated yet
- Public AI boundaries remain blocked
- sensitive implementation remains blocked
- academic data and adapters are not opened

## Local Skeleton Update

Added local license decision:

```text
C:\Users\fabia\OneDrive\Escritorio\OS\eduos-skeleton\docs\license-decision.md
```

Updated the local skeleton README with a proprietary notice.

No `.git` folder was created.

No `LICENSE` file was created.

No remote repository was created.

No runtime, database, dashboard, adapter, Public AI, approval, notification delivery, or academic data files were created.

## Readiness Checklist Update

This resolves:

```text
License decision: proprietary_notice_required
```

Still unresolved:

```text
Public claim review: missing
Publish approval: missing
```

## Still Blocked

Still blocked:

- `git init`
- GitHub repository creation
- remote push
- public repository
- public docs site
- `LICENSE` file creation
- open source license selection
- external distribution
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
license decision: missing
```

to:

```text
license decision: proprietary_notice_required
```

Remote publish and sensitive implementation remain blocked.

## Recommended Next Blocks

```text
EduOS Skeleton Public Claims Review v0.1
EduOS Skeleton Publish Approval Gate v0.1
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
License posture: proprietary_notice_required
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
