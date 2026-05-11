from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.pilot_day_1_package import generate_pilot_day_1_package
from app.demo.private_pilot_exit_decision import generate_private_pilot_exit_decision
from app.demo.private_pilot_tracker import generate_private_pilot_tracker


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

DAY_2_COMMANDS = [
    ("Morning system check", "python cli.py system-check"),
    ("Refresh release readiness", "python cli.py release-readiness"),
    ("Run daily close evidence", "python cli.py daily-close"),
    ("Review Day 1 package", "python cli.py pilot-day-1-package"),
    ("Refresh pilot tracker", "python cli.py private-pilot-tracker"),
    ("Refresh exit decision", "python cli.py private-pilot-exit-decision"),
    ("Review notification delivery approval", "python cli.py notification-delivery-approval"),
]

DAY_2_RHYTHM = [
    "Start with system-check and release-readiness before any pilot conversation.",
    "Run or confirm Executive Daily Close as the core evidence package.",
    "Review Day 1 warnings with the executive owner before expanding scope.",
    "Refresh the pilot tracker and confirm zero missing required evidence.",
    "Keep the pilot focused on Executive Daily Close unless the owner approves a narrow expansion.",
    "End Day 2 by naming the next owner action for Day 3.",
]

DAY_2_EVIDENCE = [
    "reports/system_integrity_YYYY-MM-DD.md",
    "reports/release_readiness_YYYY-MM-DD.md",
    "reports/daily_close_YYYY-MM-DD.md",
    "reports/private_pilot_tracker_YYYY-MM-DD.md",
    "reports/private_pilot_exit_decision_YYYY-MM-DD.md",
    "reports/pilot_day_1_package_YYYY-MM-DD.md",
]

DAY_2_REVIEW_CHECKS = [
    "Confirm Day 1 warnings were understood by the executive owner.",
    "Confirm no required evidence is missing before continuing pilot operations.",
    "Confirm notification delivery remains disabled or approval-gated unless explicitly configured.",
    "Confirm no public surface exposes private reports, database files, credentials, or local artifacts.",
    "Confirm whether Day 3 should continue, narrow, pause, or prepare for expansion.",
]

DAY_2_BOUNDARIES = [
    "Do not expand from one workflow to many workflows before warnings are resolved.",
    "Do not treat advisory exit decisions as automatic execution authority.",
    "Do not enable real email delivery without approved delivery controls and environment credentials.",
    "Do not expose pilot artifacts outside the private environment.",
]


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


def _day_2_status(day_1, tracker, exit_decision):
    if day_1["day_1_status"] == "blocked" or tracker["missing_required"] > 0:
        return "blocked"

    if (
        day_1["day_1_status"] == "ready_with_warnings"
        or tracker["tracker_status"] == "needs_attention"
        or "warnings" in exit_decision["decision_status"]
    ):
        return "continue_with_warnings"

    return "continue"


def _continuation_decision(day_2_status, exit_decision):
    if day_2_status == "blocked":
        return "pause_until_required_evidence_is_resolved"

    if day_2_status == "continue_with_warnings":
        return "continue_narrow_pilot"

    if exit_decision["recommended_decision"] == "expand_pilot":
        return "prepare_controlled_expansion"

    return "continue_pilot_rhythm"


def _next_action(day_2_status):
    if day_2_status == "blocked":
        return "Pause Day 2 expansion and resolve required evidence before continuing."

    if day_2_status == "continue_with_warnings":
        return "Continue Day 2 in narrow mode and review warnings with the executive owner before Day 3."

    return "Continue the pilot rhythm and prepare Day 3 evidence review."


def generate_pilot_day_2_rhythm(conn=None):
    day_1 = generate_pilot_day_1_package(conn)
    tracker = generate_private_pilot_tracker(conn)
    exit_decision = generate_private_pilot_exit_decision(conn)
    day_2_status = _day_2_status(day_1, tracker, exit_decision)

    return {
        "date": date.today().isoformat(),
        "day_2_status": day_2_status,
        "continuation_decision": _continuation_decision(day_2_status, exit_decision),
        "pilot_owner": day_1["pilot_owner"],
        "primary_workflow": day_1["primary_workflow"],
        "day_1_status": day_1["day_1_status"],
        "tracker_status": tracker["tracker_status"],
        "exit_decision_status": exit_decision["decision_status"],
        "recommended_exit_decision": exit_decision["recommended_decision"],
        "highest_exit_risk": exit_decision["highest_exit_risk"],
        "available_evidence": tracker["available_evidence"],
        "missing_required_evidence": tracker["missing_required"],
        "missing_optional_evidence": tracker["missing_optional"],
        "commands": DAY_2_COMMANDS,
        "rhythm": DAY_2_RHYTHM,
        "expected_evidence": DAY_2_EVIDENCE,
        "review_checks": DAY_2_REVIEW_CHECKS,
        "boundaries": DAY_2_BOUNDARIES,
        "next_action": _next_action(day_2_status),
    }


def export_pilot_day_2_rhythm(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_pilot_day_2_rhythm(conn)
    report_path = REPORTS_DIR / f"pilot_day_2_rhythm_{result['date']}.md"

    content = f"""# Pilot Day 2 Operating Rhythm MVP v0.1

Date: {result['date']}

## Day 2 Summary

Day 2 status: {result['day_2_status']}
Continuation decision: {result['continuation_decision']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Day 1 status: {result['day_1_status']}
Tracker status: {result['tracker_status']}
Exit decision status: {result['exit_decision_status']}
Recommended exit decision: {result['recommended_exit_decision']}
Highest exit risk: {result['highest_exit_risk']}
Available evidence: {result['available_evidence']}
Missing required evidence: {result['missing_required_evidence']}
Missing optional evidence: {result['missing_optional_evidence']}
Next action: {result['next_action']}

## Day 2 Command Runbook

{_format_commands(result['commands'])}

## Day 2 Operating Rhythm

{_format_bullets(result['rhythm'])}

## Expected Evidence

{_format_bullets(result['expected_evidence'])}

## Executive Review Checks

{_format_bullets(result['review_checks'])}

## Day 2 Boundaries

{_format_bullets(result['boundaries'])}

## Operator Note

Day 2 is about proving repeatability. Keep the pilot narrow, preserve evidence, and confirm warning context before any expansion.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "pilot_day_2_rhythm_exported",
            "info" if result["day_2_status"] == "continue" else "warning",
            "Pilot Day 2 operating rhythm exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "day_2_status": result["day_2_status"],
                "continuation_decision": result["continuation_decision"],
                "primary_workflow": result["primary_workflow"],
            },
        )

    return result, str(report_path)


def print_pilot_day_2_rhythm(conn=None):
    result, report_path = export_pilot_day_2_rhythm(conn)

    print("Pilot Day 2 Operating Rhythm:")
    print(f"Date: {result['date']}")
    print(f"Day 2 status: {result['day_2_status']}")
    print(f"Continuation decision: {result['continuation_decision']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Day 1 status: {result['day_1_status']}")
    print(f"Tracker status: {result['tracker_status']}")
    print(f"Missing required evidence: {result['missing_required_evidence']}")
    print(f"Next action: {result['next_action']}")
    print(f"Pilot Day 2 rhythm exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
