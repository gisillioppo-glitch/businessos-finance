from app.audit.audit_log import write_audit_log


def print_governance_brief(conn, findings):
    print("Governance Brief:")
    print(f"Governance findings detected: {len(findings)}")

    if findings:
        highest_governance_risk = (
            "high"
            if any(finding["severity"] == "high" for finding in findings)
            else "medium"
        )
        audit_trail_health = "needs_review"
    else:
        highest_governance_risk = "none"
        audit_trail_health = "healthy"

    print(f"Highest governance risk: {highest_governance_risk}")
    print(f"Audit trail health: {audit_trail_health}")

    if findings:
        next_best_move = "Review governance findings and resolve missing justification or critical audit events."
    else:
        next_best_move = "Maintain current governance controls and continue monitoring audit logs."

    print(f"Next best governance move: {next_best_move}")

    write_audit_log(
        conn,
        "governance_brief_generated",
        "info",
        "Governance brief generated.",
        {
            "findings_detected": len(findings),
            "highest_governance_risk": highest_governance_risk,
            "audit_trail_health": audit_trail_health,
            "next_best_move": next_best_move,
        },
    )

    return {
        "findings_detected": len(findings),
        "highest_governance_risk": highest_governance_risk,
        "audit_trail_health": audit_trail_health,
        "next_best_move": next_best_move,
    }
