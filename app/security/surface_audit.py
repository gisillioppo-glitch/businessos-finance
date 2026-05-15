from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log


ROOT_DIR = Path(__file__).resolve().parents[2]
PUBLIC_DIR = ROOT_DIR / "public"
REPORTS_DIR = ROOT_DIR / "reports"
GITIGNORE_PATH = ROOT_DIR / ".gitignore"

REQUIRED_PUBLIC_FILES = [
    "public/index.html",
    "public/styles.css",
    "public/lead-intake.js",
    "public/assets/dashboard-preview.png",
]

BLOCKED_PUBLIC_PATHS = [
    "public/finance.db",
    "public/.env",
    "public/secrets.toml",
    "public/.streamlit/secrets.toml",
]

PRIVATE_PROTECTED_PATTERNS = [
    "finance.db",
    ".env",
    ".venv/",
    ".streamlit/secrets.toml",
]

FORBIDDEN_PUBLIC_REFERENCES = [
    "finance.db",
    "sqlite3",
    "from app.",
    "import app.",
    "BUSINESSOS_ADMIN_PASSWORD",
    ".env",
    "secrets.toml",
]

REQUIRED_PUBLIC_MARKERS = [
    "demo-request-form",
    "lead-intake.js",
    "request-demo",
]

PUBLIC_TEXT_SUFFIXES = {".html", ".css", ".js", ".txt", ".md"}


def _check(name, status, detail):
    return {
        "name": name,
        "status": status,
        "detail": detail,
    }


def _public_files():
    if not PUBLIC_DIR.exists():
        return []

    return sorted(
        [
            path
            for path in PUBLIC_DIR.rglob("*")
            if path.is_file()
        ],
        key=lambda path: str(path.relative_to(ROOT_DIR)),
    )


def _read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def _format_check_rows(checks):
    rows = [
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]

    for check in checks:
        detail = check["detail"].replace("|", "\\|")
        rows.append(f"| {check['name']} | {check['status']} | {detail} |")

    return "\n".join(rows)


def _format_public_file_rows(files):
    rows = [
        "| Public File | Size Bytes |",
        "| --- | ---: |",
    ]

    for path in files:
        rows.append(f"| {path.relative_to(ROOT_DIR)} | {path.stat().st_size} |")

    return "\n".join(rows)


def _format_bullets(items):
    if not items:
        return "- None."

    return "\n".join(f"- {item}" for item in items)


def _check_required_public_files():
    missing = [
        path
        for path in REQUIRED_PUBLIC_FILES
        if not (ROOT_DIR / path).exists()
    ]

    if missing:
        return _check(
            "required_public_files",
            "failed",
            f"Missing required public files: {', '.join(missing)}",
        )

    return _check(
        "required_public_files",
        "passed",
        f"All {len(REQUIRED_PUBLIC_FILES)} required public files exist.",
    )


def _check_blocked_public_paths():
    exposed = [
        path
        for path in BLOCKED_PUBLIC_PATHS
        if (ROOT_DIR / path).exists()
    ]

    if exposed:
        return _check(
            "blocked_public_paths",
            "failed",
            f"Blocked private paths found under public/: {', '.join(exposed)}",
        )

    return _check(
        "blocked_public_paths",
        "passed",
        "No blocked private files were found under public/.",
    )


def _check_gitignore_private_patterns():
    if not GITIGNORE_PATH.exists():
        return _check(
            "gitignore_private_patterns",
            "failed",
            ".gitignore is missing.",
        )

    content = _read_text(GITIGNORE_PATH)
    missing = [
        pattern
        for pattern in PRIVATE_PROTECTED_PATTERNS
        if pattern not in content
    ]

    if missing:
        return _check(
            "gitignore_private_patterns",
            "failed",
            f"Missing private protection patterns: {', '.join(missing)}",
        )

    return _check(
        "gitignore_private_patterns",
        "passed",
        f"All {len(PRIVATE_PROTECTED_PATTERNS)} private protection patterns are present.",
    )


def _check_public_reference_boundary():
    findings = []

    for path in _public_files():
        if path.suffix.lower() not in PUBLIC_TEXT_SUFFIXES:
            continue

        content = _read_text(path)
        for reference in FORBIDDEN_PUBLIC_REFERENCES:
            if reference in content:
                findings.append(f"{path.relative_to(ROOT_DIR)} contains {reference}")

    if findings:
        return _check(
            "public_reference_boundary",
            "failed",
            "; ".join(findings),
        )

    return _check(
        "public_reference_boundary",
        "passed",
        "Public text files do not reference private runtime internals or secrets.",
    )


def _check_public_lead_intake_markers():
    public_text = "\n".join(
        _read_text(path)
        for path in _public_files()
        if path.suffix.lower() in PUBLIC_TEXT_SUFFIXES
    )

    missing = [
        marker
        for marker in REQUIRED_PUBLIC_MARKERS
        if marker not in public_text
    ]

    if missing:
        return _check(
            "public_lead_intake_markers",
            "warning",
            f"Missing public lead intake marker(s): {', '.join(missing)}",
        )

    return _check(
        "public_lead_intake_markers",
        "passed",
        "Public landing lead-intake markers are present.",
    )


def generate_public_private_surface_audit():
    checks = [
        _check_required_public_files(),
        _check_blocked_public_paths(),
        _check_gitignore_private_patterns(),
        _check_public_reference_boundary(),
        _check_public_lead_intake_markers(),
    ]

    failed = [check for check in checks if check["status"] == "failed"]
    warnings = [check for check in checks if check["status"] == "warning"]

    if failed:
        overall_status = "surface_blocked"
    elif warnings:
        overall_status = "surface_ready_with_warnings"
    else:
        overall_status = "surface_ready"

    return {
        "date": date.today().isoformat(),
        "overall_status": overall_status,
        "total_checks": len(checks),
        "passed_checks": len([check for check in checks if check["status"] == "passed"]),
        "warning_checks": len(warnings),
        "failed_checks": len(failed),
        "checks": checks,
        "public_files": _public_files(),
        "findings": [check["detail"] for check in failed + warnings],
    }


def export_public_private_surface_audit(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_public_private_surface_audit()
    report_path = REPORTS_DIR / f"public_private_surface_audit_{result['date']}.md"

    content = f"""# Public Private Surface Audit v0.1

Date: {result['date']}

## Summary

Overall status: {result['overall_status']}
Total checks: {result['total_checks']}
Passed checks: {result['passed_checks']}
Warning checks: {result['warning_checks']}
Failed checks: {result['failed_checks']}
Public files found: {len(result['public_files'])}

## Public Surface Inventory

{_format_public_file_rows(result['public_files'])}

## Checks

{_format_check_rows(result['checks'])}

## Findings

{_format_bullets(result['findings'])}

## Boundary Meaning

The public landing surface can remain separate from the private BusinessOS runtime only if static assets stay under `public/` and private runtime files remain outside that directory.

This audit is read-only. It does not publish files, mutate private data, or send external communication.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "public_private_surface_audit_exported",
            "info" if result["failed_checks"] == 0 else "warning",
            "Public/private surface audit exported.",
            {
                "overall_status": result["overall_status"],
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "failed_checks": result["failed_checks"],
                "warning_checks": result["warning_checks"],
            },
        )

    return result, str(report_path)


def print_public_private_surface_audit(conn=None):
    result, report_path = export_public_private_surface_audit(conn)

    print("Public Private Surface Audit:")
    print(f"Overall status: {result['overall_status']}")
    print(f"Total checks: {result['total_checks']}")
    print(f"Passed checks: {result['passed_checks']}")
    print(f"Warning checks: {result['warning_checks']}")
    print(f"Failed checks: {result['failed_checks']}")
    print(f"Public files found: {len(result['public_files'])}")
    print(f"Report exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return result
