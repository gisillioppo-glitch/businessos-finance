from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.private_pilot_intake import generate_private_pilot_intake


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

PILOT_PHASES = [
    {
        "days": "Day 1",
        "phase": "Kickoff and boundary confirmation",
        "objective": "Confirm owner, scope, protected data boundary, and pilot success criteria.",
        "evidence": "Signed pilot scope and owner confirmation.",
    },
    {
        "days": "Days 2-3",
        "phase": "Baseline observation",
        "objective": "Run BusinessOS against current operating data and capture starting evidence.",
        "evidence": "Initial command center, daily close, and readiness artifacts.",
    },
    {
        "days": "Days 4-7",
        "phase": "Daily close rhythm",
        "objective": "Use Executive Daily Close as the primary operating rhythm and verify owner review.",
        "evidence": "Daily close reports, notification outbox, and evidence index.",
    },
    {
        "days": "Days 8-10",
        "phase": "Governance and approval review",
        "objective": "Review sensitive findings, approvals, escalation paths, and human-control rules.",
        "evidence": "Approval decisions, sensitivity findings, and audit logs.",
    },
    {
        "days": "Days 11-13",
        "phase": "Executive value review",
        "objective": "Compare daily rhythm, visibility, and decision quality against baseline pain points.",
        "evidence": "Pilot review notes and readiness reports.",
    },
    {
        "days": "Day 14",
        "phase": "Exit decision",
        "objective": "Decide whether to extend, expand, pause, or close the pilot.",
        "evidence": "Pilot exit decision and recommended next module.",
    },
]

DAILY_OPERATING_RHYTHM = [
    "Run or verify Executive Daily Close.",
    "Review Command Center health and highest risk.",
    "Review notification outbox and delivery approval status.",
    "Review governance sensitivity and approval items.",
    "Record owner feedback and next action for the following day.",
]

SUCCESS_CRITERIA = [
    "Executive owner reviews at least 5 daily close artifacts during the pilot.",
    "BusinessOS identifies at least one useful risk, action, or follow-up that would otherwise be manual.",
    "No sensitive data or credential boundary is violated.",
    "Pilot users can explain the value of the command layer in one sentence.",
    "Exit decision is made with evidence, not only opinion.",
]

EXIT_DECISIONS = [
    "Extend pilot: keep same workflow for another 14 days.",
    "Expand pilot: add one adjacent workflow or department.",
    "Convert to implementation: define production hardening requirements.",
    "Pause: resolve readiness/security gaps before continuing.",
    "Close: archive evidence and mark no current fit.",
]

PILOT_ROLES = [
    ("Executive Owner", "Maximum Authority", "Owns final decision and reviews daily close evidence."),
    ("Pilot Operator", "Operations / Admin", "Runs CLI/dashboard checks and captures evidence."),
    ("Governance Reviewer", "Governance / Compliance", "Reviews sensitive items, approvals, and boundaries."),
    ("Support Owner", "Support Manager", "Tracks incidents, questions, and pilot friction."),
]


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _format_phase_rows(phases):
    rows = [
        "| Days | Phase | Objective | Evidence |",
        "| --- | --- | --- | --- |",
    ]

    for phase in phases:
        rows.append(
            f"| {phase['days']} | {phase['phase']} | {phase['objective']} | {phase['evidence']} |"
        )

    return "\n".join(rows)


def _format_role_rows(roles):
    rows = [
        "| Role | Type | Responsibility |",
        "| --- | --- | --- |",
    ]

    for role, role_type, responsibility in roles:
        rows.append(f"| {role} | {role_type} | {responsibility} |")

    return "\n".join(rows)


def generate_private_pilot_plan(conn=None):
    today = date.today().isoformat()
    intake = generate_private_pilot_intake(conn)

    if intake["intake_status"] == "not_ready_for_pilot":
        plan_status = "blocked"
        first_action = "Resolve blocking readiness items before defining a pilot start date."
    elif intake["intake_status"] == "pilot_candidate_with_warnings":
        plan_status = "pilot_plan_ready_with_warnings"
        first_action = "Confirm warning context with the executive owner, then start with Executive Daily Close."
    else:
        plan_status = "pilot_plan_ready"
        first_action = "Schedule Day 1 kickoff and confirm owner, scope, and baseline evidence."

    return {
        "date": today,
        "plan_status": plan_status,
        "intake_status": intake["intake_status"],
        "recommended_module": intake["recommended_module"],
        "recommendation_reason": intake["recommendation_reason"],
        "first_action": first_action,
        "pilot_length_days": 14,
        "pilot_owner": "Executive Owner",
        "primary_workflow": intake["recommended_module"],
        "phases": PILOT_PHASES,
        "daily_rhythm": DAILY_OPERATING_RHYTHM,
        "success_criteria": SUCCESS_CRITERIA,
        "exit_decisions": EXIT_DECISIONS,
        "roles": PILOT_ROLES,
        "boundaries": intake["pilot_boundaries"],
    }


def export_private_pilot_plan(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_private_pilot_plan(conn)
    report_path = REPORTS_DIR / f"private_pilot_plan_{result['date']}.md"

    content = f"""# Private Pilot Plan MVP v0.1

Date: {result['date']}

## Pilot Plan Summary

Plan status: {result['plan_status']}
Intake status: {result['intake_status']}
Pilot length: {result['pilot_length_days']} days
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Recommended module: {result['recommended_module']}
Recommendation reason: {result['recommendation_reason']}
First action: {result['first_action']}

## Pilot Roles

{_format_role_rows(result['roles'])}

## 14-Day Pilot Timeline

{_format_phase_rows(result['phases'])}

## Daily Operating Rhythm

{_format_bullets(result['daily_rhythm'])}

## Success Criteria

{_format_bullets(result['success_criteria'])}

## Exit Decisions

{_format_bullets(result['exit_decisions'])}

## Pilot Boundaries

{_format_bullets(result['boundaries'])}

## Suggested Operator Note

Keep the pilot narrow. The first goal is not to automate everything; it is to prove that BusinessOS can create a trustworthy daily operating rhythm with evidence, ownership, and safe escalation.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "private_pilot_plan_exported",
            "info" if result["plan_status"] != "blocked" else "warning",
            "Private pilot plan exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "plan_status": result["plan_status"],
                "primary_workflow": result["primary_workflow"],
            },
        )

    return result, str(report_path)


def print_private_pilot_plan(conn=None):
    result, report_path = export_private_pilot_plan(conn)

    print("Private Pilot Plan:")
    print(f"Date: {result['date']}")
    print(f"Plan status: {result['plan_status']}")
    print(f"Pilot length: {result['pilot_length_days']} days")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"First action: {result['first_action']}")
    print(f"Private pilot plan exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
