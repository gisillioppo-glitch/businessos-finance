# Dashboard Pilot Expansion Approval Request Page v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Product Meaning

The private dashboard now exposes the formal pilot expansion approval request as read-only governance evidence. This closes the visibility loop after request creation: executives can see that the request exists and remains pending without approving, rejecting, expanding scope, or executing delivery from the UI.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared approval request visibility candidate
- Private data touched: sanitized approval metadata only
- Public surface touched: no
- Approval required: yes
- Evidence generated: dashboard view only
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats approval request visibility

## Scope

- Add `Approval Request` to role-based dashboard navigation.
- Load the latest `reports/pilot_expansion_approval_request_creation_YYYY-MM-DD.md`.
- Show creation status, approval request status, priority, pending conditions, request id, request description, and approval gate context.
- Show request evidence, creation commands, protected boundaries, and operator note.
- Keep all approval decisions in the existing approval flow.
- Update release readiness dashboard page checks.

## Boundaries

- No approval or rejection from dashboard.
- No controlled expansion execution.
- No workflow expansion.
- No external delivery enablement.
- No report regeneration from dashboard.
- No public exposure of private pilot artifacts.
- No bypass of owner acknowledgement, pending conditions, or governance controls.

## Validation

Run:

```bash
python -m py_compile app/dashboard/main.py app/security/access_control.py app/readiness/release_readiness.py
python cli.py pilot-expansion-approval-request-creation
python cli.py release-readiness
python cli.py system-check
python cli.py runtime-stability
python scripts/smoke_test.py quick
```
