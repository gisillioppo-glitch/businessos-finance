from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.private_demo_dry_run import generate_private_demo_dry_run
from app.readiness.release_readiness import generate_release_readiness


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

PILOT_DIAGNOSTIC_QUESTIONS = [
    "What daily executive process currently requires the most manual follow-up?",
    "Who owns finance, operations, governance, support, and daily close decisions?",
    "Which decisions should never execute without approval?",
    "What evidence does leadership need at the end of each day?",
    "Which notifications should be internal-only versus externally delivered?",
    "What data must stay private during the pilot?",
    "What would make the pilot successful after 14 days?",
]

PILOT_MODULE_OPTIONS = [
    {
        "module": "Executive Daily Close",
        "fit": "Best first pilot when leadership needs daily evidence, notifications, and operating rhythm.",
        "owner": "Executive Owner",
        "risk": "Medium",
    },
    {
        "module": "Approvals + Governance Sensitivity",
        "fit": "Best first pilot when the organization needs control over sensitive actions and decision approvals.",
        "owner": "Governance / Executive Owner",
        "risk": "High",
    },
    {
        "module": "Command Center Dashboard",
        "fit": "Best first pilot when the organization needs unified visibility before automation.",
        "owner": "Executive Owner",
        "risk": "Medium",
    },
    {
        "module": "Support + Assistance",
        "fit": "Best first pilot when internal help, escalation, and incident follow-up are fragmented.",
        "owner": "Support Manager",
        "risk": "Medium",
    },
]

PILOT_READINESS_CRITERIA = [
    "Private demo dry run is not blocked.",
    "Release readiness has no failed checks.",
    "Pilot scope is limited to one primary workflow.",
    "Maximum Authority owner is identified.",
    "Sensitive files, credentials, and private database remain outside public surface.",
    "Real external email delivery remains disabled until explicitly configured and approved.",
]

PILOT_BOUNDARIES = [
    "Do not promise public production deployment during the private pilot.",
    "Do not expose raw finance.db, credentials, local files, or repository internals.",
    "Do not enable real email delivery without SMTP credentials, approval gate, and dry-run review.",
    "Do not broaden the pilot beyond one workflow until success criteria are reviewed.",
]


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _format_numbered(items):
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def _format_module_rows(modules):
    rows = [
        "| Module | Fit | Suggested Owner | Risk |",
        "| --- | --- | --- | --- |",
    ]

    for module in modules:
        rows.append(
            f"| {module['module']} | {module['fit']} | {module['owner']} | {module['risk']} |"
        )

    return "\n".join(rows)


def _recommended_starting_module(dry_run, readiness):
    if dry_run["overall_status"] == "blocked" or readiness["overall_status"] == "blocked":
        return {
            "module": "No pilot yet",
            "reason": "Resolve blocking readiness checks before proposing a private pilot.",
        }

    if dry_run["warning_checks"] > 0 or readiness["warning_checks"] > 0:
        return {
            "module": "Executive Daily Close",
            "reason": "Start with controlled evidence and daily operating rhythm while naming readiness warnings clearly.",
        }

    return {
        "module": "Command Center Dashboard + Executive Daily Close",
        "reason": "Readiness is green enough to present unified visibility plus daily close as the first private pilot loop.",
    }


def generate_private_pilot_intake(conn=None):
    today = date.today().isoformat()
    readiness = generate_release_readiness()
    dry_run = generate_private_demo_dry_run(conn)
    recommendation = _recommended_starting_module(dry_run, readiness)

    blocked = dry_run["overall_status"] == "blocked" or readiness["overall_status"] == "blocked"
    if blocked:
        intake_status = "not_ready_for_pilot"
    elif dry_run["warning_checks"] > 0 or readiness["warning_checks"] > 0:
        intake_status = "pilot_candidate_with_warnings"
    else:
        intake_status = "pilot_candidate"

    return {
        "date": today,
        "intake_status": intake_status,
        "readiness_status": readiness["overall_status"],
        "dry_run_status": dry_run["overall_status"],
        "recommended_module": recommendation["module"],
        "recommendation_reason": recommendation["reason"],
        "diagnostic_questions": PILOT_DIAGNOSTIC_QUESTIONS,
        "module_options": PILOT_MODULE_OPTIONS,
        "readiness_criteria": PILOT_READINESS_CRITERIA,
        "pilot_boundaries": PILOT_BOUNDARIES,
    }


def export_private_pilot_intake(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_private_pilot_intake(conn)
    report_path = REPORTS_DIR / f"private_pilot_intake_{result['date']}.md"

    content = f"""# Private Pilot Intake MVP v0.1

Date: {result['date']}

## Pilot Intake Status

Intake status: {result['intake_status']}
Release readiness: {result['readiness_status']}
Private demo dry run: {result['dry_run_status']}
Recommended starting module: {result['recommended_module']}
Recommendation reason: {result['recommendation_reason']}

## Diagnostic Questions

{_format_numbered(result['diagnostic_questions'])}

## Candidate Pilot Modules

{_format_module_rows(result['module_options'])}

## Pilot Readiness Criteria

{_format_bullets(result['readiness_criteria'])}

## Pilot Boundaries

{_format_bullets(result['pilot_boundaries'])}

## Suggested Close

If the organization agrees with the recommended starting module, define a 14-day private pilot with one executive owner, one workflow, daily evidence review, and no public deployment commitment.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "private_pilot_intake_exported",
            "info" if result["intake_status"] != "not_ready_for_pilot" else "warning",
            "Private pilot intake exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "intake_status": result["intake_status"],
                "recommended_module": result["recommended_module"],
            },
        )

    return result, str(report_path)


def print_private_pilot_intake(conn=None):
    result, report_path = export_private_pilot_intake(conn)

    print("Private Pilot Intake:")
    print(f"Date: {result['date']}")
    print(f"Intake status: {result['intake_status']}")
    print(f"Release readiness: {result['readiness_status']}")
    print(f"Private demo dry run: {result['dry_run_status']}")
    print(f"Recommended starting module: {result['recommended_module']}")
    print(f"Diagnostic questions: {len(result['diagnostic_questions'])}")
    print(f"Private pilot intake exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
