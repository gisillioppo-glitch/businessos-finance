import re
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.alerts.alert_status import get_executive_alert_status_summary  # noqa: E402
from app.alerts.executive_alerts import get_executive_alerts  # noqa: E402
from app.governance.sensitivity_rules import get_governance_sensitivity_findings  # noqa: E402
from app.notifications.delivery_approval import (  # noqa: E402
    get_notification_delivery_approval_rows,
    get_notification_delivery_approval_summary,
)
from app.notifications.email_delivery import (  # noqa: E402
    get_secure_email_delivery_status,
    parse_secure_email_delivery_report,
)
from app.notifications.outbox import get_notification_outbox, get_notification_summary  # noqa: E402
from app.security.access_control import (  # noqa: E402
    get_allowed_pages,
    get_default_role,
    validate_credentials,
)
from app.security.config import settings  # noqa: E402

DB_PATH = ROOT_DIR / "finance.db"


CUSTOM_CSS = """
<style>
:root {
    --bos-bg: #070708;
    --bos-panel: #121214;
    --bos-panel-soft: #17171a;
    --bos-border: rgba(255, 255, 255, 0.08);
    --bos-red: #e31b23;
    --bos-red-soft: rgba(227, 27, 35, 0.16);
    --bos-gold: #f4b740;
    --bos-green: #35c46f;
    --bos-text: #f6f4ef;
    --bos-muted: #9d9da5;
}

.stApp {
    background: radial-gradient(circle at top left, rgba(227, 27, 35, 0.10), transparent 30%), var(--bos-bg);
    color: var(--bos-text);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1f0608 0%, #0b0b0d 38%, #080808 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] * {
    color: var(--bos-text);
}

div[data-testid="stSidebarUserContent"] {
    padding-top: 1.4rem;
}

.main .block-container {
    padding-top: 2.1rem;
    max-width: 1280px;
}

h1, h2, h3 {
    letter-spacing: 0;
}

[data-testid="stMetric"] {
    background: transparent;
}

.bos-topbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1.35rem;
}

.bos-title {
    font-size: 2.15rem;
    line-height: 1.08;
    font-weight: 800;
    margin: 0;
}

.bos-subtitle {
    color: var(--bos-muted);
    font-size: 0.98rem;
    margin-top: 0.45rem;
}

.bos-chip {
    border: 1px solid rgba(227, 27, 35, 0.35);
    background: rgba(227, 27, 35, 0.10);
    color: #ffd7d9;
    border-radius: 999px;
    padding: 0.45rem 0.7rem;
    font-size: 0.82rem;
    white-space: nowrap;
}

.bos-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.015)), var(--bos-panel);
    border: 1px solid var(--bos-border);
    border-radius: 8px;
    padding: 1.1rem 1.15rem;
    min-height: 138px;
    box-shadow: 0 14px 38px rgba(0, 0, 0, 0.22);
}

.bos-card-title {
    color: #dedce0;
    font-size: 0.95rem;
    font-weight: 650;
    margin-bottom: 0.65rem;
}

.bos-card-value {
    color: var(--bos-text);
    font-size: 2.05rem;
    line-height: 1.05;
    font-weight: 800;
}

.bos-card-value.red {
    color: #ff383f;
}

.bos-card-value.green {
    color: var(--bos-green);
}

.bos-card-value.gold {
    color: var(--bos-gold);
}

.bos-card-caption {
    color: var(--bos-muted);
    font-size: 0.84rem;
    margin-top: 0.55rem;
}

.bos-panel {
    background: var(--bos-panel);
    border: 1px solid var(--bos-border);
    border-radius: 8px;
    padding: 1.2rem 1.35rem;
    min-height: 100%;
    box-shadow: 0 14px 38px rgba(0, 0, 0, 0.20);
}

.bos-section-title {
    font-size: 1.05rem;
    font-weight: 750;
    margin-bottom: 0.85rem;
}

.bos-brief-item {
    display: grid;
    grid-template-columns: 0.75rem 1fr;
    gap: 0.65rem;
    align-items: start;
    margin: 0.82rem 0;
}

.bos-dot {
    width: 0.52rem;
    height: 0.52rem;
    border-radius: 999px;
    background: var(--bos-red);
    margin-top: 0.42rem;
    box-shadow: 0 0 18px rgba(227, 27, 35, 0.6);
}

.bos-item-main {
    color: var(--bos-text);
    font-weight: 650;
    font-size: 0.96rem;
}

.bos-item-sub {
    color: var(--bos-muted);
    font-size: 0.84rem;
    margin-top: 0.1rem;
}

.bos-row {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 0.8rem;
    align-items: center;
    padding: 0.72rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.bos-row:last-child {
    border-bottom: 0;
}

.bos-badge {
    border-radius: 999px;
    padding: 0.25rem 0.58rem;
    font-size: 0.76rem;
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: var(--bos-text);
    white-space: nowrap;
}

.bos-badge.high {
    color: #ff6066;
    border-color: rgba(227, 27, 35, 0.45);
    background: rgba(227, 27, 35, 0.10);
}

.bos-badge.medium {
    color: #ffc066;
    border-color: rgba(244, 183, 64, 0.42);
    background: rgba(244, 183, 64, 0.08);
}

.bos-badge.low, .bos-badge.none, .bos-badge.healthy {
    color: #72e39b;
    border-color: rgba(53, 196, 111, 0.38);
    background: rgba(53, 196, 111, 0.08);
}

.bos-alert-dot {
    display: inline-block;
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 999px;
    margin-right: 0.55rem;
    background: var(--bos-red);
}

.bos-login-card {
    max-width: 460px;
    margin: 7vh auto 0 auto;
    background: var(--bos-panel);
    border: 1px solid var(--bos-border);
    border-radius: 8px;
    padding: 1.4rem;
}

@media (max-width: 900px) {
    .bos-topbar {
        display: block;
    }

    .bos-chip {
        display: inline-block;
        margin-top: 0.8rem;
    }
}
</style>
"""


def get_scalar(query, params=None):
    if params is None:
        params = ()

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(query, params).fetchone()[0]


def get_rows(query, params=None):
    if params is None:
        params = ()

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(query, params).fetchall()]


def load_cash_flow_series():
    with sqlite3.connect(DB_PATH) as conn:
        frame = pd.read_sql_query(
            """
            SELECT
                date,
                SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) AS net_cash_flow
            FROM transactions
            GROUP BY date
            ORDER BY date
            """,
            conn,
        )

    if frame.empty:
        return pd.DataFrame({"date": [], "net_cash_flow": []})

    frame["date"] = pd.to_datetime(frame["date"])
    return frame



def get_latest_report_path(prefix):
    reports_path = ROOT_DIR / "reports"

    if not reports_path.exists():
        return None

    matches = sorted(reports_path.glob(f"{prefix}_*.md"), reverse=True)
    return matches[0] if matches else None


def extract_metric_from_markdown(content, label, default=0):
    pattern = rf"{re.escape(label)}:\s*(\d+)"
    match = re.search(pattern, content)
    return int(match.group(1)) if match else default


def load_daily_close_status():
    report_path = get_latest_report_path("daily_close")

    if not report_path:
        return {
            "exists": False,
            "report_path": None,
            "completed_steps": 0,
            "total_steps": 0,
            "evidence_available": 0,
            "evidence_missing": 0,
            "steps": [],
        }

    content = report_path.read_text(encoding="utf-8")
    steps = []

    for line in content.splitlines():
        if not line.startswith("|") or line.startswith("| ---") or line.startswith("| Step"):
            continue

        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) == 3:
            steps.append(
                {
                    "name": parts[0],
                    "status": parts[1],
                    "detail": parts[2],
                }
            )

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "completed_steps": extract_metric_from_markdown(content, "Completed close steps"),
        "total_steps": extract_metric_from_markdown(content, "Total close steps"),
        "evidence_available": extract_metric_from_markdown(content, "Evidence available"),
        "evidence_missing": extract_metric_from_markdown(content, "Evidence missing"),
        "steps": steps,
    }


def load_evidence_index_status():
    report_path = get_latest_report_path("executive_evidence_index")

    if not report_path:
        return {
            "exists": False,
            "report_path": None,
            "items": [],
        }

    content = report_path.read_text(encoding="utf-8")
    items = []

    for line in content.splitlines():
        if not line.startswith("|") or line.startswith("| ---") or line.startswith("| Evidence"):
            continue

        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) == 4:
            items.append(
                {
                    "label": parts[0],
                    "status": parts[1],
                    "report_path": parts[2],
                    "purpose": parts[3],
                }
            )

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "items": items,
    }


def load_system_integrity_status():
    report_path = get_latest_report_path("system_integrity")

    if not report_path:
        return {
            "exists": False,
            "report_path": None,
            "date": None,
            "overall_status": "missing",
            "total_checks": 0,
            "passed_checks": 0,
            "warning_checks": 0,
            "failed_checks": 0,
            "checks": [],
        }

    content = report_path.read_text(encoding="utf-8")
    checks = []

    for line in content.splitlines():
        if not line.startswith("|") or line.startswith("| ---") or line.startswith("| Check"):
            continue

        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) == 3:
            checks.append(
                {
                    "name": parts[0],
                    "status": parts[1],
                    "detail": parts[2],
                }
            )

    date_match = re.search(r"Date:\s*([0-9-]+)", content)
    status_match = re.search(r"Overall status:\s*([a-z_]+)", content)

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "date": date_match.group(1) if date_match else None,
        "overall_status": status_match.group(1) if status_match else "unknown",
        "total_checks": extract_metric_from_markdown(content, "Total checks"),
        "passed_checks": extract_metric_from_markdown(content, "Passed checks"),
        "warning_checks": extract_metric_from_markdown(content, "Warning checks"),
        "failed_checks": extract_metric_from_markdown(content, "Failed checks"),
        "checks": checks,
    }



def load_private_demo_dry_run_status():
    report_path = get_latest_report_path("private_demo_dry_run")

    if not report_path:
        return {
            "exists": False,
            "report_path": None,
            "date": None,
            "overall_status": "missing",
            "total_checks": 0,
            "passed_checks": 0,
            "warning_checks": 0,
            "failed_checks": 0,
            "release_readiness_source": "missing",
            "package_path": None,
            "script_path": None,
            "checks": [],
            "run_sequence": [],
            "dashboard_pages": [],
        }

    content = report_path.read_text(encoding="utf-8")
    checks = []
    run_sequence = []
    dashboard_pages = []
    section = None
    package_path = None
    script_path = None

    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("## "):
            section = stripped.replace("## ", "", 1)
            continue

        if stripped.startswith("- Private demo package:"):
            package_path = stripped.split(":", 1)[1].strip()
            continue

        if stripped.startswith("- Private demo script:"):
            script_path = stripped.split(":", 1)[1].strip()
            continue

        if section == "Checks":
            if not stripped.startswith("|") or stripped.startswith("| ---") or stripped.startswith("| Check"):
                continue

            parts = [part.strip() for part in stripped.strip("|").split("|")]
            if len(parts) == 4:
                checks.append(
                    {
                        "name": parts[0],
                        "status": parts[1],
                        "severity": parts[2],
                        "detail": parts[3],
                    }
                )

        elif section == "Demo Run Sequence":
            match = re.match(r"\d+\.\s+(.*)", stripped)
            if match:
                run_sequence.append(match.group(1))

        elif section == "Dashboard Pages Available" and stripped.startswith("- "):
            dashboard_pages.append(stripped[2:])

    date_match = re.search(r"Date:\s*([0-9-]+)", content)
    status_match = re.search(r"Overall status:\s*([a-z_]+)", content)
    readiness_match = re.search(r"Release readiness source:\s*([a-z_]+)", content)

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "date": date_match.group(1) if date_match else None,
        "overall_status": status_match.group(1) if status_match else "unknown",
        "total_checks": extract_metric_from_markdown(content, "Total checks"),
        "passed_checks": extract_metric_from_markdown(content, "Passed checks"),
        "warning_checks": extract_metric_from_markdown(content, "Warning checks"),
        "failed_checks": extract_metric_from_markdown(content, "Failed checks"),
        "release_readiness_source": readiness_match.group(1) if readiness_match else "unknown",
        "package_path": package_path,
        "script_path": script_path,
        "checks": checks,
        "run_sequence": run_sequence,
        "dashboard_pages": dashboard_pages,
    }


def load_private_pilot_plan_status():
    report_path = get_latest_report_path("private_pilot_plan")

    if not report_path:
        return {
            "exists": False,
            "report_path": None,
            "date": None,
            "plan_status": "missing",
            "intake_status": "missing",
            "pilot_length": 0,
            "pilot_owner": "Not assigned",
            "primary_workflow": "Not selected",
            "recommended_module": "Not selected",
            "first_action": "Run python cli.py private-pilot-plan.",
            "roles": [],
            "timeline": [],
            "daily_rhythm": [],
            "success_criteria": [],
            "exit_decisions": [],
            "boundaries": [],
        }

    content = report_path.read_text(encoding="utf-8")
    section = None
    roles = []
    timeline = []
    daily_rhythm = []
    success_criteria = []
    exit_decisions = []
    boundaries = []

    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("## "):
            section = stripped.replace("## ", "", 1)
            continue

        if section == "Pilot Roles":
            if not stripped.startswith("|") or stripped.startswith("| ---") or stripped.startswith("| Role"):
                continue

            parts = [part.strip() for part in stripped.strip("|").split("|")]
            if len(parts) == 3:
                roles.append(
                    {
                        "role": parts[0],
                        "type": parts[1],
                        "responsibility": parts[2],
                    }
                )

        elif section == "14-Day Pilot Timeline":
            if not stripped.startswith("|") or stripped.startswith("| ---"):
                continue

            parts = [part.strip() for part in stripped.strip("|").split("|")]
            if len(parts) == 4 and parts[0] != "Days":
                timeline.append(
                    {
                        "days": parts[0],
                        "phase": parts[1],
                        "objective": parts[2],
                        "evidence": parts[3],
                    }
                )

        elif section == "Daily Operating Rhythm" and stripped.startswith("- "):
            daily_rhythm.append(stripped[2:])

        elif section == "Success Criteria" and stripped.startswith("- "):
            success_criteria.append(stripped[2:])

        elif section == "Exit Decisions" and stripped.startswith("- "):
            exit_decisions.append(stripped[2:])

        elif section == "Pilot Boundaries" and stripped.startswith("- "):
            boundaries.append(stripped[2:])

    date_match = re.search(r"Date:\s*([0-9-]+)", content)
    plan_status_match = re.search(r"Plan status:\s*([a-z_]+)", content)
    intake_status_match = re.search(r"Intake status:\s*([a-z_]+)", content)
    pilot_length_match = re.search(r"Pilot length:\s*(\d+)\s*days", content)
    pilot_owner_match = re.search(r"Pilot owner:\s*(.+)", content)
    primary_workflow_match = re.search(r"Primary workflow:\s*(.+)", content)
    recommended_module_match = re.search(r"Recommended module:\s*(.+)", content)
    first_action_match = re.search(r"First action:\s*(.+)", content)

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "date": date_match.group(1) if date_match else None,
        "plan_status": plan_status_match.group(1) if plan_status_match else "unknown",
        "intake_status": intake_status_match.group(1) if intake_status_match else "unknown",
        "pilot_length": int(pilot_length_match.group(1)) if pilot_length_match else 0,
        "pilot_owner": pilot_owner_match.group(1).strip() if pilot_owner_match else "Not assigned",
        "primary_workflow": primary_workflow_match.group(1).strip() if primary_workflow_match else "Not selected",
        "recommended_module": recommended_module_match.group(1).strip() if recommended_module_match else "Not selected",
        "first_action": first_action_match.group(1).strip() if first_action_match else "No first action recorded",
        "roles": roles,
        "timeline": timeline,
        "daily_rhythm": daily_rhythm,
        "success_criteria": success_criteria,
        "exit_decisions": exit_decisions,
        "boundaries": boundaries,
    }

def load_private_pilot_tracker_status():
    report_path = get_latest_report_path("private_pilot_tracker")

    if not report_path:
        return {
            "exists": False,
            "report_path": None,
            "date": None,
            "tracker_status": "missing",
            "plan_status": "missing",
            "pilot_owner": "Not assigned",
            "primary_workflow": "Not selected",
            "pilot_length": 0,
            "available_evidence": 0,
            "missing_required": 0,
            "missing_optional": 0,
            "next_action": "Run python cli.py private-pilot-tracker.",
            "daily_steps": [],
            "evidence_rows": [],
            "operator_note": "No tracker artifact generated yet.",
        }

    content = report_path.read_text(encoding="utf-8")
    section = None
    daily_steps = []
    evidence_rows = []
    operator_note = []

    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("## "):
            section = stripped.replace("## ", "", 1)
            continue

        if section == "Daily Operator Steps" and stripped.startswith("- "):
            daily_steps.append(stripped[2:])

        elif section == "Evidence Checklist":
            if not stripped.startswith("|") or stripped.startswith("| ---"):
                continue

            parts = [part.strip() for part in stripped.strip("|").split("|")]
            if len(parts) == 6 and parts[0] != "Evidence":
                evidence_rows.append(
                    {
                        "evidence": parts[0],
                        "status": parts[1],
                        "required": parts[2],
                        "owner": parts[3],
                        "latest_report": parts[4],
                        "purpose": parts[5],
                    }
                )

        elif section == "Operator Note" and stripped:
            operator_note.append(stripped)

    date_match = re.search(r"Date:\s*([0-9-]+)", content)
    tracker_status_match = re.search(r"Tracker status:\s*([a-z_]+)", content)
    plan_status_match = re.search(r"Plan status:\s*([a-z_]+)", content)
    pilot_owner_match = re.search(r"Pilot owner:\s*(.+)", content)
    primary_workflow_match = re.search(r"Primary workflow:\s*(.+)", content)
    pilot_length_match = re.search(r"Pilot length:\s*(\d+)\s*days", content)
    available_evidence_match = re.search(r"Available evidence:\s*(\d+)", content)
    missing_required_match = re.search(r"Missing required evidence:\s*(\d+)", content)
    missing_optional_match = re.search(r"Missing optional evidence:\s*(\d+)", content)
    next_action_match = re.search(r"Next action:\s*(.+)", content)

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "date": date_match.group(1) if date_match else None,
        "tracker_status": tracker_status_match.group(1) if tracker_status_match else "unknown",
        "plan_status": plan_status_match.group(1) if plan_status_match else "unknown",
        "pilot_owner": pilot_owner_match.group(1).strip() if pilot_owner_match else "Not assigned",
        "primary_workflow": primary_workflow_match.group(1).strip() if primary_workflow_match else "Not selected",
        "pilot_length": int(pilot_length_match.group(1)) if pilot_length_match else 0,
        "available_evidence": int(available_evidence_match.group(1)) if available_evidence_match else 0,
        "missing_required": int(missing_required_match.group(1)) if missing_required_match else 0,
        "missing_optional": int(missing_optional_match.group(1)) if missing_optional_match else 0,
        "next_action": next_action_match.group(1).strip() if next_action_match else "No next action recorded",
        "daily_steps": daily_steps,
        "evidence_rows": evidence_rows,
        "operator_note": " ".join(operator_note) if operator_note else "No operator note recorded.",
    }
def load_private_pilot_exit_decision_status():
    report_path = get_latest_report_path("private_pilot_exit_decision")

    if not report_path:
        return {
            "exists": False,
            "report_path": None,
            "date": None,
            "decision_status": "missing",
            "recommended_decision": "missing",
            "highest_exit_risk": "unknown",
            "pilot_owner": "Not assigned",
            "primary_workflow": "Not selected",
            "tracker_status": "missing",
            "plan_status": "missing",
            "available_evidence": 0,
            "missing_required": 0,
            "missing_optional": 0,
            "next_action": "Run python cli.py private-pilot-exit-decision.",
            "rationale": [],
            "conditions": [],
            "evidence_rows": [],
            "exit_options": [],
            "operator_note": "No exit decision artifact generated yet.",
        }

    content = report_path.read_text(encoding="utf-8")
    section = None
    rationale = []
    conditions = []
    evidence_rows = []
    exit_options = []
    operator_note = []

    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("## "):
            section = stripped.replace("## ", "", 1)
            continue

        if section == "Decision Rationale" and stripped.startswith("- "):
            rationale.append(stripped[2:])

        elif section == "Conditions Before Execution" and stripped.startswith("- "):
            conditions.append(stripped[2:])

        elif section == "Evidence Summary":
            if not stripped.startswith("|") or stripped.startswith("| ---"):
                continue

            parts = [part.strip() for part in stripped.strip("|").split("|")]
            if len(parts) == 4 and parts[0] != "Evidence":
                evidence_rows.append(
                    {
                        "evidence": parts[0],
                        "status": parts[1],
                        "required": parts[2],
                        "latest_report": parts[3],
                    }
                )

        elif section == "Allowed Exit Options":
            if not stripped.startswith("|") or stripped.startswith("| ---"):
                continue

            parts = [part.strip() for part in stripped.strip("|").split("|")]
            if len(parts) == 2 and parts[0] != "Decision":
                exit_options.append(
                    {
                        "decision": parts[0],
                        "meaning": parts[1],
                    }
                )

        elif section == "Operator Note" and stripped:
            operator_note.append(stripped)

    date_match = re.search(r"Date:\s*([0-9-]+)", content)
    decision_status_match = re.search(r"Decision status:\s*([a-z_]+)", content)
    recommended_decision_match = re.search(r"Recommended decision:\s*([a-z_]+)", content)
    highest_exit_risk_match = re.search(r"Highest exit risk:\s*(.+)", content)
    pilot_owner_match = re.search(r"Pilot owner:\s*(.+)", content)
    primary_workflow_match = re.search(r"Primary workflow:\s*(.+)", content)
    tracker_status_match = re.search(r"Tracker status:\s*([a-z_]+)", content)
    plan_status_match = re.search(r"Plan status:\s*([a-z_]+)", content)
    available_evidence_match = re.search(r"Available evidence:\s*(\d+)", content)
    missing_required_match = re.search(r"Missing required evidence:\s*(\d+)", content)
    missing_optional_match = re.search(r"Missing optional evidence:\s*(\d+)", content)
    next_action_match = re.search(r"Next action:\s*(.+)", content)

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "date": date_match.group(1) if date_match else None,
        "decision_status": decision_status_match.group(1) if decision_status_match else "unknown",
        "recommended_decision": recommended_decision_match.group(1) if recommended_decision_match else "unknown",
        "highest_exit_risk": highest_exit_risk_match.group(1).strip() if highest_exit_risk_match else "unknown",
        "pilot_owner": pilot_owner_match.group(1).strip() if pilot_owner_match else "Not assigned",
        "primary_workflow": primary_workflow_match.group(1).strip() if primary_workflow_match else "Not selected",
        "tracker_status": tracker_status_match.group(1) if tracker_status_match else "unknown",
        "plan_status": plan_status_match.group(1) if plan_status_match else "unknown",
        "available_evidence": int(available_evidence_match.group(1)) if available_evidence_match else 0,
        "missing_required": int(missing_required_match.group(1)) if missing_required_match else 0,
        "missing_optional": int(missing_optional_match.group(1)) if missing_optional_match else 0,
        "next_action": next_action_match.group(1).strip() if next_action_match else "No next action recorded",
        "rationale": rationale,
        "conditions": conditions,
        "evidence_rows": evidence_rows,
        "exit_options": exit_options,
        "operator_note": " ".join(operator_note) if operator_note else "No operator note recorded.",
    }
def load_pilot_day_1_package_status():
    report_path = get_latest_report_path("pilot_day_1_package")

    if not report_path:
        return {
            "exists": False,
            "report_path": None,
            "date": None,
            "day_1_status": "missing",
            "pilot_owner": "Not assigned",
            "primary_workflow": "Not selected",
            "plan_status": "missing",
            "tracker_status": "missing",
            "exit_decision_status": "missing",
            "recommended_exit_decision": "missing",
            "highest_exit_risk": "unknown",
            "available_evidence": 0,
            "missing_required_evidence": 0,
            "missing_optional_evidence": 0,
            "next_action": "Run python cli.py pilot-day-1-package.",
            "commands": [],
            "expected_evidence": [],
            "owner_review": [],
            "risks": [],
            "close_criteria": [],
            "operator_note": "No Pilot Day 1 package generated yet.",
        }

    content = report_path.read_text(encoding="utf-8")
    section = None
    commands = []
    expected_evidence = []
    owner_review = []
    risks = []
    close_criteria = []
    operator_note = []

    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("## "):
            section = stripped.replace("## ", "", 1)
            continue

        if section == "Day 1 Command Runbook":
            if not stripped.startswith("|") or stripped.startswith("| ---") or stripped.startswith("| Purpose"):
                continue

            parts = [part.strip().strip("`") for part in stripped.strip("|").split("|")]
            if len(parts) == 2:
                commands.append({"purpose": parts[0], "command": parts[1]})

        elif section == "Expected Evidence" and stripped.startswith("- "):
            expected_evidence.append(stripped[2:])

        elif section == "Executive Owner Review" and stripped.startswith("- "):
            owner_review.append(stripped[2:])

        elif section == "Day 1 Risks and Boundaries" and stripped.startswith("- "):
            risks.append(stripped[2:])

        elif section == "Day 1 Close Criteria" and stripped.startswith("- "):
            close_criteria.append(stripped[2:])

        elif section == "Operator Note" and stripped:
            operator_note.append(stripped)

    date_match = re.search(r"Date:\s*([0-9-]+)", content)
    day_1_status_match = re.search(r"Day 1 status:\s*([a-z_]+)", content)
    pilot_owner_match = re.search(r"Pilot owner:\s*(.+)", content)
    primary_workflow_match = re.search(r"Primary workflow:\s*(.+)", content)
    plan_status_match = re.search(r"Plan status:\s*([a-z_]+)", content)
    tracker_status_match = re.search(r"Tracker status:\s*([a-z_]+)", content)
    exit_decision_status_match = re.search(r"Exit decision status:\s*([a-z_]+)", content)
    recommended_exit_decision_match = re.search(r"Recommended exit decision:\s*([a-z_]+)", content)
    highest_exit_risk_match = re.search(r"Highest exit risk:\s*(.+)", content)
    available_evidence_match = re.search(r"Available evidence:\s*(\d+)", content)
    missing_required_match = re.search(r"Missing required evidence:\s*(\d+)", content)
    missing_optional_match = re.search(r"Missing optional evidence:\s*(\d+)", content)
    next_action_match = re.search(r"Next action:\s*(.+)", content)

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "date": date_match.group(1) if date_match else None,
        "day_1_status": day_1_status_match.group(1) if day_1_status_match else "unknown",
        "pilot_owner": pilot_owner_match.group(1).strip() if pilot_owner_match else "Not assigned",
        "primary_workflow": primary_workflow_match.group(1).strip() if primary_workflow_match else "Not selected",
        "plan_status": plan_status_match.group(1) if plan_status_match else "unknown",
        "tracker_status": tracker_status_match.group(1) if tracker_status_match else "unknown",
        "exit_decision_status": exit_decision_status_match.group(1) if exit_decision_status_match else "unknown",
        "recommended_exit_decision": recommended_exit_decision_match.group(1) if recommended_exit_decision_match else "unknown",
        "highest_exit_risk": highest_exit_risk_match.group(1).strip() if highest_exit_risk_match else "unknown",
        "available_evidence": int(available_evidence_match.group(1)) if available_evidence_match else 0,
        "missing_required_evidence": int(missing_required_match.group(1)) if missing_required_match else 0,
        "missing_optional_evidence": int(missing_optional_match.group(1)) if missing_optional_match else 0,
        "next_action": next_action_match.group(1).strip() if next_action_match else "No next action recorded",
        "commands": commands,
        "expected_evidence": expected_evidence,
        "owner_review": owner_review,
        "risks": risks,
        "close_criteria": close_criteria,
        "operator_note": " ".join(operator_note) if operator_note else "No operator note recorded.",
    }
def load_pilot_day_2_rhythm_status():
    report_path = get_latest_report_path("pilot_day_2_rhythm")

    if not report_path:
        return {
            "exists": False,
            "report_path": None,
            "date": None,
            "day_2_status": "missing",
            "continuation_decision": "missing",
            "pilot_owner": "Not assigned",
            "primary_workflow": "Not selected",
            "day_1_status": "missing",
            "tracker_status": "missing",
            "exit_decision_status": "missing",
            "recommended_exit_decision": "missing",
            "highest_exit_risk": "unknown",
            "available_evidence": 0,
            "missing_required_evidence": 0,
            "missing_optional_evidence": 0,
            "next_action": "Run python cli.py pilot-day-2-rhythm.",
            "commands": [],
            "rhythm": [],
            "expected_evidence": [],
            "review_checks": [],
            "boundaries": [],
            "operator_note": "No Pilot Day 2 rhythm generated yet.",
        }

    content = report_path.read_text(encoding="utf-8")
    section = None
    commands = []
    rhythm = []
    expected_evidence = []
    review_checks = []
    boundaries = []
    operator_note = []

    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("## "):
            section = stripped.replace("## ", "", 1)
            continue

        if section == "Day 2 Command Runbook":
            if not stripped.startswith("|") or stripped.startswith("| ---") or stripped.startswith("| Purpose"):
                continue

            parts = [part.strip().strip("`") for part in stripped.strip("|").split("|")]
            if len(parts) == 2:
                commands.append({"purpose": parts[0], "command": parts[1]})

        elif section == "Day 2 Operating Rhythm" and stripped.startswith("- "):
            rhythm.append(stripped[2:])

        elif section == "Expected Evidence" and stripped.startswith("- "):
            expected_evidence.append(stripped[2:])

        elif section == "Executive Review Checks" and stripped.startswith("- "):
            review_checks.append(stripped[2:])

        elif section == "Day 2 Boundaries" and stripped.startswith("- "):
            boundaries.append(stripped[2:])

        elif section == "Operator Note" and stripped:
            operator_note.append(stripped)

    date_match = re.search(r"Date:\s*([0-9-]+)", content)
    day_2_status_match = re.search(r"Day 2 status:\s*([a-z_]+)", content)
    continuation_decision_match = re.search(r"Continuation decision:\s*([a-z_]+)", content)
    pilot_owner_match = re.search(r"Pilot owner:\s*(.+)", content)
    primary_workflow_match = re.search(r"Primary workflow:\s*(.+)", content)
    day_1_status_match = re.search(r"Day 1 status:\s*([a-z_]+)", content)
    tracker_status_match = re.search(r"Tracker status:\s*([a-z_]+)", content)
    exit_decision_status_match = re.search(r"Exit decision status:\s*([a-z_]+)", content)
    recommended_exit_decision_match = re.search(r"Recommended exit decision:\s*([a-z_]+)", content)
    highest_exit_risk_match = re.search(r"Highest exit risk:\s*(.+)", content)
    available_evidence_match = re.search(r"Available evidence:\s*(\d+)", content)
    missing_required_match = re.search(r"Missing required evidence:\s*(\d+)", content)
    missing_optional_match = re.search(r"Missing optional evidence:\s*(\d+)", content)
    next_action_match = re.search(r"Next action:\s*(.+)", content)

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "date": date_match.group(1) if date_match else None,
        "day_2_status": day_2_status_match.group(1) if day_2_status_match else "unknown",
        "continuation_decision": continuation_decision_match.group(1) if continuation_decision_match else "unknown",
        "pilot_owner": pilot_owner_match.group(1).strip() if pilot_owner_match else "Not assigned",
        "primary_workflow": primary_workflow_match.group(1).strip() if primary_workflow_match else "Not selected",
        "day_1_status": day_1_status_match.group(1) if day_1_status_match else "unknown",
        "tracker_status": tracker_status_match.group(1) if tracker_status_match else "unknown",
        "exit_decision_status": exit_decision_status_match.group(1) if exit_decision_status_match else "unknown",
        "recommended_exit_decision": recommended_exit_decision_match.group(1) if recommended_exit_decision_match else "unknown",
        "highest_exit_risk": highest_exit_risk_match.group(1).strip() if highest_exit_risk_match else "unknown",
        "available_evidence": int(available_evidence_match.group(1)) if available_evidence_match else 0,
        "missing_required_evidence": int(missing_required_match.group(1)) if missing_required_match else 0,
        "missing_optional_evidence": int(missing_optional_match.group(1)) if missing_optional_match else 0,
        "next_action": next_action_match.group(1).strip() if next_action_match else "No next action recorded",
        "commands": commands,
        "rhythm": rhythm,
        "expected_evidence": expected_evidence,
        "review_checks": review_checks,
        "boundaries": boundaries,
        "operator_note": " ".join(operator_note) if operator_note else "No operator note recorded.",
    }


def load_pilot_expansion_review_decision_status():
    report_path = get_latest_report_path("pilot_expansion_review_decision")

    if not report_path:
        return {
            "exists": False,
            "report_path": None,
            "date": None,
            "decision_status": "missing",
            "recommended_decision": "missing",
            "pilot_owner": "Not assigned",
            "primary_workflow": "Not selected",
            "continuation_scope": "unknown",
            "expansion_prep_status": "missing",
            "review_recommendation": "missing",
            "expansion_status": "unknown",
            "delivery_status": "unknown",
            "pending_conditions": 0,
            "missing_required_evidence": 0,
            "highest_exit_risk": "unknown",
            "next_action": "Run python cli.py pilot-expansion-review-decision.",
            "conditions": [],
            "rationale": [],
            "commands": [],
            "decision_options": [],
            "boundaries": [],
            "operator_note": "No pilot expansion review decision artifact generated yet.",
        }

    content = report_path.read_text(encoding="utf-8")
    section = None
    conditions = []
    rationale = []
    commands = []
    decision_options = []
    boundaries = []
    operator_note = []

    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("## "):
            section = stripped.replace("## ", "", 1)
            continue

        if section == "Condition Gate":
            if not stripped.startswith("|") or stripped.startswith("| ---") or stripped.startswith("| Condition"):
                continue

            parts = [part.strip() for part in stripped.strip("|").split("|")]
            if len(parts) == 3:
                conditions.append(
                    {
                        "condition": parts[0],
                        "status": parts[1],
                        "detail": parts[2],
                    }
                )

        elif section == "Decision Rationale" and stripped.startswith("- "):
            rationale.append(stripped[2:])

        elif section == "Decision Commands":
            if not stripped.startswith("|") or stripped.startswith("| ---") or stripped.startswith("| Purpose"):
                continue

            parts = [part.strip().strip("`") for part in stripped.strip("|").split("|")]
            if len(parts) == 2:
                commands.append({"purpose": parts[0], "command": parts[1]})

        elif section == "Decision Options" and stripped.startswith("- "):
            decision_options.append(stripped[2:])

        elif section == "Boundaries" and stripped.startswith("- "):
            boundaries.append(stripped[2:])

        elif section == "Operator Note" and stripped:
            operator_note.append(stripped)

    date_match = re.search(r"Date:\s*([0-9-]+)", content)
    decision_status_match = re.search(r"Decision status:\s*([a-z_]+)", content)
    recommended_decision_match = re.search(r"Recommended decision:\s*([a-z_]+)", content)
    pilot_owner_match = re.search(r"Pilot owner:\s*(.+)", content)
    primary_workflow_match = re.search(r"Primary workflow:\s*(.+)", content)
    continuation_scope_match = re.search(r"Continuation scope:\s*([a-z_]+)", content)
    expansion_prep_status_match = re.search(r"Expansion prep status:\s*([a-z_]+)", content)
    review_recommendation_match = re.search(r"Review recommendation:\s*([a-z_]+)", content)
    expansion_status_match = re.search(r"Expansion status:\s*([a-z_]+)", content)
    delivery_status_match = re.search(r"Delivery status:\s*([a-z_]+)", content)
    pending_conditions_match = re.search(r"Pending conditions:\s*(\d+)", content)
    missing_required_match = re.search(r"Missing required evidence:\s*(\d+)", content)
    highest_exit_risk_match = re.search(r"Highest exit risk:\s*(.+)", content)
    next_action_match = re.search(r"Next action:\s*(.+)", content)

    return {
        "exists": True,
        "report_path": str(report_path.relative_to(ROOT_DIR)),
        "date": date_match.group(1) if date_match else None,
        "decision_status": decision_status_match.group(1) if decision_status_match else "unknown",
        "recommended_decision": recommended_decision_match.group(1) if recommended_decision_match else "unknown",
        "pilot_owner": pilot_owner_match.group(1).strip() if pilot_owner_match else "Not assigned",
        "primary_workflow": primary_workflow_match.group(1).strip() if primary_workflow_match else "Not selected",
        "continuation_scope": continuation_scope_match.group(1) if continuation_scope_match else "unknown",
        "expansion_prep_status": expansion_prep_status_match.group(1) if expansion_prep_status_match else "unknown",
        "review_recommendation": review_recommendation_match.group(1) if review_recommendation_match else "unknown",
        "expansion_status": expansion_status_match.group(1) if expansion_status_match else "unknown",
        "delivery_status": delivery_status_match.group(1) if delivery_status_match else "unknown",
        "pending_conditions": int(pending_conditions_match.group(1)) if pending_conditions_match else 0,
        "missing_required_evidence": int(missing_required_match.group(1)) if missing_required_match else 0,
        "highest_exit_risk": highest_exit_risk_match.group(1).strip() if highest_exit_risk_match else "unknown",
        "next_action": next_action_match.group(1).strip() if next_action_match else "No next action recorded",
        "conditions": conditions,
        "rationale": rationale,
        "commands": commands,
        "decision_options": decision_options,
        "boundaries": boundaries,
        "operator_note": " ".join(operator_note) if operator_note else "No operator note recorded.",
    }
def load_scheduled_daily_close_status():
    today = date.today().isoformat()
    current_time_local = datetime.now().strftime("%H:%M")
    today_report_path = ROOT_DIR / "reports" / f"daily_close_{today}.md"
    today_report_exists = today_report_path.exists()

    default_status = {
        "exists": False,
        "schedule_name": "executive_daily_close",
        "enabled": False,
        "run_time_local": "18:00",
        "last_run_date": None,
        "last_started_at": None,
        "last_completed_at": None,
        "last_status": "missing",
        "last_message": "Scheduled daily close table has not been initialized.",
        "today": today,
        "current_time_local": current_time_local,
        "today_report_exists": today_report_exists,
        "today_report_path": str(today_report_path.relative_to(ROOT_DIR)),
        "next_action": "missing_schedule",
    }

    with sqlite3.connect(DB_PATH) as conn:
        table_exists = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'scheduled_daily_close'
            LIMIT 1
            """
        ).fetchone()

        if not table_exists:
            return default_status

        row = conn.execute(
            """
            SELECT
                schedule_name,
                enabled,
                run_time_local,
                last_run_date,
                last_started_at,
                last_completed_at,
                last_status,
                last_message
            FROM scheduled_daily_close
            WHERE schedule_name = 'executive_daily_close'
            LIMIT 1
            """
        ).fetchone()

    if not row:
        return default_status

    enabled = bool(row[1])
    run_time_local = row[2]
    last_run_date = row[3]

    if not enabled:
        next_action = "disabled"
    elif last_run_date == today:
        next_action = "already_recorded_today"
    elif today_report_exists:
        next_action = "close_already_available"
    elif current_time_local < run_time_local:
        next_action = "waiting_for_run_time"
    else:
        next_action = "due"

    return {
        "exists": True,
        "schedule_name": row[0],
        "enabled": enabled,
        "run_time_local": run_time_local,
        "last_run_date": last_run_date,
        "last_started_at": row[4],
        "last_completed_at": row[5],
        "last_status": row[6],
        "last_message": row[7],
        "today": today,
        "current_time_local": current_time_local,
        "today_report_exists": today_report_exists,
        "today_report_path": str(today_report_path.relative_to(ROOT_DIR)),
        "next_action": next_action,
    }


def load_dashboard_data():
    transactions_count = get_scalar("SELECT COUNT(*) FROM transactions")
    total_income = get_scalar("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'income'")
    total_expenses = get_scalar("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'expense'")
    net_cash_flow = total_income - total_expenses

    active_finance_actions = get_scalar(
        """
        SELECT COUNT(*)
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
        """
    )

    high_finance_actions = get_scalar(
        """
        SELECT COUNT(*)
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
          AND priority = 'high'
        """
    )

    active_operations_tasks = get_scalar(
        """
        SELECT COUNT(*)
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
        """
    )

    overdue_operations_tasks = get_scalar(
        """
        SELECT COUNT(*)
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
          AND deadline_date IS NOT NULL
          AND deadline_date < date('now')
        """
    )

    active_support_incidents = get_scalar(
        """
        SELECT COUNT(*)
        FROM support_incidents
        WHERE status IN ('open', 'investigating', 'waiting')
        """
    )

    critical_support_incidents = get_scalar(
        """
        SELECT COUNT(*)
        FROM support_incidents
        WHERE status IN ('open', 'investigating', 'waiting')
          AND severity IN ('critical', 'high')
        """
    )

    active_assistance_requests = get_scalar(
        """
        SELECT COUNT(*)
        FROM assistance_requests
        WHERE status IN ('open', 'triaged', 'waiting_approval', 'in_progress')
        """
    )

    high_assistance_requests = get_scalar(
        """
        SELECT COUNT(*)
        FROM assistance_requests
        WHERE status IN ('open', 'triaged', 'waiting_approval', 'in_progress')
          AND severity IN ('critical', 'high')
        """
    )

    waiting_approval_requests = get_scalar(
        """
        SELECT COUNT(*)
        FROM assistance_requests
        WHERE status = 'waiting_approval'
        """
    )

    pending_approval_requests = get_scalar(
        """
        SELECT COUNT(*)
        FROM approval_requests
        WHERE status = 'pending'
        """
    )

    approved_approval_requests = get_scalar(
        """
        SELECT COUNT(*)
        FROM approval_requests
        WHERE status = 'approved'
        """
    )

    rejected_approval_requests = get_scalar(
        """
        SELECT COUNT(*)
        FROM approval_requests
        WHERE status = 'rejected'
        """
    )

    high_pending_approval_requests = get_scalar(
        """
        SELECT COUNT(*)
        FROM approval_requests
        WHERE status = 'pending'
          AND priority IN ('critical', 'high')
        """
    )
    total_people = get_scalar("SELECT COUNT(*) FROM business_users")

    active_people = get_scalar(
        """
        SELECT COUNT(*)
        FROM business_users
        WHERE status = 'active'
        """
    )

    admin_people = get_scalar(
        """
        SELECT COUNT(*)
        FROM business_users
        WHERE access_level = 'admin'
        """
    )

    manager_people = get_scalar(
        """
        SELECT COUNT(*)
        FROM business_users
        WHERE access_level = 'manager'
        """
    )

    governance_findings = get_scalar(
        """
        SELECT COUNT(*)
        FROM audit_logs
        WHERE event_type = 'governance_finding_detected'
        """
    )

    error_events = get_scalar(
        """
        SELECT COUNT(*)
        FROM audit_logs
        WHERE severity IN ('error', 'critical')
        """
    )

    if error_events > 0 or overdue_operations_tasks > 0 or high_assistance_requests > 0:
        overall_health = "Needs Attention"
        highest_risk = "High"
        next_move = "Resolve overdue operations work and triage high-severity assistance requests."
        health_class = "red"
    elif active_support_incidents > 0 or active_operations_tasks > 0 or active_finance_actions > 0 or active_assistance_requests > 0:
        overall_health = "Watch"
        highest_risk = "Medium"
        next_move = "Review active actions, incidents, and operations tasks before expanding workload."
        health_class = "gold"
    else:
        overall_health = "Healthy"
        highest_risk = "None"
        next_move = "Maintain current operating cadence."
        health_class = "green"

    recent_incidents = get_rows(
        """
        SELECT title, severity, status, owner_role
        FROM support_incidents
        ORDER BY created_at DESC
        LIMIT 3
        """
    )

    active_tasks = get_rows(
        """
        SELECT title, priority, status, owner_role
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
        ORDER BY
            CASE priority
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                ELSE 4
            END,
            created_at DESC
        LIMIT 4
        """
    )

    recommended_actions = get_rows(
        """
        SELECT recommended_action, priority, status, owner_role
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
        ORDER BY
            CASE priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                ELSE 3
            END,
            created_at DESC
        LIMIT 3
        """
    )

    assistance_requests = get_rows(
        """
        SELECT title, request_type, severity, status, owner_role
        FROM assistance_requests
        WHERE status IN ('open', 'triaged', 'waiting_approval', 'in_progress')
        ORDER BY
            CASE severity
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            created_at DESC
        LIMIT 5
        """
    )

    approval_requests = get_rows(
        """
        SELECT title, approval_type, priority, status, approver_role, status_justification
        FROM approval_requests
        ORDER BY
            CASE status
                WHEN 'pending' THEN 1
                WHEN 'approved' THEN 2
                WHEN 'rejected' THEN 3
                WHEN 'cancelled' THEN 4
                ELSE 5
            END,
            CASE priority
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            created_at DESC
        LIMIT 8
        """
    )
    people_users = get_rows(
        """
        SELECT full_name, email, role, department, status, access_level
        FROM business_users
        ORDER BY
            CASE access_level
                WHEN 'admin' THEN 1
                WHEN 'executive' THEN 2
                WHEN 'manager' THEN 3
                WHEN 'operator' THEN 4
                ELSE 5
            END,
            department,
            full_name
        LIMIT 8
        """
    )

    with sqlite3.connect(DB_PATH) as conn:
        sensitivity_findings = get_governance_sensitivity_findings(conn)
        executive_alerts = get_executive_alerts(conn)
        executive_alert_status_summary = get_executive_alert_status_summary(conn)
        notification_summary = get_notification_summary(conn)
        notification_outbox = get_notification_outbox(conn, limit=50)
        delivery_approval_summary = get_notification_delivery_approval_summary(conn)
        delivery_approval_rows = get_notification_delivery_approval_rows(conn)
        secure_email_status = get_secure_email_delivery_status(conn)
        secure_email_report = parse_secure_email_delivery_report()

    high_sensitivity_findings = sum(1 for finding in sensitivity_findings if finding["severity"] == "high")
    medium_sensitivity_findings = sum(1 for finding in sensitivity_findings if finding["severity"] == "medium")
    critical_executive_alerts = sum(1 for alert in executive_alerts if alert["severity"] == "critical")
    high_executive_alerts = sum(1 for alert in executive_alerts if alert["severity"] == "high")
    open_executive_alerts = sum(1 for alert in executive_alerts if alert["status"] == "open")
    acknowledged_executive_alerts = sum(1 for alert in executive_alerts if alert["status"] == "acknowledged")
    in_review_executive_alerts = sum(1 for alert in executive_alerts if alert["status"] == "in_review")
    resolved_executive_alerts = executive_alert_status_summary["resolved"]

    if high_sensitivity_findings > 0:
        highest_sensitivity_risk = "High"
        sensitivity_next_move = "Review high-sensitivity findings and confirm approvals before execution."
    elif medium_sensitivity_findings > 0:
        highest_sensitivity_risk = "Medium"
        sensitivity_next_move = "Review medium-sensitivity findings and confirm ownership."
    else:
        highest_sensitivity_risk = "Low"
        sensitivity_next_move = "Maintain current governance sensitivity controls."

    daily_close_status = load_daily_close_status()
    evidence_index_status = load_evidence_index_status()
    system_integrity_status = load_system_integrity_status()
    scheduled_daily_close_status = load_scheduled_daily_close_status()
    private_demo_dry_run_status = load_private_demo_dry_run_status()
    private_pilot_plan_status = load_private_pilot_plan_status()
    private_pilot_tracker_status = load_private_pilot_tracker_status()
    private_pilot_exit_decision_status = load_private_pilot_exit_decision_status()
    pilot_day_1_package_status = load_pilot_day_1_package_status()
    pilot_day_2_rhythm_status = load_pilot_day_2_rhythm_status()
    pilot_expansion_review_decision_status = load_pilot_expansion_review_decision_status()

    return {
        "transactions_count": transactions_count,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_cash_flow": net_cash_flow,
        "active_finance_actions": active_finance_actions,
        "high_finance_actions": high_finance_actions,
        "active_operations_tasks": active_operations_tasks,
        "overdue_operations_tasks": overdue_operations_tasks,
        "active_support_incidents": active_support_incidents,
        "critical_support_incidents": critical_support_incidents,
        "active_assistance_requests": active_assistance_requests,
        "high_assistance_requests": high_assistance_requests,
        "waiting_approval_requests": waiting_approval_requests,
        "pending_approval_requests": pending_approval_requests,
        "approved_approval_requests": approved_approval_requests,
        "rejected_approval_requests": rejected_approval_requests,
        "high_pending_approval_requests": high_pending_approval_requests,
        "total_people": total_people,
        "active_people": active_people,
        "admin_people": admin_people,
        "manager_people": manager_people,
        "governance_findings": governance_findings,
        "error_events": error_events,
        "overall_health": overall_health,
        "highest_risk": highest_risk,
        "next_move": next_move,
        "health_class": health_class,
        "recent_incidents": recent_incidents,
        "active_tasks": active_tasks,
        "recommended_actions": recommended_actions,
        "assistance_requests": assistance_requests,
        "approval_requests": approval_requests,
        "people_users": people_users,
        "sensitivity_findings": sensitivity_findings,
        "sensitive_findings": len(sensitivity_findings),
        "high_sensitivity_findings": high_sensitivity_findings,
        "medium_sensitivity_findings": medium_sensitivity_findings,
        "highest_sensitivity_risk": highest_sensitivity_risk,
        "sensitivity_next_move": sensitivity_next_move,
        "executive_alerts": executive_alerts,
        "executive_alert_count": len(executive_alerts),
        "critical_executive_alerts": critical_executive_alerts,
        "high_executive_alerts": high_executive_alerts,
        "open_executive_alerts": open_executive_alerts,
        "acknowledged_executive_alerts": acknowledged_executive_alerts,
        "in_review_executive_alerts": in_review_executive_alerts,
        "resolved_executive_alerts": resolved_executive_alerts,
        "cash_flow_series": load_cash_flow_series(),
        "daily_close_status": daily_close_status,
        "evidence_index_status": evidence_index_status,
        "notification_summary": notification_summary,
        "notification_outbox": notification_outbox,
        "delivery_approval_summary": delivery_approval_summary,
        "delivery_approval_rows": delivery_approval_rows,
        "secure_email_status": secure_email_status,
        "secure_email_report": secure_email_report,
        "system_integrity_status": system_integrity_status,
        "scheduled_daily_close_status": scheduled_daily_close_status,
        "private_demo_dry_run_status": private_demo_dry_run_status,
        "private_pilot_plan_status": private_pilot_plan_status,
        "private_pilot_tracker_status": private_pilot_tracker_status,
        "private_pilot_exit_decision_status": private_pilot_exit_decision_status,
        "pilot_day_1_package_status": pilot_day_1_package_status,
        "pilot_day_2_rhythm_status": pilot_day_2_rhythm_status,
        "pilot_expansion_review_decision_status": pilot_expansion_review_decision_status,
    }


def render_metric_card(title, value, caption, color_class=""):
    st.markdown(
        f"""
        <div class="bos-card">
            <div class="bos-card-title">{title}</div>
            <div class="bos-card-value {color_class}">{value}</div>
            <div class="bos-card-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_panel_start(title):
    st.markdown(
        f"""
        <div class="bos-panel">
            <div class="bos-section-title">{title}</div>
        """,
        unsafe_allow_html=True,
    )


def render_panel_end():
    st.markdown("</div>", unsafe_allow_html=True)


def render_brief_item(main_text, sub_text):
    st.markdown(
        f"""
        <div class="bos-brief-item">
            <div class="bos-dot"></div>
            <div>
                <div class="bos-item-main">{main_text}</div>
                <div class="bos-item-sub">{sub_text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_row(title, subtitle, status):
    status_class = str(status).lower().replace("_", "-")
    if status_class == "critical":
        status_class = "high"
    elif status_class in ("approved", "completed", "available", "sent", "green"):
        status_class = "healthy"
    elif status_class in ("missing", "failed", "blocked", "overdue", "rejected"):
        status_class = "high"
    elif status_class in ("pending", "in-progress", "waiting-approval", "waiting"):
        status_class = "medium"
    elif status_class in ("cancelled", "dismissed"):
        status_class = "low"

    st.markdown(
        f"""
        <div class="bos-row">
            <div>
                <div class="bos-item-main">{title}</div>
                <div class="bos-item-sub">{subtitle}</div>
            </div>
            <div class="bos-badge {status_class}">{status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown('<div class="bos-login-card">', unsafe_allow_html=True)
    st.title("BusinessOS")
    st.caption("Private executive dashboard. Sign in to continue.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in")

    if submitted:
        if validate_credentials(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = get_default_role(username)
            st.rerun()

        st.error("Invalid username or password.")

    if settings.using_default_password:
        st.warning(
            "Local MVP credentials are active. Change BUSINESSOS_ADMIN_PASSWORD before deploying."
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


def render_sidebar():
    role = st.session_state.get("role", "viewer")
    username = st.session_state.get("username", "user")
    allowed_pages = get_allowed_pages(role)

    st.sidebar.title("BusinessOS")
    st.sidebar.caption("Intelligence for better decisions")
    st.sidebar.divider()
    page = st.sidebar.radio("Navigation", allowed_pages)
    st.sidebar.divider()
    st.sidebar.caption(f"Signed in as {username}")
    st.sidebar.caption(f"Role: {role}")

    if st.sidebar.button("Refresh", use_container_width=True):
        st.rerun()

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    return page


def render_dashboard(data):
    st.markdown(
        f"""
        <div class="bos-topbar">
            <div>
                <div class="bos-title">BusinessOS Command Center</div>
                <div class="bos-subtitle">Unified executive intelligence across Alerts, Finance, Operations, Governance, Sensitivity, Support, Assistance, Approvals, Daily Close, Notifications, Delivery Approval, Secure Email, and People.</div>
            </div>
            <div class="bos-chip">System Health: {data['overall_health']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Financial Health", data["overall_health"], f"Net cash flow ${data['net_cash_flow']:,.2f}", data["health_class"])
    with col2:
        render_metric_card("Open Risks", data["highest_risk"], f"{data['overdue_operations_tasks']} overdue operations task(s)", "red")
    with col3:
        render_metric_card("Pending Actions", data["active_finance_actions"], "Requires executive review", "gold")
    with col4:
        render_metric_card("Critical Incidents", data["active_support_incidents"], "Active support workload", "red")

    left, right = st.columns([1, 1.95])

    with left:
        render_panel_start("Executive Brief")
        render_brief_item(data["next_move"], "Recommended cross-module executive move")
        render_brief_item(
            f"{data['active_finance_actions']} finance action(s) are active",
            "Finance intelligence remains in execution mode",
        )
        render_brief_item(
            f"{data['overdue_operations_tasks']} overdue operations task(s)",
            "Operations needs follow-up before workload expansion",
        )
        render_brief_item(
            f"{data['active_support_incidents']} support incident(s) active",
            "Support investigation is part of current system risk",
        )
        render_brief_item(
            f"{data['active_assistance_requests']} assistance request(s) active",
            "Internal users are asking BusinessOS for help, decisions, or routing",
        )
        render_panel_end()

    with right:
        render_panel_start("Cash Flow Overview")
        if data["cash_flow_series"].empty:
            st.info("No cash flow data available yet.")
        else:
            st.area_chart(data["cash_flow_series"], x="date", y="net_cash_flow", height=285)
        render_panel_end()

    ops_col, incident_col, alert_col = st.columns(3)

    with ops_col:
        render_panel_start("Operations Overview")
        if data["active_tasks"]:
            for task in data["active_tasks"]:
                render_status_row(task["title"], f"{task['owner_role']} | {task['status']}", task["priority"])
        else:
            render_status_row("No active operations tasks", "Operations workload is clear", "healthy")
        render_panel_end()

    with incident_col:
        render_panel_start("Recent Incidents")
        if data["recent_incidents"]:
            for incident in data["recent_incidents"]:
                render_status_row(incident["title"], f"{incident['owner_role']} | {incident['status']}", incident["severity"])
        else:
            render_status_row("No active incidents", "Support queue is clear", "healthy")
        render_panel_end()

    with alert_col:
        render_panel_start("Executive Alerts")
        if data["executive_alerts"]:
            for alert in data["executive_alerts"][:4]:
                render_status_row(
                    alert["title"],
                    f"{alert['source_module']} | {alert['owner_role']} | {alert['status']}",
                    alert["severity"],
                )
        else:
            render_status_row("No executive alerts", "System is clear for regular operating rhythm", "healthy")
        render_panel_end()


def render_module_page(page, data):
    st.markdown(
        f"""
        <div class="bos-topbar">
            <div>
                <div class="bos-title">{page}</div>
                <div class="bos-subtitle">Focused module view from the current BusinessOS dataset.</div>
            </div>
            <div class="bos-chip">Access: {st.session_state.get('role', 'viewer')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if page == "Alerts":
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Executive Alerts", data["executive_alert_count"], "Active cross-module alerts", "gold")
        with c2:
            render_metric_card("Open", data["open_executive_alerts"], "Awaiting owner acknowledgement", "red")
        with c3:
            render_metric_card("Acknowledged", data["acknowledged_executive_alerts"], "Owner has seen the alert", "gold")
        with c4:
            render_metric_card("In Review", data["in_review_executive_alerts"], "Resolution is being reviewed", "gold")
        with c5:
            render_metric_card("Resolved", data["resolved_executive_alerts"], "Closed with justification", "green")

        left, right = st.columns([1.55, 1])

        with left:
            render_panel_start("Executive Alert Queue")
            if data["executive_alerts"]:
                for alert in data["executive_alerts"][:10]:
                    render_status_row(
                        alert["title"],
                        f"{alert['source_module']} | {alert['owner_role']} | {alert['status']} | {alert['recommended_action']}",
                        alert["severity"],
                    )
            else:
                render_status_row("No executive alerts", "System is clear for regular operating rhythm", "healthy")
            render_panel_end()

        with right:
            render_panel_start("Alert Brief")
            render_brief_item(
                f"{data['executive_alert_count']} active executive alert(s)",
                "Cross-module signals are now consolidated into one executive queue",
            )
            render_brief_item(
                f"{data['high_executive_alerts']} high alert(s)",
                "High alerts should receive same-day owner follow-up",
            )
            render_brief_item(
                data["sensitivity_next_move"],
                "Governance sensitivity is feeding the alert layer",
            )
            render_panel_end()

    elif page == "Finance":
        c1, c2, c3 = st.columns(3)
        with c1:
            render_metric_card("Transactions", data["transactions_count"], "Loaded records", "")
        with c2:
            render_metric_card("Income", f"${data['total_income']:,.2f}", "Current sample dataset", "green")
        with c3:
            render_metric_card("Expenses", f"${data['total_expenses']:,.2f}", "Current sample dataset", "red")

    elif page == "Operations":
        c1, c2 = st.columns(2)
        with c1:
            render_metric_card("Active Tasks", data["active_operations_tasks"], "Open, in progress, or blocked", "gold")
        with c2:
            render_metric_card("Overdue Tasks", data["overdue_operations_tasks"], "Needs owner follow-up", "red")

    elif page == "Governance":
        c1, c2 = st.columns(2)
        with c1:
            render_metric_card("Governance Findings", data["governance_findings"], "Detected from audit logs", "green")
        with c2:
            render_metric_card("Error/Critical Events", data["error_events"], "Audit severity monitor", "green")

    elif page == "Support":
        c1, c2 = st.columns(2)
        with c1:
            render_metric_card("Active Incidents", data["active_support_incidents"], "Open, investigating, or waiting", "red")
        with c2:
            render_metric_card("Critical/High Incidents", data["critical_support_incidents"], "Escalation-sensitive queue", "gold")

    elif page == "Assistance":
        c1, c2, c3 = st.columns(3)
        with c1:
            render_metric_card("Active Requests", data["active_assistance_requests"], "Open, triaged, approval, or in progress", "gold")
        with c2:
            render_metric_card("High-Severity Requests", data["high_assistance_requests"], "Requires owner attention", "red")
        with c3:
            render_metric_card("Waiting Approval", data["waiting_approval_requests"], "Blocked on approval", "gold")

        left, right = st.columns([1.4, 1])

        with left:
            render_panel_start("Active Assistance Requests")
            if data["assistance_requests"]:
                for request in data["assistance_requests"]:
                    render_status_row(
                        request["title"],
                        f"{request['owner_role']} | {request['request_type']} | {request['status']}",
                        request["severity"],
                    )
            else:
                render_status_row("No active assistance requests", "Internal request queue is clear", "healthy")
            render_panel_end()

        with right:
            render_panel_start("Assistance Brief")
            render_brief_item(
                f"{data['active_assistance_requests']} active assistance request(s)",
                "Internal work is now visible as request flow",
            )
            render_brief_item(
                f"{data['high_assistance_requests']} high-severity request(s)",
                "Prioritize owner assignment and triage",
            )
            render_brief_item(
                f"{data['waiting_approval_requests']} waiting for approval",
                "Governance-sensitive requests should not bypass review",
            )
            render_panel_end()

    elif page == "Approvals":
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Pending", data["pending_approval_requests"], "Awaiting executive decision", "red")
        with c2:
            render_metric_card("Approved", data["approved_approval_requests"], "Confirmed with justification", "green")
        with c3:
            render_metric_card("Rejected", data["rejected_approval_requests"], "Stopped or sent back", "gold")
        with c4:
            render_metric_card("High Priority", data["high_pending_approval_requests"], "Pending high/critical approvals", "red")

        left, right = st.columns([1.55, 1])

        with left:
            render_panel_start("Approval Decision Queue")
            if data["approval_requests"]:
                for approval in data["approval_requests"]:
                    detail = f"{approval['approver_role']} | {approval['approval_type']} | {approval['status']}"
                    if approval["status_justification"]:
                        detail = f"{detail} | {approval['status_justification']}"
                    render_status_row(approval["title"], detail, approval["priority"])
            else:
                render_status_row("No approval requests", "Approval queue is clear", "healthy")
            render_panel_end()

        with right:
            render_panel_start("Approval Brief")
            render_brief_item(
                f"{data['pending_approval_requests']} pending approval(s)",
                "Pending approvals are the current executive decision queue",
            )
            render_brief_item(
                f"{data['approved_approval_requests']} approved approval(s)",
                "Approved items have moved through controlled review",
            )
            render_brief_item(
                f"{data['rejected_approval_requests']} rejected approval(s)",
                "Rejected items were stopped or returned for a better path",
            )
            render_panel_end()
    elif page == "Daily Close":
        daily_close = data["daily_close_status"]
        evidence_index = data["evidence_index_status"]
        completed_steps = daily_close["completed_steps"]
        total_steps = daily_close["total_steps"]
        step_caption = "Latest executive close report" if daily_close["exists"] else "No daily close report found"

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Close Steps", f"{completed_steps}/{total_steps}", step_caption, "green" if completed_steps == total_steps and total_steps > 0 else "gold")
        with c2:
            render_metric_card("Evidence Available", daily_close["evidence_available"], "Reports found for today's evidence index", "green")
        with c3:
            render_metric_card("Evidence Missing", daily_close["evidence_missing"], "Missing evidence items requiring follow-up", "red" if daily_close["evidence_missing"] else "green")
        with c4:
            render_metric_card("Evidence Items", len(evidence_index["items"]), "Indexed executive proof points", "green" if evidence_index["items"] else "gold")

        left, right = st.columns([1.45, 1])

        with left:
            render_panel_start("Daily Close Steps")
            if daily_close["steps"]:
                for step in daily_close["steps"]:
                    render_status_row(step["name"], step["detail"], step["status"])
            else:
                render_status_row("No daily close report", "Run python cli.py daily-close to generate today's executive close", "medium")
            render_panel_end()

        with right:
            render_panel_start("Close Brief")
            render_brief_item(
                daily_close["report_path"] or "Daily close report not generated",
                "Latest executive close artifact",
            )
            render_brief_item(
                evidence_index["report_path"] or "Evidence index not generated",
                "Latest evidence index artifact",
            )
            render_brief_item(
                f"{daily_close['evidence_missing']} missing evidence item(s)",
                "Missing evidence should be resolved before treating the day as fully closed",
            )
            render_panel_end()

        render_panel_start("Evidence Register")
        if evidence_index["items"]:
            for item in evidence_index["items"]:
                render_status_row(
                    item["label"],
                    f"{item['report_path']} | {item['purpose']}",
                    item["status"],
                )
        else:
            render_status_row("No evidence index items", "Run python cli.py evidence-index or python cli.py daily-close", "medium")
        render_panel_end()
    elif page == "Scheduled Close":
        schedule = data["scheduled_daily_close_status"]
        enabled_label = "Enabled" if schedule["enabled"] else "Disabled"
        report_label = "Available" if schedule["today_report_exists"] else "Missing"
        next_action = schedule["next_action"].replace("_", " ").title()
        last_status = (schedule["last_status"] or "unknown").replace("_", " ").title()

        next_action_class = {
            "due": "red",
            "waiting_for_run_time": "gold",
            "already_recorded_today": "green",
            "close_already_available": "green",
            "disabled": "red",
            "missing_schedule": "red",
        }.get(schedule["next_action"], "gold")

        last_status_class = {
            "completed": "green",
            "skipped_existing_close": "green",
            "ready": "gold",
            "running": "gold",
            "failed": "red",
            "missing": "red",
        }.get(schedule["last_status"], "gold")
        last_status_badge = {
            "completed": "healthy",
            "skipped_existing_close": "healthy",
            "ready": "medium",
            "running": "medium",
            "failed": "high",
            "missing": "high",
        }.get(schedule["last_status"], "medium")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Schedule", enabled_label, schedule["schedule_name"], "green" if schedule["enabled"] else "red")
        with c2:
            render_metric_card("Run Time", schedule["run_time_local"], "Local time gate", "")
        with c3:
            render_metric_card("Today Close", report_label, schedule["today_report_path"], "green" if schedule["today_report_exists"] else "gold")
        with c4:
            render_metric_card("Last Status", last_status, schedule["last_run_date"] or "No recorded run", last_status_class)
        with c5:
            render_metric_card("Next Action", next_action, f"Current local time {schedule['current_time_local']}", next_action_class)

        left, right = st.columns([1.55, 1])

        with left:
            render_panel_start("Schedule State")
            render_status_row("Schedule name", schedule["schedule_name"], "healthy" if schedule["exists"] else "high")
            render_status_row("Today", f"{schedule['today']} | current local time {schedule['current_time_local']}", "healthy")
            render_status_row("Run time gate", schedule["run_time_local"], "medium")
            render_status_row("Today close report", schedule["today_report_path"], "healthy" if schedule["today_report_exists"] else "medium")
            render_status_row("Last run date", schedule["last_run_date"] or "No run recorded", last_status_badge)
            render_status_row("Last started", schedule["last_started_at"] or "No start recorded", last_status_badge)
            render_status_row("Last completed", schedule["last_completed_at"] or "No completion recorded", last_status_badge)
            render_panel_end()

        with right:
            render_panel_start("Scheduled Close Brief")
            render_brief_item(
                schedule["last_message"] or "No scheduler message recorded",
                "Latest scheduler outcome",
            )
            render_brief_item(
                "python cli.py daily-close-schedule",
                "Use CLI to inspect schedule status",
            )
            render_brief_item(
                "python cli.py scheduled-daily-close",
                "Use CLI or an external scheduler to run the gated close",
            )
            render_panel_end()
    elif page == "Notifications":
        notification_summary = data["notification_summary"]
        notifications = data["notification_outbox"]

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Total", notification_summary["total"], "Internal delivery records", "")
        with c2:
            render_metric_card("Queued", notification_summary["queued"], "Ready for protected delivery", "gold")
        with c3:
            render_metric_card("Sent", notification_summary["sent"], "Marked as delivered", "green")
        with c4:
            render_metric_card("Dismissed", notification_summary["dismissed"], "Closed without delivery", "gold")
        with c5:
            render_metric_card("Failed", notification_summary["failed"], "Needs delivery review", "red")

        status_filter = st.selectbox(
            "Status filter",
            ["all", "queued", "sent", "dismissed", "failed"],
            index=0,
        )
        filtered_notifications = [
            notification
            for notification in notifications
            if status_filter == "all" or notification["status"] == status_filter
        ]

        status_styles = {
            "queued": "medium",
            "sent": "healthy",
            "dismissed": "low",
            "failed": "high",
        }

        left, right = st.columns([1.6, 1])

        with left:
            render_panel_start("Notification Outbox")
            if filtered_notifications:
                for notification in filtered_notifications:
                    detail = (
                        f"{notification['channel']} | "
                        f"{notification['recipient_name']} <{notification['recipient_email']}> | "
                        f"{notification['recipient_role']} | "
                        f"{notification['source_module']}:{notification['source_reference_id']}"
                    )
                    render_status_row(
                        notification["subject"],
                        detail,
                        status_styles.get(notification["status"], notification["status"]),
                    )
            else:
                render_status_row("No notifications found", "Notification outbox has no records for this status", "healthy")
            render_panel_end()

        with right:
            render_panel_start("Notification Brief")
            render_brief_item(
                f"{notification_summary['queued']} queued notification(s)",
                "Queued items require delivery approval before protected sending",
            )
            render_brief_item(
                f"{notification_summary['sent']} sent notification(s)",
                "Sent items have been marked by the protected status workflow",
            )
            render_brief_item(
                f"{notification_summary['failed']} failed notification(s)",
                "Failed items should be reviewed before delivery automation expands",
            )
            render_panel_end()
    elif page == "Delivery Approval":
        delivery_summary = data["delivery_approval_summary"]
        delivery_rows = data["delivery_approval_rows"]

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Queued", delivery_summary["queued_notifications"], "Notification records awaiting delivery", "gold")
        with c2:
            render_metric_card("Pending", delivery_summary["pending_delivery_approvals"], "Delivery approvals waiting", "red" if delivery_summary["pending_delivery_approvals"] else "green")
        with c3:
            render_metric_card("Approved", delivery_summary["approved_delivery_approvals"], "Approved delivery gates", "green")
        with c4:
            render_metric_card("Ready", delivery_summary["ready_to_deliver"], "Queued and approved", "green" if delivery_summary["ready_to_deliver"] else "gold")
        with c5:
            render_metric_card("Blocked", delivery_summary["blocked_notifications"], "Queued without approval", "red" if delivery_summary["blocked_notifications"] else "green")

        approval_filter = st.selectbox(
            "Approval status filter",
            ["all", "missing", "pending", "approved", "rejected", "cancelled"],
            index=0,
        )
        filtered_rows = [
            row
            for row in delivery_rows
            if approval_filter == "all" or row["approval_status"] == approval_filter
        ]

        left, right = st.columns([1.6, 1])

        with left:
            render_panel_start("Delivery Approval Queue")
            if filtered_rows:
                for row in filtered_rows:
                    detail = (
                        f"{row['notification_status']} | "
                        f"{row['recipient_name']} <{row['recipient_email']}> | "
                        f"{row['recipient_role']} | "
                        f"Approver: {row['approver_role']}"
                    )
                    render_status_row(
                        row["subject"],
                        detail,
                        row["approval_status"],
                    )
            else:
                render_status_row("No delivery approvals found", "No records match this approval status", "healthy")
            render_panel_end()

        with right:
            render_panel_start("Delivery Approval Brief")
            render_brief_item(
                f"{delivery_summary['blocked_notifications']} blocked notification(s)",
                "Blocked items cannot be marked sent until approval is approved",
            )
            render_brief_item(
                f"{delivery_summary['ready_to_deliver']} ready notification(s)",
                "Ready items have queued notification status and approved delivery approval",
            )
            render_brief_item(
                "python cli.py notification-delivery-approval",
                "Use CLI to refresh delivery approval requests and report",
            )
            render_panel_end()
    elif page == "Secure Email":
        email_status = data["secure_email_status"]
        email_report = data["secure_email_report"]

        mode = email_status["delivery_mode"]
        mode_class = {
            "disabled": "gold",
            "dry_run": "gold",
            "configuration_error": "red",
            "smtp": "green",
        }.get(mode, "gold")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Mode", mode.replace("_", " ").title(), "Current adapter mode", mode_class)
        with c2:
            render_metric_card("Dry Run", "Yes" if email_status["dry_run"] else "No", "External delivery guard", "gold" if email_status["dry_run"] else "green")
        with c3:
            render_metric_card("Configured", "Yes" if email_status["smtp_configured"] else "No", "SMTP credentials present", "green" if email_status["smtp_configured"] else "gold")
        with c4:
            render_metric_card("Ready", email_status["ready_to_deliver"], "Approved queued email notifications", "green" if email_status["ready_to_deliver"] else "gold")
        with c5:
            render_metric_card("Failed", email_report["failed"], "Latest delivery report failures", "red" if email_report["failed"] else "green")

        left, right = st.columns([1.6, 1])

        with left:
            render_panel_start("Latest Secure Email Results")
            if email_report["results"]:
                for result in email_report["results"]:
                    render_status_row(
                        result["subject"],
                        f"{result['recipient_email']} | {result['message']}",
                        result["delivery_status"],
                    )
            else:
                render_status_row(
                    "No delivery results",
                    email_report["report_path"] or "Run python cli.py secure-email-delivery to export a report",
                    "healthy" if email_report["exists"] else "medium",
                )
            render_panel_end()

        with right:
            render_panel_start("Secure Email Brief")
            render_brief_item(
                email_report["report_path"] or "Secure email report not generated",
                "Latest secure email delivery artifact",
            )
            render_brief_item(
                f"{email_report['sent']} sent, {email_report['blocked_or_skipped']} blocked/skipped",
                "Latest delivery run outcome",
            )
            render_brief_item(
                "python cli.py secure-email-delivery",
                "Use CLI to run the adapter; dashboard remains read-only",
            )
            render_panel_end()
    elif page == "System Integrity":
        system_integrity = data["system_integrity_status"]
        overall_status = system_integrity["overall_status"]
        overall_class = {
            "passed": "green",
            "warning": "gold",
            "failed": "red",
        }.get(overall_status, "gold")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Overall", overall_status.title(), "Latest system-check result", overall_class)
        with c2:
            render_metric_card("Total", system_integrity["total_checks"], "Checks evaluated", "")
        with c3:
            render_metric_card("Passed", system_integrity["passed_checks"], "Healthy controls", "green")
        with c4:
            render_metric_card("Warnings", system_integrity["warning_checks"], "Needs review", "gold" if system_integrity["warning_checks"] else "green")
        with c5:
            render_metric_card("Failed", system_integrity["failed_checks"], "Critical failures", "red" if system_integrity["failed_checks"] else "green")

        status_filter = st.selectbox(
            "Check status filter",
            ["all", "passed", "warning", "failed"],
            index=0,
        )
        filtered_checks = [
            check
            for check in system_integrity["checks"]
            if status_filter == "all" or check["status"] == status_filter
        ]

        status_styles = {
            "passed": "healthy",
            "warning": "medium",
            "failed": "high",
        }

        left, right = st.columns([1.6, 1])

        with left:
            render_panel_start("Integrity Checks")
            if filtered_checks:
                for check in filtered_checks:
                    render_status_row(
                        check["name"],
                        check["detail"],
                        status_styles.get(check["status"], check["status"]),
                    )
            else:
                render_status_row("No checks found", "No integrity checks match this filter", "healthy")
            render_panel_end()

        with right:
            render_panel_start("Integrity Brief")
            render_brief_item(
                system_integrity["report_path"] or "System integrity report not generated",
                "Latest exported system-check artifact",
            )
            render_brief_item(
                f"{system_integrity['passed_checks']} of {system_integrity['total_checks']} checks passing",
                "System integrity coverage across modules, tables, reports, and security boundaries",
            )
            render_brief_item(
                f"{system_integrity['warning_checks']} warning(s) and {system_integrity['failed_checks']} failed check(s)",
                "Warnings are expected during active uncommitted work; failures require immediate review",
            )
            render_panel_end()
    elif page == "Pilot Plan":
        pilot = data["private_pilot_plan_status"]
        plan_status = pilot["plan_status"]
        plan_class = {
            "pilot_plan_ready": "green",
            "pilot_plan_ready_with_warnings": "gold",
            "blocked": "red",
            "missing": "red",
        }.get(plan_status, "gold")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Plan Status", plan_status.replace("_", " ").title(), "Latest private pilot plan", plan_class)
        with c2:
            render_metric_card("Length", f"{pilot['pilot_length']} days", "Controlled pilot window", "")
        with c3:
            render_metric_card("Owner", pilot["pilot_owner"], "Maximum authority owner", "gold")
        with c4:
            render_metric_card("Workflow", pilot["primary_workflow"], "Primary pilot workflow", "green" if pilot["primary_workflow"] != "No pilot yet" else "red")
        with c5:
            render_metric_card("Phases", len(pilot["timeline"]), "Pilot timeline phases", "")

        left, right = st.columns([1.55, 1])

        with left:
            render_panel_start("14-Day Pilot Timeline")
            if pilot["timeline"]:
                for phase in pilot["timeline"]:
                    detail = f"{phase['objective']} Evidence: {phase['evidence']}"
                    render_status_row(
                        f"{phase['days']} | {phase['phase']}",
                        detail,
                        "healthy",
                    )
            else:
                render_status_row("No pilot timeline found", "Run python cli.py private-pilot-plan", "medium")
            render_panel_end()

            render_panel_start("Daily Operating Rhythm")
            if pilot["daily_rhythm"]:
                for index, item in enumerate(pilot["daily_rhythm"], start=1):
                    render_status_row(f"Daily step {index}", item, "healthy")
            else:
                render_status_row("No daily rhythm found", "Generate the pilot plan artifact", "medium")
            render_panel_end()

        with right:
            render_panel_start("Pilot Evidence")
            render_brief_item(
                pilot["report_path"] or "Private pilot plan report not generated",
                "Latest private pilot plan artifact",
            )
            render_brief_item(
                pilot["intake_status"].replace("_", " ").title(),
                "Source intake status",
            )
            render_brief_item(
                pilot["recommended_module"],
                "Recommended starting module",
            )
            render_brief_item(
                pilot["first_action"],
                "Immediate next action before pilot kickoff",
            )
            render_panel_end()

            render_panel_start("Pilot Roles")
            if pilot["roles"]:
                for role in pilot["roles"]:
                    render_status_row(
                        role["role"],
                        f"{role['type']} | {role['responsibility']}",
                        "healthy",
                    )
            else:
                render_status_row("No pilot roles found", "Run python cli.py private-pilot-plan", "medium")
            render_panel_end()

            render_panel_start("Exit Decisions")
            if pilot["exit_decisions"]:
                for decision in pilot["exit_decisions"]:
                    render_status_row(decision, "Allowed pilot outcome", "medium")
            else:
                render_status_row("No exit decisions found", "Generate the pilot plan artifact", "medium")
            render_panel_end()

        render_panel_start("Success Criteria")
        if pilot["success_criteria"]:
            for criterion in pilot["success_criteria"]:
                render_status_row(criterion, "Pilot success evidence", "healthy")
        else:
            render_status_row("No success criteria found", "Generate the pilot plan artifact", "medium")
        render_panel_end()

        render_panel_start("Pilot Boundaries")
        if pilot["boundaries"]:
            for boundary in pilot["boundaries"]:
                render_status_row(boundary, "Protected pilot boundary", "medium")
        else:
            render_status_row("No pilot boundaries found", "Generate the pilot plan artifact", "medium")
        render_panel_end()
    elif page == "Pilot Tracker":
        tracker = data["private_pilot_tracker_status"]
        tracker_status = tracker["tracker_status"]
        tracker_class = {
            "on_track": "green",
            "needs_attention": "gold",
            "blocked": "red",
            "missing": "red",
        }.get(tracker_status, "gold")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Tracker Status", tracker_status.replace("_", " ").title(), "Latest pilot daily tracker", tracker_class)
        with c2:
            render_metric_card("Evidence", tracker["available_evidence"], "Available tracker artifacts", "green" if tracker["available_evidence"] else "red")
        with c3:
            render_metric_card("Missing Required", tracker["missing_required"], "Blocks pilot if above zero", "red" if tracker["missing_required"] else "green")
        with c4:
            render_metric_card("Missing Optional", tracker["missing_optional"], "Needs attention if above zero", "gold" if tracker["missing_optional"] else "green")
        with c5:
            render_metric_card("Length", f"{tracker['pilot_length']} days", "Controlled pilot window", "")

        left, right = st.columns([1.45, 1])

        with left:
            render_panel_start("Evidence Checklist")
            if tracker["evidence_rows"]:
                for item in tracker["evidence_rows"]:
                    status = "healthy" if item["status"] == "available" else "high"
                    required_label = "required" if item["required"] == "yes" else "optional"
                    render_status_row(
                        f"{item['evidence']} | {item['status'].title()}",
                        f"{required_label.title()} | {item['owner']} | {item['latest_report']}",
                        status,
                    )
            else:
                render_status_row("No tracker evidence found", "Run python cli.py private-pilot-tracker", "medium")
            render_panel_end()

            render_panel_start("Daily Operator Steps")
            if tracker["daily_steps"]:
                for index, step in enumerate(tracker["daily_steps"], start=1):
                    render_status_row(f"Step {index}", step, "healthy")
            else:
                render_status_row("No daily tracker steps found", "Generate the tracker artifact", "medium")
            render_panel_end()

        with right:
            render_panel_start("Pilot Tracker Summary")
            render_brief_item(
                tracker["report_path"] or "Private pilot tracker report not generated",
                "Latest tracker artifact",
            )
            render_brief_item(
                tracker["plan_status"].replace("_", " ").title(),
                "Linked pilot plan status",
            )
            render_brief_item(
                tracker["pilot_owner"],
                "Pilot owner",
            )
            render_brief_item(
                tracker["primary_workflow"],
                "Primary pilot workflow",
            )
            render_panel_end()

            render_panel_start("Next Action")
            render_status_row(
                tracker["next_action"],
                "Operator action before continuing the pilot rhythm",
                "medium" if tracker_status == "needs_attention" else tracker_status,
            )
            render_panel_end()

            render_panel_start("Operator Note")
            render_brief_item(
                tracker["operator_note"],
                "Read-only guidance from the tracker report",
            )
            render_panel_end()
    elif page == "Pilot Exit":
        exit_decision = data["private_pilot_exit_decision_status"]
        decision_status = exit_decision["decision_status"]
        decision_class = {
            "decision_ready": "green",
            "decision_ready_with_warnings": "gold",
            "blocked": "red",
            "missing": "red",
        }.get(decision_status, "gold")
        risk_class = {
            "low": "green",
            "medium": "gold",
            "high": "red",
            "critical": "red",
        }.get(exit_decision["highest_exit_risk"].lower(), "gold")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Decision Status", decision_status.replace("_", " ").title(), "Latest pilot exit artifact", decision_class)
        with c2:
            render_metric_card("Recommendation", exit_decision["recommended_decision"].replace("_", " ").title(), "Advisory only", decision_class)
        with c3:
            render_metric_card("Exit Risk", exit_decision["highest_exit_risk"].title(), "Before final owner decision", risk_class)
        with c4:
            render_metric_card("Evidence", exit_decision["available_evidence"], "Available decision artifacts", "green" if exit_decision["available_evidence"] else "red")
        with c5:
            render_metric_card("Missing Required", exit_decision["missing_required"], "Blocks final decision if above zero", "red" if exit_decision["missing_required"] else "green")

        left, right = st.columns([1.45, 1])

        with left:
            render_panel_start("Decision Rationale")
            if exit_decision["rationale"]:
                for item in exit_decision["rationale"]:
                    render_status_row(item, "Why BusinessOS recommends this exit decision", "medium")
            else:
                render_status_row("No decision rationale found", "Run python cli.py private-pilot-exit-decision", "medium")
            render_panel_end()

            render_panel_start("Conditions Before Execution")
            if exit_decision["conditions"]:
                for condition in exit_decision["conditions"]:
                    render_status_row(condition, "Required before acting on the recommendation", "healthy")
            else:
                render_status_row("No execution conditions found", "Generate the exit decision artifact", "medium")
            render_panel_end()

            render_panel_start("Evidence Summary")
            if exit_decision["evidence_rows"]:
                for item in exit_decision["evidence_rows"]:
                    status = "healthy" if item["status"] == "available" else "high"
                    required_label = "required" if item["required"] == "yes" else "optional"
                    render_status_row(
                        f"{item['evidence']} | {item['status'].title()}",
                        f"{required_label.title()} | {item['latest_report']}",
                        status,
                    )
            else:
                render_status_row("No exit evidence found", "Run python cli.py private-pilot-exit-decision", "medium")
            render_panel_end()

        with right:
            render_panel_start("Exit Decision Summary")
            render_brief_item(
                exit_decision["report_path"] or "Private pilot exit decision report not generated",
                "Latest exit decision artifact",
            )
            render_brief_item(
                exit_decision["pilot_owner"],
                "Pilot owner",
            )
            render_brief_item(
                exit_decision["primary_workflow"],
                "Primary workflow",
            )
            render_brief_item(
                exit_decision["tracker_status"].replace("_", " ").title(),
                "Source tracker status",
            )
            render_panel_end()

            render_panel_start("Next Action")
            render_status_row(
                exit_decision["next_action"],
                "Executive owner must confirm before execution",
                "medium" if decision_status == "decision_ready_with_warnings" else decision_status,
            )
            render_panel_end()

            render_panel_start("Allowed Exit Options")
            if exit_decision["exit_options"]:
                for option in exit_decision["exit_options"]:
                    render_status_row(
                        option["decision"].replace("_", " ").title(),
                        option["meaning"],
                        "medium",
                    )
            else:
                render_status_row("No exit options found", "Generate the exit decision artifact", "medium")
            render_panel_end()

            render_panel_start("Operator Note")
            render_brief_item(
                exit_decision["operator_note"],
                "Decision support only; no automatic execution",
            )
            render_panel_end()
    elif page == "Pilot Day 1":
        day_1 = data["pilot_day_1_package_status"]
        day_1_status = day_1["day_1_status"]
        day_1_class = {
            "ready": "green",
            "ready_with_warnings": "gold",
            "blocked": "red",
            "missing": "red",
        }.get(day_1_status, "gold")
        risk_class = {
            "low": "green",
            "medium": "gold",
            "high": "red",
            "critical": "red",
        }.get(day_1["highest_exit_risk"].lower(), "gold")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Day 1 Status", day_1_status.replace("_", " ").title(), "Latest Day 1 package", day_1_class)
        with c2:
            render_metric_card("Workflow", day_1["primary_workflow"], "Primary pilot workflow", "green" if day_1["primary_workflow"] != "Not selected" else "red")
        with c3:
            render_metric_card("Evidence", day_1["available_evidence"], "Available pilot artifacts", "green" if day_1["available_evidence"] else "red")
        with c4:
            render_metric_card("Missing Required", day_1["missing_required_evidence"], "Blocks Day 1 if above zero", "red" if day_1["missing_required_evidence"] else "green")
        with c5:
            render_metric_card("Exit Risk", day_1["highest_exit_risk"].title(), "Before expansion", risk_class)

        left, right = st.columns([1.45, 1])

        with left:
            render_panel_start("Day 1 Command Runbook")
            if day_1["commands"]:
                for item in day_1["commands"]:
                    render_status_row(item["purpose"], item["command"], "healthy")
            else:
                render_status_row("No command runbook found", "Run python cli.py pilot-day-1-package", "medium")
            render_panel_end()

            render_panel_start("Expected Evidence")
            if day_1["expected_evidence"]:
                for evidence in day_1["expected_evidence"]:
                    render_status_row(evidence, "Expected Day 1 artifact", "healthy")
            else:
                render_status_row("No evidence list found", "Generate the Day 1 package artifact", "medium")
            render_panel_end()

            render_panel_start("Close Criteria")
            if day_1["close_criteria"]:
                for criterion in day_1["close_criteria"]:
                    render_status_row(criterion, "Required before closing Day 1", "healthy")
            else:
                render_status_row("No close criteria found", "Generate the Day 1 package artifact", "medium")
            render_panel_end()

        with right:
            render_panel_start("Day 1 Summary")
            render_brief_item(
                day_1["report_path"] or "Pilot Day 1 package not generated",
                "Latest Day 1 package artifact",
            )
            render_brief_item(day_1["pilot_owner"], "Pilot owner")
            render_brief_item(day_1["plan_status"].replace("_", " ").title(), "Linked plan status")
            render_brief_item(day_1["tracker_status"].replace("_", " ").title(), "Linked tracker status")
            render_brief_item(day_1["recommended_exit_decision"].replace("_", " ").title(), "Advisory exit decision")
            render_panel_end()

            render_panel_start("Next Action")
            render_status_row(day_1["next_action"], "Executive owner confirms before scope expansion", "medium" if day_1_status == "ready_with_warnings" else day_1_status)
            render_panel_end()

            render_panel_start("Executive Owner Review")
            if day_1["owner_review"]:
                for item in day_1["owner_review"]:
                    render_status_row(item, "Owner review checkpoint", "medium")
            else:
                render_status_row("No owner review checklist found", "Generate the Day 1 package artifact", "medium")
            render_panel_end()

            render_panel_start("Risks and Boundaries")
            if day_1["risks"]:
                for risk in day_1["risks"]:
                    render_status_row(risk, "Protected Day 1 boundary", "medium")
            else:
                render_status_row("No risk boundaries found", "Generate the Day 1 package artifact", "medium")
            render_panel_end()

        render_panel_start("Operator Note")
        render_brief_item(day_1["operator_note"], "Read-only guidance for controlled Day 1 operation")
        render_panel_end()
    elif page == "Pilot Day 2":
        day_2 = data["pilot_day_2_rhythm_status"]
        day_2_status = day_2["day_2_status"]
        day_2_class = {
            "continue": "green",
            "continue_with_warnings": "gold",
            "blocked": "red",
            "missing": "red",
        }.get(day_2_status, "gold")
        risk_class = {
            "low": "green",
            "medium": "gold",
            "high": "red",
            "critical": "red",
        }.get(day_2["highest_exit_risk"].lower(), "gold")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Day 2 Status", day_2_status.replace("_", " ").title(), "Latest Day 2 rhythm", day_2_class)
        with c2:
            render_metric_card("Decision", day_2["continuation_decision"].replace("_", " ").title(), "Continuation guidance", day_2_class)
        with c3:
            render_metric_card("Evidence", day_2["available_evidence"], "Available pilot artifacts", "green" if day_2["available_evidence"] else "red")
        with c4:
            render_metric_card("Missing Required", day_2["missing_required_evidence"], "Blocks continuation if above zero", "red" if day_2["missing_required_evidence"] else "green")
        with c5:
            render_metric_card("Exit Risk", day_2["highest_exit_risk"].title(), "Before Day 3", risk_class)

        left, right = st.columns([1.45, 1])

        with left:
            render_panel_start("Day 2 Operating Rhythm")
            if day_2["rhythm"]:
                for index, item in enumerate(day_2["rhythm"], start=1):
                    render_status_row(f"Rhythm {index}", item, "healthy")
            else:
                render_status_row("No operating rhythm found", "Run python cli.py pilot-day-2-rhythm", "medium")
            render_panel_end()

            render_panel_start("Day 2 Command Runbook")
            if day_2["commands"]:
                for item in day_2["commands"]:
                    render_status_row(item["purpose"], item["command"], "healthy")
            else:
                render_status_row("No command runbook found", "Run python cli.py pilot-day-2-rhythm", "medium")
            render_panel_end()

            render_panel_start("Expected Evidence")
            if day_2["expected_evidence"]:
                for evidence in day_2["expected_evidence"]:
                    render_status_row(evidence, "Expected Day 2 artifact", "healthy")
            else:
                render_status_row("No evidence list found", "Generate the Day 2 rhythm artifact", "medium")
            render_panel_end()

        with right:
            render_panel_start("Day 2 Summary")
            render_brief_item(
                day_2["report_path"] or "Pilot Day 2 rhythm not generated",
                "Latest Day 2 rhythm artifact",
            )
            render_brief_item(day_2["pilot_owner"], "Pilot owner")
            render_brief_item(day_2["primary_workflow"], "Primary workflow")
            render_brief_item(day_2["day_1_status"].replace("_", " ").title(), "Source Day 1 status")
            render_brief_item(day_2["tracker_status"].replace("_", " ").title(), "Source tracker status")
            render_panel_end()

            render_panel_start("Next Action")
            render_status_row(day_2["next_action"], "Before Day 3 planning", "medium" if day_2_status == "continue_with_warnings" else day_2_status)
            render_panel_end()

            render_panel_start("Executive Review Checks")
            if day_2["review_checks"]:
                for item in day_2["review_checks"]:
                    render_status_row(item, "Executive review checkpoint", "medium")
            else:
                render_status_row("No review checks found", "Generate the Day 2 rhythm artifact", "medium")
            render_panel_end()

            render_panel_start("Day 2 Boundaries")
            if day_2["boundaries"]:
                for boundary in day_2["boundaries"]:
                    render_status_row(boundary, "Protected continuation boundary", "medium")
            else:
                render_status_row("No boundaries found", "Generate the Day 2 rhythm artifact", "medium")
            render_panel_end()

        render_panel_start("Operator Note")
        render_brief_item(day_2["operator_note"], "Read-only guidance for repeatable pilot operation")
        render_panel_end()
    elif page == "Pilot Expansion":
        expansion = data["pilot_expansion_review_decision_status"]
        decision_status = expansion["decision_status"]
        decision_class = {
            "ready_to_schedule_expansion_review": "green",
            "decision_ready_with_conditions": "gold",
            "blocked_missing_required_evidence": "red",
            "blocked_scope_not_narrow": "red",
            "missing": "red",
        }.get(decision_status, "gold")
        risk_class = {
            "low": "green",
            "medium": "gold",
            "high": "red",
            "critical": "red",
        }.get(expansion["highest_exit_risk"].lower(), "gold")
        expansion_class = "green" if expansion["expansion_status"] == "approved" else "gold"

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Decision Status", decision_status.replace("_", " ").title(), "Latest expansion decision", decision_class)
        with c2:
            render_metric_card("Recommendation", expansion["recommended_decision"].replace("_", " ").title(), "Advisory only", decision_class)
        with c3:
            render_metric_card("Pending Conditions", expansion["pending_conditions"], "Blocks approval if above zero", "gold" if expansion["pending_conditions"] else "green")
        with c4:
            render_metric_card("Missing Required", expansion["missing_required_evidence"], "Required evidence gate", "red" if expansion["missing_required_evidence"] else "green")
        with c5:
            render_metric_card("Exit Risk", expansion["highest_exit_risk"].title(), "Before expansion", risk_class)

        left, right = st.columns([1.45, 1])

        with left:
            render_panel_start("Condition Gate")
            if expansion["conditions"]:
                status_styles = {
                    "met": "healthy",
                    "pending": "medium",
                    "not_approved": "medium",
                    "missing": "high",
                    "blocked": "high",
                }
                for condition in expansion["conditions"]:
                    status = status_styles.get(condition["status"], "medium")
                    render_status_row(
                        f"{condition['condition']} | {condition['status'].replace('_', ' ').title()}",
                        condition["detail"],
                        status,
                    )
            else:
                render_status_row("No expansion conditions found", "Run python cli.py pilot-expansion-review-decision", "medium")
            render_panel_end()

            render_panel_start("Decision Rationale")
            if expansion["rationale"]:
                for item in expansion["rationale"]:
                    render_status_row(item, "Why BusinessOS recommends this expansion decision", "medium")
            else:
                render_status_row("No rationale found", "Generate the expansion decision artifact", "medium")
            render_panel_end()

            render_panel_start("Decision Commands")
            if expansion["commands"]:
                for item in expansion["commands"]:
                    render_status_row(item["purpose"], item["command"], "healthy")
            else:
                render_status_row("No command list found", "Generate the expansion decision artifact", "medium")
            render_panel_end()

        with right:
            render_panel_start("Expansion Summary")
            render_brief_item(
                expansion["report_path"] or "Pilot expansion decision report not generated",
                "Latest expansion review decision artifact",
            )
            render_brief_item(expansion["pilot_owner"], "Pilot owner")
            render_brief_item(expansion["primary_workflow"], "Primary workflow")
            render_brief_item(expansion["continuation_scope"].replace("_", " ").title(), "Continuation scope")
            render_brief_item(expansion["expansion_prep_status"].replace("_", " ").title(), "Expansion prep status")
            render_brief_item(expansion["review_recommendation"].replace("_", " ").title(), "Review recommendation")
            render_panel_end()

            render_panel_start("Approval Boundary")
            render_status_row(
                expansion["expansion_status"].replace("_", " ").title(),
                f"Delivery status: {expansion['delivery_status'].replace('_', ' ').title()}",
                expansion_class,
            )
            render_status_row(
                expansion["next_action"],
                "Executive owner must confirm before any controlled expansion",
                "medium" if expansion["pending_conditions"] else decision_class,
            )
            render_panel_end()

            render_panel_start("Decision Options")
            if expansion["decision_options"]:
                for option in expansion["decision_options"]:
                    render_status_row(option.replace("_", " ").title(), "Allowed decision label", "medium")
            else:
                render_status_row("No decision options found", "Generate the expansion decision artifact", "medium")
            render_panel_end()

        render_panel_start("Boundaries")
        if expansion["boundaries"]:
            for boundary in expansion["boundaries"]:
                render_status_row(boundary, "Protected expansion boundary", "medium")
        else:
            render_status_row("No boundaries found", "Generate the expansion decision artifact", "medium")
        render_panel_end()

        render_panel_start("Operator Note")
        render_brief_item(expansion["operator_note"], "Read-only guidance; no automatic expansion approval")
        render_panel_end()
    elif page == "Demo Readiness":
        demo = data["private_demo_dry_run_status"]
        overall_status = demo["overall_status"]
        overall_class = {
            "ready_for_private_demo": "green",
            "ready_with_warnings": "gold",
            "blocked": "red",
            "missing": "red",
        }.get(overall_status, "gold")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Demo Status", overall_status.replace("_", " ").title(), "Latest private demo dry run", overall_class)
        with c2:
            render_metric_card("Passed", demo["passed_checks"], "Dry-run controls passing", "green")
        with c3:
            render_metric_card("Warnings", demo["warning_checks"], "Name before demo", "gold" if demo["warning_checks"] else "green")
        with c4:
            render_metric_card("Failed", demo["failed_checks"], "Blocks presentation", "red" if demo["failed_checks"] else "green")
        with c5:
            render_metric_card("Segments", len(demo["run_sequence"]), "Operator run sequence", "")

        status_filter = st.selectbox(
            "Demo check status filter",
            ["all", "passed", "warning", "failed"],
            index=0,
        )
        filtered_checks = [
            check
            for check in demo["checks"]
            if status_filter == "all" or check["status"] == status_filter
        ]

        status_styles = {
            "passed": "healthy",
            "warning": "medium",
            "failed": "high",
        }

        left, right = st.columns([1.6, 1])

        with left:
            render_panel_start("Private Demo Checks")
            if filtered_checks:
                for check in filtered_checks:
                    detail = f"{check['severity']} | {check['detail']}"
                    render_status_row(
                        check["name"],
                        detail,
                        status_styles.get(check["status"], check["status"]),
                    )
            else:
                render_status_row("No demo checks found", "Run python cli.py private-demo-dry-run", "medium")
            render_panel_end()

            render_panel_start("Demo Run Sequence")
            if demo["run_sequence"]:
                for index, step in enumerate(demo["run_sequence"], start=1):
                    render_status_row(f"Step {index}", step, "healthy")
            else:
                render_status_row("No run sequence found", "Generate the private demo dry-run report", "medium")
            render_panel_end()

        with right:
            render_panel_start("Demo Evidence")
            render_brief_item(
                demo["report_path"] or "Private demo dry-run report not generated",
                "Latest dry-run evidence artifact",
            )
            render_brief_item(
                demo["package_path"] or "Private demo package not generated",
                "Package with demo scope, commands, and boundaries",
            )
            render_brief_item(
                demo["script_path"] or "Private demo script not generated",
                "Operator script and presentation arc",
            )
            render_brief_item(
                demo["release_readiness_source"].replace("_", " ").title(),
                "Release readiness source used by the dry run",
            )
            render_panel_end()

            render_panel_start("Available Demo Pages")
            if demo["dashboard_pages"]:
                for page_name in demo["dashboard_pages"]:
                    render_status_row(page_name, "Available in private demo scope", "healthy")
            else:
                render_status_row("No pages found", "Run python cli.py private-demo-dry-run", "medium")
            render_panel_end()
    elif page == "People":
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Total Users", data["total_people"], "Registered internal users", "")
        with c2:
            render_metric_card("Active Users", data["active_people"], "Currently enabled", "green")
        with c3:
            render_metric_card("Admin Users", data["admin_people"], "Maximum access level", "red")
        with c4:
            render_metric_card("Managers", data["manager_people"], "Department leadership", "gold")

        left, right = st.columns([1.5, 1])

        with left:
            render_panel_start("People Directory")
            if data["people_users"]:
                for user in data["people_users"]:
                    render_status_row(
                        user["full_name"],
                        f"{user['department']} | {user['role']} | {user['email']}",
                        user["access_level"],
                    )
            else:
                render_status_row("No users found", "People directory has not been initialized", "healthy")
            render_panel_end()

        with right:
            render_panel_start("People Brief")
            render_brief_item(
                f"{data['active_people']} active user(s)",
                "BusinessOS has an initialized internal user layer",
            )
            render_brief_item(
                f"{data['admin_people']} admin user(s)",
                "Admin coverage protects institutional control",
            )
            render_brief_item(
                f"{data['manager_people']} manager user(s)",
                "Managers are ready for routing, approvals, and ownership",
            )
            render_panel_end()

    elif page == "Sensitivity":
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Sensitive Findings", data["sensitive_findings"], "Signals requiring institutional control", "gold")
        with c2:
            render_metric_card("High Sensitivity", data["high_sensitivity_findings"], "Needs executive attention", "red")
        with c3:
            render_metric_card("Medium Sensitivity", data["medium_sensitivity_findings"], "Needs owner review", "gold")
        with c4:
            render_metric_card("Highest Risk", data["highest_sensitivity_risk"], "Governance sensitivity level", "red" if data["highest_sensitivity_risk"] == "High" else "gold")

        left, right = st.columns([1.55, 1])

        with left:
            render_panel_start("Sensitivity Findings")
            if data["sensitivity_findings"]:
                for finding in data["sensitivity_findings"][:8]:
                    render_status_row(
                        finding["message"],
                        f"{finding['source']} | {finding['finding_type']}",
                        finding["severity"],
                    )
            else:
                render_status_row("No sensitive findings", "Governance sensitivity controls are clear", "healthy")
            render_panel_end()

        with right:
            render_panel_start("Sensitivity Brief")
            render_brief_item(
                f"{data['sensitive_findings']} sensitive finding(s)",
                "BusinessOS is actively classifying institutional sensitivity",
            )
            render_brief_item(
                f"{data['high_sensitivity_findings']} high-sensitivity finding(s)",
                "High findings should be reviewed before dependent actions proceed",
            )
            render_brief_item(
                data["sensitivity_next_move"],
                "Recommended governance sensitivity move",
            )
            render_panel_end()

def main():
    st.set_page_config(
        page_title="BusinessOS Command Center",
        page_icon="B",
        layout="wide",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    if not st.session_state.get("authenticated"):
        render_login()

    page = render_sidebar()
    data = load_dashboard_data()

    if page == "Dashboard":
        render_dashboard(data)
    else:
        render_module_page(page, data)


if __name__ == "__main__":
    main()

















