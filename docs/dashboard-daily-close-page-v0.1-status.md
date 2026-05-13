# Dashboard Daily Close Page v0.1

## Product Meaning

The Dashboard Daily Close Page makes the executive close visible inside the private BusinessOS Command Center.

This turns the daily close from a CLI/report artifact into a dashboard page where leadership can confirm whether the operating day has been closed with supporting evidence.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared daily close dashboard pattern candidate
- Private data touched: read-only
- Public surface touched: no
- Approval required: no
- Evidence generated: report only
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats close dashboard pattern with different domain content

## Why It Matters

BusinessOS now has a visual close layer for institutional discipline. A leader can see close completion, evidence availability, missing proof points, and the latest report paths without searching through files or CLI output.

## Current Capabilities

- Adds a `Daily Close` page to the private Streamlit dashboard navigation.
- Displays completed close steps versus total close steps.
- Displays available and missing evidence counts.
- Shows the latest daily close report path.
- Shows the latest executive evidence index report path.
- Lists each daily close step and status.
- Lists each evidence register item and status.
- Maps `completed` and `available` states to healthy dashboard badges.
- Adds `Daily Close` to dashboard role-based access control.

## Validation

Validated with:

```bash
python -m py_compile app/dashboard/main.py app/security/access_control.py
python -c "from app.dashboard.main import load_dashboard_data; data=load_dashboard_data(); print(data['daily_close_status']); print(data['evidence_index_status']['items'][:2])"
```

## Next Step

Later versions can add direct dashboard actions for running daily close, refreshing evidence, and linking each evidence item to a report viewer.
