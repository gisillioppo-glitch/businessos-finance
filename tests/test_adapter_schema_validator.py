import unittest

from app.system.adapter_schema_validator import (
    BLOCKED_OVERALL_STATUS,
    INVALID_INPUT_STATUS,
    VALID_OVERALL_STATUS,
    build_adapter_schema_validation_run,
    format_adapter_schema_report,
    format_adapter_schema_validation_run_report,
    validate_adapter_schema,
)


COMMON_FAMILIES = [
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
]


def businessos_schema():
    schema = base_schema(
        adapter_name="businessos_reference",
        branch_name="BusinessOS",
        branch_id="businessos",
        rollback_rule="branch_only_businessos_runtime",
    )
    schema["supported_core_families"] = COMMON_FAMILIES + ["demo_pilot"]
    schema["demo_pilot_adapter"] = {
        "source": "app/demo",
        "rule": "private demo and pilot copy remains BusinessOS-owned",
    }
    return schema


def eduos_schema():
    schema = base_schema(
        adapter_name="eduos_non_sensitive",
        branch_name="EduOS",
        branch_id="eduos",
        branch_visibility="private_future_branch",
        branch_mode="local_only_skeleton",
        rollback_rule="local_only_skeleton_no_runtime",
    )
    schema["role_registry"] = {
        "conceptual_roles": [
            "administrator",
            "teacher",
            "guardian",
            "student",
            "counselor",
            "support_specialist",
        ],
        "public_roles": "none",
        "rule": "roles remain conceptual until access enforcement is approved",
    }
    return schema


def base_schema(
    adapter_name,
    branch_name,
    branch_id,
    rollback_rule,
    branch_visibility="private",
    branch_mode=None,
):
    schema = {
        "adapter_name": adapter_name,
        "adapter_version": "0.1",
        "branch_name": branch_name,
        "branch_id": branch_id,
        "branch_visibility": branch_visibility,
        "branch_owner": "operator",
        "supported_core_families": list(COMMON_FAMILIES),
        "validation_profile": "planning",
        "rollback_rule": rollback_rule,
        "role_registry": {
            "roles": ["admin", "executive", "viewer"],
            "public_roles": "none",
            "rule": "dashboard access is private and role-bound",
        },
        "page_registry": {
            "rule": "pages remain private dashboard surfaces",
        },
        "approval_policy": {
            "statuses": ["pending", "approved", "rejected", "cancelled"],
            "priorities": ["low", "medium", "high", "critical"],
            "gate_required": True,
            "external_delivery_requires_approval": True,
            "dashboard_mutation_requires_approval": True,
        },
        "protected_source_policy": {
            "rule": "sensitive workflows require future approval gates",
        },
        "evidence_registry": {
            "visibility": "private",
            "rule": "evidence remains private and report-backed",
        },
        "notification_policy": {
            "delivery_mode": "queue_only",
            "rule": "external delivery remains queued or approval-gated",
        },
        "readiness_check_registry": {
            "rule": "checks run without private data",
        },
        "runtime_check_registry": {
            "rule": "runtime is blocked unless explicitly approved",
        },
        "scheduler_job_registry": {
            "rule": "scheduler execution remains observable and non-public",
        },
        "governance_rule_pack": {
            "rule": "public/private protections remain branch-owned",
        },
        "command_summary_adapter": {
            "rule": "summary inputs remain status artifacts only",
        },
        "public_boundary_policy": {
            "public_ai_private_runtime_access": "denied",
            "public_db_access": "denied",
            "public_report_access": "denied",
            "public_cli_execution": "denied",
            "public_approval_mutation": "denied",
            "public_notification_delivery": "denied",
            "public_live_private_status_claims": "denied",
            "public_intake_handoff": "sanitized_only",
        },
    }
    if branch_mode is not None:
        schema["branch_mode"] = branch_mode
    return schema


class AdapterSchemaValidatorTests(unittest.TestCase):
    def assert_blocked_for(self, schema, reason):
        result = validate_adapter_schema(schema)

        self.assertEqual(result["overall_status"], BLOCKED_OVERALL_STATUS)
        self.assertIn(reason, result["blocking_reasons"])
        self.assertEqual(result["runtime_authority"], "none")
        self.assertEqual(result["implementation_authority"], "none")

    def test_valid_businessos_reference_schema(self):
        result = validate_adapter_schema(businessos_schema())

        self.assertEqual(result["overall_status"], VALID_OVERALL_STATUS)
        self.assertEqual(result["adapter_name"], "businessos_reference")
        self.assertEqual(result["branch_name"], "BusinessOS")
        self.assertEqual(result["blocking_failures"], 0)

    def test_valid_eduos_non_sensitive_schema(self):
        result = validate_adapter_schema(eduos_schema())

        self.assertEqual(result["overall_status"], VALID_OVERALL_STATUS)
        self.assertEqual(result["adapter_name"], "eduos_non_sensitive")
        self.assertEqual(result["branch_name"], "EduOS")
        self.assertFalse(result["sensitive_input_required"])

    def test_missing_root_field_blocks(self):
        schema = businessos_schema()
        del schema["adapter_name"]

        self.assert_blocked_for(schema, "required_root_fields_missing")

    def test_missing_registry_blocks(self):
        schema = businessos_schema()
        del schema["approval_policy"]

        self.assert_blocked_for(schema, "required_registry_missing")

    def test_public_private_violation_blocks(self):
        schema = businessos_schema()
        schema["public_boundary_policy"]["public_db_access"] = "allowed"

        self.assert_blocked_for(
            schema,
            "public_ai_private_runtime_access_requested",
        )

    def test_approval_gap_blocks(self):
        schema = businessos_schema()
        schema["approval_policy"] = {"gate_required": False}
        schema["notification_policy"]["external_delivery_enabled"] = True

        self.assert_blocked_for(
            schema,
            "approval_gate_missing_for_action_family",
        )

    def test_domain_leakage_blocks(self):
        schema = businessos_schema()
        schema["universal_labels"] = ["Finance"]

        self.assert_blocked_for(
            schema,
            "businessos_domain_logic_marked_universal",
        )

    def test_sensitive_data_required_blocks(self):
        schema = eduos_schema()
        schema["evidence_registry"]["student_data_required"] = True

        self.assert_blocked_for(
            schema,
            "sensitive_data_required_for_validation",
        )

    def test_repository_runtime_scope_blocks(self):
        schema = eduos_schema()
        schema["repository_creation_implied"] = True

        self.assert_blocked_for(schema, "runtime_implementation_implied")

    def test_missing_rollback_blocks(self):
        schema = businessos_schema()
        del schema["rollback_rule"]

        self.assert_blocked_for(schema, "required_root_fields_missing")

    def test_invalid_schema_type_returns_invalid_input(self):
        result = validate_adapter_schema(["not", "a", "schema"])

        self.assertEqual(result["overall_status"], INVALID_INPUT_STATUS)
        self.assertEqual(result["blocking_reasons"], ["schema_root_not_object"])

    def test_safe_report_format_without_file_write(self):
        result = validate_adapter_schema(businessos_schema())
        report = format_adapter_schema_report(result)

        self.assertIn("# Adapter Schema Check", report)
        self.assertIn("Overall status: adapter_schema_valid_for_design", report)
        self.assertIn("Runtime behavior: none", report)
        self.assertIsNone(result["report_path"])
        self.assertTrue(result["safe_to_commit"])

    def test_validation_run_report_summarizes_multiple_controlled_schemas(self):
        businessos_result = validate_adapter_schema(businessos_schema())
        eduos_result = validate_adapter_schema(eduos_schema())

        run = build_adapter_schema_validation_run(
            [businessos_result, eduos_result],
            schema_paths=[
                "config/adapters/businessos.adapter.schema.json",
                "config/adapters/eduos.adapter.schema.json",
            ],
            report_date="2026-05-31",
        )
        report = format_adapter_schema_validation_run_report(run)

        self.assertEqual(run["overall_status"], VALID_OVERALL_STATUS)
        self.assertEqual(run["schema_count"], 2)
        self.assertEqual(run["passed_schema_count"], 2)
        self.assertEqual(run["blocking_failures"], 0)
        self.assertIn("# Adapter Schema Validation Run", report)
        self.assertIn("businessos.adapter.schema.json", report)
        self.assertIn("eduos.adapter.schema.json", report)
        self.assertIn("Runtime behavior: none", report)
        self.assertIn("Fixture creation: blocked", report)


if __name__ == "__main__":
    unittest.main()
