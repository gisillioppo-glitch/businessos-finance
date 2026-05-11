from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.private_pilot_plan import generate_private_pilot_plan


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"


TRACKER_EVIDENCE = [
    {
        "name": "Private pilot plan",
        "prefix": "private_pilot_plan",
        "required": True,
        "owner": "Executive Owner",
        "purpose": "Confirms pilot scope, owner, timeline, and protected boundaries.",
    },
    {
        "name": "Executive daily close",
        "prefix": "daily_close",
        "required": True,
        "owner": "Executive Owner",
        "purpose": "Shows the daily operating rhythm and executive review package.",
    },
    {
        "name": "Command center",
        "prefix": "command_center",
        "required": True,
        "owner": "Pilot Operator",
        "purpose": "Shows unified health, highest risk, and next best executive move.",
    },
    {
        "name": "Executive evidence index",
        "prefix": "executive_evidence_index",
        "required": True,
        "owner": "Pilot Operator",
        "purpose": "Confirms evidence exists before the executive review.",
    },
    {
        "name": "Notification delivery approval",
        "prefix": "notification_delivery_approval",
        "required": False,
        "owner": "Governance Reviewer",
        "purpose": "Confirms outbound communication remains controlled.",
    },
    {
        "name": "System integrity",
        "prefix": "system_integrity",
        "required": True,
        "owner": "Pilot Operator",
        "purpose": "Confirms platform checks are not failing before pilot use.",
    },
    {
        "name": "Release readiness",
        "prefix": "release_readiness",
        "required": False,
        "owner": "Executive Owner",
        "purpose": "Confirms the demo/pilot surface remains ready with known warnings only.",
    },
]

DAILY_OPERATOR_STEPS = [
    "Confirm the pilot plan remains aligned with the executive owner.",
    "Run or verify Executive Daily Close evidence for the day.",
    "Review Command Center highest risk and next best executive move.",
    "Check notification and delivery approval status before external communication.",
    "Record whether the day is on track, needs attention, or blocked.",
]


def _latest_report(prefix):
    if not REPORTS_DIR.exists():
        return None

    reports = list(REPORTS_DIR.glob(f"{prefix}_*.md"))

    if prefix == "daily_close":
        reports = [
            report for report in reports
            if not report.name.startswith("daily_close_distribution_")
        ]

    reports = sorted(
        reports,
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return reports[0] if reports else None


def _status_from_evidence(evidence_rows, plan_status):
    missing_required = [row for row in evidence_rows if row["required"] and row["status"] == "missing"]
    missing_optional = [row for row in evidence_rows if not row["required"] and row["status"] == "missing"]

    if plan_status == "blocked" or missing_required:
        return "blocked"

    if "warning" in plan_status or missing_optional:
        return "needs_attention"

    return "on_track"


def _next_action(tracker_status, missing_required, missing_optional):
    if tracker_status == "blocked":
        missing_names = ", ".join(row["name"] for row in missing_required)
        return f"Restore required pilot evidence before continuing: {missing_names}."

    if tracker_status == "needs_attention":
        if missing_optional:
            missing_names = ", ".join(row["name"] for row in missing_optional)
            return f"Confirm optional pilot evidence when available: {missing_names}."
        return "Confirm warning context with the executive owner before continuing the pilot rhythm."

    return "Continue the daily pilot rhythm and capture executive feedback."


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _format_evidence_rows(rows):
    table = [
        "| Evidence | Status | Required | Owner | Latest report | Purpose |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        table.append(
            f"| {row['name']} | {row['status']} | {row['required_label']} | {row['owner']} | {row['latest_report']} | {row['purpose']} |"
        )

    return "\n".join(table)


def generate_private_pilot_tracker(conn=None):
    today = date.today().isoformat()
    plan = generate_private_pilot_plan(conn)
    evidence_rows = []

    for item in TRACKER_EVIDENCE:
        latest_report = _latest_report(item["prefix"])
        evidence_rows.append(
            {
                "name": item["name"],
                "prefix": item["prefix"],
                "required": item["required"],
                "required_label": "yes" if item["required"] else "no",
                "owner": item["owner"],
                "purpose": item["purpose"],
                "status": "available" if latest_report else "missing",
                "latest_report": str(latest_report.relative_to(ROOT_DIR)) if latest_report else "missing",
            }
        )

    missing_required = [row for row in evidence_rows if row["required"] and row["status"] == "missing"]
    missing_optional = [row for row in evidence_rows if not row["required"] and row["status"] == "missing"]
    tracker_status = _status_from_evidence(evidence_rows, plan["plan_status"])

    return {
        "date": today,
        "tracker_status": tracker_status,
        "plan_status": plan["plan_status"],
        "pilot_owner": plan["pilot_owner"],
        "primary_workflow": plan["primary_workflow"],
        "pilot_length_days": plan["pilot_length_days"],
        "evidence_rows": evidence_rows,
        "available_evidence": len([row for row in evidence_rows if row["status"] == "available"]),
        "missing_required": len(missing_required),
        "missing_optional": len(missing_optional),
        "daily_operator_steps": DAILY_OPERATOR_STEPS,
        "next_action": _next_action(tracker_status, missing_required, missing_optional),
    }


def export_private_pilot_tracker(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_private_pilot_tracker(conn)
    report_path = REPORTS_DIR / f"private_pilot_tracker_{result['date']}.md"

    content = f"""# Private Pilot Daily Tracker MVP v0.1

Date: {result['date']}

## Tracker Summary

Tracker status: {result['tracker_status']}
Plan status: {result['plan_status']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Pilot length: {result['pilot_length_days']} days
Available evidence: {result['available_evidence']}
Missing required evidence: {result['missing_required']}
Missing optional evidence: {result['missing_optional']}
Next action: {result['next_action']}

## Daily Operator Steps

{_format_bullets(result['daily_operator_steps'])}

## Evidence Checklist

{_format_evidence_rows(result['evidence_rows'])}

## Operator Note

Use this tracker as the daily pilot control point. It does not replace the detailed reports; it tells the operator whether enough evidence exists to continue the pilot rhythm safely.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "private_pilot_tracker_exported",
            "info" if result["tracker_status"] == "on_track" else "warning",
            "Private pilot daily tracker exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "tracker_status": result["tracker_status"],
                "available_evidence": result["available_evidence"],
                "missing_required": result["missing_required"],
                "missing_optional": result["missing_optional"],
            },
        )

    return result, str(report_path)


def print_private_pilot_tracker(conn=None):
    result, report_path = export_private_pilot_tracker(conn)

    print("Private Pilot Daily Tracker:")
    print(f"Date: {result['date']}")
    print(f"Tracker status: {result['tracker_status']}")
    print(f"Plan status: {result['plan_status']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Available evidence: {result['available_evidence']}")
    print(f"Missing required evidence: {result['missing_required']}")
    print(f"Missing optional evidence: {result['missing_optional']}")
    print(f"Next action: {result['next_action']}")
    print(f"Private pilot tracker exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
