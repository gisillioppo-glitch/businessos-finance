from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.pilot_day_1_package import generate_pilot_day_1_package
from app.demo.pilot_day_2_rhythm import generate_pilot_day_2_rhythm
from app.demo.private_pilot_exit_decision import generate_private_pilot_exit_decision
from app.demo.private_pilot_tracker import generate_private_pilot_tracker


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

DAY_3_REVIEW_COMMANDS = [
    ("Refresh system integrity", "python cli.py system-check"),
    ("Refresh release readiness", "python cli.py release-readiness"),
    ("Review Day 1 package", "python cli.py pilot-day-1-package"),
    ("Review Day 2 rhythm", "python cli.py pilot-day-2-rhythm"),
    ("Review pilot start confirmation", "python cli.py private-pilot-start-confirmation"),
    ("Refresh pilot tracker", "python cli.py private-pilot-tracker"),
    ("Refresh exit decision", "python cli.py private-pilot-exit-decision"),
    ("Review evidence index", "python cli.py evidence-index"),
]

DAY_3_EVIDENCE_SIGNALS = [
    "Required evidence completeness",
    "Start confirmation status",
    "Day 1 status",
    "Day 2 continuation decision",
    "Tracker status",
    "Exit decision status",
    "Highest exit risk",
]

DAY_3_REVIEW_QUESTIONS = [
    "Did the pilot repeat the core workflow without missing required evidence?",
    "Is the start confirmation still accepted, conditional, or blocked?",
    "Did the executive owner understand and accept the warning context?",
    "Are warnings stable enough to continue without expanding scope?",
    "Is there enough evidence to prepare an expansion review?",
    "Should Day 4 continue, pause, or prepare expansion?",
]

DAY_3_BOUNDARIES = [
    "Do not expand if required evidence is missing.",
    "Do not expand while Day 2 remains warning-heavy without owner confirmation.",
    "Do not treat an expansion review as expansion approval.",
    "Do not enable external delivery or expose private artifacts.",
]


RISK_ORDER = {
    "none": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _format_commands(commands):
    rows = [
        "| Purpose | Command |",
        "| --- | --- |",
    ]

    for purpose, command in commands:
        rows.append(f"| {purpose} | `{command}` |")

    return "\n".join(rows)


def _format_signal_rows(signals):
    rows = [
        "| Signal | Value |",
        "| --- | --- |",
    ]

    for signal, value in signals:
        rows.append(f"| {signal} | {value} |")

    return "\n".join(rows)


def _evidence_review_status(day_2, tracker, exit_decision):
    if day_2["day_2_status"] == "blocked" or tracker["missing_required"] > 0:
        return "blocked"

    start_confirmation_status = day_2.get("start_confirmation_status", "missing")
    if start_confirmation_status == "blocked":
        return "blocked"

    highest_risk = RISK_ORDER.get(exit_decision["highest_exit_risk"], 0)

    if (
        day_2["day_2_status"] == "continue_with_warnings"
        or tracker["tracker_status"] == "needs_attention"
        or "warnings" in exit_decision["decision_status"]
        or start_confirmation_status in {"missing", "requires_owner_confirmation"}
        or highest_risk >= RISK_ORDER["medium"]
    ):
        return "review_with_warnings"

    if exit_decision["recommended_decision"] == "expand_pilot":
        return "ready_for_expansion_review"

    return "evidence_review_ready"


def _recommendation(status, day_2, exit_decision):
    if status == "blocked":
        return "pause_for_required_evidence"

    if status == "review_with_warnings":
        return "continue_narrow_pilot"

    if (
        status == "ready_for_expansion_review"
        or exit_decision["recommended_decision"] == "expand_pilot"
        or day_2["continuation_decision"] == "prepare_controlled_expansion"
    ):
        return "prepare_expansion_review"

    return "continue_pilot_rhythm"


def _next_action(status, recommendation):
    if status == "blocked":
        return "Pause Day 3 progression and restore required pilot evidence before continuing."

    if recommendation == "continue_narrow_pilot":
        return "Continue the pilot in narrow mode and confirm warning acceptance with the executive owner."

    if recommendation == "prepare_expansion_review":
        return "Prepare an expansion review package, but do not approve expansion from Day 3 alone."

    return "Continue the pilot rhythm and collect Day 4 operating evidence."


def generate_pilot_day_3_evidence_review(conn=None):
    day_1 = generate_pilot_day_1_package(conn)
    day_2 = generate_pilot_day_2_rhythm(conn)
    tracker = generate_private_pilot_tracker(conn)
    exit_decision = generate_private_pilot_exit_decision(conn)
    day_3_status = _evidence_review_status(day_2, tracker, exit_decision)
    recommendation = _recommendation(day_3_status, day_2, exit_decision)

    evidence_signals = [
        ("Required evidence completeness", "complete" if tracker["missing_required"] == 0 else "missing_required"),
        ("Start confirmation status", day_2.get("start_confirmation_status", "missing")),
        ("Day 1 status", day_1["day_1_status"]),
        ("Day 2 continuation decision", day_2["continuation_decision"]),
        ("Tracker status", tracker["tracker_status"]),
        ("Exit decision status", exit_decision["decision_status"]),
        ("Highest exit risk", exit_decision["highest_exit_risk"]),
    ]

    return {
        "date": date.today().isoformat(),
        "day_3_status": day_3_status,
        "evidence_recommendation": recommendation,
        "pilot_owner": day_1["pilot_owner"],
        "primary_workflow": day_1["primary_workflow"],
        "day_1_status": day_1["day_1_status"],
        "day_2_status": day_2["day_2_status"],
        "start_confirmation_status": day_2.get("start_confirmation_status", "missing"),
        "start_confirmation_report": day_2.get("start_confirmation_report", "not_available"),
        "start_confirmation_detail": day_2.get("start_confirmation_detail", "No start confirmation detail recorded."),
        "continuation_decision": day_2["continuation_decision"],
        "tracker_status": tracker["tracker_status"],
        "exit_decision_status": exit_decision["decision_status"],
        "recommended_exit_decision": exit_decision["recommended_decision"],
        "highest_exit_risk": exit_decision["highest_exit_risk"],
        "available_evidence": tracker["available_evidence"],
        "missing_required_evidence": tracker["missing_required"],
        "missing_optional_evidence": tracker["missing_optional"],
        "commands": DAY_3_REVIEW_COMMANDS,
        "evidence_signals": evidence_signals,
        "review_questions": DAY_3_REVIEW_QUESTIONS,
        "boundaries": DAY_3_BOUNDARIES,
        "next_action": _next_action(day_3_status, recommendation),
    }


def export_pilot_day_3_evidence_review(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_day_3_evidence_review(conn)
    report_path = REPORTS_DIR / f"pilot_day_3_evidence_review_{result['date']}.md"

    content = f"""# Pilot Day 3 Evidence Review MVP v0.1

Date: {result['date']}

## Day 3 Summary

Day 3 status: {result['day_3_status']}
Evidence recommendation: {result['evidence_recommendation']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Day 1 status: {result['day_1_status']}
Day 2 status: {result['day_2_status']}
Start confirmation status: {result['start_confirmation_status']}
Start confirmation report: {result['start_confirmation_report']}
Start confirmation detail: {result['start_confirmation_detail']}
Continuation decision: {result['continuation_decision']}
Tracker status: {result['tracker_status']}
Exit decision status: {result['exit_decision_status']}
Recommended exit decision: {result['recommended_exit_decision']}
Highest exit risk: {result['highest_exit_risk']}
Available evidence: {result['available_evidence']}
Missing required evidence: {result['missing_required_evidence']}
Missing optional evidence: {result['missing_optional_evidence']}
Next action: {result['next_action']}

## Day 3 Review Commands

{_format_commands(result['commands'])}

## Evidence Signals

{_format_signal_rows(result['evidence_signals'])}

## Review Questions

{_format_bullets(result['review_questions'])}

## Day 3 Boundaries

{_format_bullets(result['boundaries'])}

## Operator Note

Day 3 is evidence review only. It may prepare an expansion review, but it does not approve expansion or change delivery controls.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "pilot_day_3_evidence_review_exported",
            "info" if result["day_3_status"] in ["evidence_review_ready", "ready_for_expansion_review"] else "warning",
            "Pilot Day 3 evidence review exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "day_3_status": result["day_3_status"],
                "evidence_recommendation": result["evidence_recommendation"],
                "primary_workflow": result["primary_workflow"],
            },
        )

    return result, str(report_path)


def print_pilot_day_3_evidence_review(conn=None):
    result, report_path = export_pilot_day_3_evidence_review(conn)

    print("Pilot Day 3 Evidence Review:")
    print(f"Date: {result['date']}")
    print(f"Day 3 status: {result['day_3_status']}")
    print(f"Evidence recommendation: {result['evidence_recommendation']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Day 2 status: {result['day_2_status']}")
    print(f"Start confirmation status: {result['start_confirmation_status']}")
    print(f"Continuation decision: {result['continuation_decision']}")
    print(f"Tracker status: {result['tracker_status']}")
    print(f"Missing required evidence: {result['missing_required_evidence']}")
    print(f"Highest exit risk: {result['highest_exit_risk']}")
    print(f"Next action: {result['next_action']}")
    print(f"Pilot Day 3 evidence review exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
