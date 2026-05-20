# Smoke Profile Capacity Rebalance v0.1

## Product Meaning

Smoke Profile Capacity Rebalance v0.1 keeps BusinessOS standard smoke below the runtime warning threshold while preserving meaningful validation coverage.

The prior standard profile had grown to `59/60` commands after the Area Review Index and dashboard page work. This block removes duplicate notification and delivery checks from the early standard/full sequence while keeping the post-daily-close checks that validate the same surfaces after fresh evidence generation.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS runtime validation profile
- Private data touched: no
- Public surface touched: no
- Approval required: no
- Evidence generated: no
- Audit generated: no
- Reusable core candidate: yes
- Extraction timing: after second vertical repeats smoke profile growth control

## Why It Matters

BusinessOS adds features in small blocks. Without profile hygiene, the standard smoke can become too large for daily work and start warning during normal development.

This keeps:

```text
quick    -> fast opening check
standard -> daily development validation
full     -> deep release checkpoint
```

## Current Capabilities

- Removes duplicate early notification checks from standard smoke.
- Removes the same duplicate early notification checks from full smoke.
- Keeps notification, delivery approval, and secure email validation later in the flow.
- Preserves pilot chain separation in full profile.
- Keeps the standard profile below the runtime warning threshold.

## Safety Boundary

This block does not change product behavior, database state, dashboard behavior, delivery behavior, approvals, or report generation.

It only changes smoke profile composition.

## Validation

Pending final block validation.

## Next Step

Use the recovered smoke profile capacity before adding new commands to standard smoke.
