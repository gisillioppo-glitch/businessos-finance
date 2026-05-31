import json
from datetime import date
from pathlib import Path


VALID_OVERALL_STATUS = "adapter_schema_valid_for_design"
WARNING_OVERALL_STATUS = "adapter_schema_valid_with_warnings"
BLOCKED_OVERALL_STATUS = "adapter_schema_blocked"
INVALID_INPUT_STATUS = "adapter_schema_invalid_input"

RUNTIME_AUTHORITY = "none"
IMPLEMENTATION_AUTHORITY = "none"

REQUIRED_ROOT_FIELDS = (
    "adapter_name",
    "adapter_version",
    "branch_name",
    "branch_id",
    "branch_visibility",
    "branch_owner",
    "supported_core_families",
    "validation_profile",
    "rollback_rule",
)

SUPPORTED_FAMILIES = frozenset(
    {
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
        "demo_pilot",
        "public_boundary",
    }
)

FAMILY_REGISTRIES = {
    "identity": "role_registry",
    "dashboard": "page_registry",
    "approvals": "approval_policy",
    "evidence": "evidence_registry",
    "readiness": "readiness_check_registry",
    "runtime": "runtime_check_registry",
    "scheduler": "scheduler_job_registry",
    "notifications": "notification_policy",
    "governance": "governance_rule_pack",
    "command_center": "command_summary_adapter",
    "demo_pilot": "demo_pilot_adapter",
    "public_boundary": "public_boundary_policy",
}

ALWAYS_REQUIRED_REGISTRIES = (
    "protected_source_policy",
    "public_boundary_policy",
)

DANGEROUS_PUBLIC_KEYS = frozenset(
    {
        "public_ai_private_runtime_access",
        "public_db_access",
        "public_report_access",
        "public_route_private_db_access",
        "public_route_private_report_access",
        "public_cli_execution",
        "public_approval_mutation",
        "public_notification_delivery",
        "public_scheduler_execution",
        "public_live_private_status_claims",
        "public_student_data_access",
        "public_teacher_data_access",
        "public_guardian_data_access",
        "public_grade_access",
        "public_attendance_access",
        "public_assessment_content_access",
        "public_private_report_access",
        "public_workflow_mutation",
        "public_guardian_delivery",
        "private_db_access",
        "private_report_access",
        "private_runtime_access",
    }
)

ACTION_FAMILY_KEYS = frozenset(
    {
        "dashboard_mutation_enabled",
        "external_delivery_enabled",
        "notification_delivery_enabled",
        "scheduler_execution_enabled",
        "workflow_mutation_enabled",
    }
)

SENSITIVE_KEYS = frozenset(
    {
        "sensitive_data_required",
        "private_data_required",
        "academic_data_required",
        "student_data_required",
        "teacher_data_required",
        "guardian_data_required",
        "grade_data_required",
        "attendance_data_required",
        "assessment_content_required",
        "intervention_data_required",
        "raw_lms_export_required",
        "raw_sis_export_required",
        "classroom_credentials_required",
        "lms_credentials_required",
        "sis_credentials_required",
    }
)

RUNTIME_SCOPE_KEYS = frozenset(
    {
        "repository_creation_implied",
        "repository_creation_requested",
        "package_creation_implied",
        "package_creation_requested",
        "runtime_implementation_implied",
        "runtime_implementation_requested",
        "adapter_runtime_execution",
        "adapter_runtime_enabled",
        "eduos_runtime_enabled",
        "eduos_repository_creation",
        "os_core_package_creation",
        "code_extraction_requested",
    }
)

BUSINESSOS_BRANCH_LABELS = frozenset(
    {
        "finance",
        "operations",
        "governance",
        "support",
        "assistance",
        "daily close",
        "scheduled close",
        "delivery approval",
        "secure email",
        "demo readiness",
        "private demo",
        "pilot plan",
        "pilot tracker",
        "pilot expansion",
        "command center",
        "executive alerts",
        "daily finance brief",
    }
)


def load_adapter_schema(path):
    schema_path = Path(path)
    try:
        return json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "invalid_input": True,
            "error": exc.__class__.__name__,
            "detail": "schema could not be loaded safely",
        }


def validate_adapter_schema(schema, profile="planning"):
    if not isinstance(schema, dict):
        return build_adapter_schema_result(
            [
                _check(
                    "schema_input",
                    "invalid_input",
                    "critical",
                    "schema root must be an object",
                    "schema_root_not_object",
                )
            ],
            {
                "validation_profile": profile,
                "schema_format": "dict",
                "schema_source": "provided_object",
            },
        )

    if schema.get("invalid_input"):
        return build_adapter_schema_result(
            [
                _check(
                    "schema_input",
                    "invalid_input",
                    "critical",
                    schema.get("detail", "schema input is invalid"),
                    schema.get("error", "schema_invalid_input"),
                )
            ],
            {
                "validation_profile": profile,
                "schema_format": "json",
                "schema_source": "provided_path",
            },
        )

    metadata = {
        "adapter_name": schema.get("adapter_name", "unknown"),
        "adapter_version": schema.get("adapter_version", "unknown"),
        "branch_name": schema.get("branch_name", "unknown"),
        "validation_profile": schema.get("validation_profile", profile),
        "schema_format": "dict",
        "schema_source": "provided_object",
        "sensitive_input_required": _contains_trigger(schema, SENSITIVE_KEYS),
    }

    checks = []
    for validator in (
        validate_required_root_fields,
        validate_supported_families,
        validate_required_registries,
        validate_public_boundary,
        validate_approval_gates,
        validate_evidence_visibility,
        validate_runtime_scope,
        validate_domain_ownership,
        validate_rollback_rule,
    ):
        checks.extend(_as_checks(validator(schema)))

    return build_adapter_schema_result(checks, metadata)


def validate_required_root_fields(schema):
    missing = [field for field in REQUIRED_ROOT_FIELDS if not schema.get(field)]
    if schema.get("branch_id") == "eduos" and not schema.get("branch_mode"):
        missing.append("branch_mode")

    if missing:
        return _check(
            "required_root_fields",
            "failed",
            "blocker",
            "missing required root fields: " + ", ".join(sorted(missing)),
            "required_root_fields_missing",
        )

    return _check(
        "required_root_fields",
        "passed",
        "info",
        "required root fields are present",
    )


def validate_supported_families(schema):
    families = schema.get("supported_core_families")
    if not isinstance(families, list) or not families:
        return _check(
            "supported_core_families",
            "failed",
            "blocker",
            "supported_core_families must be a non-empty list",
            "supported_core_families_missing",
        )

    unsupported = sorted(
        family for family in families if family not in SUPPORTED_FAMILIES
    )
    if unsupported:
        return _check(
            "supported_core_families",
            "failed",
            "blocker",
            "unsupported families: " + ", ".join(unsupported),
            "schema_format_unsupported",
        )

    return _check(
        "supported_core_families",
        "passed",
        "info",
        "supported families are explicit and recognized",
    )


def validate_required_registries(schema):
    families = schema.get("supported_core_families")
    if not isinstance(families, list):
        families = []

    required = {FAMILY_REGISTRIES[family] for family in families if family in FAMILY_REGISTRIES}
    required.update(ALWAYS_REQUIRED_REGISTRIES)
    missing = sorted(name for name in required if not schema.get(name))

    if missing:
        return _check(
            "required_registries",
            "failed",
            "blocker",
            "missing required registries: " + ", ".join(missing),
            "required_registry_missing",
        )

    return _check(
        "required_registries",
        "passed",
        "info",
        "required registries are present",
    )


def validate_public_boundary(schema):
    if _contains_unsafe_value(schema, DANGEROUS_PUBLIC_KEYS):
        return _check(
            "public_boundary",
            "failed",
            "blocker",
            "public or Public AI access requests private runtime or data",
            "public_ai_private_runtime_access_requested",
        )

    boundary = schema.get("public_boundary_policy")
    if not isinstance(boundary, dict):
        return _check(
            "public_boundary",
            "failed",
            "blocker",
            "public boundary policy is missing",
            "required_registry_missing",
        )

    return _check(
        "public_boundary",
        "passed",
        "info",
        "public boundary denies private access",
    )


def validate_approval_gates(schema):
    approval_policy = schema.get("approval_policy")
    if not isinstance(approval_policy, dict):
        return _check(
            "approval_gates",
            "failed",
            "blocker",
            "approval policy is missing",
            "approval_gate_missing_for_action_family",
        )

    if _contains_unsafe_value(schema, ACTION_FAMILY_KEYS):
        if not _approval_gate_present(schema):
            return _check(
                "approval_gates",
                "failed",
                "blocker",
                "action-producing family is enabled without approval gate",
                "approval_gate_missing_for_action_family",
            )

    return _check(
        "approval_gates",
        "passed",
        "info",
        "approval gates are explicit for action-producing scope",
    )


def validate_evidence_visibility(schema):
    if _contains_trigger(schema, SENSITIVE_KEYS):
        return _check(
            "evidence_visibility",
            "failed",
            "blocker",
            "schema requires sensitive or private data for validation",
            "sensitive_data_required_for_validation",
        )

    evidence_registry = schema.get("evidence_registry")
    if isinstance(evidence_registry, dict) and not (
        evidence_registry.get("rule") or evidence_registry.get("visibility")
    ):
        return _check(
            "evidence_visibility",
            "warning",
            "warning",
            "evidence registry should describe visibility or rule",
            "optional_registry_detail_missing",
        )

    return _check(
        "evidence_visibility",
        "passed",
        "info",
        "evidence validation does not require sensitive input",
    )


def validate_runtime_scope(schema):
    if _contains_unsafe_value(schema, RUNTIME_SCOPE_KEYS):
        return _check(
            "runtime_scope",
            "failed",
            "blocker",
            "schema implies repository, package, runtime, or adapter execution",
            "runtime_implementation_implied",
        )

    if schema.get("branch_id") == "eduos":
        branch_mode = schema.get("branch_mode")
        if branch_mode != "local_only_skeleton":
            return _check(
                "runtime_scope",
                "failed",
                "blocker",
                "EduOS planning must remain local_only_skeleton",
                "runtime_implementation_implied",
            )

    return _check(
        "runtime_scope",
        "passed",
        "info",
        "schema does not imply runtime, package, repository, or adapter execution",
    )


def validate_domain_ownership(schema):
    if schema.get("universal_labels"):
        leaked = _matching_labels(schema.get("universal_labels"), BUSINESSOS_BRANCH_LABELS)
        if leaked:
            return _check(
                "domain_ownership",
                "failed",
                "blocker",
                "branch-owned labels marked universal: " + ", ".join(leaked),
                "businessos_domain_logic_marked_universal",
            )

    if schema.get("branch_id") == "eduos" and schema.get("businessos_runtime"):
        return _check(
            "domain_ownership",
            "failed",
            "blocker",
            "EduOS schema cannot mark BusinessOS runtime as owned or required",
            "eduos_academic_logic_marked_businessos_runtime",
        )

    return _check(
        "domain_ownership",
        "passed",
        "info",
        "domain labels remain branch-owned",
    )


def validate_rollback_rule(schema):
    rollback_rule = schema.get("rollback_rule")
    if not rollback_rule:
        return _check(
            "rollback_rule",
            "failed",
            "blocker",
            "rollback rule is missing",
            "rollback_rule_missing",
        )

    lowered = str(rollback_rule).lower()
    unsafe_terms = ("repository", "package", "runtime enabled", "public ai private")
    if any(term in lowered for term in unsafe_terms):
        return _check(
            "rollback_rule",
            "failed",
            "blocker",
            "rollback rule implies blocked runtime or repository scope",
            "runtime_implementation_implied",
        )

    return _check(
        "rollback_rule",
        "passed",
        "info",
        "rollback returns to branch-only or local-only operation",
    )


def build_adapter_schema_result(checks, metadata):
    normalized_checks = [_normalize_check(check) for check in checks]
    failed = [
        check
        for check in normalized_checks
        if check["status"] in {"failed", "blocked", "invalid_input"}
        or check["severity"] in {"blocker", "critical"}
    ]
    warnings = [check for check in normalized_checks if check["status"] == "warning"]
    invalid = [
        check
        for check in normalized_checks
        if check["status"] == "invalid_input" or check["severity"] == "critical"
    ]

    if invalid:
        overall_status = INVALID_INPUT_STATUS
    elif failed:
        overall_status = BLOCKED_OVERALL_STATUS
    elif warnings:
        overall_status = WARNING_OVERALL_STATUS
    else:
        overall_status = VALID_OVERALL_STATUS

    return {
        "date": metadata.get("date"),
        "adapter_name": metadata.get("adapter_name", "unknown"),
        "adapter_version": metadata.get("adapter_version", "unknown"),
        "branch_name": metadata.get("branch_name", "unknown"),
        "validation_profile": metadata.get("validation_profile", "planning"),
        "overall_status": overall_status,
        "total_checks": len(normalized_checks),
        "passed_checks": _count_status(normalized_checks, "passed"),
        "warning_checks": _count_status(normalized_checks, "warning"),
        "failed_checks": len(failed),
        "blocking_failures": len(failed),
        "blocking_reasons": [
            check["reason"] for check in failed if check.get("reason")
        ],
        "warnings": [check["detail"] for check in warnings],
        "checks": normalized_checks,
        "schema_path": metadata.get("schema_path", "provided_object"),
        "schema_format": metadata.get("schema_format", "dict"),
        "schema_source": metadata.get("schema_source", "provided_object"),
        "sensitive_input_required": bool(metadata.get("sensitive_input_required")),
        "report_path": None,
        "safe_to_commit": True,
        "runtime_authority": RUNTIME_AUTHORITY,
        "implementation_authority": IMPLEMENTATION_AUTHORITY,
    }


def format_adapter_schema_report(result):
    lines = [
        "# Adapter Schema Check",
        "",
        f"Date: {result.get('date') or 'not_exported'}",
        f"Adapter: {result.get('adapter_name', 'unknown')}",
        f"Adapter version: {result.get('adapter_version', 'unknown')}",
        f"Branch: {result.get('branch_name', 'unknown')}",
        f"Validation profile: {result.get('validation_profile', 'planning')}",
        f"Overall status: {result.get('overall_status', 'unknown')}",
        "",
        "## Summary",
        "",
        f"Total checks: {result.get('total_checks', 0)}",
        f"Passed checks: {result.get('passed_checks', 0)}",
        f"Warning checks: {result.get('warning_checks', 0)}",
        f"Failed checks: {result.get('failed_checks', 0)}",
        f"Blocking failures: {result.get('blocking_failures', 0)}",
        "",
        "## Schema Input",
        "",
        f"Schema path: {result.get('schema_path', 'provided_object')}",
        f"Schema format: {result.get('schema_format', 'dict')}",
        f"Schema source: {result.get('schema_source', 'provided_object')}",
        f"Sensitive input required: {str(result.get('sensitive_input_required', False)).lower()}",
        "",
        "## Checks",
        "",
        "| Check | Status | Severity | Detail |",
        "| --- | --- | --- | --- |",
    ]

    for check in result.get("checks", []):
        lines.append(
            "| {name} | {status} | {severity} | {detail} |".format(
                name=_safe_cell(check.get("name", "")),
                status=_safe_cell(check.get("status", "")),
                severity=_safe_cell(check.get("severity", "")),
                detail=_safe_cell(check.get("detail", "")),
            )
        )

    lines.extend(
        [
            "",
            "## Blocking Reasons",
            "",
        ]
    )
    blocking_reasons = result.get("blocking_reasons") or []
    if blocking_reasons:
        lines.extend(f"- {_safe_line(reason)}" for reason in blocking_reasons)
    else:
        lines.append("None.")

    lines.extend(["", "## Warnings", ""])
    warnings = result.get("warnings") or []
    if warnings:
        lines.extend(f"- {_safe_line(warning)}" for warning in warnings)
    else:
        lines.append("None.")

    lines.extend(
        [
            "",
            "## Boundary Classification",
            "",
            "```text",
            "OS Core candidate: yes",
            "BusinessOS-specific: adapter_owned_if_businessos",
            "EduOS-specific: adapter_owned_if_eduos",
            "Public AI boundary: deny_by_default",
            "Sensitive data exposure: none",
            "Runtime behavior: none",
            "Approval behavior: validation_only",
            "Notification delivery: none",
            "Remote publish: blocked",
            "Repository creation: blocked",
            "Package creation: blocked",
            "Code extraction: blocked",
            "Adapter implementation: blocked",
            "Schema validator implementation authority: none",
            "```",
            "",
            "## Operator Note",
            "",
            "This report summarizes adapter schema validation only. It does not grant runtime, implementation, repository, package, adapter execution, EduOS runtime, or Public AI private runtime authority.",
        ]
    )

    return "\n".join(lines) + "\n"


def export_adapter_schema_report(result, reports_dir="reports", report_date=None):
    if not result.get("safe_to_commit", False):
        result["overall_status"] = BLOCKED_OVERALL_STATUS
        result["blocking_failures"] = result.get("blocking_failures", 0) + 1
        result.setdefault("blocking_reasons", []).append("report_not_safe_to_commit")
        result["runtime_authority"] = RUNTIME_AUTHORITY
        result["implementation_authority"] = IMPLEMENTATION_AUTHORITY
        return result

    export_date = report_date or date.today().isoformat()
    report_path = Path(reports_dir) / f"adapter_schema_check_{export_date}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    result["date"] = export_date
    result["report_path"] = str(report_path)
    report_path.write_text(format_adapter_schema_report(result), encoding="utf-8")
    return result


def build_adapter_schema_validation_run(results, schema_paths=None, report_date=None):
    normalized_results = list(results)
    failed = [
        result
        for result in normalized_results
        if result.get("overall_status")
        in {BLOCKED_OVERALL_STATUS, INVALID_INPUT_STATUS}
        or result.get("blocking_failures", 0) > 0
    ]
    warnings = [
        result
        for result in normalized_results
        if result.get("overall_status") == WARNING_OVERALL_STATUS
        or result.get("warning_checks", 0) > 0
    ]

    if failed:
        overall_status = BLOCKED_OVERALL_STATUS
    elif warnings:
        overall_status = WARNING_OVERALL_STATUS
    else:
        overall_status = VALID_OVERALL_STATUS

    return {
        "date": report_date,
        "overall_status": overall_status,
        "schema_count": len(normalized_results),
        "passed_schema_count": len(normalized_results) - len(failed) - len(warnings),
        "warning_schema_count": len(warnings),
        "failed_schema_count": len(failed),
        "total_checks": sum(result.get("total_checks", 0) for result in normalized_results),
        "passed_checks": sum(result.get("passed_checks", 0) for result in normalized_results),
        "warning_checks": sum(result.get("warning_checks", 0) for result in normalized_results),
        "failed_checks": sum(result.get("failed_checks", 0) for result in normalized_results),
        "blocking_failures": sum(result.get("blocking_failures", 0) for result in normalized_results),
        "schema_paths": list(schema_paths or []),
        "results": normalized_results,
        "report_path": None,
        "safe_to_commit": True,
        "runtime_authority": RUNTIME_AUTHORITY,
        "implementation_authority": IMPLEMENTATION_AUTHORITY,
    }


def format_adapter_schema_validation_run_report(run):
    lines = [
        "# Adapter Schema Validation Run",
        "",
        f"Date: {run.get('date') or 'not_exported'}",
        f"Overall status: {run.get('overall_status', 'unknown')}",
        f"Schema count: {run.get('schema_count', 0)}",
        f"Passed schemas: {run.get('passed_schema_count', 0)}",
        f"Warning schemas: {run.get('warning_schema_count', 0)}",
        f"Failed schemas: {run.get('failed_schema_count', 0)}",
        "",
        "## Summary",
        "",
        f"Total checks: {run.get('total_checks', 0)}",
        f"Passed checks: {run.get('passed_checks', 0)}",
        f"Warning checks: {run.get('warning_checks', 0)}",
        f"Failed checks: {run.get('failed_checks', 0)}",
        f"Blocking failures: {run.get('blocking_failures', 0)}",
        "",
        "## Schema Results",
        "",
        "| Schema | Adapter | Branch | Status | Checks | Blocking failures |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    schema_paths = run.get("schema_paths") or []
    for index, result in enumerate(run.get("results", [])):
        schema_path = (
            schema_paths[index]
            if index < len(schema_paths)
            else result.get("schema_path", "provided_object")
        )
        lines.append(
            "| {schema} | {adapter} | {branch} | {status} | {checks} | {blocking} |".format(
                schema=_safe_cell(Path(schema_path).name),
                adapter=_safe_cell(result.get("adapter_name", "unknown")),
                branch=_safe_cell(result.get("branch_name", "unknown")),
                status=_safe_cell(result.get("overall_status", "unknown")),
                checks=_safe_cell(
                    f"{result.get('passed_checks', 0)}/{result.get('total_checks', 0)}"
                ),
                blocking=_safe_cell(result.get("blocking_failures", 0)),
            )
        )

    lines.extend(
        [
            "",
            "## Boundary Classification",
            "",
            "```text",
            "OS Core candidate: yes",
            "BusinessOS-specific: adapter_owned_if_businessos",
            "EduOS-specific: adapter_owned_if_eduos",
            "Public AI boundary: deny_by_default",
            "Sensitive data exposure: none",
            "Runtime behavior: none",
            "Approval behavior: validation_only",
            "Notification delivery: none",
            "Remote publish: blocked",
            "Repository creation: blocked",
            "Package creation: blocked",
            "Code extraction: blocked",
            "Fixture creation: blocked",
            "Adapter implementation: blocked",
            "Schema validation run authority: evidence_only",
            "```",
            "",
            "## Operator Note",
            "",
            "This run report summarizes controlled adapter schema validation evidence only. It does not grant runtime, implementation, repository, package, fixture, adapter execution, EduOS runtime, or Public AI private runtime authority.",
        ]
    )

    return "\n".join(lines) + "\n"


def export_adapter_schema_validation_run(run, reports_dir="reports", report_date=None):
    export_date = report_date or date.today().isoformat()
    report_path = Path(reports_dir) / f"adapter_schema_validation_run_{export_date}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    run["date"] = export_date
    run["report_path"] = str(report_path)
    report_path.write_text(
        format_adapter_schema_validation_run_report(run),
        encoding="utf-8",
    )
    return run


def _check(name, status, severity, detail, reason=None):
    return {
        "name": name,
        "status": status,
        "severity": severity,
        "detail": detail,
        "reason": reason,
    }


def _as_checks(value):
    if isinstance(value, list):
        return value
    return [value]


def _normalize_check(check):
    normalized = dict(check)
    normalized.setdefault("name", "unknown")
    normalized.setdefault("status", "not_applicable")
    normalized.setdefault("severity", "info")
    normalized.setdefault("detail", "")
    normalized.setdefault("reason", None)
    return normalized


def _count_status(checks, status):
    return sum(1 for check in checks if check["status"] == status)


def _approval_gate_present(schema):
    policy = schema.get("approval_policy")
    if not isinstance(policy, dict):
        return False

    gate_values = (
        policy.get("gate_required"),
        policy.get("approval_required"),
        policy.get("external_delivery_requires_approval"),
        policy.get("dashboard_mutation_requires_approval"),
        policy.get("scheduler_execution_requires_observability"),
    )
    return any(value is True or value == "required" for value in gate_values)


def _contains_trigger(value, keys):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in keys and _is_truthy_unsafe(child):
                return True
            if _contains_trigger(child, keys):
                return True
    elif isinstance(value, list):
        return any(_contains_trigger(item, keys) for item in value)
    return False


def _contains_unsafe_value(value, keys):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in keys and _is_access_allowed(child):
                return True
            if _contains_unsafe_value(child, keys):
                return True
    elif isinstance(value, list):
        return any(_contains_unsafe_value(item, keys) for item in value)
    return False


def _is_access_allowed(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    lowered = str(value).strip().lower()
    return lowered in {
        "allow",
        "allowed",
        "enabled",
        "true",
        "yes",
        "requested",
        "required",
        "live",
        "write",
        "mutate",
        "execute",
    }


def _is_truthy_unsafe(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() not in {
        "",
        "false",
        "no",
        "none",
        "not_required",
        "blocked",
        "denied",
    }


def _matching_labels(values, blocked_labels):
    if isinstance(values, str):
        candidates = [values]
    elif isinstance(values, list):
        candidates = values
    else:
        return []

    normalized_blocked = {label.lower() for label in blocked_labels}
    return sorted(
        str(value)
        for value in candidates
        if str(value).strip().lower() in normalized_blocked
    )


def _safe_cell(value):
    return _safe_line(value).replace("|", "/")


def _safe_line(value):
    return str(value).replace("\n", " ").strip()
