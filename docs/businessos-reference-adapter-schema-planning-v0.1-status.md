# BusinessOS Reference Adapter Schema Planning v0.1

Date: 2026-05-30

## Status

Closed for reference schema planning.

## Purpose

This block defines the planning shape for a future BusinessOS reference adapter schema.

The goal is not to create an adapter schema file, create `python cli.py adapter-schema-check`, implement validator code, implement adapters, create an `os-core` package, create a repository, move BusinessOS code, open EduOS runtime, or allow Public AI private runtime access. The goal is to document what the BusinessOS reference adapter schema must contain before executable validation is approved.

## Current Inputs

Current posture:

```text
BusinessOS reference branch: stable
Adapter schema checklist: closed
Adapter schema validator plan: closed
Adapter schema validator implementation decision: closed_not_approved_yet
BusinessOS reference adapter schema: planning_now
EduOS non-sensitive adapter schema: not_planned_yet
OS Core package creation: blocked
Repository creation: blocked
Adapter implementation: blocked
Code extraction: blocked
Public AI private runtime access: blocked
```

BusinessOS is the reference branch only. It is not universal OS Core by itself.

## Planning Decision

```text
BusinessOS_reference_schema_planned: yes
schema_file_created: no
schema_format_selected_for_future: json
future_schema_location_candidate: config/adapters/businessos.adapter.schema.json
schema_runtime_authority: none
validator_command_created: no
adapter_implementation: blocked
OS_Core_package_creation: blocked
EduOS_runtime: blocked
Public_AI_private_runtime_access: blocked
```

The future BusinessOS reference schema should be a non-sensitive JSON configuration artifact.

The location is approved as a planning target only. The file is not created in this block.

## Future Root Fields

The future BusinessOS reference schema should include these root fields:

```text
adapter_name: businessos_reference
adapter_version: 0.1
branch_name: BusinessOS
branch_id: businessos
branch_visibility: private
branch_owner: operator
supported_core_families:
  - identity
  - dashboard
  - approvals
  - evidence
  - readiness
  - runtime
  - scheduler
  - notifications
  - governance
  - command_center
  - demo_pilot
  - public_boundary
validation_profile: planning
rollback_rule: branch_only_businessos_runtime
```

These fields are branch-owned configuration. They do not create shared runtime behavior.

## Future Registries

The future schema should define these registries.

```text
role_registry:
  source: app/security/access_control.py
  roles: admin, executive, viewer
  public_roles: none
  rule: dashboard access is private and role-bound

page_registry:
  source: app/security/access_control.py
  rule: pages remain BusinessOS-owned labels and private dashboard surfaces

approval_policy:
  source: app/approvals/config.py
  statuses: pending, approved, rejected, cancelled
  priorities: low, medium, high, critical
  protected_source_modules: pilot_expansion
  rule: action-producing flows remain approval-aware

protected_source_policy:
  source: app/approvals/config.py
  rule: pilot expansion sources cannot bypass approval gates

evidence_registry:
  source: app/evidence/config.py
  reports: Command Center, Executive Alerts, Approval Decisions, Governance Brief, Support Brief, Daily Finance Brief
  distribution_mode: email_ready_queue
  rule: evidence remains private and report-backed

notification_policy:
  source: app/evidence/config.py and app/notifications
  rule: external delivery remains queued or approval-gated

readiness_check_registry:
  source: app/system/integrity_check.py and app/readiness/release_readiness.py
  rule: system and release checks remain BusinessOS-local

runtime_check_registry:
  source: app/system/runtime_stability.py and scripts/smoke_test.py
  rule: smoke profile limits and heavy command guardrails remain explicit

scheduler_job_registry:
  source: app/scheduler/scheduled_daily_close.py
  rule: scheduled close remains observable and non-public

governance_rule_pack:
  source: app/governance and app/security
  rule: sensitivity and public/private protections remain branch-owned

command_summary_adapter:
  source: app/command_center
  rule: executive summary inputs remain BusinessOS report and status artifacts

demo_pilot_adapter:
  source: app/demo
  rule: private demo and pilot copy remains BusinessOS-owned

public_boundary_policy:
  source: public surface and security checks
  rule: deny private DB, private reports, CLI execution, approval mutation, notification delivery, and live private status claims
```

## Family Posture

```text
identity: schema_planning_only
dashboard: schema_planning_only
approvals: schema_planning_only
evidence: schema_planning_only
readiness: schema_planning_only
runtime: schema_planning_only
scheduler: schema_planning_only
notifications: schema_planning_only
governance: schema_planning_only
command_center: schema_planning_only
demo_pilot: schema_planning_only
public_boundary: schema_planning_only
```

No family is approved for adapter runtime implementation in this block.

## Branch-Owned Labels

These BusinessOS labels must remain in the adapter schema and must not become universal OS Core labels:

- Finance
- Operations
- Governance
- Support
- Assistance
- Daily Close
- Scheduled Close
- Delivery Approval
- Secure Email
- Demo Readiness
- Private Demo
- Pilot Plan
- Pilot Tracker
- Pilot Expansion
- Command Center
- Executive Alerts
- Daily Finance Brief

OS Core may later define neutral slots for these concepts, but BusinessOS wording, copy, source names, and domain meaning remain branch-owned.

## Public Boundary Requirements

The future BusinessOS reference schema must enforce:

```text
public_db_access: denied
public_report_access: denied
public_cli_execution: denied
public_approval_mutation: denied
public_notification_delivery: denied
public_scheduler_execution: denied
public_live_private_status_claims: denied
public_intake_handoff: sanitized_only
```

Public AI remains outside private runtime authority.

## Validation Expectations

When the validator is eventually implemented, the BusinessOS reference schema should pass only if:

- all required root fields are present
- supported families are explicit
- registries exist for each supported family
- registry references use non-sensitive metadata only
- BusinessOS labels remain branch-owned
- no private data rows are required
- no private reports are embedded
- no credentials or secrets are referenced
- approval gates remain explicit
- dashboard actions remain read-only or approval-gated
- external delivery remains queued or approval-gated
- rollback returns to BusinessOS branch-only operation

## Remaining Blockers

Still unresolved after this block:

```text
schema_file_created: no
fixture_policy_approved: no
report_format_finalized: no
failure_semantics_finalized: no
EduOS_non_sensitive_schema_posture_planned: no
adapter_schema_validator_implementation: no
adapter_implementation: no
OS_Core_package_creation: no
repository_creation: no
code_extraction: no
```

## Extraction Gate Impact

This block satisfies:

```text
BusinessOS_reference_schema_planned: yes
schema_format_selected_for_future: json
schema_location_candidate_selected: yes
```

It does not satisfy:

```text
BusinessOS_reference_schema_file_created: no
Adapter schema validator implementation: no
Adapter implementation: no
OS Core package creation: no
OS Core repository creation: no
code extraction approval: no
EduOS runtime implementation approval: no
Public AI runtime approval: no
```

## Recommended Next Blocks

Recommended sequence:

```text
EduOS Non-Sensitive Adapter Schema Planning v0.1 (closed)
Adapter Schema Validator Fixture Policy v0.1
Adapter Schema Validator Report Format and Failure Semantics v0.1
Adapter Schema Validator Implementation Scope v0.1
```

Executable validator implementation should remain blocked until those planning gates are closed.

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: yes
EduOS-specific: no
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: schema_planning_only
Notification delivery: unchanged
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema validator implementation: blocked
Reference schema posture: planned_not_created
```

## Validation

Validation for this block:

```text
documentation ASCII check
py_compile
system-check
release-readiness
runtime-stability
quick smoke
```

Expected result:

```text
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

This block gives the future validator a concrete BusinessOS reference shape without turning BusinessOS into OS Core. The next useful step is to define the EduOS non-sensitive schema posture so the validator can eventually compare more than one branch without opening EduOS runtime.
