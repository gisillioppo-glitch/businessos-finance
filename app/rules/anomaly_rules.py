from app.audit.audit_log import write_audit_log


def calculate_expense_anomaly_severity(amount, average_expense):
    if average_expense <= 0:
        return "info"

    if amount > average_expense * 3.0:
        return "critical"

    if amount > average_expense * 2.0:
        return "high"

    if amount > average_expense * 1.5:
        return "medium"

    if amount > average_expense * 1.2:
        return "low"

    return "info"


def detect_expense_anomalies(conn):
    write_audit_log(
        conn,
        "rule_started",
        "info",
        "Expense anomaly detection rule started.",
        {"rule": "expense_amount_greater_than_1_5x_average"},
    )

    rows = conn.execute(
        """
        SELECT id, date, category, amount
        FROM transactions
        WHERE type = 'expense'
        """
    ).fetchall()

    if not rows:
        write_audit_log(
            conn,
            "rule_finished",
            "info",
            "No expenses found. No anomalies detected.",
            {"anomalies_found": 0},
        )
        print("No expenses found. No anomalies detected.")
        return []

    average_expense = sum(float(row[3]) for row in rows) / len(rows)
    threshold = average_expense * 1.5

    anomalies = [
        {
            "id": row[0],
            "date": row[1],
            "category": row[2],
            "amount": float(row[3]),
        }
        for row in rows
        if float(row[3]) > threshold
    ]

    if not anomalies:
        write_audit_log(
            conn,
            "rule_finished",
            "info",
            "Expense anomaly detection finished with no anomalies.",
            {
                "average_expense": float(average_expense),
                "threshold": float(threshold),
                "anomalies_found": 0,
            },
        )
        print("No expense anomalies detected.")
        return []

    alerts = []

    for row in anomalies:
        severity = calculate_expense_anomaly_severity(
            row["amount"],
            average_expense,
        )

        alert = (
            f"[{severity.upper()}] Anomaly detected: "
            f"${row['amount']:.2f} on {row['date']} "
            f"(category: {row['category']})"
        )

        print(alert)
        alerts.append(alert)

        write_audit_log(
            conn,
            "anomaly_detected",
            severity,
            alert,
            {
                "severity": severity,
                "transaction_id": row["id"],
                "date": row["date"],
                "category": row["category"],
                "amount": float(row["amount"]),
                "average_expense": float(average_expense),
                "threshold": float(threshold),
            },
        )

    write_audit_log(
        conn,
        "rule_finished",
        "info",
        "Expense anomaly detection rule finished.",
        {"anomalies_found": len(alerts)},
    )
    return alerts
