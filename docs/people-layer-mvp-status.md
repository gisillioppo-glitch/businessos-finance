# BusinessOS People Layer MVP v0.1

## Product Meaning

The People Layer is the first internal user operating layer for BusinessOS. It turns the system from module-only intelligence into an institution-aware runtime that knows who the people are, what roles they hold, and what level of access they have.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS internal identity model
- Private data touched: yes
- Public surface touched: no
- Approval required: future
- Evidence generated: no
- Audit generated: yes
- Reusable core candidate: yes
- Extraction timing: after identity and role hardening

## Why It Matters

BusinessOS cannot become an institutional operating system without people, roles, permissions, and accountability. This block creates the foundation for future employee views, manager oversight, approval flows, security enforcement, and human + AI collaboration.

## Current Capabilities

- Create the `business_users` SQLite table.
- Seed default institutional users for Executive, Finance, Operations, and Support.
- Deduplicate users by email.
- Track role, department, status, and access level.
- Print a People Directory from the CLI.
- Generate People Summary KPIs.
- Generate a People Brief with highest people risk and next best people move.
- Write audit logs for created users and duplicate skips.
- Validate People commands through the smoke test.

## Architecture

```text
app/people/
  __init__.py
  schema.py
  users.py
  people_views.py
  people_brief.py
```

## Database Table

```text
business_users
```

Fields:

```text
id
created_at
full_name
email
role
department
manager_id
status
access_level
source_module
source_reference_id
```

## CLI Commands

```bash
python cli.py people
python cli.py people-brief
```

## Status

People Layer MVP v0.1 is ready when:

- People commands run successfully.
- Smoke test passes.
- The block is committed and tagged.

Suggested tag:

```text
businessos-people-layer-mvp-v0.1
```

## Next Recommended Blocks

- Assistance / Escalation System for user-submitted help requests.
- Approval Workflow Layer for sensitive actions.
- User access enforcement across dashboard pages.
- Lead-to-demo processing inside BusinessOS.
