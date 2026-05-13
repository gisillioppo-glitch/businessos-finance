# Notification Outbox MVP v0.1

## Product Meaning

The Notification Outbox MVP gives BusinessOS a safe internal delivery queue.

Instead of sending emails directly from local MVP code, BusinessOS now prepares notification records with recipient, subject, body, source, and status. This creates the foundation for secure future delivery through email, Slack, Teams, or another protected notification channel.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS daily close notification context
- Private data touched: yes
- Public surface touched: no
- Approval required: future
- Evidence generated: no
- Audit generated: yes
- Reusable core candidate: yes
- Extraction timing: after second vertical repeats notification outbox pattern

## Why It Matters

BusinessOS should not only generate intelligence; it should route it to the correct responsible person. The outbox turns daily close distribution into an operational queue that can be reviewed, audited, and later connected to real delivery providers without exposing credentials or sending uncontrolled messages.

## Current Capabilities

- Adds `notification_outbox` table.
- Adds `python cli.py notifications`.
- Queues Daily Close Distribution packages as email notifications.
- Prevents duplicate queued messages for the same recipient/date/source.
- Preserves sent notifications if a future delivery layer marks them sent.
- Tracks queued, sent, dismissed, and failed status counts.
- Writes audit logs when notifications are queued, updated, or viewed.
- Adds notification validation to the smoke test.

## Current Flow

```text
python cli.py daily-close
-> generate evidence reports
-> export daily close
-> export daily close distribution
-> queue CEO/manager notifications
-> review with python cli.py notifications
```

## Safety Boundary

This MVP does not send real email. It stores email-ready messages internally so delivery credentials can be added later through a protected integration.

## Next Step

The next version can add notification status transitions, dashboard visibility, and a secure provider adapter for actual email delivery.
