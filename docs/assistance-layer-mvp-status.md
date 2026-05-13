# BusinessOS Assistance Layer MVP v0.1

## Product Meaning

The Assistance Layer is the first internal request and escalation intake system for BusinessOS. It lets institutional users create structured requests for help, approvals, incidents, access changes, and executive decisions.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS assistance and escalation context
- Private data touched: yes
- Public surface touched: no
- Approval required: future
- Evidence generated: no
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats institutional request intake pattern

## Why It Matters

BusinessOS should not only observe the institution. It should become a place where people can ask for help, escalate issues, request decisions, and create accountable operational follow-up. This block connects People Layer, Operations, Governance, Support, and future approval workflows.

## Current Capabilities

- Create the `assistance_requests` SQLite table.
- Seed default assistance requests from Operations and Support signals.
- Deduplicate active requests by title and source reference.
- Track request type, severity, owner, requester, status, and source module.
- Print active assistance requests from the CLI.
- Generate Assistance Summary KPIs.
- Generate an Assistance Brief with highest assistance risk and next best move.
- Write audit logs for created requests, duplicate skips, list views, and KPI views.
- Validate Assistance commands through the smoke test.

## Architecture

```text
app/assistance/
  __init__.py
  schema.py
  requests.py
  request_views.py
  assistance_brief.py
```

## Database Table

```text
assistance_requests
```

Fields:

```text
id
created_at
title
description
request_type
severity
requester_email
requester_role
owner_role
status
status_justification
source_module
source_reference_id
```

## Request Types

```text
help
approval
incident
access
decision
```

## Status Flow

```text
open -> triaged -> waiting_approval -> in_progress -> resolved
```

Dismissed requests are kept for auditability.

## CLI Commands

```bash
python cli.py assistance
python cli.py assistance-brief
```

## Status

Assistance Layer MVP v0.1 is ready when:

- Assistance commands run successfully.
- Smoke test passes.
- The block is committed and tagged.

Suggested tag:

```text
businessos-assistance-layer-mvp-v0.1
```

## Next Recommended Blocks

- Assistance status updates with justification.
- Governance approval checks for sensitive assistance requests.
- Dashboard Assistance page.
- Lead-to-demo processing inside private BusinessOS.
