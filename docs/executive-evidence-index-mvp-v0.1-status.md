# Executive Evidence Index MVP v0.1

## Product meaning

BusinessOS now has an executive evidence index that consolidates the key reports generated during the operating day. It tells leadership which decision, alert, governance, support, command center, and finance evidence files are available.

## Why it matters

As the system grows, evidence can spread across many reports. This block creates a single register for institutional review, audit readiness, and executive handoff. The operating system can now point to its own evidence trail.

## MVP scope

- Add an evidence index module.
- Track expected daily reports.
- Print available and missing evidence items.
- Export a Markdown evidence index report.
- Add `evidence-index` CLI command.
- Add smoke test coverage.

## CLI command

```bash
python cli.py evidence-index
```

## Output

`reports/executive_evidence_index_YYYY-MM-DD.md`

## Evidence tracked

- Command Center
- Executive Alerts
- Approval Decisions
- Governance Brief
- Support Brief
- Daily Finance Brief

## Files

- `app/evidence/__init__.py`
- `app/evidence/evidence_index.py`
- `cli.py`
- `scripts/smoke_test.py`
- `README.md`

## Suggested tag

`businessos-executive-evidence-index-mvp-v0.1`
