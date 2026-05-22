from datetime import date
from pathlib import Path
import re

from app.audit.audit_log import write_audit_log


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

CHAIN_ARTIFACTS = [
    {
        "label": "Start Confirmation",
        "prefix": "private_pilot_start_confirmation",
        "status_label": "Confirmation status",
        "owner_label": "Pilot owner",
    },
    {
        "label": "Day 1 Package",
        "prefix": "pilot_day_1_package",
        "status_label": "Day 1 status",
        "owner_label": "Pilot owner",
    },
    {
        "label": "Day 2 Rhythm",
        "prefix": "pilot_day_2_rhythm",
        "status_label": "Day 2 status",
        "owner_label": "Pilot owner",
    },
    {
        "label": "Day 3 Evidence Review",
        "prefix": "pilot_day_3_evidence_review",
        "status_label": "Day 3 status",
        "owner_label": "Pilot owner",
    },
    {
        "label": "Day 4 Owner Confirmation",
        "prefix": "pilot_day_4_owner_confirmation",
        "status_label": "Day 4 status",
        "owner_label": "Pilot owner",
    },
    {
        "label": "Day 5 Narrow Continuation",
        "prefix": "pilot_day_5_narrow_continuation",
        "status_label": "Day 5 status",
        "owner_label": "Pilot owner",
    },
    {
        "label": "Expansion Prep",
        "prefix": "pilot_expansion_review_prep",
        "status_label": "Expansion prep status",
        "owner_label": "Pilot owner",
    },
    {
        "label": "Expansion Decision",
        "prefix": "pilot_expansion_review_decision",
        "status_label": "Decision status",
        "owner_label": "Pilot owner",
    },
]


def _latest_report(prefix):
    reports = sorted(REPORTS_DIR.glob(f"{prefix}_*.md"))
    return reports[-1] if reports else None


def _extract_value(content, label, default="not_recorded"):
    match = re.search(rf"^{re.escape(label)}:\s*(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else default


def _chain_status(rows):
    missing = [row for row in rows if not row["exists"]]
    blocked = [row for row in rows if row["status"].startswith("blocked")]
    unresolved_confirmation = [
        row
        for row in rows
        if row["start_confirmation_status"] in {"missing", "requires_owner_confirmation", "not_recorded"}
    ]

    if missing:
        return "chain_incomplete"

    if blocked:
        return "chain_blocked"

    if unresolved_confirmation:
        return "chain_ready_with_conditions"

    return "chain_ready"


def _next_action(status):
    if status == "chain_incomplete":
        return "Generate missing pilot chain artifacts before relying on expansion decision guidance."

    if status == "chain_blocked":
        return "Resolve the blocked confirmation or pilot artifact before continuing."

    if status == "chain_ready_with_conditions":
        return "Keep pilot operation narrow and obtain owner acknowledgement before controlled expansion approval."

    return "Use the chain as evidence for a future controlled expansion approval review."


def _format_chain_rows(rows):
    lines = [
        "| Artifact | Status | Start Confirmation | Report |",
        "| --- | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| {row['label']} | {row['status']} | {row['start_confirmation_status']} | {row['report_path']} |"
        )

    return "\n".join(lines)


def generate_pilot_owner_confirmation_chain_index():
    rows = []

    for artifact in CHAIN_ARTIFACTS:
        report = _latest_report(artifact["prefix"])

        if not report:
            rows.append(
                {
                    "label": artifact["label"],
                    "exists": False,
                    "status": "missing",
                    "start_confirmation_status": "missing",
                    "start_confirmation_report": "not_available",
                    "owner": "not_recorded",
                    "primary_workflow": "not_recorded",
                    "report_path": "not_available",
                }
            )
            continue

        content = report.read_text(encoding="utf-8")
        start_status = _extract_value(content, "Start confirmation status")

        if artifact["prefix"] == "private_pilot_start_confirmation":
            start_status = _extract_value(content, "Confirmation status")

        rows.append(
            {
                "label": artifact["label"],
                "exists": True,
                "status": _extract_value(content, artifact["status_label"]),
                "start_confirmation_status": start_status,
                "start_confirmation_report": _extract_value(content, "Start confirmation report"),
                "owner": _extract_value(content, artifact["owner_label"]),
                "primary_workflow": _extract_value(content, "Primary workflow"),
                "report_path": str(report.relative_to(ROOT_DIR)),
            }
        )

    status = _chain_status(rows)

    return {
        "date": date.today().isoformat(),
        "chain_status": status,
        "artifacts_total": len(rows),
        "artifacts_present": len([row for row in rows if row["exists"]]),
        "blocked_artifacts": len([row for row in rows if row["status"].startswith("blocked")]),
        "conditional_confirmation_artifacts": len(
            [
                row
                for row in rows
                if row["start_confirmation_status"] in {"requires_owner_confirmation", "missing", "not_recorded"}
            ]
        ),
        "rows": rows,
        "next_action": _next_action(status),
    }


def export_pilot_owner_confirmation_chain_index(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_owner_confirmation_chain_index()
    report_path = REPORTS_DIR / f"pilot_owner_confirmation_chain_index_{result['date']}.md"

    content = f"""# Pilot Owner Confirmation Chain Index v0.1

Date: {result['date']}

## Chain Summary

Chain status: {result['chain_status']}
Artifacts total: {result['artifacts_total']}
Artifacts present: {result['artifacts_present']}
Blocked artifacts: {result['blocked_artifacts']}
Conditional confirmation artifacts: {result['conditional_confirmation_artifacts']}
Next action: {result['next_action']}

## Confirmation Chain

{_format_chain_rows(result['rows'])}

## Governance Boundary

- This index summarizes existing pilot artifacts only.
- This index does not approve controlled expansion.
- This index does not add workflows.
- This index does not enable external delivery.
- This index does not expose private pilot artifacts outside the private environment.

## Operator Note

Use this index before any expansion approval discussion to confirm that Day 1 through expansion decision remain tied to the same owner confirmation context.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "pilot_owner_confirmation_chain_index_exported",
            "info" if result["chain_status"] == "chain_ready" else "warning",
            "Pilot owner confirmation chain index exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "chain_status": result["chain_status"],
                "artifacts_present": result["artifacts_present"],
            },
        )

    return result, str(report_path)


def print_pilot_owner_confirmation_chain_index(conn=None):
    result, report_path = export_pilot_owner_confirmation_chain_index(conn)

    print("Pilot Owner Confirmation Chain Index:")
    print(f"Date: {result['date']}")
    print(f"Chain status: {result['chain_status']}")
    print(f"Artifacts present: {result['artifacts_present']}/{result['artifacts_total']}")
    print(f"Blocked artifacts: {result['blocked_artifacts']}")
    print(f"Conditional confirmation artifacts: {result['conditional_confirmation_artifacts']}")
    print(f"Next action: {result['next_action']}")
    print(f"Pilot owner confirmation chain index exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
