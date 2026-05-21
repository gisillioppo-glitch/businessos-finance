from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.private_demo_final_review import generate_private_demo_final_review
from app.demo.private_pilot_plan import generate_private_pilot_plan
from app.demo.private_pilot_tracker import generate_private_pilot_tracker


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"


START_CONDITIONS = [
    "Private demo final review is ready for private demo.",
    "Pilot plan is ready and limited to one primary workflow.",
    "Pilot tracker has required evidence available.",
    "Executive Owner is confirmed as Maximum Authority.",
    "No public deployment commitment is made during pilot start.",
    "Real external email delivery remains disabled unless separately approved and configured.",
]

NO_START_CONDITIONS = [
    "Private demo final review is blocked.",
    "Pilot plan is blocked.",
    "Pilot tracker is blocked or missing required evidence.",
    "Executive owner is not confirmed.",
    "Pilot scope expands beyond one workflow before Day 1.",
    "Public/private boundary cannot be explained clearly to the pilot evaluator.",
]

DAY_1_OPERATOR_ACTIONS = [
    "Confirm executive owner and pilot operator.",
    "Confirm primary workflow and pilot boundaries.",
    "Review private demo final review status.",
    "Review pilot plan and daily tracker evidence.",
    "Start Day 1 only if the final gate is ready or ready with named conditions.",
]


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _format_gate_rows(gates):
    rows = [
        "| Gate | Status | Detail |",
        "| --- | --- | --- |",
    ]

    for gate in gates:
        detail = str(gate["detail"]).replace("|", "\\|")
        rows.append(f"| {gate['name']} | {gate['status']} | {detail} |")

    return "\n".join(rows)


def _gate(name, status, detail):
    return {
        "name": name,
        "status": status,
        "detail": detail,
    }


def _final_status(gates):
    if any(gate["status"] == "blocked" for gate in gates):
        return "blocked"

    if any(gate["status"] == "condition" for gate in gates):
        return "ready_with_conditions"

    return "ready_to_start_private_pilot"


def _recommendation(status):
    if status == "blocked":
        return "Do not start the private pilot. Resolve blocked gates before Day 1."

    if status == "ready_with_conditions":
        return "Start only if the executive owner accepts the named conditions and the scope stays narrow."

    return "Ready to start the private pilot with one owner, one workflow, and daily evidence review."


def generate_private_pilot_start_gate(conn=None):
    today = date.today().isoformat()
    demo_review = generate_private_demo_final_review(conn)
    pilot_plan = generate_private_pilot_plan(conn)
    pilot_tracker = generate_private_pilot_tracker(conn)

    gates = []

    if demo_review["final_status"] == "blocked":
        gates.append(
            _gate(
                "Private demo final review",
                "blocked",
                "Private demo final review is blocked.",
            )
        )
    elif demo_review["final_status"] == "ready_with_warnings":
        gates.append(
            _gate(
                "Private demo final review",
                "condition",
                "Warnings must be named before starting pilot.",
            )
        )
    else:
        gates.append(
            _gate(
                "Private demo final review",
                "passed",
                "Ready for private demo.",
            )
        )

    if pilot_plan["plan_status"] == "blocked":
        gates.append(_gate("Pilot plan", "blocked", pilot_plan["first_action"]))
    elif pilot_plan["plan_status"] == "pilot_plan_ready_with_warnings":
        gates.append(_gate("Pilot plan", "condition", pilot_plan["first_action"]))
    else:
        gates.append(_gate("Pilot plan", "passed", pilot_plan["first_action"]))

    if pilot_tracker["tracker_status"] == "blocked":
        gates.append(_gate("Pilot tracker", "blocked", pilot_tracker["next_action"]))
    elif pilot_tracker["tracker_status"] == "needs_attention":
        gates.append(_gate("Pilot tracker", "condition", pilot_tracker["next_action"]))
    else:
        gates.append(_gate("Pilot tracker", "passed", pilot_tracker["next_action"]))

    owner_status = "passed" if pilot_plan["pilot_owner"] == "Executive Owner" else "condition"
    gates.append(
        _gate(
            "Executive owner",
            owner_status,
            pilot_plan["pilot_owner"],
        )
    )

    workflow_status = "passed" if pilot_plan["primary_workflow"] else "blocked"
    gates.append(
        _gate(
            "Pilot workflow",
            workflow_status,
            pilot_plan["primary_workflow"] or "missing",
        )
    )

    status = _final_status(gates)

    return {
        "date": today,
        "start_gate_status": status,
        "recommendation": _recommendation(status),
        "demo_final_status": demo_review["final_status"],
        "pilot_plan_status": pilot_plan["plan_status"],
        "pilot_tracker_status": pilot_tracker["tracker_status"],
        "pilot_owner": pilot_plan["pilot_owner"],
        "primary_workflow": pilot_plan["primary_workflow"],
        "pilot_length_days": pilot_plan["pilot_length_days"],
        "gates": gates,
        "passed_gates": sum(1 for gate in gates if gate["status"] == "passed"),
        "conditional_gates": sum(1 for gate in gates if gate["status"] == "condition"),
        "blocked_gates": sum(1 for gate in gates if gate["status"] == "blocked"),
        "start_conditions": START_CONDITIONS,
        "no_start_conditions": NO_START_CONDITIONS,
        "day_1_operator_actions": DAY_1_OPERATOR_ACTIONS,
    }


def export_private_pilot_start_gate(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_private_pilot_start_gate(conn)
    report_path = REPORTS_DIR / f"private_pilot_start_gate_{result['date']}.md"

    content = f"""# Private Pilot Start Gate v0.1

Date: {result['date']}

## Start Gate Summary

Start gate status: {result['start_gate_status']}
Recommendation: {result['recommendation']}
Private demo final review: {result['demo_final_status']}
Pilot plan: {result['pilot_plan_status']}
Pilot tracker: {result['pilot_tracker_status']}
Pilot owner: {result['pilot_owner']}
Primary workflow: {result['primary_workflow']}
Pilot length: {result['pilot_length_days']} days
Passed gates: {result['passed_gates']}
Conditional gates: {result['conditional_gates']}
Blocked gates: {result['blocked_gates']}

## Gates

{_format_gate_rows(result['gates'])}

## Start Conditions

{_format_bullets(result['start_conditions'])}

## No-Start Conditions

{_format_bullets(result['no_start_conditions'])}

## Day 1 Operator Actions

{_format_bullets(result['day_1_operator_actions'])}

## Operator Note

This gate does not start the pilot automatically. It tells the operator whether Day 1 can begin, whether named conditions must be accepted, or whether the pilot should stay blocked.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "private_pilot_start_gate_exported",
            "info" if result["start_gate_status"] != "blocked" else "warning",
            "Private pilot start gate exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "start_gate_status": result["start_gate_status"],
                "conditional_gates": result["conditional_gates"],
                "blocked_gates": result["blocked_gates"],
            },
        )

    return result, str(report_path)


def print_private_pilot_start_gate(conn=None):
    result, report_path = export_private_pilot_start_gate(conn)

    print("Private Pilot Start Gate:")
    print(f"Date: {result['date']}")
    print(f"Start gate status: {result['start_gate_status']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Private demo final review: {result['demo_final_status']}")
    print(f"Pilot plan: {result['pilot_plan_status']}")
    print(f"Pilot tracker: {result['pilot_tracker_status']}")
    print(f"Pilot owner: {result['pilot_owner']}")
    print(f"Primary workflow: {result['primary_workflow']}")
    print(f"Gates: {result['passed_gates']} passed, {result['conditional_gates']} condition, {result['blocked_gates']} blocked")
    print(f"Private pilot start gate exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
