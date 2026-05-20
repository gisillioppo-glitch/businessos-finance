# Area Review Freshness Guard v0.1 Status

## Product Meaning

Area Review Freshness Guard prevents the executive area review index from silently relying on stale area reports.

The index now compares each source area review date with the index date and marks the area as:

```text
fresh
stale
missing
```

This keeps the dashboard and exported report honest about whether the visible area review posture is based on same-day evidence.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared executive evidence freshness pattern candidate
- Private data touched: read-only report metadata
- Public surface touched: no
- Approval required: no
- Evidence generated: yes
- Audit generated: yes, when exported with a database connection
- Reusable core candidate: partial
- Extraction timing: after a second vertical needs same-day evidence freshness checks

## Scope

Included:

- freshness field per area review source
- stale detection against the area review index date
- `area_review_index_stale` overall status
- stale area count in the exported report
- dashboard parsing for freshness and report date
- dashboard stale KPI and stale filter
- backward-compatible dashboard parsing for older five-column index reports

Not included:

- automatic regeneration from the dashboard
- mutation of Finance, Operations, Governance, or Support records
- external notifications
- email delivery

## Operator Flow

```text
python cli.py area-review-index
```

The command now reports stale area reviews if any source report date differs from the index date.

When stale reports are found, the recommended next action is:

```text
python cli.py area-review-bundle
```

## Dashboard Behavior

The private dashboard Area Review Index page now shows:

- overall area review index status
- reviewed area count
- attention area count
- stale area count
- missing area count
- freshness and report date per area
- stale status filter

The dashboard remains read-only.

## Validation

```text
py_compile OK
area-review-index OK
dashboard loader freshness parse OK
system-check OK: 57 passed / 1 warning / 0 failed during active edits
release-readiness OK: 13 passed / 1 warning / 0 failed during active edits
runtime-stability OK: 7 passed / 1 warning / 0 failed during active edits
quick smoke OK: 10 commands

Area review index result:
Overall status: area_review_attention_required
Areas reviewed: 4
Areas missing: 0
Stale areas: 0
Attention areas: 3
Monitoring areas: 1

Boundary coverage: 97/97
```

## Completion Criteria

This block is complete when:

- `area-review-index` exports freshness fields
- dashboard reads both current and older index report formats
- system-check passes
- release-readiness passes
- runtime-stability passes
- quick smoke passes
- git status is clean except for the local `BussinessOS Avance.pdf`
