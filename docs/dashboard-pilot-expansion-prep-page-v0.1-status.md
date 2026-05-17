# Dashboard Pilot Expansion Prep Page v0.1

## Product Meaning

Dashboard Pilot Expansion Prep Page v0.1 brings the expansion review preparation packet into the protected dashboard.

It lets operators and leaders inspect whether a pilot is ready for an expansion review before looking at the advisory expansion decision page.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared pilot methodology candidate
- Private data touched: sanitized only
- Public surface touched: no
- Approval required: no
- Evidence generated: no
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats pilot expansion preparation workflow

## Why It Matters

Expansion preparation and expansion approval must remain separate. The prep page makes that boundary visible:

```text
prepare the review packet
review pending conditions
keep expansion not approved until governance clears it
```

This protects the pilot from accidental scope creep while still giving leadership a clear expansion review path.

## Current Capabilities

- Adds `Expansion Prep` to private dashboard navigation.
- Parses the latest `reports/pilot_expansion_review_prep_YYYY-MM-DD.md`.
- Shows expansion prep status, recommendation, pending conditions, missing required evidence, and exit risk.
- Displays the preparation condition gate.
- Displays preparation commands.
- Displays evidence to include in an expansion review.
- Displays review questions and boundaries.
- Keeps the page read-only.
- Keeps approval and decision recommendation in the separate `Pilot Expansion` page.

## Safety Boundary

The page does not approve expansion, add workflows, enable delivery, mutate pilot records, publish data, or bypass governance.

Operators refresh the artifact from CLI with `python cli.py pilot-expansion-review-prep`.

## Integration

- CLI source: `python cli.py pilot-expansion-review-prep`
- Dashboard page: `Expansion Prep`
- Reports: reads `reports/pilot_expansion_review_prep_YYYY-MM-DD.md`
- Governance: supports controlled pilot expansion preparation
- Public surface: none

## Validation

Pending final block validation.

## Next Step

Use this page before reviewing the advisory `Pilot Expansion` decision page.
