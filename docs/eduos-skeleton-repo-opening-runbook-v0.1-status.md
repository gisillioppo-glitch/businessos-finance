# EduOS Skeleton Repo Opening Runbook v0.1

Date: 2026-05-25

## Status

Closed for MVP validation.

## Purpose

This block documents the future runbook for opening the EduOS skeleton as a private repository if explicit approval is granted later.

The goal is not to approve repository creation, run `git init`, create a remote repository, push to GitHub, publish docs, or open implementation. The goal is to make the future opening sequence controlled and auditable.

## Decision

```text
EduOS skeleton repo opening runbook: ready_when_approved
approval_required: yes
approval_decision: not_granted
repository_name: eduos-skeleton
visibility: private_when_created
repository_creation: blocked
git_repository: not opened
remote_repository: blocked
sensitive_implementation: blocked
```

The runbook is ready for future use only.

Approval is not granted in this block.

Do not execute repository commands yet.

## Preconditions

Before running any repository command:

- approval decision must be `approved`
- target repository name must be `eduos-skeleton`
- visibility must be private
- proprietary notice must remain required
- pre-publish local audit must be rerun
- sensitive-file scan must pass
- allowed-extension scan must pass
- ASCII check must pass
- no `.git` folder may exist before the opening block begins
- no runtime code may exist
- no academic data may exist
- no BusinessOS private artifacts may exist

## Future Runbook

Only after explicit approval:

1. Re-run local skeleton scans.
2. Confirm no `.git` folder exists.
3. Confirm only `.md` and `.json` files exist.
4. Confirm no `LICENSE` file exists unless a license/proprietary notice block approves it.
5. Create the private GitHub repository named `eduos-skeleton`.
6. Run `git init` inside the skeleton folder.
7. Add only approved skeleton files.
8. Commit the initial skeleton.
9. Add the private remote.
10. Push to the private remote.
11. Record remote URL and commit hash in a BusinessOS status document.
12. Re-run BusinessOS system-check, release-readiness, runtime-stability, and quick smoke.

## Commands Still Blocked

Do not run these now:

```text
git init
git add
git commit
git remote add
git push
```

## Local Skeleton Update

Added local repo opening runbook:

```text
C:\Users\fabia\OneDrive\Escritorio\OS\eduos-skeleton\docs\repo-opening-runbook.md
```

Updated the local skeleton README with the runbook status.

No `.git` folder was created.

No `LICENSE` file was created.

No remote repository was created.

No runtime, database, dashboard, adapter, Public AI, approval, notification delivery, or academic data files were created.

## Readiness Checklist Update

This resolves:

```text
Repo opening runbook: ready_when_approved
```

Still unresolved:

```text
Explicit private repository approval: missing
Repository creation execution: blocked
```

## Still Blocked

Still blocked:

- `git init`
- GitHub repository creation
- remote push
- public repository
- private repository creation
- public docs site
- public demo
- public AI explanation
- school-facing distribution
- marketing claims
- product readiness claims
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
repo opening runbook: missing
```

to:

```text
repo opening runbook: ready_when_approved
repository_creation: blocked
```

Remote publish and sensitive implementation remain blocked.

## Recommended Next Blocks

```text
EduOS Skeleton Private Repo Approval Decision v0.1
EduOS Skeleton Opening Pause / Handoff v0.1
```

## Boundary Classification

```text
OS Core candidate: no
BusinessOS-specific: no
EduOS-specific: yes
Public AI boundary: blocked
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: runbook_ready_approval_not_granted
Notification delivery: none
Remote publish: blocked
Repo opening posture: ready_when_approved
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
