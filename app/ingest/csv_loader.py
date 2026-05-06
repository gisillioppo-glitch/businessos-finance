import hashlib
import sqlite3
from datetime import datetime

import pandas as pd


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
    df = pd.read_csv(path)

    required_columns = {"date", "type", "category", "amount", "description"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["date"] = pd.to_datetime(df["date"])
    df["type"] = df["type"].str.lower().str.strip()
    df["category"] = df["category"].str.lower().str.strip()
    df["amount"] = df["amount"].astype(float)
    df["description"] = df["description"].fillna("").astype(str).str.strip()

    df["id"] = df.apply(create_transaction_hash, axis=1)

    return df


def insert_transactions(conn, df):
    inserted_count = 0
    skipped_count = 0

    try:
        for _, row in df.iterrows():
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
