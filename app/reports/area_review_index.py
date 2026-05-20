from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

AREA_REVIEW_SOURCES = [
    {
        "area": "Finance",
        "prefix": "finance_area_review",
        "risk_label": "Highest financial risk",
        "activity_label": "Active actions",
    },
    {
        "area": "Operations",
        "prefix": "operations_area_review",
        "risk_label": "Highest operational risk",
        "activity_label": "Active tasks",
    },
    {
        "area": "Governance",
        "prefix": "governance_area_review",
        "risk_label": "Highest sensitivity risk",
        "activity_label": "Sensitive findings",
    },
    {
        "area": "Support",
        "prefix": "support_area_review",
        "risk_label": "Highest support risk",
        "activity_label": "Active incidents",
    },
]

RISK_ORDER = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
    "none": 0,
    "n/a": 0,
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


def _extract_value(content, label, default="n/a"):
    for line in content.splitlines():
        if line.startswith(f"{label}:"):
            return line.split(":", 1)[1].strip()
    return default


def _risk_rank(value):
    return RISK_ORDER.get(value.lower(), 0)


def _area_status(entry):
    if entry["missing"]:
        return "missing"

    if entry["is_stale"]:
        return "stale"

    risk_rank = _risk_rank(entry["highest_risk"])
    active_value = entry["active_count"]

    if risk_rank >= RISK_ORDER["high"]:
        return "needs_executive_attention"

    if risk_rank == RISK_ORDER["medium"] or active_value not in {"0", "none", "n/a"}:
        return "monitoring_required"

    return "clear"


def _overall_status(entries):
    if any(entry["missing"] for entry in entries):
        return "area_review_index_incomplete"

    if any(entry["is_stale"] for entry in entries):
        return "area_review_index_stale"

    if any(entry["area_status"] == "needs_executive_attention" for entry in entries):
        return "area_review_attention_required"

    if any(entry["area_status"] == "monitoring_required" for entry in entries):
        return "area_review_monitoring_required"

    return "area_review_clear"


def _next_action(entries):
    missing = [entry for entry in entries if entry["missing"]]
    if missing:
        return f"Generate missing area review for {missing[0]['area']}."

    stale = [entry for entry in entries if entry["is_stale"]]
    if stale:
        return "Run python cli.py area-review-bundle to refresh stale area reviews."

    attention = [
        entry for entry in entries
        if entry["area_status"] == "needs_executive_attention"
    ]
    if attention:
        first = attention[0]
        return f"Review {first['area']} first: {first['next_action']}"

    monitoring = [
        entry for entry in entries
        if entry["area_status"] == "monitoring_required"
    ]
    if monitoring:
        first = monitoring[0]
        return f"Monitor {first['area']}: {first['next_action']}"

    return "Maintain area review cadence."


def _format_area_rows(entries):
    rows = [
        "| Area | Status | Freshness | Report Date | Risk | Active Signal | Source Report |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for entry in entries:
        rows.append(
            f"| {entry['area']} | {entry['area_status']} | {entry['freshness']} | {entry['report_date']} | {entry['highest_risk']} | {entry['active_label']}: {entry['active_count']} | {entry['report_path']} |"
        )

    return "\n".join(rows)


def _format_next_actions(entries):
    rows = [
        "| Area | Next Action |",
        "| --- | --- |",
    ]

    for entry in entries:
        rows.append(f"| {entry['area']} | {entry['next_action']} |")

    return "\n".join(rows)


def _load_area_entry(source, index_date):
    report = _latest_report(source["prefix"])

    if not report:
        return {
            "area": source["area"],
            "missing": True,
            "report_path": "missing",
            "report_date": "n/a",
            "freshness": "missing",
            "is_stale": False,
            "review_status": "missing",
            "review_recommendation": "generate_area_review",
            "highest_risk": "n/a",
            "active_label": source["activity_label"],
            "active_count": "n/a",
            "next_action": f"Generate {source['area']} area review.",
            "area_status": "missing",
        }

    content = report.read_text(encoding="utf-8")
    report_date = _extract_value(content, "Date")
    is_stale = report_date != index_date
    entry = {
        "area": source["area"],
        "missing": False,
        "report_path": str(report.relative_to(ROOT_DIR)),
        "report_date": report_date,
        "freshness": "stale" if is_stale else "fresh",
        "is_stale": is_stale,
        "review_status": _extract_value(content, "Review status"),
        "review_recommendation": _extract_value(content, "Review recommendation"),
        "highest_risk": _extract_value(content, source["risk_label"]),
        "active_label": source["activity_label"],
        "active_count": _extract_value(content, source["activity_label"]),
        "next_action": _extract_value(content, "Next action"),
    }
    entry["area_status"] = _area_status(entry)
    return entry


def generate_area_review_index():
    index_date = date.today().isoformat()
    entries = [_load_area_entry(source, index_date) for source in AREA_REVIEW_SOURCES]

    return {
        "date": index_date,
        "overall_status": _overall_status(entries),
        "areas_reviewed": sum(1 for entry in entries if not entry["missing"]),
        "areas_missing": sum(1 for entry in entries if entry["missing"]),
        "stale_areas": sum(1 for entry in entries if entry["is_stale"]),
        "attention_areas": sum(
            1 for entry in entries
            if entry["area_status"] == "needs_executive_attention"
        ),
        "monitoring_areas": sum(
            1 for entry in entries
            if entry["area_status"] == "monitoring_required"
        ),
        "clear_areas": sum(1 for entry in entries if entry["area_status"] == "clear"),
        "entries": entries,
        "next_action": _next_action(entries),
    }


def export_area_review_index(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    result = generate_area_review_index()
    report_path = REPORTS_DIR / f"area_review_index_{result['date']}.md"

    content = f"""# Area Review Executive Index v0.1

Date: {result['date']}

## Index Summary

Overall status: {result['overall_status']}
Areas reviewed: {result['areas_reviewed']}
Areas missing: {result['areas_missing']}
Stale areas: {result['stale_areas']}
Attention areas: {result['attention_areas']}
Monitoring areas: {result['monitoring_areas']}
Clear areas: {result['clear_areas']}
Next action: {result['next_action']}

## Area Status

{_format_area_rows(result['entries'])}

## Area Next Actions

{_format_next_actions(result['entries'])}

## Operator Note

This index is read-only. It summarizes the latest available area review reports and does not regenerate area reviews or mutate underlying Finance, Operations, Governance, or Support records.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "area_review_index_exported",
            "info" if result["overall_status"] == "area_review_clear" else "warning",
            "Area review executive index exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "overall_status": result["overall_status"],
                "areas_reviewed": result["areas_reviewed"],
                "areas_missing": result["areas_missing"],
                "stale_areas": result["stale_areas"],
                "attention_areas": result["attention_areas"],
            },
        )

    return result, str(report_path)


def print_area_review_index(conn=None):
    result, report_path = export_area_review_index(conn)

    print("Area Review Executive Index:")
    print(f"Date: {result['date']}")
    print(f"Overall status: {result['overall_status']}")
    print(f"Areas reviewed: {result['areas_reviewed']}")
    print(f"Areas missing: {result['areas_missing']}")
    print(f"Stale areas: {result['stale_areas']}")
    print(f"Attention areas: {result['attention_areas']}")
    print(f"Monitoring areas: {result['monitoring_areas']}")
    print(f"Clear areas: {result['clear_areas']}")
    print(f"Next action: {result['next_action']}")
    print(f"Area review index exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return result
