def create_notification_outbox_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS notification_outbox (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        channel TEXT NOT NULL,
        recipient_name TEXT NOT NULL,
        recipient_email TEXT NOT NULL,
        recipient_role TEXT,
        recipient_department TEXT,
        subject TEXT NOT NULL,
        body TEXT NOT NULL,
        status TEXT NOT NULL,
        source_module TEXT NOT NULL,
        source_reference_id TEXT NOT NULL,
        sent_at TEXT
    )
    """
    conn.execute(query)
    conn.commit()
