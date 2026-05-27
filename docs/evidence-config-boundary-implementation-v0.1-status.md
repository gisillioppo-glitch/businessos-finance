# Evidence Config Boundary Implementation v0.1

Date: 2026-05-27

## Status

Closed for MVP validation.

## Purpose

This block implements the first BusinessOS-only evidence config boundary.

The goal is not to change evidence runtime behavior, extract code, create an OS Core package, open EduOS implementation, create shared evidence tables, change dashboard behavior, expose private reports, or send external delivery. The goal is to move branch-owned evidence defaults behind read-only accessors while preserving current BusinessOS behavior.

## Scope

- Add `app/evidence/config.py`.
- Move current evidence report registry behind read-only accessors.
- Move current department-to-report distribution mapping behind read-only accessors.
- Move delivery mode and subject prefix behind read-only accessors.
- Keep compatibility aliases in current modules.
- Keep report filenames, report labels, evidence purpose copy, distribution output, and notification queue behavior unchanged.

## Implementation

New config accessors:

```text
get_evidence_config
get_evidence_reports
get_evidence_statuses
get_department_reports
get_default_distribution_reports
get_distribution_delivery_mode
get_distribution_subject_prefix
```

The config is BusinessOS-only and read-only:

```text
branch_id: businessos
statuses: available, missing
evidence_reports: current BusinessOS evidence registry
department_reports: current BusinessOS distribution mapping
distribution_delivery_mode: email_ready_queue
distribution_subject_prefix: BusinessOS Daily Close
```

## Behavior Preservation

Preserved behavior:

- `python cli.py evidence-index` still reports 6 expected evidence items.
- evidence labels and report prefixes remain unchanged.
- `python cli.py daily-close` still exports the same daily close chain.
- `python cli.py daily-close-distribution` still prepares the same 4 recipient packages.
- distribution mode remains `email_ready_queue`.
- notification queue handoff remains unchanged.
- audit behavior remains unchanged.

## Extraction Boundary

This implementation improves future OS Core readiness, but extraction remains blocked.

Still blocked:

- OS Core package creation
- shared evidence schema
- shared database tables
- EduOS evidence implementation
- Public AI evidence access
- external evidence disclosure
- external delivery authority
- dashboard authority changes

## Recommended Next Blocks

```text
Evidence Registry Contract Tests v0.1
OS Core Approval Extraction Readiness Review v0.1
EduOS Skeleton Approval Decision Revisit v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: partially
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none_new
Runtime behavior: preserved
Approval behavior: unchanged
Notification delivery: unchanged
Remote publish: none
Code extraction: blocked
```

## Validation

Expected validation for this block:

```text
python -m py_compile app/evidence/config.py app/evidence/evidence_index.py app/evidence/daily_close_distribution.py
python cli.py evidence-index
python cli.py daily-close
python cli.py daily-close-distribution
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected result:

```text
py_compile: passed
evidence-index: passed
daily-close: passed
daily-close-distribution: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

Evidence now has a read-only BusinessOS config boundary. The next safe move is tests around evidence registry and distribution behavior, not extraction.
