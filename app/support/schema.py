def create_support_incidents_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS support_incidents (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        severity TEXT NOT NULL,
        owner_role TEXT NOT NULL,
        status TEXT NOT NULL,
        status_justification TEXT,
        source_module TEXT,
        source_reference_id TEXT
    )
    """
    conn.execute(query)
    conn.commit()
