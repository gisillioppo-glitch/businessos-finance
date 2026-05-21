from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.private_demo_dry_run import export_private_demo_dry_run
from app.demo.private_demo_package import DO_NOT_SHOW_ITEMS, PRE_DEMO_CHECKLIST, SHOW_ITEMS
from app.readiness.release_readiness import generate_release_readiness


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"


SUPPORTING_ARTIFACTS = [
    ("Release Readiness", "release_readiness"),
    ("System Integrity", "system_integrity"),
    ("Runtime Stability", "runtime_stability"),
    ("Area Review Index", "area_review_index"),
    ("Daily Close", "daily_close"),
    ("Private Demo Package", "private_demo_package"),
    ("Private Demo Script", "private_demo_script"),
    ("Private Demo Dry Run", "private_demo_dry_run"),
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


def _find_check(checks, name):
    for check in checks:
        if check["name"] == name:
            return check
    return {
        "name": name,
        "status": "missing",
        "severity": "critical",
        "detail": "not found",
    }


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _format_check_rows(checks):
    rows = [
        "| Check | Status | Severity | Detail |",
        "| --- | --- | --- | --- |",
    ]

    for check in checks:
        detail = str(check["detail"]).replace("|", "\\|")
        rows.append(
            f"| {check['name']} | {check['status']} | {check['severity']} | {detail} |"
        )

    return "\n".join(rows)


def _format_artifact_rows(artifacts):
    rows = [
        "| Artifact | Latest report |",
        "| --- | --- |",
    ]

    for artifact in artifacts:
        rows.append(f"| {artifact['label']} | {artifact['path']} |")

    return "\n".join(rows)


def _build_artifacts():
    artifacts = []

    for label, prefix in SUPPORTING_ARTIFACTS:
        report = _latest_report(prefix)
        artifacts.append(
            {
                "label": label,
                "path": str(report.relative_to(ROOT_DIR)) if report else "missing",
            }
        )

    return artifacts


def _final_status(readiness, dry_run):
    if readiness["overall_status"] == "blocked" or dry_run["overall_status"] == "blocked":
        return "blocked"

    if (
        readiness["overall_status"] == "ready_with_warnings"
        or dry_run["overall_status"] == "ready_with_warnings"
    ):
        return "ready_with_warnings"

    return "ready_for_private_demo"


def _recommendation(final_status):
    if final_status == "blocked":
        return "Do not run the private demo. Resolve failed checks first."

    if final_status == "ready_with_warnings":
        return "Demo only if the warning is named clearly and the demo stays inside the protected boundary."

    return "Ready for private demo. Keep the demo inside the prepared show list and avoid private internals."


def generate_private_demo_final_review(conn=None):
    today = date.today().isoformat()
    readiness = generate_release_readiness()
    dry_run, dry_run_path = export_private_demo_dry_run(conn)
    area_freshness = _find_check(readiness["checks"], "Area review freshness")
    boundary_coverage = _find_check(readiness["checks"], "Boundary classification coverage")

    final_status = _final_status(readiness, dry_run)

    return {
        "date": today,
        "final_status": final_status,
        "recommendation": _recommendation(final_status),
        "readiness_status": readiness["overall_status"],
        "readiness_total": readiness["total_checks"],
        "readiness_passed": readiness["passed_checks"],
        "readiness_warnings": readiness["warning_checks"],
        "readiness_failed": readiness["failed_checks"],
        "dry_run_status": dry_run["overall_status"],
        "dry_run_total": dry_run["total_checks"],
        "dry_run_passed": dry_run["passed_checks"],
        "dry_run_warnings": dry_run["warning_checks"],
        "dry_run_failed": dry_run["failed_checks"],
        "dry_run_path": str(Path(dry_run_path).relative_to(ROOT_DIR)),
        "area_freshness": area_freshness,
        "boundary_coverage": boundary_coverage,
        "readiness_checks": readiness["checks"],
        "dry_run_checks": dry_run["checks"],
        "artifacts": _build_artifacts(),
        "show_items": SHOW_ITEMS,
        "do_not_show_items": DO_NOT_SHOW_ITEMS,
        "pre_demo_checklist": PRE_DEMO_CHECKLIST,
    }


def export_private_demo_final_review(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_private_demo_final_review(conn)
    report_path = REPORTS_DIR / f"private_demo_final_review_{result['date']}.md"

    content = f"""# Private Demo Final Review v0.1

Date: {result['date']}

## Final Demo Decision

Final status: {result['final_status']}
Recommendation: {result['recommendation']}

## Readiness Summary

Release readiness: {result['readiness_status']}
Readiness checks: {result['readiness_passed']} passed, {result['readiness_warnings']} warning, {result['readiness_failed']} failed, {result['readiness_total']} total

Private demo dry run: {result['dry_run_status']}
Dry run checks: {result['dry_run_passed']} passed, {result['dry_run_warnings']} warning, {result['dry_run_failed']} failed, {result['dry_run_total']} total
Dry run report: {result['dry_run_path']}

## Freshness And Boundary Gates

Area review freshness: {result['area_freshness']['status']} | {result['area_freshness']['detail']}
Boundary coverage: {result['boundary_coverage']['status']} | {result['boundary_coverage']['detail']}

## Supporting Artifacts

{_format_artifact_rows(result['artifacts'])}

## Show

{_format_bullets(result['show_items'])}

## Do Not Show

{_format_bullets(result['do_not_show_items'])}

## Pre-Demo Checklist

{_format_bullets(result['pre_demo_checklist'])}

## Release Readiness Checks

{_format_check_rows(result['readiness_checks'])}

## Dry Run Checks

{_format_check_rows(result['dry_run_checks'])}
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "private_demo_final_review_exported",
            "info" if result["final_status"] != "blocked" else "warning",
            "Private demo final review exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "final_status": result["final_status"],
                "readiness_status": result["readiness_status"],
                "dry_run_status": result["dry_run_status"],
            },
        )

    return result, str(report_path)


def print_private_demo_final_review(conn=None):
    result, report_path = export_private_demo_final_review(conn)

    print("Private Demo Final Review:")
    print(f"Date: {result['date']}")
    print(f"Final status: {result['final_status']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Release readiness: {result['readiness_status']}")
    print(f"Private demo dry run: {result['dry_run_status']}")
    print(
        "Area review freshness: "
        f"{result['area_freshness']['status']} | {result['area_freshness']['detail']}"
    )
    print(f"Private demo final review exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return result
