from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.private_pilot_tracker import generate_private_pilot_tracker


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

EXIT_OPTIONS = [
    {
        "decision": "extend_pilot",
        "meaning": "Keep the same workflow active for another controlled pilot window.",
    },
    {
        "decision": "expand_pilot",
        "meaning": "Add one adjacent workflow or department after the current rhythm proves stable.",
    },
    {
        "decision": "convert_to_implementation",
        "meaning": "Move from private pilot to production hardening and implementation planning.",
    },
    {
        "decision": "pause_pilot",
        "meaning": "Pause until missing evidence, readiness warnings, or owner concerns are resolved.",
    },
    {
        "decision": "close_no_fit",
        "meaning": "Archive evidence and close the pilot if current value is not strong enough.",
    },
]


def _decision_from_tracker(tracker):
    if tracker["tracker_status"] == "blocked" or tracker["missing_required"] > 0:
        return {
            "decision_status": "blocked",
            "recommended_decision": "pause_pilot",
            "highest_exit_risk": "high",
            "next_action": "Resolve missing required evidence before making an exit decision.",
            "rationale": [
                "The pilot tracker is blocked or missing required evidence.",
                "An executive exit decision should not be made without the required evidence set.",
            ],
            "conditions": [
                "Restore required evidence.",
                "Re-run the tracker and release readiness checks.",
                "Confirm the executive owner has reviewed the restored evidence.",
            ],
        }

    if tracker["tracker_status"] == "needs_attention":
        return {
            "decision_status": "decision_ready_with_warnings",
            "recommended_decision": "extend_pilot",
            "highest_exit_risk": "medium",
            "next_action": "Confirm warning context with the executive owner, then extend the pilot rhythm before expansion.",
            "rationale": [
                "Required pilot evidence is available.",
                "The tracker still carries warning context that should be reviewed before expansion.",
                "Extending the same workflow protects momentum without increasing operational scope too early.",
            ],
            "conditions": [
                "Executive owner confirms the current warnings are acceptable.",
                "Pilot operator continues daily close and tracker evidence capture.",
                "Governance reviewer confirms no protected boundary was violated.",
            ],
        }

    return {
        "decision_status": "decision_ready",
        "recommended_decision": "expand_pilot",
        "highest_exit_risk": "low",
        "next_action": "Review expansion scope with the executive owner and add one adjacent workflow only.",
        "rationale": [
            "The pilot tracker is on track.",
            "Required evidence exists and no blocking signal is present.",
            "A narrow expansion is safer than jumping directly to a broad implementation.",
        ],
        "conditions": [
            "Executive owner approves the adjacent workflow.",
            "Pilot operator keeps the same daily evidence rhythm.",
            "Governance reviewer confirms the new workflow boundaries before expansion.",
        ],
    }


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _format_exit_options(options):
    rows = [
        "| Decision | Meaning |",
        "| --- | --- |",
    ]

    for option in options:
        rows.append(f"| {option['decision']} | {option['meaning']} |")

    return "\n".join(rows)


def _format_evidence_summary(rows):
    table = [
        "| Evidence | Status | Required | Latest report |",
        "| --- | --- | --- | --- |",
    ]

    for row in rows:
        table.append(
            f"| {row['name']} | {row['status']} | {row['required_label']} | {row['latest_report']} |"
        )

    return "\n".join(table)


def generate_private_pilot_exit_decision(conn=None):
    tracker = generate_private_pilot_tracker(conn)
    decision = _decision_from_tracker(tracker)

    return {
        "date": date.today().isoformat(),
        "decision_status": decision["decision_status"],
        "recommended_decision": decision["recommended_decision"],
        "highest_exit_risk": decision["highest_exit_risk"],
        "next_action": decision["next_action"],
        "rationale": decision["rationale"],
        "conditions": decision["conditions"],
        "tracker_status": tracker["tracker_status"],
        "plan_status": tracker["plan_status"],
        "pilot_owner": tracker["pilot_owner"],
        "primary_workflow": tracker["primary_workflow"],
        "available_evidence": tracker["available_evidence"],
        "missing_required": tracker["missing_required"],
        "missing_optional": tracker["missing_optional"],
        "evidence_rows": tracker["evidence_rows"],
        "exit_options": EXIT_OPTIONS,
    }


def export_private_pilot_exit_decision(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_private_pilot_exit_decision(conn)
    report_path = REPORTS_DIR / f"private_pilot_exit_decision_{result['date']}.md"

    content = f"""# Private Pilot Exit Decision MVP v0.1

Date: {result['date']}

## Exit Decision Summary

Decision status: {result['decision_status']}
Recommended decision: {result['recommended_decision']}
Highest exit risk: {result['highest_exit_risk']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Tracker status: {result['tracker_status']}
Plan status: {result['plan_status']}
Available evidence: {result['available_evidence']}
Missing required evidence: {result['missing_required']}
Missing optional evidence: {result['missing_optional']}
Next action: {result['next_action']}

## Decision Rationale

{_format_bullets(result['rationale'])}

## Conditions Before Execution

{_format_bullets(result['conditions'])}

## Evidence Summary

{_format_evidence_summary(result['evidence_rows'])}

## Allowed Exit Options

{_format_exit_options(result['exit_options'])}

## Operator Note

This report is a decision support artifact. It does not execute the exit decision automatically; the executive owner must confirm the final pilot decision.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "private_pilot_exit_decision_exported",
            "info" if result["decision_status"] == "decision_ready" else "warning",
            "Private pilot exit decision exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "decision_status": result["decision_status"],
                "recommended_decision": result["recommended_decision"],
                "highest_exit_risk": result["highest_exit_risk"],
            },
        )

    return result, str(report_path)


def print_private_pilot_exit_decision(conn=None):
    result, report_path = export_private_pilot_exit_decision(conn)

    print("Private Pilot Exit Decision:")
    print(f"Date: {result['date']}")
    print(f"Decision status: {result['decision_status']}")
    print(f"Recommended decision: {result['recommended_decision']}")
    print(f"Highest exit risk: {result['highest_exit_risk']}")
    print(f"Tracker status: {result['tracker_status']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Next action: {result['next_action']}")
    print(f"Private pilot exit decision exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
