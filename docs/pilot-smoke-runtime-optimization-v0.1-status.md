# Pilot Smoke Runtime Optimization v0.1

Date: 2026-05-12

## Status

Closed for MVP validation.

## Product Meaning

This block reduces daily validation friction while preserving full release coverage. BusinessOS now separates smoke testing into quick, standard, and full profiles so the first live OS branch can be checked frequently without repeatedly running the heavy pilot package chain.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS validation workflow
- Private data touched: no
- Public surface touched: no
- Approval required: no
- Evidence generated: report only
- Audit generated: no
- Reusable core candidate: yes
- Extraction timing: after second vertical reuses profile-based smoke validation

## Scope

- Add smoke profiles: `quick`, `standard`, and `full`.
- Keep `standard` as the default smoke profile.
- Reserve the heavy pilot chain for the `full` profile.
- Use the active Python executable for subprocess commands.
- Add per-command timing and timeout handling.
- Update runtime stability review so it measures the optimized default profile and records full-profile heavy commands separately.

## Commands

```bash
python scripts/smoke_test.py quick
python scripts/smoke_test.py
python scripts/smoke_test.py full
```

## Boundaries

- Full validation remains available.
- Pilot commands remain approval-gated.
- No governance, approval, or expansion behavior is weakened.
- This block optimizes smoke execution structure, not business logic.

## Validation

Run:

```bash
python -m py_compile scripts/smoke_test.py app/system/runtime_stability.py
python scripts/smoke_test.py quick
python scripts/smoke_test.py
python cli.py runtime-stability
```
