import sqlite3

from app.actions.action_status import demo_update_first_open_action
from app.actions.action_views import (
    print_action_summary_kpis,
    print_recommended_actions_list,
)
from app.actions.recommended_actions import generate_recommended_actions
from app.audit.audit_log import write_audit_log
from app.db.connection import DB_PATH, create_connection
from app.db.schema import (
    create_audit_logs_table,
    create_recommended_actions_table,
    create_transactions_table,
)
from app.ingest.csv_loader import insert_transactions, load_csv
from app.operations.schema import create_operations_tasks_table
from app.operations.tasks import create_operations_task
from app.reports.executive_brief import print_daily_executive_brief
from app.reports.report_export import export_daily_brief_report
from app.reports.report_history import print_report_history
from app.rules.anomaly_rules import detect_expense_anomalies
from app.rules.cash_flow import generate_cash_flow_summary
from app.rules.financial_risk_rules import evaluate_financial_risk_rules
from app.support.schema import create_support_incidents_table

CSV_PATH = "data/raw/sample.csv"
DEMO_MODE = False


def main():
    print("Starting BusinessOS Finance Module MVP...")

    conn = create_connection()

    try:
        create_transactions_table(conn)
        create_audit_logs_table(conn)
        create_recommended_actions_table(conn)
        create_operations_tasks_table(conn)
        create_support_incidents_table(conn)

        write_audit_log(
            conn,
            "application_started",
            "info",
            "BusinessOS Finance Module MVP started.",
            {"csv_path": CSV_PATH, "db_path": DB_PATH},
        )

        df = load_csv(CSV_PATH)

        write_audit_log(
            conn,
            "csv_loaded",
            "info",
            "CSV file loaded successfully.",
            {"csv_path": CSV_PATH, "rows_loaded": len(df)},
        )

        inserted_count, skipped_count = insert_transactions(conn, df)

        print(f"Inserted {inserted_count} new transactions into {DB_PATH}.")
        print(f"Skipped {skipped_count} duplicate transactions.")

        write_audit_log(
            conn,
            "transactions_processed",
            "info",
            "Transactions were processed.",
            {
                "inserted_count": inserted_count,
                "skipped_count": skipped_count,
            },
        )

        cash_flow_summary = generate_cash_flow_summary(conn)
        risks = evaluate_financial_risk_rules(conn, cash_flow_summary)
        actions = generate_recommended_actions(conn, risks)
        if actions:
            operations_task = create_operations_task(
                conn,
                "Review finance recommended actions",
                "Review active finance recommended actions and confirm owner progress.",
                "Operations Manager",
                "medium",
                None,
                "finance",
                "recommended_actions",
            )

            if operations_task["was_created"]:
                print(
                    f"Operations Task Created: {operations_task['title']} "
                    f"(Status: {operations_task['status']})"
                )
            else:
                print(
                    f"[SKIPPED] Duplicate operations task already exists "
                    f"(Status: {operations_task['status']}): {operations_task['title']}"
                )


        if DEMO_MODE:
            demo_update_first_open_action(conn)

        print_recommended_actions_list(conn)
        action_kpis = print_action_summary_kpis(conn)
        executive_brief = print_daily_executive_brief(
            conn,
            cash_flow_summary,
            risks,
            action_kpis,
        )
        export_daily_brief_report(conn, executive_brief)
        print_report_history(conn)

        alerts = detect_expense_anomalies(conn)

        write_audit_log(
            conn,
            "application_finished",
            "info",
            "BusinessOS Finance Module MVP finished successfully.",
            {"alerts_generated": len(alerts)},
        )

        print("BusinessOS Finance Module MVP finished successfully.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at {CSV_PATH}.")
        write_audit_log(
            conn,
            "application_error",
            "error",
            "CSV file not found.",
            {"csv_path": CSV_PATH},
        )

    except ValueError as error:
        print(f"Data validation error: {error}")
        write_audit_log(
            conn,
            "application_error",
            "error",
            "CSV validation failed.",
            {"error": str(error)},
        )

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
    