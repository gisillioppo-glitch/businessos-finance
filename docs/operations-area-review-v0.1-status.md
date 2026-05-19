# Operations Area Review v0.1

## Product Meaning

Operations Area Review v0.1 gives BusinessOS a formal area-level operations review artifact.

It evaluates the active operations task queue, detects current operational escalations, records the next operations move, and defines close criteria without completing or dismissing tasks automatically.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared operations review candidate
- Private data touched: read-only
- Public surface touched: no
- Approval required: no
- Evidence generated: yes
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats operations area review workflow

## Why It Matters

Command Center currently flags operations as part of the operating attention state. An operations area review gives the operator a clean answer:

```text
What is active?
What is escalated?
Can it close?
What evidence is needed next?
```

## Current Capabilities

- Adds `python cli.py operations-area-review`.
- Exports `reports/operations_area_review_YYYY-MM-DD.md`.
- Lists active operations tasks.
- Summarizes open, in-progress, blocked, critical, high, medium, and low task counts.
- Includes operations escalation review.
- Produces a review status and recommendation.
- Defines operations close criteria.
- Keeps task state unchanged.
- Adds standard/full smoke coverage for the command.

## Safety Boundary

This review does not complete, dismiss, reassign, or mutate operations tasks.

It is advisory and read-only except for exporting the review artifact and writing an audit log.

## Validation

Pending final block validation.

## Next Step

Use this review before deciding whether to complete active operations tasks, unblock dependencies, or keep work under monitoring.
