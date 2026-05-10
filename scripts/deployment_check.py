"""Deployment readiness checks for BusinessOS MVP."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

PUBLIC_REQUIRED_FILES = [
    "public/index.html",
    "public/styles.css",
    "public/assets/dashboard-preview.png",
    "public/lead-intake.js",
]

PRIVATE_BLOCKED_FILES = [
    ".env",
    ".streamlit/secrets.toml",
]

REQUIRED_GITIGNORE_PATTERNS = [
    "finance.db",
    ".env",
    ".streamlit/secrets.toml",
    ".venv/",
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


def read_text(path):
    return path.read_text(encoding="utf-8")


def check_required_public_files(errors):
    for relative_path in PUBLIC_REQUIRED_FILES:
        path = ROOT_DIR / relative_path

        if not path.exists():
            errors.append(f"Missing public file: {relative_path}")


def check_private_files_not_present(errors):
    for relative_path in PRIVATE_BLOCKED_FILES:
        path = ROOT_DIR / relative_path

        if path.exists():
            errors.append(f"Private file must not be committed or published: {relative_path}")


def check_gitignore(errors):
    gitignore_path = ROOT_DIR / ".gitignore"

    if not gitignore_path.exists():
        errors.append("Missing .gitignore")
        return

    gitignore_text = read_text(gitignore_path)

    for pattern in REQUIRED_GITIGNORE_PATTERNS:
        if pattern not in gitignore_text:
            errors.append(f"Missing .gitignore protection: {pattern}")


def check_public_surface(errors):
    public_dir = ROOT_DIR / "public"

    if not public_dir.exists():
        errors.append("Missing public directory")
        return

    for path in public_dir.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in {".html", ".css", ".js", ".txt", ".md"}:
            continue

        text = read_text(path)

        for forbidden in FORBIDDEN_PUBLIC_REFERENCES:
            if forbidden in text:
                relative_path = path.relative_to(ROOT_DIR)
                errors.append(
                    f"Forbidden private reference in {relative_path}: {forbidden}"
                )


def check_lead_intake_surface(errors):
    index_path = ROOT_DIR / "public/index.html"

    if not index_path.exists():
        return

    index_text = read_text(index_path)

    for marker in REQUIRED_PUBLIC_MARKERS:
        if marker not in index_text:
            errors.append(f"Missing lead intake marker in public/index.html: {marker}")


def main():
    errors = []

    check_required_public_files(errors)
    check_private_files_not_present(errors)
    check_gitignore(errors)
    check_public_surface(errors)
    check_lead_intake_surface(errors)

    if errors:
        print("Deployment readiness check failed:")

        for error in errors:
            print(f"- {error}")

        raise SystemExit(1)

    print("Deployment readiness check passed.")
    print("Public landing surface is separated from private BusinessOS runtime.")


if __name__ == "__main__":
    main()
