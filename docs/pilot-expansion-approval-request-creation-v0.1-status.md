# Pilot Expansion Approval Request Creation v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Product Meaning

Pilot Expansion Approval Request Creation converts the controlled pilot expansion approval draft into a formal pending approval request. It moves the process from read-only preparation into the governance approval queue while keeping expansion execution blocked until an authorized approval decision happens later.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared approval request creation candidate
- Private data touched: sanitized approval metadata only
- Public surface touched: no
- Approval required: yes
- Evidence generated: report and database approval request
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats approval request creation

## Scope

- Add `app/demo/pilot_expansion_approval_request_creation.py`.
- Add CLI command `python cli.py pilot-expansion-approval-request-creation`.
- Read the latest generated approval request draft context.
- Create or reuse one formal pending approval request in `approval_requests`.
- Export `reports/pilot_expansion_approval_request_creation_YYYY-MM-DD.md`.
- Add audit evidence for the creation/export step.
- Add the command to the full pilot smoke chain, not the standard daily smoke profile.

## Boundaries

- No controlled expansion approval.
- No workflow expansion.
- No external delivery enablement.
- No automatic approval status change.
- No public exposure of private pilot artifacts.
- No bypass of owner acknowledgement, pending conditions, or governance controls.

## Validation

Run:

```bash
python -m py_compile app/demo/pilot_expansion_approval_request_creation.py cli.py scripts/smoke_test.py
python cli.py pilot-expansion-approval-request-creation
python cli.py approvals
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```
