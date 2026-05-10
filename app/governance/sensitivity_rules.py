import json

from app.audit.audit_log import write_audit_log


SENSITIVE_APPROVAL_TYPES = {"decision", "access", "budget", "policy", "incident"}
SENSITIVE_REQUEST_TYPES = {"approval", "access", "decision", "incident"}
SENSITIVE_MODULES = {"governance", "approvals", "security"}
PRIVILEGED_ACCESS_LEVELS = {"admin", "executive"}
HIGH_RISK_LEVELS = {"high", "critical"}


def _add_finding(findings, finding_type, severity, source, message, metadata):
    findings.append(
        {
            "finding_type": finding_type,
            "severity": severity,
            "source": source,
            "message": message,
            "metadata": metadata,
        }
    )


def get_governance_sensitivity_findings(conn):
    findings = []

    approval_rows = conn.execute(
        """
        SELECT id, title, approval_type, priority, status, approver_role
        FROM approval_requests
        WHERE status = 'pending'
        """
    ).fetchall()

    for approval_id, title, approval_type, priority, status, approver_role in approval_rows:
        if approval_type in SENSITIVE_APPROVAL_TYPES or priority in HIGH_RISK_LEVELS:
            severity = "high" if priority in HIGH_RISK_LEVELS else "medium"
            _add_finding(
                findings,
                "approval_required",
                severity,
                "approval_requests",
                f"Approval required: {title}",
                {
                    "approval_id": approval_id,
                    "approval_type": approval_type,
                    "priority": priority,
                    "status": status,
                    "approver_role": approver_role,
                },
            )

    assistance_rows = conn.execute(
        """
        SELECT id, title, request_type, severity, status, owner_role
        FROM assistance_requests
        WHERE status IN ('open', 'triaged', 'waiting_approval', 'in_progress')
        """
    ).fetchall()

    for request_id, title, request_type, request_severity, status, owner_role in assistance_rows:
        if request_type in SENSITIVE_REQUEST_TYPES or request_severity in HIGH_RISK_LEVELS:
            severity = "high" if request_severity in HIGH_RISK_LEVELS else "medium"
            _add_finding(
                findings,
                "sensitive_assistance_request",
                severity,
                "assistance_requests",
                f"Sensitive assistance request detected: {title}",
                {
                    "request_id": request_id,
                    "request_type": request_type,
                    "request_severity": request_severity,
                    "status": status,
                    "owner_role": owner_role,
                },
            )

    privileged_user_rows = conn.execute(
        """
        SELECT id, full_name, email, role, department, access_level, status
        FROM business_users
        WHERE status = 'active'
          AND access_level IN ('admin', 'executive')
        """
    ).fetchall()

    for user_id, full_name, email, role, department, access_level, status in privileged_user_rows:
        _add_finding(
            findings,
            "privileged_access_detected",
            "medium",
            "business_users",
            f"Privileged access detected: {full_name}",
            {
                "user_id": user_id,
                "full_name": full_name,
                "email": email,
                "role": role,
                "department": department,
                "access_level": access_level,
                "status": status,
            },
        )

    overdue_task_rows = conn.execute(
        """
        SELECT id, title, priority, status, owner_role, deadline_date
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
          AND deadline_date IS NOT NULL
          AND deadline_date < date('now')
        """
    ).fetchall()

    for task_id, title, priority, status, owner_role, deadline_date in overdue_task_rows:
        severity = "high" if priority in {"high", "critical", "medium"} else "medium"
        _add_finding(
            findings,
            "overdue_sensitive_operation",
            severity,
            "operations_tasks",
            f"Overdue sensitive operation detected: {title}",
            {
                "task_id": task_id,
                "priority": priority,
                "status": status,
                "owner_role": owner_role,
                "deadline_date": deadline_date,
            },
        )

    support_rows = conn.execute(
        """
        SELECT id, title, severity, status, owner_role
        FROM support_incidents
        WHERE status IN ('open', 'investigating', 'waiting')
          AND severity IN ('high', 'critical')
        """
    ).fetchall()

    for incident_id, title, severity, status, owner_role in support_rows:
        _add_finding(
            findings,
            "high_risk_support_incident",
            "high",
            "support_incidents",
            f"High-risk support incident detected: {title}",
            {
                "incident_id": incident_id,
                "incident_severity": severity,
                "status": status,
                "owner_role": owner_role,
            },
        )

    audit_rows = conn.execute(
        """
        SELECT timestamp, event_type, severity, message, metadata
        FROM audit_logs
        ORDER BY timestamp DESC
        LIMIT 200
        """
    ).fetchall()

    for timestamp, event_type, audit_severity, message, metadata_json in audit_rows:
        metadata = {}

        if metadata_json:
            try:
                metadata = json.loads(metadata_json)
            except json.JSONDecodeError:
                metadata = {}

        if audit_severity in {"error", "critical"}:
            _add_finding(
                findings,
                "critical_audit_event",
                "high",
                "audit_logs",
                f"Critical audit event detected: {message}",
                {
                    "timestamp": timestamp,
                    "event_type": event_type,
                    "audit_severity": audit_severity,
                    "metadata": metadata,
                },
            )

        if event_type.endswith("status_updated") and not metadata.get("justification"):
            _add_finding(
                findings,
                "missing_sensitive_justification",
                "medium",
                "audit_logs",
                "Sensitive status update missing justification.",
                {
                    "timestamp": timestamp,
                    "event_type": event_type,
                    "audit_severity": audit_severity,
                    "metadata": metadata,
                },
            )

    return findings


def evaluate_governance_sensitivity_rules(conn):
    findings = get_governance_sensitivity_findings(conn)

    if not findings:
        print("Governance Sensitivity Rules: No sensitive governance signals detected.")
        write_audit_log(
            conn,
            "governance_sensitivity_evaluated",
            "info",
            "Governance sensitivity rules evaluated with no findings detected.",
            {"sensitive_findings_found": 0},
        )
        return []

    print("Governance Sensitivity Rules:")

    for finding in findings:
        print(
            f"[{finding['severity'].upper()}] "
            f"{finding['finding_type']} | "
            f"{finding['source']} | "
            f"{finding['message']}"
        )

        write_audit_log(
            conn,
            "governance_sensitivity_detected",
            finding["severity"],
            finding["message"],
            finding,
        )

    write_audit_log(
        conn,
        "governance_sensitivity_evaluated",
        "info",
        "Governance sensitivity rules evaluated.",
        {"sensitive_findings_found": len(findings)},
    )

    return findings


def print_governance_sensitivity_brief(conn, findings=None):
    if findings is None:
        findings = evaluate_governance_sensitivity_rules(conn)

    high_findings = 0
    medium_findings = 0

    for finding in findings:
        if finding["severity"] == "high":
            high_findings += 1
        elif finding["severity"] == "medium":
            medium_findings += 1

    if high_findings > 0:
        highest_sensitivity_risk = "high"
        next_best_move = "Review high-sensitivity findings and confirm approvals before execution."
    elif medium_findings > 0:
        highest_sensitivity_risk = "medium"
        next_best_move = "Review medium-sensitivity findings and confirm ownership."
    else:
        highest_sensitivity_risk = "low"
        next_best_move = "Maintain current governance sensitivity controls."

    brief = {
        "sensitive_findings": len(findings),
        "high_findings": high_findings,
        "medium_findings": medium_findings,
        "highest_sensitivity_risk": highest_sensitivity_risk,
        "next_best_move": next_best_move,
    }

    print("Governance Sensitivity Brief:")
    print(f"Sensitive findings: {brief['sensitive_findings']}")
    print(f"High sensitivity findings: {brief['high_findings']}")
    print(f"Medium sensitivity findings: {brief['medium_findings']}")
    print(f"Highest sensitivity risk: {brief['highest_sensitivity_risk']}")
    print(f"Next best sensitivity move: {brief['next_best_move']}")

    write_audit_log(
        conn,
        "governance_sensitivity_brief_viewed",
        "info",
        "Governance sensitivity brief viewed.",
        brief,
    )

    return brief

