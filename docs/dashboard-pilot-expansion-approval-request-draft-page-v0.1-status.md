# Dashboard Pilot Expansion Approval Request Draft Page v0.1

Date: 2026-05-21

## Status

Closed for MVP validation.

## Product Meaning

The private dashboard now exposes the controlled pilot expansion approval request draft as a visual, read-only executive page. This makes the prepared request shape visible before any future block creates a real pending approval request.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared approval request drafting candidate
- Private data touched: sanitized only
- Public surface touched: no
- Approval required: yes
- Evidence generated: report only
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats approval request drafting

## Scope

- Add `Approval Draft` to role-based dashboard navigation.
- Load the latest `reports/pilot_expansion_approval_request_draft_YYYY-MM-DD.md`.
- Show draft status, request priority, approval type, requester, approver, pending conditions, and recommended request action.
- Render request description, approval conditions, draft commands, gate context, pending conditions, protected boundaries, and operator note.
- Keep all execution in CLI artifacts.

## Boundaries

- No database approval request creation.
- No controlled expansion approval.
- No workflow expansion.
- No delivery enablement.
- No report regeneration from the dashboard.
- No public exposure of private pilot artifacts.
- No bypass of owner acknowledgement or governance controls.

## Validation

Run:

```bash
python -m py_compile app/dashboard/main.py app/security/access_control.py
python cli.py pilot-expansion-approval-request-draft
python scripts/smoke_test.py quick
```
