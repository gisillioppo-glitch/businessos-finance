# BusinessOS Governance Sensitivity Rules v0.1

## Product Meaning

Governance Sensitivity Rules v0.1 defines the first formal policy layer for detecting sensitive institutional activity inside BusinessOS.

This block answers the question:

```text
What makes an action sensitive enough to require control?
```

## Why It Matters

BusinessOS now has People, Assistance, and Approvals. The next governance step is to define which signals require attention, approval, justification, or escalation. This creates rule-based governance before advanced AI/ML detection.

## Current Rule Categories

### Approval Sensitivity

Sensitive if:

```text
approval_type in decision, access, budget, policy, incident
priority in high, critical
status = pending
```

### Assistance Sensitivity

Sensitive if:

```text
request_type in approval, access, decision, incident
severity in high, critical
```

### Privileged Access Sensitivity

Sensitive if:

```text
access_level in admin, executive
status = active
```

### Operations Sensitivity

Sensitive if:

```text
operations task is active and overdue
```

### Support Sensitivity

Sensitive if:

```text
support incident severity in high, critical
status in open, investigating, waiting
```

### Audit Sensitivity

Sensitive if:

```text
audit severity in error, critical
status update event missing justification
```

## CLI Commands

```bash
python cli.py gov-sensitivity
python cli.py gov-sensitivity-brief
```

## Output Example

```text
Governance Sensitivity Rules:
[HIGH] approval_required | approval_requests | Approval required: Approve overdue operations intervention
[MEDIUM] privileged_access_detected | business_users | Privileged access detected: Executive Owner
```

## Files

```text
app/governance/sensitivity_rules.py
cli.py
scripts/smoke_test.py
README.md
```

## Status

Governance Sensitivity Rules v0.1 is ready when:

- Sensitivity commands run successfully.
- Smoke test passes.
- The block is committed and tagged.

Suggested tag:

```text
businessos-governance-sensitivity-rules-v0.1
```

## Next Recommended Blocks

- Governance sensitivity dashboard page.
- Approval Status v0.2.
- Governance rules configuration file.
- Protected Mode design doc.
