import argparse
import sqlite3

from app.actions.action_views import (
    print_action_summary_kpis,
    print_recommended_actions_list,
)
from app.approvals.approval_brief import print_approval_brief
from app.approvals.approval_report import export_approval_report
from app.approvals.approval_views import (
    print_approval_request_summary_kpis,
    print_approval_requests_list,
)
from app.approvals.requests import ensure_default_approval_requests
from app.approvals.approval_status import (
    demo_approve_first_pending_approval_request,
    demo_reject_first_pending_approval_request,
)
from app.approvals.schema import create_approval_requests_table
from app.alerts.executive_alerts import (
    print_executive_alerts,
    print_executive_alerts_brief,
)
from app.alerts.executive_alerts_report import export_executive_alerts_report
from app.alerts.alert_status import (
    demo_acknowledge_first_open_executive_alert,
    demo_resolve_first_in_review_executive_alert,
    demo_review_first_acknowledged_executive_alert,
)
from app.assistance.assistance_brief import print_assistance_brief
from app.assistance.request_views import (
    print_assistance_request_summary_kpis,
    print_assistance_requests_list,
)
from app.assistance.requests import ensure_default_assistance_requests
from app.assistance.request_status import demo_triage_first_open_assistance_request
from app.assistance.schema import create_assistance_requests_table
from app.command_center.command_center_brief import print_command_center_brief
from app.command_center.command_center_report import export_command_center_report
from app.command_center.command_center_summary import generate_command_center_summary
from app.db.connection import create_connection
from app.evidence.daily_close import export_daily_close_report
from app.evidence.daily_close_distribution import export_daily_close_distribution
from app.evidence.evidence_index import (
    export_executive_evidence_index,
    get_executive_evidence_index,
)
from app.governance.findings import (
    evaluate_governance_findings,
    print_governance_kpis,
)
from app.governance.governance_brief import print_governance_brief
from app.governance.governance_report import export_governance_report
from app.governance.sensitivity_rules import (
    evaluate_governance_sensitivity_rules,
    print_governance_sensitivity_brief,
)
from app.notifications.outbox import (
    print_notification_outbox,
    print_notification_summary,
)
from app.operations.escalation_rules import evaluate_operations_escalation_rules
from app.people.people_brief import print_people_brief
from app.people.people_views import (
    print_people_list,
    print_people_summary_kpis,
)
from app.people.schema import create_business_users_table
from app.people.users import ensure_default_business_users
from app.operations.operations_brief import print_operations_brief
from app.operations.task_views import (
    print_operations_task_summary_kpis,
    print_operations_tasks_list,
)
from app.reports.report_history import print_report_history
from app.support.incident_views import (
    print_support_incident_summary_kpis,
    print_support_incidents_list,
)
from app.support.support_brief import print_support_brief
from app.support.support_report import export_support_report
from main import main as run_main
from scripts.health_check import main as run_health_check


def run_actions():
    conn = create_connection()

    try:
        print_recommended_actions_list(conn)
        print_action_summary_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_reports():
    conn = create_connection()

    try:
        print_report_history(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_notifications():
    conn = create_connection()

    try:
        print_notification_outbox(conn)
        print_notification_summary(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_ops_tasks():
    conn = create_connection()

    try:
        print_operations_tasks_list(conn)
        print_operations_task_summary_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_ops_escalations():
    conn = create_connection()

    try:
        evaluate_operations_escalation_rules(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_ops_brief():
    conn = create_connection()

    try:
        task_kpis = print_operations_task_summary_kpis(conn)
        escalations = evaluate_operations_escalation_rules(conn)
        print_operations_brief(conn, task_kpis, escalations)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_gov_findings():
    conn = create_connection()

    try:
        evaluate_governance_findings(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_gov_kpis():
    conn = create_connection()

    try:
        print_governance_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_gov_brief():
    conn = create_connection()

    try:
        findings = evaluate_governance_findings(conn)
        print_governance_brief(conn, findings)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_gov_report():
    conn = create_connection()

    try:
        findings = evaluate_governance_findings(conn)
        governance_brief = print_governance_brief(conn, findings)
        export_governance_report(conn, governance_brief)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_gov_sensitivity():
    conn = create_connection()

    try:
        evaluate_governance_sensitivity_rules(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_gov_sensitivity_brief():
    conn = create_connection()

    try:
        findings = evaluate_governance_sensitivity_rules(conn)
        print_governance_sensitivity_brief(conn, findings)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_support_incidents():
    conn = create_connection()

    try:
        print_support_incidents_list(conn)
        print_support_incident_summary_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_support_brief():
    conn = create_connection()

    try:
        incident_kpis = print_support_incident_summary_kpis(conn)
        print_support_brief(conn, incident_kpis)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_support_report():
    conn = create_connection()

    try:
        incident_kpis = print_support_incident_summary_kpis(conn)
        support_brief = print_support_brief(conn, incident_kpis)
        export_support_report(conn, support_brief)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_command_center():
    conn = create_connection()

    try:
        summary = generate_command_center_summary(conn)
        print_command_center_brief(conn, summary)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_command_report():
    conn = create_connection()

    try:
        summary = generate_command_center_summary(conn)
        command_brief = print_command_center_brief(conn, summary)
        export_command_center_report(conn, command_brief)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_people():
    conn = create_connection()

    try:
        create_business_users_table(conn)
        ensure_default_business_users(conn)
        print_people_list(conn)
        print_people_summary_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_people_brief():
    conn = create_connection()

    try:
        create_business_users_table(conn)
        ensure_default_business_users(conn)
        people_kpis = print_people_summary_kpis(conn)
        print_people_brief(conn, people_kpis)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_assistance():
    conn = create_connection()

    try:
        create_assistance_requests_table(conn)
        ensure_default_assistance_requests(conn)
        print_assistance_requests_list(conn)
        print_assistance_request_summary_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_assistance_brief():
    conn = create_connection()

    try:
        create_assistance_requests_table(conn)
        ensure_default_assistance_requests(conn)
        request_kpis = print_assistance_request_summary_kpis(conn)
        print_assistance_brief(conn, request_kpis)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_assistance_status():
    conn = create_connection()

    try:
        create_assistance_requests_table(conn)
        ensure_default_assistance_requests(conn)
        demo_triage_first_open_assistance_request(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_approvals():
    conn = create_connection()

    try:
        create_approval_requests_table(conn)
        ensure_default_approval_requests(conn)
        print_approval_requests_list(conn)
        print_approval_request_summary_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_approval_brief():
    conn = create_connection()

    try:
        create_approval_requests_table(conn)
        ensure_default_approval_requests(conn)
        approval_kpis = print_approval_request_summary_kpis(conn)
        print_approval_brief(conn, approval_kpis)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_approval_report():
    conn = create_connection()

    try:
        create_approval_requests_table(conn)
        ensure_default_approval_requests(conn)
        approval_kpis = print_approval_request_summary_kpis(conn)
        approval_brief = print_approval_brief(conn, approval_kpis)
        export_approval_report(conn, approval_kpis, approval_brief)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_approval_approve():
    conn = create_connection()

    try:
        create_approval_requests_table(conn)
        ensure_default_approval_requests(conn)
        demo_approve_first_pending_approval_request(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_approval_reject():
    conn = create_connection()

    try:
        create_approval_requests_table(conn)
        ensure_default_approval_requests(conn)
        demo_reject_first_pending_approval_request(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_daily_close():
    print("Executive Daily Close started.")

    close_steps = []

    run_main()
    close_steps.append({"name": "Daily Finance Brief", "status": "completed", "detail": "Finance run and daily brief generated."})

    run_gov_report()
    close_steps.append({"name": "Governance Brief", "status": "completed", "detail": "Governance report generated."})

    run_support_report()
    close_steps.append({"name": "Support Brief", "status": "completed", "detail": "Support report generated."})

    run_command_report()
    close_steps.append({"name": "Command Center", "status": "completed", "detail": "Command Center report generated."})

    run_approval_report()
    close_steps.append({"name": "Approval Decisions", "status": "completed", "detail": "Approval decision report generated."})

    run_executive_alerts_report()
    close_steps.append({"name": "Executive Alerts", "status": "completed", "detail": "Executive Alerts report generated."})

    conn = create_connection()

    try:
        export_executive_evidence_index(conn)
        evidence_index = get_executive_evidence_index()
        close_steps.append({"name": "Evidence Index", "status": "completed", "detail": "Executive evidence index generated."})
        export_daily_close_report(conn, close_steps, evidence_index)
        export_daily_close_distribution(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

    print("Executive Daily Close completed.")

def run_evidence_index():
    conn = create_connection()

    try:
        export_executive_evidence_index(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_daily_close_distribution():
    conn = create_connection()

    try:
        export_daily_close_distribution(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_executive_alerts():
    conn = create_connection()

    try:
        print_executive_alerts(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_executive_alerts_brief():
    conn = create_connection()

    try:
        alerts = print_executive_alerts(conn)
        print_executive_alerts_brief(conn, alerts)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_executive_alert_status():
    conn = create_connection()

    try:
        demo_acknowledge_first_open_executive_alert(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_executive_alert_review():
    conn = create_connection()

    try:
        demo_review_first_acknowledged_executive_alert(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_executive_alert_resolve():
    conn = create_connection()

    try:
        demo_resolve_first_in_review_executive_alert(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()
def run_executive_alerts_report():
    conn = create_connection()

    try:
        alerts = print_executive_alerts(conn)
        alert_brief = print_executive_alerts_brief(conn, alerts)
        export_executive_alerts_report(conn, alerts, alert_brief)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()
def main():
    parser = argparse.ArgumentParser(
        description="BusinessOS CLI"
    )

    parser.add_argument(
        "command",
        choices=[
            "run",
            "health",
            "actions",
            "reports",
            "notifications",
            "ops-tasks",
            "ops-escalations",
            "ops-brief",
            "gov-findings",
            "gov-kpis",
            "gov-brief",
            "gov-report",
            "gov-sensitivity",
            "gov-sensitivity-brief",
            "support-incidents",
            "support-brief",
            "support-report",
            "command-center",
            "command-report",
            "people",
            "people-brief",
            "assistance",
            "assistance-brief",
            "assistance-status",
            "approvals",
            "approval-brief",
            "approval-report",
            "approval-approve",
            "approval-reject",
            "evidence-index",
            "daily-close",
            "daily-close-distribution",
            "executive-alerts",
            "executive-alerts-brief",
            "executive-alerts-report",
            "executive-alert-status",
            "executive-alert-review",
            "executive-alert-resolve",
        ],
        help="Command to execute.",
    )

    args = parser.parse_args()

    if args.command == "run":
        run_main()
    elif args.command == "health":
        run_health_check()
    elif args.command == "actions":
        run_actions()
    elif args.command == "reports":
        run_reports()
    elif args.command == "notifications":
        run_notifications()
    elif args.command == "ops-tasks":
        run_ops_tasks()
    elif args.command == "ops-escalations":
        run_ops_escalations()
    elif args.command == "ops-brief":
        run_ops_brief()
    elif args.command == "gov-findings":
        run_gov_findings()
    elif args.command == "gov-kpis":
        run_gov_kpis()
    elif args.command == "gov-brief":
        run_gov_brief()
    elif args.command == "gov-report":
        run_gov_report()
    elif args.command == "gov-sensitivity":
        run_gov_sensitivity()
    elif args.command == "gov-sensitivity-brief":
        run_gov_sensitivity_brief()
    elif args.command == "support-incidents":
        run_support_incidents()
    elif args.command == "support-brief":
        run_support_brief()
    elif args.command == "support-report":
        run_support_report()
    elif args.command == "command-center":
        run_command_center()
    elif args.command == "command-report":
        run_command_report()
    elif args.command == "people":
        run_people()
    elif args.command == "people-brief":
        run_people_brief()
    elif args.command == "assistance":
        run_assistance()
    elif args.command == "assistance-brief":
        run_assistance_brief()
    elif args.command == "assistance-status":
        run_assistance_status()
    elif args.command == "approvals":
        run_approvals()
    elif args.command == "approval-brief":
        run_approval_brief()
    elif args.command == "approval-report":
        run_approval_report()
    elif args.command == "approval-approve":
        run_approval_approve()
    elif args.command == "approval-reject":
        run_approval_reject()
    elif args.command == "evidence-index":
        run_evidence_index()
    elif args.command == "daily-close":
        run_daily_close()
    elif args.command == "daily-close-distribution":
        run_daily_close_distribution()
    elif args.command == "executive-alerts":
        run_executive_alerts()
    elif args.command == "executive-alerts-brief":
        run_executive_alerts_brief()
    elif args.command == "executive-alerts-report":
        run_executive_alerts_report()
    elif args.command == "executive-alert-status":
        run_executive_alert_status()
    elif args.command == "executive-alert-review":
        run_executive_alert_review()
    elif args.command == "executive-alert-resolve":
        run_executive_alert_resolve()


if __name__ == "__main__":
    main()
































