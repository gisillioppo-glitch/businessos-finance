from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT_DIR / "docs"
BOUNDARY_HEADING = "## Boundary Classification"


def get_boundary_classification_coverage():
    if not DOCS_DIR.exists():
        return {
            "total": 0,
            "covered": 0,
            "missing": ["docs folder missing"],
        }

    status_docs = sorted(DOCS_DIR.glob("*status.md"))
    missing = []

    for status_doc in status_docs:
        content = status_doc.read_text(encoding="utf-8")
        if BOUNDARY_HEADING not in content:
            missing.append(status_doc.name)

    total = len(status_docs)
    return {
        "total": total,
        "covered": total - len(missing),
        "missing": missing,
    }


def format_boundary_classification_detail(coverage):
    if coverage["total"] > 0 and not coverage["missing"]:
        return f"{coverage['covered']}/{coverage['total']} status docs covered"

    return "missing: " + ", ".join(coverage["missing"])
