import argparse
import sqlite3

from app.actions.action_views import (
    print_action_summary_kpis,
    print_recommended_actions_list,
)
from app.db.connection import create_connection
from app.operations.escalation_rules import evaluate_operations_escalation_rules
from app.operations.operations_brief import print_operations_brief
from app.operations.task_views import (
    print_operations_task_summary_kpis,
    print_operations_tasks_list,
)
from app.reports.report_history import print_report_history
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


def main():
    parser = argparse.ArgumentParser(
        description="BusinessOS Finance Module CLI"
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


if __name__ == "__main__":
    main()
