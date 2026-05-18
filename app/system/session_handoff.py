import subprocess
from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.system.boundary_classification import (
    format_boundary_classification_detail,
    get_boundary_classification_coverage,
)


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

KNOWN_LOCAL_ARTIFACTS = {
    '?? "BussinessOS Avance.pdf"',
    "?? BussinessOS Avance.pdf",
}

KEY_REPORT_PREFIXES = [
    "system_integrity",
    "release_readiness",
    "runtime_stability",
    "public_private_surface_audit",
    "public_surface_publish_checklist",
    "daily_close",
    "daily_close_distribution",
    "notification_delivery_approval",
    "secure_email_delivery",
    "pilot_expansion_review_prep",
    "pilot_expansion_review_decision",
]

NEXT_RECOMMENDED_BLOCKS = [
    "Pilot Expansion Decision Dashboard Refresh v0.2",
    "Support Area Review v0.1",
    "Operations Area Review v0.1",
]


def _run_git(command):
    result = subprocess.run(
        command,
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return None

    return result.stdout.strip()


def _git_status_lines():
    output = _run_git(["git", "status", "--short"])
    if output is None:
        return ["git status unavailable"]

    return [line.strip() for line in output.splitlines() if line.strip()]


def _latest_report(prefix):
    if not REPORTS_DIR.exists():
        return None

    reports = list(REPORTS_DIR.glob(f"{prefix}_*.md"))
    if prefix == "daily_close":
        reports = [
            report for report in reports
            if not report.name.startswith("daily_close_distribution_")
        ]

    reports = sorted(reports, key=lambda path: path.stat().st_mtime, reverse=True)
    return reports[0] if reports else None


def _extract_metric(content, label, default="unknown"):
    for line in content.splitlines():
        if line.startswith(f"{label}:"):
            return line.split(":", 1)[1].strip()
    return default


def _extract_first_metric(content, labels, default="unknown"):
    for label in labels:
        value = _extract_metric(content, label, None)
        if value is not None:
            return value
    return default


def _report_summary(prefix):
    report = _latest_report(prefix)
    if not report:
        return {
            "name": prefix,
            "path": "missing",
            "status": "missing",
            "detail": "No report found",
        }

    content = report.read_text(encoding="utf-8")
    status_labels = [
        "Overall status",
        "Release readiness status",
        "Surface audit status",
        "Expansion prep status",
        "Decision status",
        "Delivery mode",
    ]
    if prefix == "pilot_expansion_review_decision":
        status_labels = ["Decision status", *status_labels]
    elif prefix == "pilot_expansion_review_prep":
        status_labels = ["Expansion prep status", *status_labels]

    status = _extract_first_metric(content, status_labels)
    failed = _extract_first_metric(content, ["Failed checks", "Blocked checks"], "n/a")
    warnings = _extract_metric(content, "Warning checks", "n/a")

    return {
        "name": prefix,
        "path": str(report.relative_to(ROOT_DIR)),
        "status": status,
        "detail": f"failed: {failed} | warnings: {warnings}",
    }


def _format_report_rows(reports):
    rows = [
        "| Report | Latest Artifact | Status | Detail |",
        "| --- | --- | --- | --- |",
    ]

    for report in reports:
        detail = report["detail"].replace("|", "\\|")
        rows.append(
            f"| {report['name']} | {report['path']} | {report['status']} | {detail} |"
        )

    return "\n".join(rows)


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def generate_session_handoff_snapshot():
    today = date.today().isoformat()
    git_lines = _git_status_lines()
    handoff_report_lines = {
        f"?? reports/session_handoff_{today}.md",
        f" M reports/session_handoff_{today}.md",
        f"M reports/session_handoff_{today}.md",
    }
    relevant_git_lines = [
        line
        for line in git_lines
        if line not in KNOWN_LOCAL_ARTIFACTS and line not in handoff_report_lines
    ]

    latest_commit = _run_git(["git", "log", "-1", "--oneline"]) or "unknown"
    head_tags = _run_git(["git", "tag", "--points-at", "HEAD"]) or "none"
    current_branch = _run_git(["git", "branch", "--show-current"]) or "unknown"

    boundary_coverage = get_boundary_classification_coverage()
    report_summaries = [_report_summary(prefix) for prefix in KEY_REPORT_PREFIXES]

    return {
        "date": today,
        "branch": current_branch,
        "latest_commit": latest_commit,
        "head_tags": head_tags.splitlines() if head_tags != "none" else ["none"],
        "git_status": "clean except known local artifacts" if not relevant_git_lines else "; ".join(relevant_git_lines),
        "known_local_artifacts": ["BussinessOS Avance.pdf"],
        "boundary_coverage": format_boundary_classification_detail(boundary_coverage),
        "reports": report_summaries,
        "next_recommended_blocks": NEXT_RECOMMENDED_BLOCKS,
    }


def export_session_handoff_snapshot(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_session_handoff_snapshot()
    report_path = REPORTS_DIR / f"session_handoff_{result['date']}.md"

    content = f"""# BusinessOS Session Handoff Snapshot v0.1

Date: {result['date']}

## Current Git State

Branch: {result['branch']}
Latest commit: {result['latest_commit']}
Head tag(s):
{_format_bullets(result['head_tags'])}
Git status: {result['git_status']}
Known local artifacts:
{_format_bullets(result['known_local_artifacts'])}

## Governance Coverage

Boundary classification coverage: {result['boundary_coverage']}

## Latest System Artifacts

{_format_report_rows(result['reports'])}

## Recommended Next Blocks

{_format_bullets(result['next_recommended_blocks'])}

## Operator Note

This handoff snapshot is a read-only operating summary for pausing, resuming, or moving work across chats. It does not mutate operational records or publish any public surface.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "session_handoff_snapshot_exported",
            "info",
            "Session handoff snapshot exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "git_status": result["git_status"],
                "boundary_coverage": result["boundary_coverage"],
            },
        )

    return result, str(report_path)


def print_session_handoff_snapshot(conn=None):
    result, report_path = export_session_handoff_snapshot(conn)

    print("BusinessOS Session Handoff Snapshot:")
    print(f"Date: {result['date']}")
    print(f"Branch: {result['branch']}")
    print(f"Latest commit: {result['latest_commit']}")
    print(f"Git status: {result['git_status']}")
    print(f"Boundary classification coverage: {result['boundary_coverage']}")
    print("Recommended next blocks:")
    for block in result["next_recommended_blocks"]:
        print(f"- {block}")

    print(f"Session handoff snapshot exported: {Path(report_path).relative_to(ROOT_DIR)}")
    return result
