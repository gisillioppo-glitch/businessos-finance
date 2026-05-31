import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from cli import run_adapter_schema_check


def valid_schema():
    return {
        "adapter_name": "businessos_reference",
        "adapter_version": "0.1",
        "branch_name": "BusinessOS",
        "branch_id": "businessos",
        "branch_visibility": "private",
        "branch_owner": "operator",
        "supported_core_families": [
            "identity",
            "dashboard",
            "approvals",
            "evidence",
            "readiness",
            "runtime",
            "scheduler",
            "notifications",
            "governance",
            "command_center",
            "public_boundary",
        ],
        "validation_profile": "planning",
        "rollback_rule": "branch_only_businessos_runtime",
        "role_registry": {"rule": "private roles only"},
        "page_registry": {"rule": "private pages only"},
        "approval_policy": {"gate_required": True},
        "protected_source_policy": {"rule": "approval gates required"},
        "evidence_registry": {"visibility": "private"},
        "notification_policy": {"rule": "queued or approval-gated"},
        "readiness_check_registry": {"rule": "local checks only"},
        "runtime_check_registry": {"rule": "no runtime execution"},
        "scheduler_job_registry": {"rule": "observable only"},
        "governance_rule_pack": {"rule": "deny by default"},
        "command_summary_adapter": {"rule": "status artifacts only"},
        "public_boundary_policy": {
            "public_ai_private_runtime_access": "denied",
            "public_db_access": "denied",
            "public_report_access": "denied",
        },
    }


class AdapterSchemaCliTests(unittest.TestCase):
    def run_with_schema(self, schema):
        with tempfile.TemporaryDirectory() as tmp:
            schema_path = Path(tmp) / "schema.json"
            schema_path.write_text(json.dumps(schema), encoding="utf-8")

            output = StringIO()
            with redirect_stdout(output):
                exit_code = run_adapter_schema_check(str(schema_path))

            return exit_code, output.getvalue()

    def test_valid_schema_returns_design_ready_exit_zero(self):
        exit_code, output = self.run_with_schema(valid_schema())

        self.assertEqual(exit_code, 0)
        self.assertIn("Adapter Schema Check", output)
        self.assertIn("Overall status: adapter_schema_valid_for_design", output)
        self.assertIn("Adapter name: businessos_reference", output)
        self.assertIn("Runtime authority: none", output)
        self.assertIn("Implementation authority: none", output)

    def test_blocked_schema_returns_exit_two(self):
        schema = valid_schema()
        schema["public_boundary_policy"]["public_db_access"] = "allowed"

        exit_code, output = self.run_with_schema(schema)

        self.assertEqual(exit_code, 2)
        self.assertIn("Overall status: adapter_schema_blocked", output)
        self.assertIn("public_ai_private_runtime_access_requested", output)
        self.assertIn("Runtime authority: none", output)

    def test_invalid_json_path_returns_exit_three_without_report_write(self):
        output = StringIO()
        with redirect_stdout(output):
            exit_code = run_adapter_schema_check("missing-schema.json")

        self.assertEqual(exit_code, 3)
        self.assertIn("Overall status: adapter_schema_invalid_input", output.getvalue())
        self.assertIn("Runtime authority: none", output.getvalue())


if __name__ == "__main__":
    unittest.main()
