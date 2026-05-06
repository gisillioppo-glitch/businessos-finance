import json
import uuid
from datetime import datetime


def write_audit_log(conn, event_type, severity, message, metadata=None):
    metadata_json = json.dumps(metadata or {})

    conn.execute(
        """
        INSERT INTO audit_logs (
            id,
            timestamp,
            event_type,
            severity,
            message,
            metadata
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            str(uuid.uuid4()),
            datetime.now().isoformat(),
            event_type,
            severity,
            message,
            metadata_json,
        ),
    )
    conn.commit()
