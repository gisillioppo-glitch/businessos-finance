# Adapter Schema Fixture Run

Date: 2026-06-24
Overall status: fixture_run_passed
Fixture count: 11
Passed expectations: 11
Failed expectations: 0

## Summary

Valid fixtures: 2
Blocked fixtures: 8
Invalid input fixtures: 1
Runtime authority: none
Implementation authority: none

## Fixture Results

| Fixture | Expected status | Actual status | Expected reason | Result |
| --- | --- | --- | --- | --- |
| invalid_approval_gap.schema.json | adapter_schema_blocked | adapter_schema_blocked | approval_gate_missing_for_action_family | passed |
| invalid_domain_leakage.schema.json | adapter_schema_blocked | adapter_schema_blocked | businessos_domain_logic_marked_universal | passed |
| invalid_json.schema.json | adapter_schema_invalid_input | adapter_schema_invalid_input | JSONDecodeError | passed |
| invalid_missing_registry.schema.json | adapter_schema_blocked | adapter_schema_blocked | required_registry_missing | passed |
| invalid_missing_rollback.schema.json | adapter_schema_blocked | adapter_schema_blocked | required_root_fields_missing | passed |
| invalid_missing_root_field.schema.json | adapter_schema_blocked | adapter_schema_blocked | required_root_fields_missing | passed |
| invalid_public_private_violation.schema.json | adapter_schema_blocked | adapter_schema_blocked | public_ai_private_runtime_access_requested | passed |
| invalid_repository_runtime_scope.schema.json | adapter_schema_blocked | adapter_schema_blocked | runtime_implementation_implied | passed |
| invalid_sensitive_data_required.schema.json | adapter_schema_blocked | adapter_schema_blocked | sensitive_data_required_for_validation | passed |
| valid_businessos_reference.schema.json | adapter_schema_valid_for_design | adapter_schema_valid_for_design | none | passed |
| valid_eduos_non_sensitive.schema.json | adapter_schema_valid_for_design | adapter_schema_valid_for_design | none | passed |

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: adapter_owned_if_businessos
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: validation_only
Notification delivery: none
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Fixture execution: validation_only
Adapter implementation: blocked
Fixture run authority: evidence_only
```

## Operator Note

This report summarizes synthetic fixture validation only. It does not grant runtime, implementation, repository, package, adapter execution, EduOS runtime, or Public AI private runtime authority.
