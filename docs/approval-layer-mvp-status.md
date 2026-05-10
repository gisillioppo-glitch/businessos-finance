# BusinessOS Approval Layer MVP v0.1

## Product Meaning

The Approval Layer is the first institutional decision-control layer for BusinessOS. It captures sensitive requests that should not proceed without explicit approval from an authorized role.

## Why It Matters

BusinessOS is becoming an operating system, not only a reporting surface. Sensitive decisions need approval, traceability, and ownership. This block creates the foundation for executive approval, access approval, policy approval, budget approval, and incident approval workflows.

## Current Capabilities

- Create the `approval_requests` SQLite table.
- Seed default approval requests from Assistance signals.
- Deduplicate pending approvals by title and source reference.
- Track approval type, priority, requester, approver role, status, and source module.
- Print pending approval requests from CLI.
- Generate Approval Summary KPIs.
- Generate an Approval Brief with highest approval risk and next best move.
- Write audit logs for created approvals, duplicate skips, list views, and KPI views.
- Validate Approval commands through the smoke test.

## Architecture

```text
app/approvals/
  __init__.py
  schema.py
  requests.py
  approval_views.py
  approval_brief.py
```

## Database Table

```text
approval_requests
```

Fields:

```text
id
created_at
title
description
approval_type
priority
requester_email
requester_role
approver_role
status
status_justification
source_module
source_reference_id
```

## Approval Types

```text
decision
access
budget
policy
incident
```

## Status Flow

```text
pending -> approved
pending -> rejected
pending -> cancelled
```

## CLI Commands

```bash
python cli.py approvals
python cli.py approval-brief
```

## Status

Approval Layer MVP v0.1 is ready when:

- Approval commands run successfully.
- Smoke test passes.
- The block is committed and tagged.

Suggested tag:

```text
businessos-approval-layer-mvp-v0.1
```

## Next Recommended Blocks

- Approval Status v0.2 with approve/reject/cancel and justification.
- Dashboard Approval Page v0.1.
- Governance checks for sensitive approval bypass.
- Assistance-to-approval routing rules.
