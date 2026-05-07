import json

from app.audit.audit_log import write_audit_log


def evaluate_governance_findings(conn):
    findings = []

    rows = conn.execute(
        """
        SELECT timestamp, event_type, severity, message, metadata
        FROM audit_logs
        ORDER BY timestamp DESC
        LIMIT 200
        """
    ).fetchall()

    for timestamp, event_type, severity, message, metadata_json in rows:
        metadata = {}

        if metadata_json:
            try:
                metadata = json.loads(metadata_json)
            except json.JSONDecodeError:
                metadata = {}

        if severity in {"error", "critical"}:
            findings.append(
                {
                    "finding_type": "critical_or_error_event",
                    "severity": "high",
                    "timestamp": timestamp,
                    "event_type": event_type,
                    "message": message,
                    "metadata": metadata,
                }
            )

        if event_type in {
            "recommended_action_status_updated",
            "operations_task_status_updated",
        }:
            justification = metadata.get("justification")

            if not justification:
                findings.append(
                    {
                        "finding_type": "status_update_missing_justification",
                        "severity": "medium",
                        "timestamp": timestamp,
                        "event_type": event_type,
                        "message": "Status update missing justification.",
                        "metadata": metadata,
                    }
                )

    if not findings:
        print("Governance Findings: No governance findings detected.")
        write_audit_log(
            conn,
            "governance_findings_evaluated",
            "info",
            "Governance findings evaluated with no findings detected.",
            {"findings_found": 0},
        )
        return []

    print("Governance Findings:")

    for finding in findings:
        print(
            f"[{finding['severity'].upper()}] "
            f"{finding['finding_type']} | "
            f"{finding['event_type']} | "
            f"{finding['message']}"
        )

        write_audit_log(
            conn,
            "governance_finding_detected",
            finding["severity"],
            finding["message"],
            finding,
        )

    write_audit_log(
        conn,
        "governance_findings_evaluated",
        "info",
        "Governance findings evaluated.",
        {"findings_found": len(findings)},
    )

    return findings
