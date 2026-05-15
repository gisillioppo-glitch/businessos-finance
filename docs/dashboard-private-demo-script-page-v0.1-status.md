# Dashboard Private Demo Script Page v0.1

## Product Meaning

Dashboard Private Demo Script Page v0.1 brings the private demo script into the protected dashboard.

Operators can now review the presentation arc, timeboxes, talk track, proof points, demo commands, boundaries, closing questions, and closing statement without opening the Markdown artifact directly.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared demo narrative candidate
- Private data touched: sanitized only
- Public surface touched: no
- Approval required: no
- Evidence generated: no
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats private demo narrative workflow

## Current Capabilities

- Adds `Demo Script` to private dashboard navigation.
- Parses the latest `reports/private_demo_script_YYYY-MM-DD.md`.
- Shows script readiness context, segment count, command count, closing question count, and known risk count.
- Displays the demo arc with timebox, screen, talk track, and proof point.
- Displays demo commands as read-only operator guidance.
- Displays pre-demo checklist, do-not-show boundaries, closing questions, and suggested closing statement.
- Keeps the page read-only.

## Safety Boundary

The dashboard page does not run demo commands, execute checks, open public surfaces, expose secrets, send email, mutate reports, or publish artifacts.

Operators refresh the artifact from CLI with `python cli.py private-demo-script`.

## Integration

- CLI source: `python cli.py private-demo-script`
- Dashboard page: `Demo Script`
- Reports: reads `reports/private_demo_script_YYYY-MM-DD.md`
- Database: none
- Governance: supports controlled private demo operation
- Public surface: none

## Validation

```text
py_compile OK
private-demo-script OK
loader check OK
boundary coverage OK: 80/80
system-check OK: 57/57
release-readiness OK: ready, 14/14
runtime-stability OK: runtime_stable, 8/8
quick smoke OK: 10 commands
```

Loader check:

```text
exists True
segments 7
commands 5
questions 4
risks 4
pages 28
boundary_pages 30
has_demo_script True
```

All targeted and general validation passed.

## Git Closure

Pending final handoff, push, tag, and clean status verification.

## Next Step

Use this page as the private demo run-of-show view after the demo package and demo readiness gates are current.
