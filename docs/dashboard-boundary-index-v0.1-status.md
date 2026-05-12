# Dashboard Boundary Index v0.1

## Product Meaning

Dashboard Boundary Index documents the private dashboard pages and classifies each page by architectural boundary.

It gives BusinessOS a read-only map of what the dashboard currently exposes internally, what remains BusinessOS-specific, what may become OS Core, and what must stay away from public surfaces.

## Boundary Classification

- Primary boundary: Documentation / architecture
- Secondary boundary: Shared dashboard governance pattern candidate
- Private data touched: no
- Public surface touched: no
- Approval required: no
- Evidence generated: no
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after dashboard boundary pattern repeats in a second vertical

## Current Dashboard Pages

Current private dashboard navigation includes:

```text
Dashboard
Alerts
Finance
Operations
Governance
Sensitivity
Support
Assistance
Approvals
Daily Close
Scheduled Close
Notifications
Delivery Approval
Secure Email
System Integrity
Demo Readiness
Pilot Plan
Pilot Tracker
Pilot Exit
Pilot Day 1
Pilot Day 2
Pilot Expansion
People
```

## Boundary Index

| Page | Primary Boundary | Secondary Boundary | Private Data | Public Surface | Core Candidate | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Dashboard | Shared candidate, not core yet | BusinessOS executive overview | read-only | no | partial | Executive synthesis pattern may transfer after another vertical repeats it. |
| Alerts | OS Core candidate | BusinessOS executive alert context | read-only | no | yes | Alert status and resolution patterns are reusable. |
| Finance | BusinessOS-specific | Finance domain module | read-only | no | no | Finance metrics and records stay BusinessOS-specific. |
| Operations | BusinessOS-specific | Shared work queue pattern candidate | read-only | no | partial | Work tracking shape may transfer, but business operations language remains domain-specific. |
| Governance | OS Core candidate | BusinessOS audit context | read-only | no | yes | Governance findings and policy controls are strong core candidates. |
| Sensitivity | OS Core candidate | Governance sensitivity rules | read-only | no | yes | Sensitivity classification is reusable institutional control logic. |
| Support | BusinessOS-specific | Shared incident pattern candidate | read-only | no | partial | Incident model may transfer, current language is business support-specific. |
| Assistance | OS Core candidate | BusinessOS assistance workflow | read-only | no | partial | Assistance request lifecycle could become shared intake/control pattern. |
| Approvals | OS Core candidate | BusinessOS decision context | read-only | no | yes | Approval-gated action workflow is reusable. |
| Daily Close | BusinessOS-specific | Shared daily close pattern candidate | read-only | no | partial | Operating close pattern may transfer, current content is business-specific. |
| Scheduled Close | OS Core candidate | BusinessOS daily close schedule | read-only | no | partial | Controlled recurring job visibility is reusable. |
| Notifications | OS Core candidate | BusinessOS notification outbox | read-only | no | yes | Notification state model is reusable. |
| Delivery Approval | OS Core candidate | BusinessOS notification delivery context | read-only | no | yes | Approval before delivery is reusable institutional control. |
| Secure Email | OS Core candidate | External delivery adapter visibility | read-only | no | partial | Adapter visibility may become core after security hardening and second vertical validation. |
| System Integrity | OS Core candidate | BusinessOS runtime checks | read-only | no | yes | System health and integrity checks are reusable. |
| Demo Readiness | BusinessOS-specific | Shared demo readiness candidate | sanitized only | no | partial | Demo readiness is go-to-market-specific but pattern may transfer. |
| Pilot Plan | BusinessOS-specific | Shared pilot methodology candidate | sanitized only | no | partial | Pilot methodology is BusinessOS-specific until another vertical repeats it. |
| Pilot Tracker | BusinessOS-specific | Shared pilot methodology candidate | sanitized only | no | partial | Pilot tracking remains business pilot workflow for now. |
| Pilot Exit | BusinessOS-specific | Shared pilot methodology candidate | sanitized only | no | partial | Exit decision pattern may transfer later. |
| Pilot Day 1 | BusinessOS-specific | Shared pilot methodology candidate | sanitized only | no | partial | Day-level pilot operation remains BusinessOS-specific. |
| Pilot Day 2 | BusinessOS-specific | Shared pilot methodology candidate | sanitized only | no | partial | Repeatable rhythm may transfer after second vertical validation. |
| Pilot Expansion | BusinessOS-specific | Shared pilot methodology candidate | sanitized only | no | partial | Expansion decision workflow is not core yet. |
| People | OS Core candidate | BusinessOS internal roles | read-only | no | yes | Institutional people and role layer is reusable. |

## Safety Boundary

This block does not add a dashboard page, expose new data, change access control, modify navigation, run delivery, approve actions, or publish any private system detail to the public landing.

It documents the existing private dashboard boundary only.

## Integration

- CLI: no change
- Dashboard: documented only, no UI change
- Reports: no change
- Database: no change
- Governance: supports future boundary review
- Notifications: documented as OS Core candidate
- Public surface: no change

## Validation

- Passed: dashboard navigation reviewed from `app\security\access_control.py`.
- Passed: dashboard render branches reviewed from `app\dashboard\main.py`.
- Passed: boundary fields aligned to `docs\feature-boundary-classification-template-v0.1.md`.

## Next Step

Dashboard Boundary Index Page v0.1 or Status Docs Boundary Backfill Batch 2 v0.1.

