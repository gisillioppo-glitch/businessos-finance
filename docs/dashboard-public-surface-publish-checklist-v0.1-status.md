# Dashboard Public Surface Publish Checklist v0.1

## Product Meaning

Dashboard Public Surface Publish Checklist v0.1 gives BusinessOS a protected internal go/no-go view for showing or publishing the public landing surface.

It turns public/private safety into an operator-facing checklist instead of requiring the presenter to infer publish readiness from separate reports.

## Boundary Classification

- Primary boundary: Security / public publish gate
- Secondary boundary: BusinessOS public surface readiness
- Private data touched: sanitized only
- Public surface touched: read-only inspection
- Approval required: no
- Evidence generated: yes
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second public surface repeats publish checklist pattern

## Why It Matters

BusinessOS now has a public landing, private dashboard, release readiness, surface audit, boundary index, and demo flow. Before a demo, pilot, sales conversation, or public publish, the operator needs one simple answer:

```text
Is the public surface safe to show?
```

This checklist answers that without publishing files or exposing private runtime internals.

## Current Capabilities

- Adds `python cli.py public-surface-publish-checklist`.
- Exports `reports/public_surface_publish_checklist_YYYY-MM-DD.md`.
- Adds `Publish Checklist` to private dashboard navigation.
- Shows public surface status as `safe`, `safe_with_warnings`, or `blocked`.
- Checks surface audit status, release readiness status, required public files, sensitive public paths, public inventory, lead intake surface, and local landing response.
- Links evidence artifacts for surface audit, release readiness, and system integrity.
- Keeps the dashboard page read-only.
- Adds standard/full smoke coverage for the new command.

## Safety Boundary

The checklist does not publish files, deploy the landing, expose secrets, publish the dashboard, mutate private runtime data, send email, or move files into `public/`.

It only reads existing public/static files and generates internal evidence reports.

## Validation

```text
py_compile OK
public-surface-publish-checklist OK
dashboard loader check OK
system-check OK: passed, 58/58
release-readiness OK: ready, 14/14
runtime-stability OK: runtime_stable, 8/8
quick smoke OK: 10 commands
```

Publish checklist result:

```text
Overall status: safe
Total checks: 7
Passed checks: 7
Warning checks: 0
Blocked checks: 0
Public files found: 5
Surface audit status: surface_ready
Release readiness status: ready
```

Loader check:

```text
exists True
status safe
checks 7
artifacts 3
guidance 4
blocked 0
```

All targeted and general validation passed.

## Next Step

Use this page before showing the public landing externally or preparing any publish action.
