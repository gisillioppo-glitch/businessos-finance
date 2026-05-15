# Public Private Surface Audit v0.1

## Product Meaning

Public Private Surface Audit confirms that BusinessOS keeps its public landing surface separate from the private institutional runtime.

The audit inventories the static public files, verifies required landing assets, checks that blocked private files are not exposed under `public/`, confirms private protection patterns in `.gitignore`, and scans public text files for references to runtime internals or secrets.

## Boundary Classification

- Primary boundary: Security / public-private separation
- Secondary boundary: Demo readiness and deployment hygiene
- Private data touched: no
- Public surface touched: read-only inspection of `public/`
- Approval required: no
- Evidence generated: yes
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats public/private surface separation

## Scope

This block adds:

- `python cli.py public-private-surface-audit`
- `app/security/surface_audit.py`
- `reports/public_private_surface_audit_YYYY-MM-DD.md`
- session handoff awareness of the latest surface audit report
- README documentation

## Checks Covered

```text
required_public_files
blocked_public_paths
gitignore_private_patterns
public_reference_boundary
public_lead_intake_markers
```

## Expected Result

```text
Overall status: surface_ready
Failed checks: 0
```

## Validation

```text
py_compile OK
public-private-surface-audit OK
deployment_check OK
system-check OK
release-readiness OK
runtime-stability OK
quick smoke OK
```

Command result:

```text
Overall status: surface_ready
Total checks: 5
Passed checks: 5
Warning checks: 0
Failed checks: 0
Public files found: 5
```

## Git Closure

Pending final push, tag, and clean status verification.
