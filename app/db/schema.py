def create_transactions_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,
        date TEXT NOT NULL,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        created_at TEXT NOT NULL
    )
    """
    conn.execute(query)
    conn.commit()


def create_audit_logs_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS audit_logs (
        id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        event_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        message TEXT NOT NULL,
        metadata TEXT
    )
    """
    conn.execute(query)
    conn.commit()


def create_recommended_actions_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS recommended_actions (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        risk_type TEXT NOT NULL,
        risk_severity TEXT NOT NULL,
        recommended_action TEXT NOT NULL,
        owner_role TEXT NOT NULL,
        priority TEXT NOT NULL,
        deadline_days INTEGER NOT NULL,
        status TEXT NOT NULL,        status_justification TEXT

    )
    """
    
    conn.execute(query)
    columns = [
        row[1]
        for row in conn.execute("PRAGMA table_info(recommended_actions)").fetchall()
    ]

    if "status_justification" not in columns:
        conn.execute(
            "ALTER TABLE recommended_actions ADD COLUMN status_justification TEXT"
        )

    conn.commit()
