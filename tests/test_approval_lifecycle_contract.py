import os
import sqlite3
import tempfile
import unittest

from app.approvals.approval_brief import print_approval_brief
from app.approvals.approval_report import export_approval_report
from app.approvals.approval_status import (
    demo_approve_first_pending_approval_request,
    demo_reject_first_pending_approval_request,
    get_approval_decision_summary,
    get_first_pending_approval_request,
    update_approval_request_status,
)
from app.approvals.approval_views import (
    print_approval_request_summary_kpis,
    print_approval_requests_list,
)
from app.approvals.requests import create_approval_request
from app.approvals.schema import create_approval_requests_table
from app.db.schema import create_audit_logs_table


class ApprovalLifecycleContractTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        create_audit_logs_table(self.conn)
        create_approval_requests_table(self.conn)
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()
        self.conn.close()

    def create_request(self, **overrides):
        payload = {
            "title": "Lifecycle approval",
            "description": "Lifecycle approval request.",
            "approval_type": "decision",
            "priority": "medium",
            "approver_role": "Executive Owner",
            "requester_email": "operator@businessos.local",
            "requester_role": "Operations Manager",
            "source_module": "assistance",
            "source_reference_id": "lifecycle-source",
        }
        payload.update(overrides)
        return create_approval_request(self.conn, **payload)

    def audit_events(self, event_type):
        return self.conn.execute(
            """
            SELECT event_type
            FROM audit_logs
            WHERE event_type = ?
            """,
            (event_type,),
        ).fetchall()

    def test_first_pending_selection_uses_priority_order(self):
        low = self.create_request(
            title="Low approval",
            priority="low",
            source_reference_id="low",
        )
        high = self.create_request(
            title="High approval",
            priority="high",
            source_reference_id="high",
        )
        critical = self.create_request(
            title="Critical approval",
            priority="critical",
            source_reference_id="critical",
        )

        row = get_first_pending_approval_request(self.conn)

        self.assertEqual(row[0], critical["id"])
        self.assertNotEqual(row[0], high["id"])
        self.assertNotEqual(row[0], low["id"])

    def test_protected_source_is_skipped_even_when_high_priority(self):
        self.create_request(
            title="Protected expansion",
            priority="critical",
            source_module="pilot_expansion",
            source_reference_id="pilot-expansion",
        )
        eligible = self.create_request(
            title="Eligible approval",
            priority="high",
            source_module="assistance",
            source_reference_id="eligible",
        )

        row = get_first_pending_approval_request(self.conn)

        self.assertEqual(row[0], eligible["id"])
        self.assertEqual(row[1], "Eligible approval")

    def test_demo_approve_updates_only_selected_request(self):
        selected = self.create_request(
            title="Selected approval",
            priority="high",
            source_reference_id="selected",
        )
        untouched = self.create_request(
            title="Untouched approval",
            priority="medium",
            source_reference_id="untouched",
        )

        result = demo_approve_first_pending_approval_request(self.conn)
        summary = get_approval_decision_summary(self.conn)
        untouched_status = self.conn.execute(
            "SELECT status FROM approval_requests WHERE id = ?",
            (untouched["id"],),
        ).fetchone()[0]

        self.assertEqual(result["approval_id"], selected["id"])
        self.assertEqual(result["new_status"], "approved")
        self.assertEqual(untouched_status, "pending")
        self.assertEqual(summary["approved"], 1)
        self.assertEqual(summary["pending"], 1)

    def test_demo_reject_records_justification(self):
        approval = self.create_request(
            title="Rejectable approval",
            priority="high",
            source_reference_id="rejectable",
        )

        result = demo_reject_first_pending_approval_request(self.conn)
        status, justification = self.conn.execute(
            """
            SELECT status, status_justification
            FROM approval_requests
            WHERE id = ?
            """,
            (approval["id"],),
        ).fetchone()

        self.assertEqual(result["approval_id"], approval["id"])
        self.assertEqual(status, "rejected")
        self.assertIn("Demo mode rejected", justification)

    def test_cancelled_status_counts_in_summary(self):
        approval = self.create_request()

        update_approval_request_status(
            self.conn,
            approval["id"],
            "cancelled",
            "Cancelled in lifecycle test.",
        )
        summary = get_approval_decision_summary(self.conn)

        self.assertEqual(summary["cancelled"], 1)
        self.assertEqual(summary["pending"], 0)

    def test_list_visibility_does_not_change_status(self):
        approval = self.create_request()

        rows = print_approval_requests_list(self.conn)
        status = self.conn.execute(
            "SELECT status FROM approval_requests WHERE id = ?",
            (approval["id"],),
        ).fetchone()[0]

        self.assertEqual(len(rows), 1)
        self.assertEqual(status, "pending")
        self.assertEqual(len(self.audit_events("approval_request_list_viewed")), 1)

    def test_summary_visibility_does_not_change_status(self):
        approval = self.create_request()

        summary = print_approval_request_summary_kpis(self.conn)
        status = self.conn.execute(
            "SELECT status FROM approval_requests WHERE id = ?",
            (approval["id"],),
        ).fetchone()[0]

        self.assertEqual(summary["pending"], 1)
        self.assertEqual(status, "pending")
        self.assertEqual(
            len(self.audit_events("approval_request_summary_kpis_viewed")),
            1,
        )

    def test_report_export_does_not_change_status_and_writes_audit(self):
        approval = self.create_request(priority="high")
        approval_kpis = print_approval_request_summary_kpis(self.conn)
        approval_brief = print_approval_brief(self.conn, approval_kpis)

        report_path = export_approval_report(
            self.conn,
            approval_kpis,
            approval_brief,
        )
        status = self.conn.execute(
            "SELECT status FROM approval_requests WHERE id = ?",
            (approval["id"],),
        ).fetchone()[0]

        self.assertEqual(status, "pending")
        self.assertTrue(os.path.exists(report_path))
        self.assertEqual(
            len(self.audit_events("approval_decision_report_exported")),
            1,
        )

    def test_status_update_preserves_old_status_in_result_and_audit(self):
        approval = self.create_request()

        result = update_approval_request_status(
            self.conn,
            approval["id"],
            "approved",
            "Lifecycle test approval.",
        )
        audit_count = len(self.audit_events("approval_request_status_updated"))

        self.assertEqual(result["old_status"], "pending")
        self.assertEqual(result["new_status"], "approved")
        self.assertEqual(audit_count, 1)

    def test_no_pending_demo_action_writes_noop_audit(self):
        approval = self.create_request()
        update_approval_request_status(
            self.conn,
            approval["id"],
            "approved",
            "Pre-approved before demo action.",
        )

        result = demo_approve_first_pending_approval_request(self.conn)

        self.assertIsNone(result)
        self.assertEqual(
            len(self.audit_events("approval_request_approve_demo")),
            1,
        )


if __name__ == "__main__":
    unittest.main()
