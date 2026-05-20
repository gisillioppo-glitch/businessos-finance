# System Integrity Area Review Freshness Check v0.1 Status

## Product Meaning

System Integrity Area Review Freshness Check v0.1 makes same-day area review evidence part of BusinessOS self-health.

Release readiness already uses area review freshness as a demo gate. This block adds the same evidence freshness signal to `system-check`, so system health can detect stale or missing executive area review evidence before release readiness is evaluated.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS executive evidence integrity rule
- Private data touched: read-only report metadata
- Public surface touched: no
- Approval required: no
- Evidence generated: yes
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after another vertical repeats system integrity checks for fresh executive evidence

## Scope

Included:

- system integrity check for latest area review index
- same-day date check
- stale area count check
- missing area count check
- system integrity report evidence

Not included:

- automatic area review regeneration
- dashboard mutation
- notification delivery
- public publishing

## Integrity Rule

System integrity passes the area review freshness check only when:

```text
latest area_review_index report exists
report date matches today
stale areas = 0
missing areas = 0
```

Otherwise, system integrity fails because executive area evidence is not fresh enough to trust.

## Validation

```text
py_compile OK
system-check OK: 58 passed / 1 warning / 0 failed during active edits
area review freshness check OK
release-readiness OK: 14 passed / 1 warning / 0 failed during active edits
runtime-stability OK: 7 passed / 1 warning / 0 failed during active edits
quick smoke OK: 10 commands

System check result:
Total checks: 59
Area review freshness: passed
Index report: reports/area_review_index_2026-05-19.md
Index date: 2026-05-19
Stale areas: 0
Missing areas: 0

Boundary coverage: 101/101
```

## Completion Criteria

This block is complete when:

- `system-check` includes `Area review freshness`
- the check passes with current same-day area review evidence
- py_compile passes
- system-check passes
- release-readiness passes
- quick smoke passes
- git status is clean except for the local `BussinessOS Avance.pdf`
