import argparse
import sqlite3

from app.actions.action_views import (
    print_action_summary_kpis,
    print_recommended_actions_list,
)
from app.db.connection import create_connection
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


def main():
    parser = argparse.ArgumentParser(
        description="BusinessOS Finance Module CLI"
    )

    parser.add_argument(
        "command",
        choices=["run", "health", "actions", "reports"],
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


if __name__ == "__main__":
    main()
