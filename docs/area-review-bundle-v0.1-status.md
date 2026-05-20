# Area Review Bundle v0.1

## Product Meaning

Area Review Bundle v0.1 gives BusinessOS one controlled command for refreshing all four area reviews and the executive index.

It refreshes:

```text
Finance Area Review
Operations Area Review
Governance Area Review
Support Area Review
Area Review Executive Index
```

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared multi-area review refresh candidate
- Private data touched: read-only
- Public surface touched: no
- Approval required: no
- Evidence generated: yes
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats multi-area review refresh workflow

## Why It Matters

The dashboard index should rely on fresh area review artifacts. The bundle lets operators refresh all area review evidence in one controlled step instead of running each area command manually.

## Current Capabilities

- Adds `python cli.py area-review-bundle`.
- Exports `reports/area_review_bundle_YYYY-MM-DD.md`.
- Refreshes Finance, Operations, Governance, and Support area reviews.
- Refreshes the Area Review Executive Index after area reports exist.
- Summarizes refreshed area reports, risks, index status, and next action.
- Adds standard/full smoke coverage for the command.

## Safety Boundary

This bundle does not complete finance actions, resolve operations tasks, approve governance decisions, close support incidents, send notifications, or mutate operational records.

It only refreshes review artifacts and writes audit logs.

## Validation

Pending final block validation.

## Next Step

Use this bundle before opening the Area Review Index dashboard page during a working session or demo.
