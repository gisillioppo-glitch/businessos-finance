import sqlite3
import unittest
from types import MappingProxyType

from app.approvals import requests
from app.approvals.approval_status import (
    get_first_pending_approval_request,
    update_approval_request_status,
)
from app.approvals.config import (
    get_active_statuses,
    get_approval_config,
    get_demo_protected_source_modules,
    get_valid_approval_statuses,
    get_valid_approval_types,
    get_valid_priorities,
)
from app.approvals.schema import create_approval_requests_table
from app.db.schema import create_audit_logs_table


class ApprovalConfigBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        create_audit_logs_table(self.conn)
        create_approval_requests_table(self.conn)

    def tearDown(self):
        self.conn.close()

    def audit_events(self, event_type):
        return self.conn.execute(
            """
            SELECT event_type
            FROM audit_logs
            WHERE event_type = ?
            """,
            (event_type,),
        ).fetchall()

    def create_request(self, **overrides):
        payload = {
            "title": "Approve test request",
            "description": "Test approval request.",
            "approval_type": "decision",
            "priority": "high",
            "approver_role": "Executive Owner",
            "requester_email": "REQUESTER@BUSINESSOS.LOCAL",
            "requester_role": "Operations Manager",
            "source_module": "assistance",
            "source_reference_id": "test-source",
        }
        payload.update(overrides)
        return requests.create_approval_request(self.conn, **payload)

    def test_config_accessors_return_businessos_defaults(self):
        self.assertIsInstance(get_approval_config(), MappingProxyType)
        self.assertEqual(get_approval_config()["branch_id"], "businessos")
        self.assertEqual(
            get_valid_approval_types(),
            frozenset({"decision", "access", "budget", "policy", "incident"}),
        )
        self.assertEqual(
            get_valid_priorities(),
            frozenset({"low", "medium", "high", "critical"}),
        )
        self.assertEqual(
            get_valid_approval_statuses(),
            frozenset({"pending", "approved", "rejected", "cancelled"}),
        )
        self.assertEqual(get_active_statuses(), frozenset({"pending"}))
        self.assertEqual(
            get_demo_protected_source_modules(),
            frozenset({"pilot_expansion"}),
        )

    def test_config_is_read_only(self):
        with self.assertRaises(TypeError):
            get_approval_config()["branch_id"] = "eduos"

        with self.assertRaises(AttributeError):
            get_valid_approval_types().add("academic_policy")

    def test_compatibility_aliases_match_config_accessors(self):
        self.assertEqual(requests.VALID_APPROVAL_TYPES, get_valid_approval_types())
        self.assertEqual(requests.VALID_PRIORITIES, get_valid_priorities())
        self.assertEqual(requests.ACTIVE_STATUSES, get_active_statuses())

    def test_create_valid_request_uses_config_and_writes_audit(self):
        result = self.create_request()

        self.assertTrue(result["was_created"])
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["requester_email"], "requester@businessos.local")
        self.assertEqual(len(self.audit_events("approval_request_created")), 1)

    def test_invalid_approval_type_is_rejected(self):
        with self.assertRaises(ValueError):
            self.create_request(approval_type="academic_policy")

    def test_invalid_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            self.create_request(priority="urgent")

    def test_duplicate_request_returns_existing_id_and_writes_audit(self):
        first = self.create_request()
        duplicate = self.create_request()

        self.assertEqual(duplicate["id"], first["id"])
        self.assertFalse(duplicate["was_created"])
        self.assertEqual(len(self.audit_events("approval_request_created")), 1)
        self.assertEqual(
            len(self.audit_events("approval_request_duplicate_skipped")),
            1,
        )

    def test_status_update_uses_config_and_writes_audit(self):
        approval = self.create_request()

        result = update_approval_request_status(
            self.conn,
            approval["id"],
            "approved",
            "Approved in test.",
        )

        self.assertEqual(result["old_status"], "pending")
        self.assertEqual(result["new_status"], "approved")
        self.assertEqual(result["justification"], "Approved in test.")
        self.assertEqual(
            len(self.audit_events("approval_request_status_updated")),
            1,
        )

    def test_invalid_status_is_rejected(self):
        approval = self.create_request()

        with self.assertRaises(ValueError):
            update_approval_request_status(self.conn, approval["id"], "deferred")

    def test_missing_approval_id_is_rejected(self):
        with self.assertRaises(ValueError):
            update_approval_request_status(self.conn, "missing-id", "approved")

    def test_protected_source_module_is_not_selected_for_demo_decision(self):
        self.create_request(
            title="Protected pilot expansion",
            priority="high",
            source_module="pilot_expansion",
            source_reference_id="pilot-expansion-001",
        )
        eligible = self.create_request(
            title="Eligible assistance request",
            priority="medium",
            source_module="assistance",
            source_reference_id="assistance-001",
        )

        row = get_first_pending_approval_request(self.conn)

        self.assertIsNotNone(row)
        self.assertEqual(row[0], eligible["id"])
        self.assertEqual(row[1], "Eligible assistance request")


if __name__ == "__main__":
    unittest.main()
