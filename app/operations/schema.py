def create_operations_tasks_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS operations_tasks (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        owner_role TEXT NOT NULL,
        priority TEXT NOT NULL,
        deadline_date TEXT,
        status TEXT NOT NULL,
        status_justification TEXT,
        source_module TEXT,
        source_reference_id TEXT
    )
    """
    conn.execute(query)
    conn.commit()
