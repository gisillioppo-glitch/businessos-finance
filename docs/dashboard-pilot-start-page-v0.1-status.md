# Dashboard Pilot Start Page v0.1

## Product Meaning

Dashboard Pilot Start Page brings the private pilot start gate into the protected BusinessOS dashboard.

It gives the operator and executive owner a read-only view of whether Day 1 can begin, whether conditions must be accepted, or whether the pilot is blocked before execution starts.

## Boundary Classification

- Primary boundary: Private dashboard / pilot operations
- Secondary boundary: Shared pilot governance candidate
- Private data touched: yes, reads private pilot start gate report
- Public surface touched: no
- Approval required: no, dashboard is read-only
- Evidence generated: no, dashboard reads existing artifact only
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after another OS vertical repeats pilot start dashboard pattern

## Scope

This block adds:

- `Pilot Start` to private dashboard navigation
- start gate status KPIs
- passed, conditional, and blocked gate counts
- executive recommendation panel
- gate check filter
- pilot owner and primary workflow visibility
- linked demo final review, pilot plan, and tracker status
- start/no-start conditions
- Day 1 operator actions

## Read-Only Rule

The dashboard page does not start a pilot and does not mutate system state.

Operators refresh the artifact with:

```text
python cli.py private-pilot-start-gate
```

The dashboard then reads:

```text
reports/private_pilot_start_gate_YYYY-MM-DD.md
```

## Integration

The page is connected to:

- `app/dashboard/main.py`
- `app/security/access_control.py`
- `app/readiness/release_readiness.py`
- `reports/private_pilot_start_gate_YYYY-MM-DD.md`

## Validation

Targeted validation:

```text
.venv\Scripts\python.exe -m py_compile app\dashboard\main.py app\security\access_control.py app\readiness\release_readiness.py
.venv\Scripts\python.exe cli.py private-pilot-start-gate
```

Closure validation:

```text
.venv\Scripts\python.exe cli.py system-check
.venv\Scripts\python.exe cli.py release-readiness
.venv\Scripts\python.exe cli.py runtime-stability
.venv\Scripts\python.exe scripts\smoke_test.py quick
```

## Completion Criteria

This block is complete when:

- `Pilot Start` appears in private dashboard navigation
- the page parses and displays the latest start gate artifact
- release readiness includes the new dashboard page
- boundary coverage remains complete
- system-check passes
- release-readiness is ready
- quick smoke passes
- changes are committed, pushed, and tagged without staging unrelated local artifacts
