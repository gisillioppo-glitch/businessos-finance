# BusinessOS Assistance Status MVP v0.2

## Product Meaning

Assistance Status v0.2 gives BusinessOS the first controlled lifecycle movement for internal requests. Assistance requests can now move from intake to triage with a required audit trail and justification.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS assistance lifecycle context
- Private data touched: yes
- Public surface touched: no
- Approval required: future
- Evidence generated: no
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats assistance status lifecycle

## Why It Matters

The Assistance Layer should not only collect requests. It must move work forward. Status updates make requests operational, accountable, and auditable.

## Current Capabilities

- Update assistance request status.
- Validate allowed statuses.
- Store status justification.
- Write audit logs for status changes.
- Demo-triage the first open assistance request from CLI.
- Validate the status command through smoke test.

## Statuses

```text
open
triaged
waiting_approval
in_progress
resolved
dismissed
```

## CLI Command

```bash
python cli.py assistance-status
```

Expected output example:

```text
Assistance Request Status Update: <id> changed from open to triaged.
```

If no open requests exist:

```text
Assistance Request Status Update: No open assistance requests found.
```

## Files

```text
app/assistance/request_status.py
cli.py
scripts/smoke_test.py
```

## Suggested Tag

```text
businessos-assistance-status-v0.2
```
