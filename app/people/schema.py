def create_business_users_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS business_users (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        role TEXT NOT NULL,
        department TEXT NOT NULL,
        manager_id TEXT,
        status TEXT NOT NULL,
        access_level TEXT NOT NULL,
        source_module TEXT,
        source_reference_id TEXT
    )
    """
    conn.execute(query)
    conn.commit()
