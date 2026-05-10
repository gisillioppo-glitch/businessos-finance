

def create_executive_alert_statuses_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS executive_alert_statuses (
            alert_key TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            status_justification TEXT,
            owner_role TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


VALID_EXECUTIVE_ALERT_STATUSES = {
    "open",
    "acknowledged",
    "in_review",
    "resolved",
    "dismissed",
}

ACTIVE_EXECUTIVE_ALERT_STATUSES = {
    "open",
    "acknowledged",
    "in_review",
}
