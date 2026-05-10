# BusinessOS Daily Work Plan - 2026-05-10

## Daily intent

Move BusinessOS from public presence + private MVP into a more structured institutional platform roadmap.

Today is not about adding random features. Today is about choosing the next operating layers and making measurable progress without breaking the clean architecture:

```text
Public landing -> lead intake -> private BusinessOS runtime -> future operating platform
```

## Current confirmed foundation

Completed and tagged:

- Finance MVP v1.0
- Operations MVP v1.0
- Governance MVP v1.0
- Support MVP v1.0
- Command Center MVP v1.0
- Dashboard MVP v0.1
- Security Foundation MVP v0.1
- Dashboard UI v0.2
- Landing Website MVP v0.1
- Deployment Readiness MVP v0.1
- Landing Publish MVP v0.1
- Lead Intake MVP v0.1
- Lead Intake Email Activation v0.2
- Repository Split & IP Protection MVP v0.1

Public repo:

```text
businessos-landing
```

Private repo:

```text
businessos-finance
```

## Product direction to preserve

BusinessOS is evolving from:

```text
dashboard + modules
```

to:

```text
institutional operating system
```

Core long-term layers:

1. Employee / User Operating Layer
2. Assistance / Escalation System
3. Intelligent Decision Support
4. Automated Demo / Simulation Engine
5. Enterprise Security + Governance
6. Human + AI Hybrid Model
7. Cross-industry Institutional Operating System

## Work capacity today

Minimum target:

```text
Day block: 5 hours
Night block: 2 hours
Total: 7 hours
```

Rule:

- Every block must end with a commit or a documented checkpoint.
- No public exposure of private runtime.
- No feature should bypass security/governance assumptions.
- Prefer small MVP blocks over giant unfinished systems.

## Day Block - 5 hours

### Block 1 - Stabilize public lead intake

Timebox: 45 minutes

Goal:

Confirm the public BusinessOS lead intake flow is working and documented.

Tasks:

- Open public landing URL.
- Submit one test lead.
- Confirm Formspree receives it.
- Confirm Gmail receives it.
- Confirm thank-you page loads.
- Record result in docs if needed.

Exit criteria:

```text
Lead flow tested end-to-end.
```

### Block 2 - Lead Intake v0.2 closure check

Timebox: 30 minutes

Goal:

Make sure public repo and private repo are clean and protected.

Tasks:

- Check `businessos-landing` git status.
- Check `businessos-finance` git status.
- Decide what to do with untracked PDF in private repo.
- Confirm public repo has no private references.

Exit criteria:

```text
Both repos are understood and no accidental public/private leak exists.
```

### Block 3 - Employee / User Operating Layer design

Timebox: 90 minutes

Goal:

Design the next core system layer before coding it.

MVP target:

```text
BusinessOS People Layer MVP v0.1
```

Define:

- User/employee fields.
- Roles.
- Permissions.
- Manager visibility.
- Statuses.
- Audit events.
- CLI commands.
- Future dashboard page.

Possible table:

```text
business_users
```

Possible fields:

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
```

Exit criteria:

```text
docs/people-layer-mvp-status.md drafted.
```

### Block 4 - Assistance / Escalation System design

Timebox: 75 minutes

Goal:

Define how employees/users ask for help, approvals, incident review, or escalation.

MVP target:

```text
BusinessOS Assistance Layer MVP v0.1
```

Define:

- Request types.
- Severity.
- Owner routing.
- Status flow.
- Governance link.
- Support link.
- Audit trail.

Possible table:

```text
assistance_requests
```

Possible statuses:

```text
open
triaged
waiting_approval
in_progress
resolved
dismissed
```

Exit criteria:

```text
docs/assistance-layer-mvp-status.md drafted.
```

### Block 5 - Select next implementation block

Timebox: 60 minutes

Goal:

Choose exactly one block to implement next, based on value and risk.

Candidates:

1. People Layer MVP v0.1
2. Assistance Layer MVP v0.1
3. Lead Automation Layer v0.3
4. Security v0.2
5. Dashboard Reports Download v0.3

Recommended order:

```text
People Layer -> Assistance Layer -> Security v0.2 -> Lead Automation v0.3
```

Exit criteria:

```text
One next block selected and scoped.
```

## Night Block - 2 hours

### Night Block 1 - Implement first small slice

Timebox: 90 minutes

Goal:

Implement only the first slice of the selected block.

If People Layer is selected:

- Create `app/people/`.
- Create schema file.
- Create basic user creation/listing functions.
- Add CLI command if safe.
- Add smoke test command.

If Assistance Layer is selected:

- Create `app/assistance/`.
- Create schema file.
- Create request creation/listing functions.
- Add CLI command if safe.
- Add smoke test command.

Exit criteria:

```text
Small working MVP slice runs locally.
```

### Night Block 2 - Validate and checkpoint

Timebox: 30 minutes

Tasks:

- Run smoke test.
- Run relevant import checks.
- Update docs.
- Commit and tag if complete.
- If not complete, commit only docs or leave clean checkpoint notes.

Exit criteria:

```text
No ambiguous partial work.
```

## Decision support for today

Recommended next build:

```text
BusinessOS People Layer MVP v0.1
```

Why:

- It supports employees/users.
- It enables permissions and role-based dashboards.
- It strengthens security/governance.
- It becomes the foundation for assistance/escalation routing.

Second build after People Layer:

```text
BusinessOS Assistance Layer MVP v0.1
```

Why:

- It turns users into active participants.
- It creates requests, approvals, escalations, and support entry points.
- It makes BusinessOS feel like an operating platform, not just analytics.

## Today success definition

Today is successful if at least one of these is true:

1. People Layer design is documented and ready to implement.
2. People Layer MVP first slice is implemented and tested.
3. Assistance Layer design is documented and ready to implement.
4. Lead intake public flow is confirmed and stable.

Stretch goal:

```text
People Layer MVP v0.1 committed and tagged.
```

## Do not do today

- Do not start a giant CRM.
- Do not add public backend exposure.
- Do not make the private repo public again.
- Do not build complex AI automation before user/role/permission foundations.
- Do not chase visual polish unless it supports the selected block.
