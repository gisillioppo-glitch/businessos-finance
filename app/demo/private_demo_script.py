from datetime import date
from pathlib import Path

from app.audit.audit_log import write_audit_log
from app.demo.private_demo_package import DASHBOARD_PAGES, PRE_DEMO_CHECKLIST
from app.readiness.release_readiness import generate_release_readiness


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

DEMO_ARC = [
    {
        "segment": "Opening",
        "timebox": "2 min",
        "screen": "Public landing / product positioning",
        "talk_track": "BusinessOS is a private institutional AI operating system for leaders who need one protected view across finance, operations, governance, support, decisions, and daily close.",
        "proof": "Show public landing only as product surface, not private internals.",
    },
    {
        "segment": "Private Command Center",
        "timebox": "4 min",
        "screen": "Dashboard",
        "talk_track": "This is the executive command layer. The system synthesizes operational signals and turns fragmented module data into next-best executive moves.",
        "proof": "Show overall health, risk, executive brief, module snapshot.",
    },
    {
        "segment": "Operating Modules",
        "timebox": "6 min",
        "screen": "Finance, Operations, Governance, Support",
        "talk_track": "The value is not one module. The value is the connected operating loop: finance creates signals, operations turns them into work, governance controls sensitivity, and support manages incidents.",
        "proof": "Show each page briefly; avoid deep raw data.",
    },
    {
        "segment": "Human Control Layer",
        "timebox": "5 min",
        "screen": "Assistance, Approvals, People, Sensitivity",
        "talk_track": "BusinessOS keeps humans in control. It routes help, approvals, access and sensitive findings instead of letting automation bypass institutional governance.",
        "proof": "Show approval queue, people access layer, sensitivity rules.",
    },
    {
        "segment": "Daily Close and Evidence",
        "timebox": "6 min",
        "screen": "Daily Close, Notifications, Scheduled Close",
        "talk_track": "At the end of the day, the system closes the loop: it gathers evidence, prepares executive distribution, queues notifications, and tracks what happened to those messages.",
        "proof": "Show daily close status, notification statuses, scheduled close page.",
    },
    {
        "segment": "Trust and Readiness",
        "timebox": "4 min",
        "screen": "System Integrity, Release Readiness",
        "talk_track": "Before presenting or operating, BusinessOS can check itself. This is what makes the product feel like an operating system instead of a dashboard.",
        "proof": "Show system-check and release-readiness reports/pages.",
    },
    {
        "segment": "Close",
        "timebox": "3 min",
        "screen": "Dashboard / Command Center",
        "talk_track": "The promise is simple: fewer fragmented tools, better executive visibility, safer decisions, and daily operating rhythm with evidence.",
        "proof": "Ask what workflow they would want BusinessOS to close first in their organization.",
    },
]

DEMO_COMMANDS = [
    ("Pre-demo readiness", "python cli.py release-readiness"),
    ("System health", "python cli.py system-check"),
    ("Daily close", "python cli.py daily-close"),
    ("Notification outbox", "python cli.py notifications"),
    ("Private dashboard", "streamlit run app/dashboard/main.py"),
]

DO_NOT_SHOW = [
    "finance.db raw contents.",
    ".env, credentials, tokens, local secrets, Streamlit secrets.",
    "Private implementation internals unless explicitly requested in a technical review.",
    "Untracked local artifacts such as BussinessOS Avance.pdf.",
    "Real external email sending as if production-ready; keep it positioned as protected/dry-run unless configured.",
]

CLOSING_QUESTIONS = [
    "Which daily executive process would you want automated first?",
    "Who needs to receive the daily close in your organization?",
    "Which actions should always require approval before execution?",
    "What would make this trustworthy enough for a private pilot?",
]

KNOWN_RISKS = [
    "Dashboard auth is still local MVP auth and should remain private.",
    "Email delivery is protected and should stay disabled/dry-run until credentials and approvals are configured.",
    "The data set is demo-scale, not production-scale.",
    "Release readiness may show warnings during active development blocks before commit.",
]


def _format_arc_rows():
    rows = [
        "| Segment | Timebox | Screen | Talk Track | Proof |",
        "| --- | --- | --- | --- | --- |",
    ]

    for item in DEMO_ARC:
        rows.append(
            f"| {item['segment']} | {item['timebox']} | {item['screen']} | {item['talk_track']} | {item['proof']} |"
        )

    return "\n".join(rows)


def _format_bullets(items):
    return "\n".join(f"- {item}" for item in items)


def _format_commands(commands):
    rows = [
        "| Purpose | Command |",
        "| --- | --- |",
    ]

    for purpose, command in commands:
        rows.append(f"| {purpose} | `{command}` |")

    return "\n".join(rows)


def generate_private_demo_script():
    readiness = generate_release_readiness()

    return {
        "date": date.today().isoformat(),
        "readiness": readiness,
        "demo_arc": DEMO_ARC,
        "dashboard_pages": DASHBOARD_PAGES,
        "demo_commands": DEMO_COMMANDS,
        "do_not_show": DO_NOT_SHOW,
        "closing_questions": CLOSING_QUESTIONS,
        "known_risks": KNOWN_RISKS,
        "pre_demo_checklist": PRE_DEMO_CHECKLIST,
    }


def export_private_demo_script(conn=None):
    REPORTS_DIR.mkdir(exist_ok=True)
    script = generate_private_demo_script()
    readiness = script["readiness"]
    report_path = REPORTS_DIR / f"private_demo_script_{script['date']}.md"

    content = f"""# Private Demo Script / Sketch MVP v0.1

Date: {script['date']}

## Demo Purpose

Present BusinessOS as a private institutional AI operating system that helps leaders see, close, and govern daily operations from one protected command layer.

## Readiness Context

Release readiness: {readiness['overall_status']}  
Passed checks: {readiness['passed_checks']}  
Warning checks: {readiness['warning_checks']}  
Failed checks: {readiness['failed_checks']}  

## Pre-Demo Checklist

{_format_bullets(script['pre_demo_checklist'])}

## Demo Commands

{_format_commands(script['demo_commands'])}

## Demo Arc

{_format_arc_rows()}

## Dashboard Pages Available

{_format_bullets(script['dashboard_pages'])}

## Do Not Show

{_format_bullets(script['do_not_show'])}

## Known Risks To Name Honestly

{_format_bullets(script['known_risks'])}

## Closing Questions

{_format_bullets(script['closing_questions'])}

## Suggested Closing Statement

BusinessOS is not just a dashboard. It is an operating rhythm: detect, prioritize, approve, close the day, package evidence, notify owners, and verify system integrity before the next decision cycle.
"""

    report_path.write_text(content, encoding="utf-8")

    if conn:
        write_audit_log(
            conn,
            "private_demo_script_exported",
            "info" if readiness["overall_status"] != "blocked" else "warning",
            "Private demo script exported.",
            {
                "report_path": str(report_path.relative_to(ROOT_DIR)),
                "readiness_status": readiness["overall_status"],
            },
        )

    return script, str(report_path)


def print_private_demo_script(conn=None):
    script, report_path = export_private_demo_script(conn)
    readiness = script["readiness"]

    print("Private Demo Script:")
    print(f"Date: {script['date']}")
    print(f"Readiness status: {readiness['overall_status']}")
    print(f"Demo segments: {len(script['demo_arc'])}")
    print("Opening screen: Public landing / product positioning")
    print("Primary private screen: Dashboard")
    print(f"Private demo script exported: {Path(report_path).relative_to(ROOT_DIR)}")

    return script
