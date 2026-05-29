import csv
import hashlib
import sqlite3
from datetime import datetime


def create_transaction_hash(row):
    raw_value = (
        f"{row['date'].strftime('%Y-%m-%d')}|"
        f"{row['type']}|"
        f"{row['category']}|"
        f"{row['amount']}|"
        f"{row['description']}"
    )
    return hashlib.sha256(raw_value.encode("utf-8")).hexdigest()


def load_csv(path):
    required_columns = {"date", "type", "category", "amount", "description"}

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing_columns = required_columns - set(reader.fieldnames or [])

        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        rows = []

        for row in reader:
            normalized = {
                "date": datetime.fromisoformat(row["date"].strip()),
                "type": row["type"].lower().strip(),
                "category": row["category"].lower().strip(),
                "amount": float(row["amount"]),
                "description": (row.get("description") or "").strip(),
            }
            normalized["id"] = create_transaction_hash(normalized)
            rows.append(normalized)

    return rows


def insert_transactions(conn, rows):
    inserted_count = 0
    skipped_count = 0

    try:
        for row in rows:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO transactions (
                    id,
                    date,
                    type,
                    category,
                    amount,
                    description,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["id"],
                    row["date"].strftime("%Y-%m-%d"),
                    row["type"],
                    row["category"],
                    row["amount"],
                    row["description"],
                    datetime.now().isoformat(),
                ),
            )

            if cursor.rowcount == 1:
                inserted_count += 1
            else:
                skipped_count += 1

        conn.commit()

    except sqlite3.Error:
        conn.rollback()
        raise

    return inserted_count, skipped_count
