# Adapter Schema Validator CLI Decision v0.1

Date: 2026-05-30

## Status

Closed for CLI implementation decision.

## Purpose

This block decides whether the adapter schema validator may receive a CLI command in a later implementation block.

The goal is not to edit `cli.py`, create schema files, create fixture files, export adapter schema reports, create adapter runtime, create an `os-core` package, create a repository, open EduOS runtime, introduce academic data, connect Classroom/LMS/SIS adapters, or allow Public AI private runtime access.

## Current Inputs

Current posture:

```text
Adapter schema validator module: implemented_limited
Adapter schema validator tests: implemented_inline_synthetic
CLI command: blocked_until_decision
Schema files: blocked
Fixture files: blocked
Report export: blocked
Adapter implementation: blocked
OS Core package creation: blocked
Repository creation: blocked
EduOS runtime: blocked
Public AI private runtime access: blocked
```

## CLI Decision

```text
cli_command_creation_approved_next_block: yes_limited
cli_command_name_candidate: adapter-schema-check
schema_file_creation_approved: no
fixture_file_creation_approved: no
report_export_creation_approved: no
audit_event_creation_approved: no
adapter_runtime_execution_approved: no
OS_Core_package_creation_approved: no
repository_creation_approved: no
EduOS_runtime_approved: no
Public_AI_private_runtime_access_approved: no
```

The next implementation block may add a read-only CLI command that calls the existing validator module against an explicitly supplied schema path.

This decision does not implement the command yet.

## Allowed Files For Next Block

Allowed:

```text
cli.py
tests/test_adapter_schema_cli.py
```

Optional if needed:

```text
README.md
docs/adapter-schema-validator-cli-implementation-v0.1-status.md
reports/system_integrity_2026-05-30.md
reports/release_readiness_2026-05-30.md
reports/runtime_stability_2026-05-30.md
```

Blocked:

```text
config/adapters/
tests/fixtures/adapter_schema/
reports/adapter_schema_check_YYYY-MM-DD.md
os-core/
eduos/
public/
app/dashboard/
app/notifications/
app/scheduler/
app/approvals/
app/evidence/
```

The next block must not create schema files or fixture files. CLI tests must use temporary files or inline synthetic JSON only.

## Allowed CLI Behavior

The future command may support:

```text
python cli.py adapter-schema-check --schema <path>
python cli.py adapter-schema-check --schema <path> --profile planning
```

Allowed output:

```text
Adapter Schema Check
Overall status
Adapter name
Branch name
Check counts
Blocking reasons
Warnings
Runtime authority: none
Implementation authority: none
```

The command may exit:

```text
0 for adapter_schema_valid_for_design
1 for adapter_schema_valid_with_warnings
2 for adapter_schema_blocked
3 for adapter_schema_invalid_input
```

Exit codes must not authorize implementation or runtime. They only classify design-readiness status for operator review.

## Explicitly Blocked CLI Behavior

The future command must not:

- create default BusinessOS schema files
- create default EduOS schema files
- create fixture files
- export Markdown reports
- write `reports/adapter_schema_check_YYYY-MM-DD.md`
- write audit events
- read finance database contents
- read private reports
- read dashboard session state
- read Streamlit secrets
- mutate approvals
- deliver notifications
- run scheduler jobs
- execute adapters
- create repositories
- create packages
- move BusinessOS code
- initialize EduOS runtime
- create EduOS database, dashboard, or adapters
- read or require academic data
- connect Classroom/LMS/SIS systems
- expose Public AI private runtime access

## Runtime Authority

```text
runtime_authority: none
implementation_authority: none
design_authority: adapter_schema_validation_only
adapter_authority: none
repository_authority: none
package_authority: none
public_ai_authority: none
```

The CLI may make validator results easier to inspect, but it cannot approve implementation, runtime, extraction, publishing, repository creation, package creation, EduOS runtime, adapter execution, or private access.

## Rollback Rule

Rollback for the next implementation block:

```text
remove adapter-schema-check command from cli.py
remove tests/test_adapter_schema_cli.py
return to module-only validator implementation
leave BusinessOS runtime unchanged
```

No database, report, scheduler, notification, approval, adapter, or EduOS rollback should be required because the approved CLI must not mutate runtime state.

## Validation Required For Next Block

The next CLI implementation block must validate with:

```text
py_compile
unittest tests.test_adapter_schema_validator
unittest tests.test_adapter_schema_cli
system-check
release-readiness
runtime-stability
quick smoke
```

If `pytest` becomes available, it may also be used, but it is not required because the current environment does not include it.

## Extraction Gate Impact

This block satisfies:

```text
Adapter schema validator CLI decision: yes_limited
allowed_files_defined: yes
blocked_files_defined: yes
runtime_authority_defined: none
rollback_rule_defined: yes
validation_before_commit_defined: yes
```

It does not satisfy:

```text
CLI command implemented: no
Schema files created: no
Fixture files created: no
Report export implemented: no
Adapter implementation: no
OS Core package creation: no
OS Core repository creation: no
EduOS repository creation: no
EduOS runtime implementation approval: no
Public AI runtime approval: no
```

## Recommended Next Blocks

Recommended sequence:

```text
Adapter Schema Validator CLI Implementation v0.1
Adapter Schema Validator Report Export Decision v0.1
```

Report export remains a separate decision. The CLI implementation must remain read-only and terminal-only unless report export is explicitly approved later.

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: cli_decision_only
Notification delivery: unchanged
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema validator implementation: module_implemented_cli_approved_next_block_limited
Implementation authority: none
Runtime authority: none
```

## Validation

Validation for this block:

```text
documentation ASCII check
py_compile
unittest tests.test_adapter_schema_validator
system-check
release-readiness
runtime-stability
quick smoke
```

Expected result:

```text
unittest: passed
py_compile: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

This decision opens only the next small CLI step. The command may inspect explicit non-sensitive schema files, but it cannot create schemas, export reports, execute adapters, open EduOS, create OS Core, or grant any runtime authority.
