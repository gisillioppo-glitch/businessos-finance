import os
import sqlite3

DB_PATH = "finance.db"
REPORTS_PATH = "reports"


def count_rows(conn, table_name):
    return conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]


def main():
    print("BusinessOS Finance Health Check")

    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)

    try:
        transaction_count = count_rows(conn, "transactions")
        audit_log_count = count_rows(conn, "audit_logs")
        action_count = count_rows(conn, "recommended_actions")

        print(f"Transactions: {transaction_count}")
        print(f"Audit logs: {audit_log_count}")
        print(f"Recommended actions: {action_count}")

        action_rows = conn.execute(
            """
            SELECT status, COUNT(*)
            FROM recommended_actions
            GROUP BY status
            ORDER BY status
            """
        ).fetchall()

        if action_rows:
            print("Actions by status:")
            for status, count in action_rows:
                print(f"- {status}: {count}")
        else:
            print("Actions by status: none")

        if os.path.exists(REPORTS_PATH):
            report_files = [
                file_name
                for file_name in os.listdir(REPORTS_PATH)
                if file_name.endswith(".md")
            ]
            report_files.sort(reverse=True)

            print(f"Reports: {len(report_files)}")

            if report_files:
                print(f"Latest report: {os.path.join(REPORTS_PATH, report_files[0])}")
        else:
            print("Reports: 0")

        print("Health check completed.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
