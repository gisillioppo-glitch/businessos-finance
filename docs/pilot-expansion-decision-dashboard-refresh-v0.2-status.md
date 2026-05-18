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

```text
py_compile OK
pilot-expansion-review-decision OK
dashboard loader check OK
system-check OK: passed, 58/58
release-readiness OK: ready, 14/14
runtime-stability OK: runtime_stable, 8/8
quick smoke OK: 10 commands
```

Decision result:

```text
Decision status: decision_ready_with_conditions
Recommended decision: maintain_narrow_pilot
Expansion prep status: prep_ready_with_conditions
Expansion status: not_approved
Pending conditions: 2
Missing required evidence: 0
```

Loader check:

```text
exists True
decision decision_ready_with_conditions
recommended maintain_narrow_pilot
rules 5
options 5
conditions 5
pending 2
```

All targeted and general validation passed.

## Next Step

Use this refreshed page after `Expansion Prep` and before any future controlled expansion approval block.
