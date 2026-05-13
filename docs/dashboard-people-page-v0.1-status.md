# BusinessOS Dashboard People Page v0.1

## Product Meaning

Dashboard People Page v0.1 makes the People Layer visible inside the private BusinessOS dashboard. Internal users, roles, departments, statuses, and access levels are now part of the visual operating surface.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS people dashboard visibility
- Private data touched: read-only
- Public surface touched: no
- Approval required: future
- Evidence generated: no
- Audit generated: no
- Reusable core candidate: yes
- Extraction timing: after identity and role hardening

## Why It Matters

BusinessOS needs people awareness before it can support approvals, routing, permissions, manager views, and human + AI collaboration. This page turns the People Layer from backend/CLI structure into visible product behavior.

## Current Capabilities

- Adds `People` to dashboard navigation for allowed roles.
- Loads People KPIs from SQLite.
- Displays total users, active users, admin users, and manager users.
- Displays a People Directory with name, email, role, department, status, and access level.
- Shows a People Brief panel for executive review.
- Preserves existing local dashboard login and role-based page list.

## Files Changed

```text
app/dashboard/main.py
app/security/access_control.py
README.md
docs/dashboard-people-page-v0.1-status.md
```

## Run Command

```bash
streamlit run app/dashboard/main.py
```

## Validation

```bash
python -m py_compile app/dashboard/main.py app/security/access_control.py
python scripts/smoke_test.py
```

## Suggested Tag

```text
businessos-dashboard-people-page-v0.1
```
