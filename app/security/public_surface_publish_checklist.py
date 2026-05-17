from datetime import date
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from app.audit.audit_log import write_audit_log
from app.readiness.release_readiness import generate_release_readiness
from app.security.surface_audit import (
    BLOCKED_PUBLIC_PATHS,
    REQUIRED_PUBLIC_FILES,
    export_public_private_surface_audit,
)


ROOT_DIR = Path(__file__).resolve().parents[2]
PUBLIC_DIR = ROOT_DIR / "public"
REPORTS_DIR = ROOT_DIR / "reports"
LOCAL_LANDING_URL = "http://localhost:8000"


def _check(name, status, detail, severity="critical"):
    return {
        "name": name,
        "status": status,
        "detail": detail,
        "severity": severity,
    }


def _latest_report(prefix):
    if not REPORTS_DIR.exists():
        return None

    reports = sorted(
        REPORTS_DIR.glob(f"{prefix}_*.md"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return reports[0] if reports else None


def _public_files():
    if not PUBLIC_DIR.exists():
        return []

    return sorted(
        [path for path in PUBLIC_DIR.rglob("*") if path.is_file()],
        key=lambda path: str(path.relative_to(ROOT_DIR)),
    )


def _check_surface_audit(surface_audit):
    if surface_audit["failed_checks"] > 0:
        return _check(
            "surface_audit_gate",
            "blocked",
            f"{surface_audit['failed_checks']} failed surface audit check(s).",
        )

    if surface_audit["warning_checks"] > 0:
        return _check(
            "surface_audit_gate",
            "warning",
            f"{surface_audit['warning_checks']} surface audit warning(s) require review.",
            severity="medium",
        )

    return _check(
        "surface_audit_gate",
        "passed",
        "Public/private surface audit is clear.",
    )


def _check_release_readiness(readiness):
    if readiness["overall_status"] == "blocked":
        return _check(
            "release_readiness_gate",
            "blocked",
            "Release readiness is blocked.",
        )

    if readiness["warning_checks"] > 0:
        return _check(
            "release_readiness_gate",
            "warning",
            f"{readiness['warning_checks']} release readiness warning(s) require review.",
            severity="medium",
        )

    return _check(
        "release_readiness_gate",
        "passed",
        "Release readiness is ready.",
    )


def _check_required_public_files():
    missing = [
        path
        for path in REQUIRED_PUBLIC_FILES
        if not (ROOT_DIR / path).exists()
    ]

    if missing:
        return _check(
            "required_public_files",
            "blocked",
            f"Missing required public file(s): {', '.join(missing)}.",
        )

    return _check(
        "required_public_files",
        "passed",
        f"All {len(REQUIRED_PUBLIC_FILES)} required public files are present.",
    )


def _check_sensitive_public_paths():
    exposed = [
        path
        for path in BLOCKED_PUBLIC_PATHS
        if (ROOT_DIR / path).exists()
    ]

    if exposed:
        return _check(
            "sensitive_public_paths",
            "blocked",
            f"Sensitive path(s) found in public/: {', '.join(exposed)}.",
        )

    return _check(
        "sensitive_public_paths",
        "passed",
        "No blocked sensitive files are present under public/.",
    )


def _check_public_directory_inventory():
    files = _public_files()

    if not files:
        return _check(
            "public_inventory",
            "blocked",
            "No public files were found.",
        )

    return _check(
        "public_inventory",
        "passed",
        f"{len(files)} public file(s) available for static publish review.",
    )


def _check_lead_intake_surface():
    index_path = PUBLIC_DIR / "index.html"
    intake_path = PUBLIC_DIR / "lead-intake.js"

    if not index_path.exists() or not intake_path.exists():
        return _check(
            "lead_intake_surface",
            "blocked",
            "Landing index or lead intake script is missing.",
        )

    content = index_path.read_text(encoding="utf-8", errors="replace")
    if "demo-request-form" not in content:
        return _check(
            "lead_intake_surface",
            "warning",
            "Lead intake form marker was not found in public/index.html.",
            severity="medium",
        )

    return _check(
        "lead_intake_surface",
        "passed",
        "Lead intake form and script are present.",
    )


def _check_local_landing_response():
    try:
        with urlopen(LOCAL_LANDING_URL, timeout=5) as response:
            status_code = response.getcode()
    except URLError as error:
        return _check(
            "local_landing_response",
            "warning",
            f"{LOCAL_LANDING_URL} did not respond: {error}.",
            severity="medium",
        )

    if status_code != 200:
        return _check(
            "local_landing_response",
            "warning",
            f"{LOCAL_LANDING_URL} returned {status_code}.",
            severity="medium",
        )

    return _check(
        "local_landing_response",
        "passed",
        f"{LOCAL_LANDING_URL} returned 200.",
    )


def _format_check_rows(checks):
    rows = [
        "| Check | Status | Severity | Detail |",
        "| --- | --- | --- | --- |",
    ]

    for check in checks:
        detail = check["detail"].replace("|", "\\|")
        rows.append(
            f"| {check['name']} | {check['status']} | {check['severity']} | {detail} |"
        )

    return "\n".join(rows)


def _format_artifact_rows(artifacts):
    rows = [
        "| Artifact | Path |",
        "| --- | --- |",
    ]

    for label, path in artifacts:
        detail = str(path.relative_to(ROOT_DIR)) if path else "missing"
        rows.append(f"| {label} | {detail} |")

    return "\n".join(rows)


def _format_bullets(items):
    if not items:
        return "- None."

    return "\n".join(f"- {item}" for item in items)


def generate_public_surface_publish_checklist(conn=None):
    surface_audit, surface_report_path = export_public_private_surface_audit(conn)
    readiness = generate_release_readiness()

    checks = [
        _check_surface_audit(surface_audit),
        _check_release_readiness(readiness),
        _check_required_public_files(),
        _check_sensitive_public_paths(),
        _check_public_directory_inventory(),
        _check_lead_intake_surface(),
        _check_local_landing_response(),
    ]

    blocked = [check for check in checks if check["status"] == "blocked"]
    warnings = [check for check in checks if check["status"] == "warning"]

    if blocked:
        overall_status = "blocked"
    elif warnings:
        overall_status = "safe_with_warnings"
    else:
        overall_status = "safe"

    artifacts = [
        ("Surface Audit", Path(surface_report_path)),
        ("Release Readiness", _latest_report("release_readiness")),
        ("System Integrity", _latest_report("system_integrity")),
    ]

    return {
        "date": date.today().isoformat(),
        "overall_status": overall_status,
        "total_checks": len(checks),
        "passed_checks": len([check for check in checks if check["status"] == "passed"]),
        "warning_checks": len(warnings),
        "blocked_checks": len(blocked),
        "checks": checks,
        "artifacts": artifacts,
        "public_files_found": len(_public_files()),
        "surface_status": surface_audit["overall_status"],
        "release_status": readiness["overall_status"],
        "publish_guidance": [
            "Publish only the static public/ surface.",
            "Keep private dashboard, database, reports, credentials, and internal modules out of public hosting.",
            "If any checklist item is blocked, do not publish or present the public surface until fixed.",
            "Use Surface Audit and Release Readiness as evidence before external presentation.",
        ],
    }


def export_public_surface_publish_checklist(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_public_surface_publish_checklist(conn)
    report_path = REPORTS_DIR / f"public_surface_publish_checklist_{result['date']}.md"

    content = f"""# Public Surface Publish Checklist v0.1

Date: {result['date']}

## Summary

Overall status: {result['overall_status']}
Total checks: {result['total_checks']}
Passed checks: {result['passed_checks']}
Warning checks: {result['warning_checks']}
Blocked checks: {result['blocked_checks']}
Public files found: {result['public_files_found']}
Surface audit status: {result['surface_status']}
Release readiness status: {result['release_status']}

## Checklist

{_format_check_rows(result['checks'])}

## Evidence Artifacts

{_format_artifact_rows(result['artifacts'])}

## Publish Guidance

{_format_bullets(result['publish_guidance'])}

## Boundary Meaning

This checklist is a protected internal publish gate. It confirms whether the public static surface can be shown or published without exposing private BusinessOS runtime assets.

It is read-only. It does not deploy files, mutate private data, publish the dashboard, send email, or expose credentials.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "public_surface_publish_checklist_exported",
            "info" if result["overall_status"] == "safe" else "warning",
            "Public surface publish checklist exported.",
            {
                "overall_status": result["overall_status"],
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "warning_checks": result["warning_checks"],
                "blocked_checks": result["blocked_checks"],
            },
        )

    return result, str(report_path)


def print_public_surface_publish_checklist(conn=None):
    result, report_path = export_public_surface_publish_checklist(conn)

    print("Public Surface Publish Checklist:")
    print(f"Overall status: {result['overall_status']}")
    print(f"Total checks: {result['total_checks']}")
    print(f"Passed checks: {result['passed_checks']}")
    print(f"Warning checks: {result['warning_checks']}")
    print(f"Blocked checks: {result['blocked_checks']}")
    print(f"Public files found: {result['public_files_found']}")
    print(f"Surface audit status: {result['surface_status']}")
    print(f"Release readiness status: {result['release_status']}")
    print(f"Report exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return result
