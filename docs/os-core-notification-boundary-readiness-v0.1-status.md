# OS Core Notification Boundary Readiness v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Product Meaning

OS Core Notification Boundary Readiness identifies which notification, delivery approval, and secure delivery adapter capabilities are reusable OS Core candidates before opening EduOS. It separates the domain-neutral communication control layer from BusinessOS daily close content and current business recipient roles.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS notification specialization
- Private data touched: no
- Public surface touched: no
- Approval required: no
- Evidence generated: documentation only
- Audit generated: no
- Reusable core candidate: yes
- Extraction timing: before EduOS implementation, after notification delivery policy hardening

## Scope

- Classify notification outbox, status lifecycle, delivery approval, and secure email delivery boundaries.
- Mark approval-gated external delivery as an OS Core safety requirement.
- Define EduOS notification analogs without implementing EduOS logic in BusinessOS.
- Define extraction conditions before moving notification logic into a future shared OS Core package.
- Update the institutional extraction map and README.

## OS Core Notification Candidates

These patterns are reusable across BusinessOS, EduOS, and future verticals:

- notification outbox schema shape
- queued, sent, dismissed, failed lifecycle
- channel, recipient, subject, body, source module, and source reference metadata
- delivery approval gate before external delivery
- secure adapter dry-run and disabled modes
- environment-based delivery credentials
- status update audit trail
- dashboard and CLI visibility by status
- report export for delivery readiness and delivery outcomes

## BusinessOS-Specific Notification Logic

These should remain in BusinessOS until another vertical proves the same shape:

- BusinessOS Daily Close notification content
- finance, operations, support, and executive recipient defaults
- current business role labels
- daily close distribution report content
- business-specific dashboard labels and demo narrative
- current notification subjects tied to BusinessOS operating rhythm

## Future EduOS Notification Analogs

EduOS may later reuse the core notification layer for:

- director daily school close distribution
- teacher intervention notifications
- guardian communication approvals
- assessment or grade-change approval notices
- academic risk escalation notifications
- policy-sensitive external message delivery

These are planning analogs only. Do not implement EduOS notification logic inside BusinessOS.

## Extraction Conditions

Notification logic can move toward shared OS Core when:

- recipient roles and departments are branch-configurable
- message templates are separated from delivery mechanics
- channel policy is configurable per vertical
- protected external delivery rules are policy-driven
- dashboard labels accept branch-specific language through configuration
- report language separates core delivery status from vertical content
- tests prove external delivery remains blocked without approval and credentials

## Current Readiness Assessment

```text
Notification outbox core readiness: high
Notification status lifecycle readiness: high
Delivery approval readiness: high
Secure email adapter readiness: medium
Dashboard visibility readiness: medium
BusinessOS daily close specialization: high
EduOS implementation readiness: planning only
Extraction recommendation: not yet; prepare template and role configuration first
```

## Boundaries

- No OS Core package extraction in this block.
- No EduOS implementation.
- No notification status mutation.
- No external email delivery.
- No credential handling change.
- No public exposure of private notification artifacts.
- No dashboard behavior change.

## Validation

Run:

```bash
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```
