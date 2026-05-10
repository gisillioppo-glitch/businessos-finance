# BusinessOS Dashboard Governance Sensitivity Page v0.1

## Product Meaning

Dashboard Governance Sensitivity Page v0.1 makes the Governance Sensitivity Rules visible inside the private BusinessOS dashboard.

This page shows leaders which signals require institutional control before action proceeds.

## Why It Matters

The CLI can detect sensitive signals, but a governance operating system needs visibility. This block turns rule-based sensitivity into a product surface with KPIs, findings, and recommended next moves.

## Current Capabilities

- Adds `Sensitivity` to dashboard navigation for allowed roles.
- Loads sensitivity findings from `app/governance/sensitivity_rules.py` without writing audit logs on page load.
- Displays total sensitive findings.
- Displays high and medium sensitivity findings.
- Displays highest sensitivity risk.
- Displays active sensitivity findings with source and finding type.
- Shows a Sensitivity Brief panel for executive review.

## Files Changed

```text
app/dashboard/main.py
app/security/access_control.py
app/governance/sensitivity_rules.py
README.md
docs/dashboard-governance-sensitivity-page-v0.1-status.md
```

## Run Command

```bash
streamlit run app/dashboard/main.py
```

## Validation

```bash
python -m py_compile app/dashboard/main.py app/security/access_control.py app/governance/sensitivity_rules.py
python scripts/smoke_test.py
```

## Suggested Tag

```text
businessos-dashboard-governance-sensitivity-page-v0.1
```
