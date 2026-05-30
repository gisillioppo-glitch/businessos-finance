# OS Core Adapter Schema Checklist v0.1

Date: 2026-05-29

## Status

Closed for contract planning.

## Purpose

This block turns the OS Core branch adapter contract into a practical schema checklist.

The goal is not to create adapter code, create `os-core`, move BusinessOS code, open EduOS implementation, create a repository, or publish shared runtime. The goal is to define what a future adapter must prove before it can be considered valid.

## Checklist Position

```text
BusinessOS: reference branch
EduOS: future consumer, not implemented
OS Core package: not created
Branch adapter contract: drafted
Adapter schema checklist: drafted
Adapter implementation: blocked
Code extraction: blocked
Repository creation: blocked
Public AI runtime access: blocked
```

## Adapter Schema Outcome Values

Every adapter review must end with one outcome:

```text
adapter_schema_pass_for_design
adapter_schema_defer_missing_registry
adapter_schema_defer_missing_validation
adapter_schema_block_public_private_risk
adapter_schema_block_approval_gap
adapter_schema_block_domain_leakage
adapter_schema_block_sensitive_data_requirement
adapter_schema_block_repository_or_runtime_scope
```

Only `adapter_schema_pass_for_design` allows contract design to continue.

It does not allow implementation.

## Required Root Fields

A future adapter schema must include:

| Field | Required | Rule |
| --- | --- | --- |
| `adapter_name` | yes | Branch-neutral identifier. |
| `adapter_version` | yes | Explicit version. |
| `branch_name` | yes | Branch-owned label. |
| `branch_visibility` | yes | Must not imply public access to private runtime. |
| `branch_owner` | yes | Responsible operator or organization role. |
| `supported_core_families` | yes | Explicit list, no implicit enablement. |
| `validation_profile` | yes | How adapter validation runs. |
| `rollback_rule` | yes | How behavior returns to branch-only state. |

## Required Registries

The adapter must define all required registries for any supported family:

| Registry | Required When | Must Include |
| --- | --- | --- |
| `role_registry` | identity, dashboard, approvals | roles, access levels, blocked public roles |
| `page_registry` | dashboard | pages, groups, role allowlists, read-only status |
| `approval_policy` | approvals, actions, delivery, scheduler | approval types, approvers, evidence, states |
| `protected_source_policy` | approvals, demo, automation | source names, blocked demo commands, bypass rules |
| `evidence_registry` | evidence, readiness, demo/pilot | items, source artifacts, freshness, sensitivity |
| `governance_rule_pack` | governance | rules, severity mapping, protected sources |
| `notification_policy` | notifications | recipients, templates, delivery mode, approval rule |
| `readiness_check_registry` | readiness | modules, reports, dashboard pages, daily artifacts |
| `runtime_check_registry` | runtime | smoke profiles, limits, warning thresholds |
| `scheduler_job_registry` | scheduler | jobs, approval requirements, observability |
| `command_summary_adapter` | command synthesis | summary sources, severity mapping, next action inputs |
| `demo_pilot_adapter` | demo/pilot | audiences, commands, pages, evidence, expansion policy |
| `public_boundary_policy` | public surface, Public AI | allowlist, denylist, intake schema, refusal rules |

## Universal Pass Conditions

All adapter schemas must pass:

- root fields are present
- supported families are explicit
- every supported family has its required registry
- private runtime access is denied by default
- Public AI operational access is denied
- approval-gated actions cannot run without approval
- external delivery is disabled or approval-gated
- evidence visibility is explicit
- dashboard action pages are read-only unless approval-gated
- scheduler jobs are observable and approval-aware
- branch-specific labels remain in the adapter
- branch domain logic does not become core logic
- validation can run without sensitive data
- rollback returns behavior to branch-only mode

## Universal Block Conditions

Block adapter schema approval when any are true:

- adapter requires private DB access from Public AI
- adapter requires private report access from public routes
- adapter treats BusinessOS roles as universal
- adapter treats EduOS academic assumptions as BusinessOS behavior
- adapter enables dashboard mutations without approval
- adapter sends external notification without approval
- adapter requires student, teacher, guardian, grade, attendance, or assessment data before EduOS implementation approval
- adapter requires shared database tables before package/repository approval
- adapter lacks rollback
- adapter lacks validation command
- adapter has no explicit owner

## Family Checklist Template

Use this template for each supported family:

```text
family_name:
supported: yes/no
registry_present: yes/no
branch_labels_owned_by_adapter: yes/no
private_data_rule: pass/fail
public_boundary_rule: pass/fail
approval_rule: pass/fail/not_applicable
audit_rule: pass/fail
evidence_rule: pass/fail/not_applicable
validation_command:
rollback_rule:
outcome:
notes:
```

## BusinessOS Future Adapter Checklist

BusinessOS adapter schema must prove:

- finance rules stay BusinessOS-owned
- operations tasks stay BusinessOS-owned
- support incidents stay BusinessOS-owned
- dashboard page copy stays BusinessOS-owned
- approval lifecycle can map through adapter policy
- evidence registry can map through adapter policy
- readiness/runtime checks can map through registries
- public boundary remains deny-by-default
- demo and pilot copy stays BusinessOS-owned

BusinessOS adapter implementation remains blocked.

## EduOS Future Adapter Checklist

EduOS adapter schema must prove:

- no student records are required for planning
- no teacher records are required for planning
- no guardian records are required for planning
- no grades, attendance, assessment, or LMS/SIS/Classroom data are required for planning
- academic labels remain EduOS-owned
- approval policies are planning-only until implementation approval
- evidence registry is planning-only until implementation approval
- dashboard pages are planning-only until implementation approval
- public boundary remains deny-by-default

EduOS adapter implementation remains blocked.

## Public AI Adapter Checklist

Any public-facing adapter must prove:

- public routes cannot read private DB
- public routes cannot read private reports
- Public AI cannot execute CLI commands
- Public AI cannot approve, reject, cancel, or mutate requests
- Public AI cannot trigger notification delivery
- Public AI cannot claim live private runtime status
- public copy is allowlisted
- private runtime terms are denylisted
- public intake is sanitized before handoff

Public AI runtime remains blocked.

## Minimal Validation Commands

Future adapter schema validation should eventually include:

```text
python cli.py adapter-schema-check
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

The `adapter-schema-check` command does not exist yet and is not created in this block.

## Extraction Gate Impact

This checklist satisfies one planning gate:

```text
Adapter schema checklist drafted: yes
```

It does not satisfy:

```text
Adapter implementation: no
Adapter schema validator command: no
OS Core package creation: no
code extraction approval: no
EduOS implementation approval: no
repository creation approval: no
```

## Approved Next Blocks

Recommended sequence:

```text
OS Core Adapter Schema Validator Plan v0.1 (closed)
OS Core Package Ownership and Repository Decision v0.1
EduOS Skeleton Approval Decision Revisit v0.1
OS Core Adapter Schema Validator Implementation Decision v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: checklist_only
Notification delivery: unchanged
Remote publish: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema validator implementation: blocked
Checklist posture: drafted
```

## Validation

Validation for this block:

```text
documentation ASCII check
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

This checklist protects OS Core from becoming a hidden copy of BusinessOS or a premature EduOS implementation. It makes adapters prove boundaries before they get runtime authority.
