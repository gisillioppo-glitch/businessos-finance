# Pilot Expansion Approval Request Draft v0.1

Date: 2026-05-21

## Status

Closed for MVP validation.

## Product Meaning

Pilot Expansion Approval Request Draft prepares the first formal request shape for a future controlled pilot expansion approval. It converts approval gate prep context into a decision-type approval draft without inserting a pending approval request into the database.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared approval request drafting candidate
- Private data touched: sanitized only
- Public surface touched: no
- Approval required: yes
- Evidence generated: report only
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats approval request drafting

## Scope

- Add `app/demo/pilot_expansion_approval_request_draft.py`.
- Add CLI command `python cli.py pilot-expansion-approval-request-draft`.
- Read approval gate prep context.
- Export `reports/pilot_expansion_approval_request_draft_YYYY-MM-DD.md`.
- Prepare approval request title, description, type, priority, requester, approver, source module, source reference, pending conditions, and boundaries.
- Add the command to the full pilot smoke chain, not the standard daily smoke profile.

## Boundaries

- No database approval request creation.
- No controlled expansion approval.
- No workflow expansion.
- No delivery enablement.
- No public exposure of private pilot artifacts.
- No bypass of owner acknowledgement or governance controls.

## Validation

Run:

```bash
python -m py_compile app/demo/pilot_expansion_approval_request_draft.py cli.py scripts/smoke_test.py app/system/runtime_stability.py
python cli.py pilot-expansion-approval-request-draft
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```
