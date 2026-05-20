# Dashboard System Integrity Freshness Signal v0.1 Status

## Product Meaning

Dashboard System Integrity Freshness Signal v0.1 makes the new system-check area review freshness result visible as an executive dashboard signal.

System integrity now validates that the Area Review Index is same-day, not stale, and not missing area reviews. This block surfaces that result directly on the private System Integrity dashboard page.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS executive evidence integrity dashboard signal
- Private data touched: read-only report metadata
- Public surface touched: no
- Approval required: no
- Evidence generated: no
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after another vertical repeats dashboard visibility for integrity evidence freshness

## Scope

Included:

- dashboard parser support for system integrity rows with pipe characters in detail text
- extracted `Area review freshness` check
- dedicated dashboard panel for area review freshness
- read-only dashboard behavior

Not included:

- running system-check from dashboard
- automatic area review regeneration
- mutation of report artifacts
- notification delivery

## Dashboard Behavior

The private `System Integrity` page now shows a dedicated panel for:

```text
Area review freshness
status
source report
report date
stale areas
missing areas
```

The dashboard continues to read only the latest exported system integrity report.

## Validation

```text
py_compile OK
dashboard system integrity loader OK
system-check OK: 58 passed / 1 warning / 0 failed during active edits
release-readiness OK: 14 passed / 1 warning / 0 failed during active edits
runtime-stability OK: 7 passed / 1 warning / 0 failed during active edits
quick smoke OK: 10 commands

Dashboard loader result:
Total checks: 59
Area review freshness exists: yes
Area review freshness status: passed
Area review freshness detail: reports/area_review_index_2026-05-19.md | date: 2026-05-19 | stale areas: 0 | missing areas: 0

Boundary coverage: 102/102
```

## Completion Criteria

This block is complete when:

- dashboard loader parses `Area review freshness`
- dashboard page renders the freshness signal
- py_compile passes
- loader parse check passes
- system-check passes
- quick smoke passes
- git status is clean except for the local `BussinessOS Avance.pdf`
