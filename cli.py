import argparse
import sqlite3

from app.actions.action_views import (
    print_action_summary_kpis,
    print_recommended_actions_list,
)
from app.db.connection import create_connection
from app.governance.findings import (
    evaluate_governance_findings,
    print_governance_kpis,
)
from app.governance.governance_brief import print_governance_brief
from app.governance.governance_report import export_governance_report
from app.operations.escalation_rules import evaluate_operations_escalation_rules
from app.operations.operations_brief import print_operations_brief
from app.operations.task_views import (
    print_operations_task_summary_kpis,
    print_operations_tasks_list,
)
from app.reports.report_history import print_report_history
from app.support.incident_views import (
    print_support_incident_summary_kpis,
    print_support_incidents_list,
)
from app.support.support_brief import print_support_brief
from app.support.support_report import export_support_report
from main import main as run_main
from scripts.health_check import main as run_health_check


def run_actions():
    conn = create_connection()

    try:
        print_recommended_actions_list(conn)
        print_action_summary_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_reports():
    conn = create_connection()

    try:
        print_report_history(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_ops_tasks():
    conn = create_connection()

    try:
        print_operations_tasks_list(conn)
        print_operations_task_summary_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_ops_escalations():
    conn = create_connection()

    try:
        evaluate_operations_escalation_rules(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_ops_brief():
    conn = create_connection()

    try:
        task_kpis = print_operations_task_summary_kpis(conn)
        escalations = evaluate_operations_escalation_rules(conn)
        print_operations_brief(conn, task_kpis, escalations)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_gov_findings():
    conn = create_connection()

    try:
        evaluate_governance_findings(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_gov_kpis():
    conn = create_connection()

    try:
        print_governance_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_gov_brief():
    conn = create_connection()

    try:
        findings = evaluate_governance_findings(conn)
        print_governance_brief(conn, findings)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_gov_report():
    conn = create_connection()

    try:
        findings = evaluate_governance_findings(conn)
        governance_brief = print_governance_brief(conn, findings)
        export_governance_report(conn, governance_brief)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_support_incidents():
    conn = create_connection()

    try:
        print_support_incidents_list(conn)
        print_support_incident_summary_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_support_brief():
    conn = create_connection()

    try:
        incident_kpis = print_support_incident_summary_kpis(conn)
        print_support_brief(conn, incident_kpis)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_support_report():
    conn = create_connection()

    try:
        incident_kpis = print_support_incident_summary_kpis(conn)
        support_brief = print_support_brief(conn, incident_kpis)
        export_support_report(conn, support_brief)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="BusinessOS CLI"
    )

    parser.add_argument(
        "command",
        choices=[
            "run",
            "health",
            "actions",
            "reports",
            "ops-tasks",
            "ops-escalations",
            "ops-brief",
            "gov-findings",
            "gov-kpis",
            "gov-brief",
            "gov-report",
            "support-incidents",
            "support-brief",
            "support-report",
        ],
        help="Command to execute.",
    )

    args = parser.parse_args()

    if args.command == "run":
        run_main()
    elif args.command == "health":
        run_health_check()
    elif args.command == "actions":
        run_actions()
    elif args.command == "reports":
        run_reports()
    elif args.command == "ops-tasks":
        run_ops_tasks()
    elif args.command == "ops-escalations":
        run_ops_escalations()
    elif args.command == "ops-brief":
        run_ops_brief()
    elif args.command == "gov-findings":
        run_gov_findings()
    elif args.command == "gov-kpis":
        run_gov_kpis()
    elif args.command == "gov-brief":
        run_gov_brief()
    elif args.command == "gov-report":
        run_gov_report()
    elif args.command == "support-incidents":
        run_support_incidents()
    elif args.command == "support-brief":
        run_support_brief()
    elif args.command == "support-report":
        run_support_report()


if __name__ == "__main__":
    main()
