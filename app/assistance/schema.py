def create_assistance_requests_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS assistance_requests (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        request_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        requester_email TEXT,
        requester_role TEXT,
        owner_role TEXT NOT NULL,
        status TEXT NOT NULL,
        status_justification TEXT,
        source_module TEXT,
        source_reference_id TEXT
    )
    """
    conn.execute(query)
    conn.commit()
