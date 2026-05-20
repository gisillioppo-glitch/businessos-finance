from datetime import date
from pathlib import Path

from app.actions.area_review import export_finance_area_review
from app.audit.audit_log import write_audit_log
from app.governance.area_review import export_governance_area_review
from app.operations.area_review import export_operations_area_review
from app.reports.area_review_index import export_area_review_index
from app.support.area_review import export_support_area_review


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

AREA_REVIEW_EXPORTS = [
    ("Finance", export_finance_area_review),
    ("Operations", export_operations_area_review),
    ("Governance", export_governance_area_review),
    ("Support", export_support_area_review),
]


def _relative(path):
    return str(Path(path).relative_to(ROOT_DIR))


def _format_bundle_rows(area_results):
    rows = [
        "| Area | Review Status | Risk | Report |",
        "| --- | --- | --- | --- |",
    ]

    for area in area_results:
        rows.append(
            f"| {area['area']} | {area['review_status']} | {area['risk']} | {area['report_path']} |"
        )

    return "\n".join(rows)


def _freshness_status(index_result):
    if index_result["areas_missing"]:
        return "missing_area_reviews"

    if index_result["stale_areas"]:
        return "stale_area_reviews"

    return "fresh"


def _risk_for_area(area_name, result):
    if area_name == "Finance":
        return result["highest_financial_risk"]

    if area_name == "Operations":
        return result["highest_operational_risk"]

    if area_name == "Governance":
        return result["highest_sensitivity_risk"]

    if area_name == "Support":
        return result["highest_support_risk"]

    return "n/a"


def export_area_review_bundle(conn):
    REPORTS_DIR.mkdir(exist_ok=True)
    area_results = []

    for area_name, exporter in AREA_REVIEW_EXPORTS:
        result, report_path = exporter(conn)
        area_results.append(
            {
                "area": area_name,
                "review_status": result["review_status"],
                "risk": _risk_for_area(area_name, result),
                "report_path": _relative(report_path),
            }
        )

    index_result, index_report_path = export_area_review_index(conn)

    bundle = {
        "date": date.today().isoformat(),
        "overall_status": index_result["overall_status"],
        "freshness_status": _freshness_status(index_result),
        "areas_reviewed": len(area_results),
        "areas_missing": index_result["areas_missing"],
        "stale_areas": index_result["stale_areas"],
        "attention_areas": index_result["attention_areas"],
        "monitoring_areas": index_result["monitoring_areas"],
        "clear_areas": index_result["clear_areas"],
        "next_action": index_result["next_action"],
        "area_results": area_results,
        "index_report_path": _relative(index_report_path),
    }

    report_path = REPORTS_DIR / f"area_review_bundle_{bundle['date']}.md"
    content = f"""# Area Review Bundle v0.1

Date: {bundle['date']}

## Bundle Summary

Overall status: {bundle['overall_status']}
Freshness status: {bundle['freshness_status']}
Areas reviewed: {bundle['areas_reviewed']}
Areas missing: {bundle['areas_missing']}
Stale areas: {bundle['stale_areas']}
Attention areas: {bundle['attention_areas']}
Monitoring areas: {bundle['monitoring_areas']}
Clear areas: {bundle['clear_areas']}
Index report: {bundle['index_report_path']}
Next action: {bundle['next_action']}

## Refreshed Area Reviews

{_format_bundle_rows(bundle['area_results'])}

## Operator Note

This bundle refreshes area review artifacts and the executive index. It does not complete finance actions, resolve operations tasks, approve governance decisions, close support incidents, send notifications, or mutate operational records.
"""

    report_path.write_text(content, encoding="utf-8")

    write_audit_log(
        conn,
        "area_review_bundle_exported",
        "info" if bundle["overall_status"] == "area_review_clear" else "warning",
        "Area review bundle exported.",
        {
            "report_path": str(report_path.relative_to(ROOT_DIR)),
            "overall_status": bundle["overall_status"],
            "freshness_status": bundle["freshness_status"],
            "areas_reviewed": bundle["areas_reviewed"],
            "attention_areas": bundle["attention_areas"],
            "stale_areas": bundle["stale_areas"],
            "index_report": bundle["index_report_path"],
        },
    )

    return bundle, str(report_path)


def print_area_review_bundle(conn):
    result, report_path = export_area_review_bundle(conn)

    print("Area Review Bundle:")
    print(f"Date: {result['date']}")
    print(f"Overall status: {result['overall_status']}")
    print(f"Freshness status: {result['freshness_status']}")
    print(f"Areas reviewed: {result['areas_reviewed']}")
    print(f"Areas missing: {result['areas_missing']}")
    print(f"Stale areas: {result['stale_areas']}")
    print(f"Attention areas: {result['attention_areas']}")
    print(f"Monitoring areas: {result['monitoring_areas']}")
    print(f"Clear areas: {result['clear_areas']}")
    print(f"Index report: {result['index_report_path']}")
    print(f"Next action: {result['next_action']}")
    print(f"Area review bundle exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return result
