import os
import sqlite3
import tempfile
import unittest
from types import MappingProxyType

from app.db.schema import create_audit_logs_table
from app.evidence import daily_close_distribution, evidence_index
from app.evidence.config import (
    get_default_distribution_reports,
    get_department_reports,
    get_distribution_delivery_mode,
    get_distribution_subject_prefix,
    get_evidence_config,
    get_evidence_reports,
    get_evidence_statuses,
)


class EvidenceConfigBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        create_audit_logs_table(self.conn)
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()
        self.conn.close()

    def write_report(self, prefix, report_date="2026-05-27"):
        reports_path = os.path.join(self.temp_dir.name, "reports")
        os.makedirs(reports_path, exist_ok=True)
        report_path = os.path.join(reports_path, f"{prefix}_{report_date}.md")
        with open(report_path, "w", encoding="utf-8") as file:
            file.write(f"# {prefix}\n")
        return report_path

    def audit_events(self, event_type):
        return self.conn.execute(
            """
            SELECT event_type
            FROM audit_logs
            WHERE event_type = ?
            """,
            (event_type,),
        ).fetchall()

    def test_config_accessors_return_businessos_defaults(self):
        labels = tuple(report["label"] for report in get_evidence_reports())
        prefixes = tuple(report["file_prefix"] for report in get_evidence_reports())

        self.assertIsInstance(get_evidence_config(), MappingProxyType)
        self.assertEqual(get_evidence_config()["branch_id"], "businessos")
        self.assertEqual(get_evidence_statuses(), frozenset({"available", "missing"}))
        self.assertEqual(len(get_evidence_reports()), 6)
        self.assertEqual(
            labels,
            (
                "Command Center",
                "Executive Alerts",
                "Approval Decisions",
                "Governance Brief",
                "Support Brief",
                "Daily Finance Brief",
            ),
        )
        self.assertEqual(
            prefixes,
            (
                "command_center",
                "executive_alerts",
                "approval_decisions",
                "governance_brief",
                "support_brief",
                "daily_brief",
            ),
        )
        self.assertEqual(get_distribution_delivery_mode(), "email_ready_queue")
        self.assertEqual(get_distribution_subject_prefix(), "BusinessOS Daily Close")

    def test_config_is_read_only(self):
        with self.assertRaises(TypeError):
            get_evidence_config()["branch_id"] = "eduos"

        with self.assertRaises(TypeError):
            get_evidence_reports()[0]["label"] = "School Daily Close"

        with self.assertRaises(AttributeError):
            get_evidence_statuses().add("stale")

    def test_compatibility_aliases_match_config_accessors(self):
        self.assertEqual(evidence_index.EVIDENCE_REPORTS, get_evidence_reports())
        self.assertEqual(
            daily_close_distribution.DEPARTMENT_REPORTS,
            get_department_reports(),
        )

    def test_evidence_index_marks_all_reports_missing_when_no_reports_exist(self):
        result = evidence_index.get_executive_evidence_index("2026-05-27")

        self.assertEqual(result["available_count"], 0)
        self.assertEqual(result["missing_count"], 6)
        self.assertEqual(result["total_count"], 6)
        self.assertEqual({item["status"] for item in result["items"]}, {"missing"})

    def test_evidence_index_marks_existing_reports_available(self):
        self.write_report("command_center")
        self.write_report("daily_brief")

        result = evidence_index.get_executive_evidence_index("2026-05-27")
        status_by_label = {item["label"]: item["status"] for item in result["items"]}

        self.assertEqual(result["available_count"], 2)
        self.assertEqual(result["missing_count"], 4)
        self.assertEqual(status_by_label["Command Center"], "available")
        self.assertEqual(status_by_label["Daily Finance Brief"], "available")
        self.assertEqual(status_by_label["Executive Alerts"], "missing")

    def test_evidence_index_export_writes_audit(self):
        path = evidence_index.export_executive_evidence_index(
            self.conn,
            "2026-05-27",
        )

        self.assertEqual(
            os.path.basename(path),
            "executive_evidence_index_2026-05-27.md",
        )
        self.assertEqual(len(self.audit_events("executive_evidence_index_viewed")), 1)
        self.assertEqual(len(self.audit_events("executive_evidence_index_exported")), 1)

    def test_department_report_config_preserves_businessos_mapping(self):
        self.assertEqual(
            get_department_reports()["Executive"],
            (
                "Command Center",
                "Executive Alerts",
                "Approval Decisions",
                "Governance Brief",
                "Support Brief",
                "Daily Finance Brief",
            ),
        )
        self.assertEqual(
            get_department_reports()["Finance"],
            ("Daily Finance Brief", "Command Center", "Executive Alerts"),
        )
        self.assertEqual(
            get_default_distribution_reports(),
            ("Command Center", "Executive Alerts"),
        )

    def test_distribution_uses_configured_delivery_and_subject(self):
        for report in get_evidence_reports():
            self.write_report(report["file_prefix"])

        result = daily_close_distribution.get_daily_close_distribution(
            self.conn,
            "2026-05-27",
        )

        self.assertEqual(result["delivery_mode"], get_distribution_delivery_mode())
        self.assertEqual(result["recipients_count"], 4)
        self.assertEqual(
            {package["subject"] for package in result["packages"]},
            {"BusinessOS Daily Close - 2026-05-27"},
        )

    def test_distribution_report_sets_match_department_config(self):
        for report in get_evidence_reports():
            self.write_report(report["file_prefix"])

        result = daily_close_distribution.get_daily_close_distribution(
            self.conn,
            "2026-05-27",
        )
        packages_by_department = {
            package["recipient"]["department"]: package
            for package in result["packages"]
        }

        for department in ("Finance", "Operations", "Support"):
            report_labels = tuple(
                report["label"]
                for report in packages_by_department[department]["reports"]
            )
            self.assertEqual(
                set(report_labels),
                set(get_department_reports()[department]),
            )

    def test_distribution_queues_notifications_without_external_send(self):
        for report in get_evidence_reports():
            self.write_report(report["file_prefix"])

        distribution = daily_close_distribution.get_daily_close_distribution(
            self.conn,
            "2026-05-27",
        )
        queued = daily_close_distribution.queue_daily_close_distribution_notifications(
            self.conn,
            distribution,
        )
        outbox_count = self.conn.execute(
            "SELECT COUNT(*) FROM notification_outbox WHERE status = 'queued'"
        ).fetchone()[0]

        self.assertEqual(len(queued), 4)
        self.assertEqual(outbox_count, 4)
        self.assertEqual(len(self.audit_events("notification_outbox_queued")), 4)


if __name__ == "__main__":
    unittest.main()
