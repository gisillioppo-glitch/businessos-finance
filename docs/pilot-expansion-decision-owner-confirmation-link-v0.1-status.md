# Pilot Expansion Decision Owner Confirmation Link v0.1

## Product Meaning

Pilot Expansion Decision Owner Confirmation Link connects the advisory expansion review decision to the private pilot start confirmation state inherited through expansion prep.

This keeps the expansion decision recommendation grounded in the original start confirmation before any future controlled expansion approval. Operators can now see whether the decision recommendation is based on an owner-confirmed start, a conditional owner confirmation state, a missing confirmation state, or a blocked confirmation state.

## Boundary Classification

- Primary boundary: Private pilot expansion decision
- Secondary boundary: Owner confirmation / expansion decision governance candidate
- Private data touched: yes, reads private pilot start confirmation context through expansion prep
- Public surface touched: no
- Approval required: no automated approval; controlled expansion approval remains separate
- Evidence generated: yes, refreshes expansion decision with confirmation link
- Audit generated: yes, through existing expansion decision export when run with database connection
- Reusable core candidate: partial
- Extraction timing: after another OS vertical repeats confirmation-linked expansion decision governance

## Scope

This block updates:

- `app/demo/pilot_expansion_review_decision.py`
- `app/dashboard/main.py`
- `reports/pilot_expansion_review_decision_YYYY-MM-DD.md`
- README documentation
- boundary coverage index

## Behavior

The expansion decision artifact now includes:

- start confirmation status
- start confirmation report path
- start confirmation recommendation detail

The dashboard `Pilot Expansion` page now shows:

- linked start confirmation status
- linked confirmation artifact
- start confirmation recommendation panel

## Validation

Targeted validation:

```text
.venv\Scripts\python.exe -m py_compile app\demo\pilot_expansion_review_decision.py app\dashboard\main.py
.venv\Scripts\python.exe cli.py pilot-expansion-review-decision
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

- expansion decision exports confirmation status and report path
- dashboard Pilot Expansion page displays the confirmation link
- boundary coverage remains complete
- system-check passes
- release-readiness is ready
- quick smoke passes
- changes are committed, pushed, and tagged without staging unrelated local artifacts
