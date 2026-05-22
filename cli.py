import argparse
import sqlite3

from app.actions.action_views import (
    print_action_summary_kpis,
    print_recommended_actions_list,
)
from app.actions.area_review import print_finance_area_review
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
from app.demo.private_demo_package import print_private_demo_package
from app.demo.private_demo_script import print_private_demo_script
from app.demo.private_demo_dry_run import print_private_demo_dry_run
from app.demo.private_demo_final_review import print_private_demo_final_review
from app.demo.private_pilot_intake import print_private_pilot_intake
from app.demo.private_pilot_plan import print_private_pilot_plan
from app.demo.private_pilot_start_gate import print_private_pilot_start_gate
from app.demo.private_pilot_start_confirmation import print_private_pilot_start_confirmation
from app.demo.private_pilot_tracker import print_private_pilot_tracker
from app.demo.private_pilot_exit_decision import print_private_pilot_exit_decision
from app.demo.pilot_day_1_package import print_pilot_day_1_package
from app.demo.pilot_day_2_rhythm import print_pilot_day_2_rhythm
from app.demo.pilot_day_3_evidence_review import print_pilot_day_3_evidence_review
from app.demo.pilot_day_4_owner_confirmation import print_pilot_day_4_owner_confirmation
from app.demo.pilot_day_5_narrow_continuation import print_pilot_day_5_narrow_continuation
from app.demo.pilot_expansion_review_prep import print_pilot_expansion_review_prep
from app.demo.pilot_expansion_review_decision import print_pilot_expansion_review_decision
from app.demo.pilot_owner_confirmation_chain_index import print_pilot_owner_confirmation_chain_index
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
from app.governance.area_review import print_governance_area_review
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
from app.notifications.delivery_approval import print_notification_delivery_approval
from app.notifications.email_delivery import print_secure_email_delivery
from app.notifications.status import (
    demo_dismiss_first_queued_notification,
    demo_fail_first_queued_notification,
    demo_mark_first_queued_notification_sent,
)
from app.operations.escalation_rules import evaluate_operations_escalation_rules
from app.operations.area_review import print_operations_area_review
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
from app.reports.area_review_index import print_area_review_index
from app.reports.area_review_bundle import print_area_review_bundle
from app.reports.report_history import print_report_history
from app.readiness.release_readiness import print_release_readiness
from app.scheduler.scheduled_daily_close import (
    print_scheduled_daily_close_status,
    run_scheduled_daily_close,
)
from app.security.public_surface_publish_checklist import print_public_surface_publish_checklist
from app.security.surface_audit import print_public_private_surface_audit
from app.system.integrity_check import export_system_integrity_report
from app.system.runtime_stability import print_runtime_stability_review
from app.system.session_handoff import print_session_handoff_snapshot
from app.support.incident_views import (
    print_support_incident_summary_kpis,
    print_support_incidents_list,
)
from app.support.area_review import print_support_area_review
from app.support.support_brief import print_support_brief
from app.support.support_report import export_support_report
from main import main as run_main
from scripts.health_check import main as run_health_check


def run_system_check():
    conn = create_connection()

    try:
        export_system_integrity_report(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_actions():
    conn = create_connection()

    try:
        print_recommended_actions_list(conn)
        print_action_summary_kpis(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_finance_area_review():
    conn = create_connection()

    try:
        print_finance_area_review(conn)

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


def run_area_review_index():
    conn = create_connection()

    try:
        print_area_review_index(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_area_review_bundle():
    conn = create_connection()

    try:
        print_area_review_bundle(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_release_readiness():
    conn = create_connection()

    try:
        print_release_readiness(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_public_private_surface_audit():
    conn = create_connection()

    try:
        print_public_private_surface_audit(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_public_surface_publish_checklist():
    conn = create_connection()

    try:
        print_public_surface_publish_checklist(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_private_demo_package():
    conn = create_connection()

    try:
        print_private_demo_package(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_private_demo_script():
    conn = create_connection()

    try:
        print_private_demo_script(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_private_demo_dry_run():
    conn = create_connection()

    try:
        print_private_demo_dry_run(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_private_demo_final_review():
    conn = create_connection()

    try:
        print_private_demo_final_review(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_private_pilot_intake():
    conn = create_connection()

    try:
        print_private_pilot_intake(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_private_pilot_plan():
    conn = create_connection()

    try:
        print_private_pilot_plan(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_private_pilot_start_gate():
    conn = create_connection()

    try:
        print_private_pilot_start_gate(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_private_pilot_start_confirmation():
    conn = create_connection()

    try:
        print_private_pilot_start_confirmation(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_private_pilot_tracker():
    conn = create_connection()

    try:
        print_private_pilot_tracker(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_private_pilot_exit_decision():
    conn = create_connection()

    try:
        print_private_pilot_exit_decision(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_pilot_day_1_package():
    conn = create_connection()

    try:
        print_pilot_day_1_package(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_pilot_day_2_rhythm():
    conn = create_connection()

    try:
        print_pilot_day_2_rhythm(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_pilot_day_3_evidence_review():
    conn = create_connection()

    try:
        print_pilot_day_3_evidence_review(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_runtime_stability():
    conn = create_connection()

    try:
        print_runtime_stability_review(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_session_handoff():
    conn = create_connection()

    try:
        print_session_handoff_snapshot(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_pilot_day_4_owner_confirmation():
    conn = create_connection()

    try:
        print_pilot_day_4_owner_confirmation(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_pilot_day_5_narrow_continuation():
    conn = create_connection()

    try:
        print_pilot_day_5_narrow_continuation(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_pilot_expansion_review_prep():
    conn = create_connection()

    try:
        print_pilot_expansion_review_prep(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_pilot_expansion_review_decision():
    conn = create_connection()

    try:
        print_pilot_expansion_review_decision(conn)

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


def run_notification_delivery_approval():
    conn = create_connection()

    try:
        print_notification_delivery_approval(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_secure_email_delivery():
    conn = create_connection()

    try:
        print_secure_email_delivery(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

def run_notification_sent():
    conn = create_connection()

    try:
        demo_mark_first_queued_notification_sent(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_notification_dismiss():
    conn = create_connection()

    try:
        demo_dismiss_first_queued_notification(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_notification_fail():
    conn = create_connection()

    try:
        demo_fail_first_queued_notification(conn)

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


def run_operations_area_review():
    conn = create_connection()

    try:
        print_operations_area_review(conn)

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


def run_governance_area_review():
    conn = create_connection()

    try:
        print_governance_area_review(conn)

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


def run_support_area_review():
    conn = create_connection()

    try:
        print_support_area_review(conn)

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


def run_daily_close_schedule():
    conn = create_connection()

    try:
        print_scheduled_daily_close_status(conn)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_scheduled_daily_close_command():
    conn = create_connection()

    try:
        run_scheduled_daily_close(conn, run_daily_close)

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


def run_pilot_owner_confirmation_chain_index():
    conn = create_connection()

    try:
        print_pilot_owner_confirmation_chain_index(conn)

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
            "system-check",
            "runtime-stability",
            "session-handoff",
            "actions",
            "finance-area-review",
            "reports",
            "area-review-index",
            "area-review-bundle",
            "release-readiness",
            "public-private-surface-audit",
            "public-surface-publish-checklist",
            "private-demo-package",
            "private-demo-script",
            "private-demo-dry-run",
            "private-demo-final-review",
            "private-pilot-intake",
            "private-pilot-plan",
            "private-pilot-start-gate",
            "private-pilot-start-confirmation",
            "private-pilot-tracker",
            "private-pilot-exit-decision",
            "pilot-day-1-package",
            "pilot-day-2-rhythm",
            "pilot-day-3-evidence-review",
            "pilot-day-4-owner-confirmation",
            "pilot-day-5-narrow-continuation",
            "pilot-expansion-review-prep",
            "pilot-expansion-review-decision",
            "pilot-owner-confirmation-chain",
            "notifications",
            "notification-delivery-approval",
            "secure-email-delivery",
            "notification-sent",
            "notification-dismiss",
            "notification-fail",
            "ops-tasks",
            "ops-escalations",
            "ops-brief",
            "operations-area-review",
            "gov-findings",
            "gov-kpis",
            "gov-brief",
            "gov-report",
            "gov-sensitivity",
            "gov-sensitivity-brief",
            "governance-area-review",
            "support-incidents",
            "support-brief",
            "support-report",
            "support-area-review",
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
            "daily-close-schedule",
            "scheduled-daily-close",
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
    elif args.command == "system-check":
        run_system_check()
    elif args.command == "runtime-stability":
        run_runtime_stability()
    elif args.command == "session-handoff":
        run_session_handoff()
    elif args.command == "actions":
        run_actions()
    elif args.command == "finance-area-review":
        run_finance_area_review()
    elif args.command == "reports":
        run_reports()
    elif args.command == "area-review-index":
        run_area_review_index()
    elif args.command == "area-review-bundle":
        run_area_review_bundle()
    elif args.command == "release-readiness":
        run_release_readiness()
    elif args.command == "public-private-surface-audit":
        run_public_private_surface_audit()
    elif args.command == "public-surface-publish-checklist":
        run_public_surface_publish_checklist()
    elif args.command == "private-demo-package":
        run_private_demo_package()
    elif args.command == "private-demo-script":
        run_private_demo_script()
    elif args.command == "private-demo-dry-run":
        run_private_demo_dry_run()
    elif args.command == "private-demo-final-review":
        run_private_demo_final_review()
    elif args.command == "private-pilot-intake":
        run_private_pilot_intake()
    elif args.command == "private-pilot-plan":
        run_private_pilot_plan()
    elif args.command == "private-pilot-start-gate":
        run_private_pilot_start_gate()
    elif args.command == "private-pilot-start-confirmation":
        run_private_pilot_start_confirmation()
    elif args.command == "private-pilot-tracker":
        run_private_pilot_tracker()
    elif args.command == "private-pilot-exit-decision":
        run_private_pilot_exit_decision()
    elif args.command == "pilot-day-1-package":
        run_pilot_day_1_package()
    elif args.command == "pilot-day-2-rhythm":
        run_pilot_day_2_rhythm()
    elif args.command == "pilot-day-3-evidence-review":
        run_pilot_day_3_evidence_review()
    elif args.command == "pilot-day-4-owner-confirmation":
        run_pilot_day_4_owner_confirmation()
    elif args.command == "pilot-day-5-narrow-continuation":
        run_pilot_day_5_narrow_continuation()
    elif args.command == "pilot-expansion-review-prep":
        run_pilot_expansion_review_prep()
    elif args.command == "pilot-expansion-review-decision":
        run_pilot_expansion_review_decision()
    elif args.command == "pilot-owner-confirmation-chain":
        run_pilot_owner_confirmation_chain_index()
    elif args.command == "notifications":
        run_notifications()
    elif args.command == "notification-delivery-approval":
        run_notification_delivery_approval()
    elif args.command == "secure-email-delivery":
        run_secure_email_delivery()
    elif args.command == "notification-sent":
        run_notification_sent()
    elif args.command == "notification-dismiss":
        run_notification_dismiss()
    elif args.command == "notification-fail":
        run_notification_fail()
    elif args.command == "ops-tasks":
        run_ops_tasks()
    elif args.command == "ops-escalations":
        run_ops_escalations()
    elif args.command == "ops-brief":
        run_ops_brief()
    elif args.command == "operations-area-review":
        run_operations_area_review()
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
    elif args.command == "governance-area-review":
        run_governance_area_review()
    elif args.command == "support-incidents":
        run_support_incidents()
    elif args.command == "support-brief":
        run_support_brief()
    elif args.command == "support-report":
        run_support_report()
    elif args.command == "support-area-review":
        run_support_area_review()
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
    elif args.command == "daily-close-schedule":
        run_daily_close_schedule()
    elif args.command == "scheduled-daily-close":
        run_scheduled_daily_close_command()
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

