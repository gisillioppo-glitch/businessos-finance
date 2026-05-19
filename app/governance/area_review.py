from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.governance.findings import evaluate_governance_findings, print_governance_kpis
from app.governance.governance_brief import print_governance_brief
from app.governance.sensitivity_rules import (
    evaluate_governance_sensitivity_rules,
    print_governance_sensitivity_brief,
)


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

REVIEW_COMMANDS = [
    ("Review governance findings", "python cli.py gov-findings"),
    ("Review governance KPIs", "python cli.py gov-kpis"),
    ("Refresh governance brief", "python cli.py gov-brief"),
    ("Review sensitivity rules", "python cli.py gov-sensitivity"),
    ("Refresh sensitivity brief", "python cli.py gov-sensitivity-brief"),
    ("Review command center impact", "python cli.py command-center"),
    ("Confirm release readiness", "python cli.py release-readiness"),
]

REVIEW_CLOSE_CRITERIA = [
    "No high governance finding remains unresolved.",
    "Sensitive approval or access signal has an owner and decision path.",
    "Missing justification findings have been remediated or accepted with reason.",
    "Command Center no longer depends on governance risk for next best executive move.",
    "Daily Close can reference governance state without ambiguity.",
]


def _review_status(governance_kpis, sensitivity_brief):
    if governance_kpis["high_findings"] > 0 or sensitivity_brief["high_findings"] > 0:
        return "governance_review_high_risk"

    if governance_kpis["medium_findings"] > 0 or sensitivity_brief["medium_findings"] > 0:
        return "governance_review_required"

    if sensitivity_brief["sensitive_findings"] > 0:
        return "governance_review_monitoring_required"

    return "governance_clear"


def _review_recommendation(status):
    if status == "governance_review_high_risk":
        return "resolve_high_risk_governance_signals"

    if status == "governance_review_required":
        return "review_medium_risk_governance_signals"

    if status == "governance_review_monitoring_required":
        return "confirm_sensitive_signal_ownership"

    return "maintain_governance_controls"


def _next_action(status, findings, sensitivity_findings):
    if findings:
        first = findings[0]
        return f"Review {first['finding_type']} from {first['event_type']} and confirm remediation evidence."

    if sensitivity_findings:
        first = sensitivity_findings[0]
        return f"Review {first['finding_type']} from {first['source']} and confirm owner decision path."

    if status != "governance_clear":
        return "Review governance state and confirm owner path."

    return "Maintain governance monitoring cadence."


def _format_governance_findings(findings):
    rows = [
        "| Severity | Type | Event | Message |",
        "| --- | --- | --- | --- |",
    ]

    for finding in findings:
        rows.append(
            f"| {finding['severity']} | {finding['finding_type']} | {finding['event_type']} | {finding['message']} |"
        )

    return "\n".join(rows)


def _format_sensitivity_findings(findings):
    rows = [
        "| Severity | Type | Source | Message |",
        "| --- | --- | --- | --- |",
    ]

    for finding in findings:
        rows.append(
            f"| {finding['severity']} | {finding['finding_type']} | {finding['source']} | {finding['message']} |"
        )

    return "\n".join(rows)


def _format_bullets(items):
    if not items:
        return "- None."

    return "\n".join(f"- {item}" for item in items)


def _format_commands(commands):
    rows = [
        "| Purpose | Command |",
        "| --- | --- |",
    ]

    for purpose, command in commands:
        rows.append(f"| {purpose} | `{command}` |")

    return "\n".join(rows)


def generate_governance_area_review(conn):
    findings = evaluate_governance_findings(conn)
    governance_kpis = print_governance_kpis(conn, findings)
    governance_brief = print_governance_brief(conn, findings)
    sensitivity_findings = evaluate_governance_sensitivity_rules(conn)
    sensitivity_brief = print_governance_sensitivity_brief(conn, sensitivity_findings)
    status = _review_status(governance_kpis, sensitivity_brief)

    return {
        "date": date.today().isoformat(),
        "review_status": status,
        "review_recommendation": _review_recommendation(status),
        "highest_governance_risk": governance_brief["highest_governance_risk"],
        "audit_trail_health": governance_brief["audit_trail_health"],
        "findings_detected": governance_kpis["total_findings"],
        "high_findings": governance_kpis["high_findings"],
        "medium_findings": governance_kpis["medium_findings"],
        "sensitive_findings": sensitivity_brief["sensitive_findings"],
        "high_sensitivity_findings": sensitivity_brief["high_findings"],
        "medium_sensitivity_findings": sensitivity_brief["medium_findings"],
        "highest_sensitivity_risk": sensitivity_brief["highest_sensitivity_risk"],
        "findings": findings,
        "sensitivity_findings": sensitivity_findings,
        "commands": REVIEW_COMMANDS,
        "close_criteria": REVIEW_CLOSE_CRITERIA,
        "next_action": _next_action(status, findings, sensitivity_findings),
    }


def export_governance_area_review(conn):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_governance_area_review(conn)
    report_path = REPORTS_DIR / f"governance_area_review_{result['date']}.md"

    content = f"""# Governance Area Review v0.1

Date: {result['date']}

## Governance Area Summary

Review status: {result['review_status']}
Review recommendation: {result['review_recommendation']}
Highest governance risk: {result['highest_governance_risk']}
Audit trail health: {result['audit_trail_health']}
Governance findings detected: {result['findings_detected']}
High findings: {result['high_findings']}
Medium findings: {result['medium_findings']}
Sensitive findings: {result['sensitive_findings']}
High sensitivity findings: {result['high_sensitivity_findings']}
Medium sensitivity findings: {result['medium_sensitivity_findings']}
Highest sensitivity risk: {result['highest_sensitivity_risk']}
Next action: {result['next_action']}

## Governance Findings

{_format_governance_findings(result['findings']) if result['findings'] else 'No governance findings detected.'}

## Sensitivity Findings

{_format_sensitivity_findings(result['sensitivity_findings']) if result['sensitivity_findings'] else 'No sensitivity findings detected.'}

## Review Commands

{_format_commands(result['commands'])}

## Close Criteria

{_format_bullets(result['close_criteria'])}

## Operator Note

This review is advisory and read-only. It does not approve, reject, resolve, or bypass governance controls automatically. Governance decisions should remain explicit and evidence-backed.
"""

    report_path.write_text(content, encoding="utf-8")

    write_audit_log(
        conn,
        "governance_area_review_exported",
        "info" if result["review_status"] == "governance_clear" else "warning",
        "Governance area review exported.",
        {
            "report_path": str(report_path.relative_to(ROOT_DIR)),
            "review_status": result["review_status"],
            "findings_detected": result["findings_detected"],
            "sensitive_findings": result["sensitive_findings"],
            "highest_governance_risk": result["highest_governance_risk"],
            "highest_sensitivity_risk": result["highest_sensitivity_risk"],
        },
    )

    return result, str(report_path)


def print_governance_area_review(conn):
    result, report_path = export_governance_area_review(conn)

    print("Governance Area Review:")
    print(f"Date: {result['date']}")
    print(f"Review status: {result['review_status']}")
    print(f"Review recommendation: {result['review_recommendation']}")
    print(f"Highest governance risk: {result['highest_governance_risk']}")
    print(f"Highest sensitivity risk: {result['highest_sensitivity_risk']}")
    print(f"Governance findings detected: {result['findings_detected']}")
    print(f"Sensitive findings: {result['sensitive_findings']}")
    print(f"Next action: {result['next_action']}")
    print(f"Governance area review exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return result
