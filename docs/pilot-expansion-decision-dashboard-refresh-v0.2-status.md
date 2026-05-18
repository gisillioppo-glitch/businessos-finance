# Pilot Expansion Decision Dashboard Refresh v0.2

## Product Meaning

Pilot Expansion Decision Dashboard Refresh v0.2 improves the private dashboard view for pilot expansion decision review.

It makes the distinction between preparation, advisory decision recommendation, and actual expansion approval more visible.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared pilot governance dashboard candidate
- Private data touched: sanitized only
- Public surface touched: no
- Approval required: no
- Evidence generated: yes
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats pilot expansion decision workflow

## Why It Matters

BusinessOS now has both `Expansion Prep` and `Pilot Expansion`. The decision page needs to be clear that it is advisory and does not approve scope expansion by itself.

This refresh adds a clearer decision boundary, decision rules, and highlights the current recommendation among allowed decision options.

## Current Capabilities

- Keeps `Pilot Expansion` as a read-only dashboard page.
- Parses `Decision Rules` from the latest `reports/pilot_expansion_review_decision_YYYY-MM-DD.md`.
- Adds a top-level decision boundary panel.
- Shows the recommended decision as advisory only.
- Shows expansion/prep state together without confusing preparation with approval.
- Highlights the current recommended decision in the decision options list.
- Keeps approval, workflow expansion, and delivery disabled.

## Safety Boundary

The page does not approve expansion, add workflows, enable delivery, mutate pilot state, publish data, or bypass governance.

Operators refresh the artifact from CLI with `python cli.py pilot-expansion-review-decision`.

## Validation

Pending final block validation.

## Next Step

Use this refreshed page after `Expansion Prep` and before any future controlled expansion approval block.
