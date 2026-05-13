# BusinessOS Dashboard Assistance Page v0.1

## Product Meaning

Dashboard Assistance Page v0.1 makes the Assistance Layer visible inside the private BusinessOS dashboard. Internal help, approval, incident, access, and decision requests are now part of the visual operating surface.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS assistance dashboard visibility
- Private data touched: read-only
- Public surface touched: no
- Approval required: no
- Evidence generated: no
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats assistance request dashboard pattern

## Why It Matters

BusinessOS is moving from backend workflows into a usable operating platform. Assistance requests should not live only in CLI output; leaders and operators need to see active requests, severity, owner, status, and approval pressure in one protected view.

## Current Capabilities

- Adds `Assistance` to dashboard navigation for allowed roles.
- Loads assistance request KPIs from SQLite.
- Displays active assistance requests with owner, type, status, and severity.
- Shows Assistance Brief cards for active requests, high-severity requests, and approval waiting.
- Preserves existing local dashboard login and role-based page list.

## Files Changed

```text
app/dashboard/main.py
app/security/access_control.py
README.md
docs/dashboard-assistance-page-v0.1-status.md
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
businessos-dashboard-assistance-page-v0.1
```
