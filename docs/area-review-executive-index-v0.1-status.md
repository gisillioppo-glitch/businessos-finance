# Area Review Executive Index v0.1

## Product Meaning

Area Review Executive Index v0.1 gives BusinessOS a single executive index across the four current area reviews:

```text
Finance
Operations
Governance
Support
```

It summarizes the latest available area review reports, highlights which areas need executive attention, and recommends the next area-level move without regenerating reviews or mutating records.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared executive review index candidate
- Private data touched: read-only
- Public surface touched: no
- Approval required: no
- Evidence generated: yes
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats multi-area review indexing

## Why It Matters

The area reviews are useful individually. The executive index answers the leadership-level question:

```text
Which area needs attention first?
```

## Current Capabilities

- Adds `python cli.py area-review-index`.
- Exports `reports/area_review_index_YYYY-MM-DD.md`.
- Reads latest Finance, Operations, Governance, and Support area review reports.
- Summarizes area status, risk, active signal, source report, and next action.
- Detects missing area reviews.
- Keeps underlying area records unchanged.
- Adds standard/full smoke coverage for the command.

## Safety Boundary

This index does not regenerate area reviews, complete actions, resolve incidents, approve governance decisions, or modify operational records.

It is advisory and read-only except for exporting the index artifact and writing an audit log.

## Validation

Pending final block validation.

## Next Step

Use this index as the top-level executive entry point before drilling into Finance, Operations, Governance, or Support area reviews.
