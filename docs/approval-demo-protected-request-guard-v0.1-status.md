# Approval Demo Protected Request Guard v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Product Meaning

Approval Demo Protected Request Guard prevents generic demo approval commands from changing protected pilot expansion approval requests. This keeps smoke and demo flows useful while ensuring controlled expansion approvals cannot be accidentally approved or rejected by broad demo commands.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS protected approval source policy
- Private data touched: approval metadata only
- Public surface touched: no
- Approval required: yes
- Evidence generated: no
- Audit generated: no new audit path
- Reusable core candidate: yes
- Extraction timing: before EduOS reuses demo-safe approval flows

## Scope

- Update `app/approvals/approval_status.py`.
- Keep `approval-approve` and `approval-reject` demo commands available.
- Exclude `source_module = pilot_expansion` from generic demo approval selection.
- Preserve explicit approval status update helpers for future targeted governance workflows.
- Avoid approving, rejecting, cancelling, or otherwise mutating the pilot expansion approval request.

## Boundaries

- No approval status change for the pilot expansion request.
- No controlled expansion approval.
- No workflow expansion.
- No external delivery enablement.
- No public exposure of private pilot artifacts.
- No bypass of governance controls.

## Validation

Run:

```bash
python -m py_compile app/approvals/approval_status.py
python cli.py approvals
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```
