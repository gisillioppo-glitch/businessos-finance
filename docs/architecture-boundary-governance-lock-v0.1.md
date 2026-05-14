# Architecture Boundary Governance Lock v0.1

Date: 2026-05-13

## Purpose

This lock defines the minimum closure standard for future BusinessOS blocks.

BusinessOS now has enough system controls, readiness gates, boundary classification, runtime checks, and handoff tooling that new work should not close informally.

The goal is to keep the project moving fast without letting architecture, security, public/private separation, or Git hygiene drift.

## Required Closure Rule

Every meaningful block must close with:

```text
1. Status document with Boundary Classification
2. Targeted validation
3. system-check when the block affects system health, reports, dashboard, readiness, security, or docs coverage
4. release-readiness when the block affects demo readiness, dashboard navigation, public/private boundaries, reports, or release artifacts
5. session-handoff when the block changes the recommended next state or before a long break
6. Explicit git add paths only
7. Commit
8. Push
9. Tag for completed product blocks
10. Final git status clean except known local artifacts
```

Known local artifact:

```text
BussinessOS Avance.pdf
```

This file must remain untracked, unstaged, unmodified, and outside commits.

## Validation Tiers

Use the smallest tier that fits the risk.

### Tier 1: Documentation-Only

Use for docs that do not change runtime code.

Required:

```text
Boundary Classification present
ASCII or intentional charset check
git diff --check
explicit git add paths
commit + push + tag when it closes a named block
```

Recommended:

```text
system-check
session-handoff
```

### Tier 2: Targeted Runtime Change

Use for one module, one CLI command, one parser, or one report.

Required:

```text
py_compile for touched Python files
targeted CLI command
Boundary Classification coverage remains 100%
system-check
explicit git add paths
commit + push + tag
```

Recommended:

```text
release-readiness if dashboard, reports, public/private boundary, or demo readiness is touched
session-handoff if next block state changes
```

### Tier 3: Dashboard / Readiness / Governance Change

Use for private dashboard pages, navigation, system-check, release-readiness, boundary guards, handoff, security, or public/private safety.

Required:

```text
py_compile for touched Python files
targeted import or command check
system-check
release-readiness
session-handoff when operator state changes
explicit git add paths
commit + push + tag
```

Recommended:

```text
quick smoke after shared utility or gate changes
```

### Tier 4: Release Checkpoint

Use before demos, long breaks, major branching, external review, or after multiple related blocks.

Required:

```text
quick smoke
system-check
release-readiness
runtime-stability
session-handoff
push + tag
final git status
```

Use full smoke only for deeper release checkpoints or when pilot-heavy flows changed.

## Boundary Lock

No new status document should close without:

```text
## Boundary Classification
```

The shared boundary guard must remain active in:

```text
python cli.py system-check
python cli.py release-readiness
```

Coverage should remain:

```text
100%
```

If coverage drops, stop feature work and repair the missing status document before continuing.

## Public / Private Lock

BusinessOS private runtime must stay separate from the public landing surface.

Private runtime includes:

```text
finance.db
reports/
app/
audit logs
approval decisions
daily close artifacts
notification outbox
dashboard pages
system integrity
release readiness
session handoff
```

Public surface includes:

```text
public/
businessos-landing
lead intake
sanitized public copy
```

Do not move private runtime data or internal reports into public surfaces.

## Git Lock

Never use broad staging while local artifacts are present.

Use:

```text
git add path/to/file
git add path/to/other-file
```

Do not use:

```text
git add .
```

Before commit, confirm:

```text
git diff --cached --name-only
git status --short
```

After push and tag, confirm:

```text
git status --short
git ls-remote origin main
git ls-remote --tags origin <tag>
```

## Handoff Lock

Before long breaks, chat changes, or context resets, run:

```text
python cli.py session-handoff
```

The latest handoff should capture:

```text
latest commit
git status
Boundary Classification coverage
latest system artifacts
recommended next blocks
known local artifacts
```

## Operating Meaning

This lock does not slow BusinessOS down. It defines the rails that let BusinessOS keep moving quickly without losing institutional control.

The expected rhythm is:

```text
small block
targeted validation
system/readiness check when relevant
commit
push
tag
handoff when useful
```

## Review Trigger

Revisit this lock when one of these happens:

```text
EduOS starts
OS Core extraction begins
external delivery becomes live
public AI boundary becomes interactive
multiple contributors work in the repo
CI/CD is introduced
```
