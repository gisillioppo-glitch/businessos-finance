# Area Review Freshness Doctrine and Operating Procedure v0.1

Date: 2026-05-20

## Purpose

This document defines how BusinessOS operators should understand, refresh, validate, and respond to area review freshness.

Area review freshness protects the executive operating view from silently relying on old or incomplete evidence. It is now part of the area review bundle, area review index, dashboard visibility, release readiness, and system integrity.

## Doctrine

BusinessOS should never present an executive area posture as current unless the supporting area review evidence is current.

Freshness doctrine:

```text
Executive area decisions require same-day area review evidence.
```

The dashboard may display freshness state, but it must not refresh evidence by itself. Refreshing evidence remains a controlled CLI operation.

Dashboard boundary doctrine:

```text
Dashboard shows evidence freshness; CLI refreshes evidence freshness.
```

## Freshness States

BusinessOS uses three area review freshness states:

```text
fresh
stale
missing
```

`fresh` means the latest area review report date matches the area review index date.

`stale` means the latest available area review report exists, but its date does not match the index date.

`missing` means an expected area review report does not exist.

## Current Area Sources

The current freshness model covers:

```text
Finance
Operations
Governance
Support
```

Each area produces its own area review report. The Area Review Executive Index reads those reports and records whether each source is fresh, stale, or missing.

## Normal Opening Procedure

At the start of a working session or demo preparation, run:

```text
python cli.py daily-close
python cli.py area-review-bundle
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected healthy result:

```text
Area review freshness: passed
Freshness status: fresh
Stale areas: 0
Missing areas: 0
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Refresh Command

Use the bundle command as the primary freshness refresh operation:

```text
python cli.py area-review-bundle
```

The bundle refreshes:

```text
Finance Area Review
Operations Area Review
Governance Area Review
Support Area Review
Area Review Executive Index
```

It then reports:

```text
Freshness status
Stale areas
Areas missing
Attention areas
Monitoring areas
Index report path
Next action
```

## Read-Only Commands

Use the index command when you only need to export or inspect the executive area review index:

```text
python cli.py area-review-index
```

This command summarizes latest available area review reports and freshness state, but it does not regenerate the source area reviews.

Use the dashboard only to view the latest exported state:

```text
streamlit run app/dashboard/main.py
```

The dashboard does not run `area-review-bundle`, does not mutate records, and does not silently refresh stale evidence.

## System Health Integration

`python cli.py system-check` now includes:

```text
Area review freshness
```

The check passes only when:

```text
latest area_review_index report exists
report date matches today
stale areas = 0
missing areas = 0
```

If this check fails, BusinessOS system health is not clean.

## Release Readiness Integration

`python cli.py release-readiness` also includes:

```text
Area review freshness
```

Release readiness passes this gate only when:

```text
latest area_review_index report exists
report date matches today
stale areas = 0
missing areas = 0
```

If this gate fails, the system should not be presented as ready for a controlled private demo.

## Dashboard Interpretation

The private dashboard exposes freshness in two places:

```text
Area Review Index
System Integrity
```

On `Area Review Index`, use the freshness summary to confirm:

```text
fresh areas
stale areas
missing areas
```

On `System Integrity`, use the `Area Review Freshness` signal to confirm whether the overall system health includes current area evidence.

## Failure Response

If freshness is `stale`, run:

```text
python cli.py area-review-bundle
python cli.py system-check
python cli.py release-readiness
```

If freshness is `missing`, run:

```text
python cli.py area-review-bundle
python cli.py area-review-index
python cli.py system-check
```

If freshness still fails after running the bundle:

```text
1. Check which area is stale or missing.
2. Confirm the expected area report was generated for today's date.
3. Confirm the Area Review Executive Index points to today's area reports.
4. Do not mark demo readiness as clean until stale and missing counts are zero.
```

## Demo Rule

Before a private demo, the operator should confirm:

```text
python cli.py area-review-bundle
python cli.py system-check
python cli.py release-readiness
```

Required result:

```text
Area review freshness: passed
release-readiness: ready
```

If freshness is stale or missing, pause demo preparation and refresh evidence first.

## Public Boundary

Area review freshness is private operating evidence.

It must not be published to the public landing surface, public AI surface, or unauthenticated website.

The public surface may describe that BusinessOS supports governed operational evidence, but it must not expose private area reports, area status, source report paths, owner names, approval details, or internal readiness results.

## Operator Summary

Use this sequence as the short memory:

```text
area-review-bundle refreshes evidence
area-review-index summarizes evidence
dashboard displays evidence
system-check audits evidence
release-readiness gates demo readiness
```

The system is ready only when all five agree that the area review evidence is fresh.
