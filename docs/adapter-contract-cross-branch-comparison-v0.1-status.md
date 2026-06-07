# Adapter Contract Cross-Branch Comparison v0.1

Date: 2026-06-06

## Status

Closed for cross-branch adapter contract comparison.

## Purpose

This block compares the drafted BusinessOS reference adapter contract and the drafted EduOS non-sensitive adapter contract.

The goal is not to create schema files, implement adapters, create an `os-core` package, create a repository, move BusinessOS code, open EduOS runtime, introduce academic data, connect Classroom/LMS/SIS systems, or grant Public AI private runtime access. The goal is to identify which contract patterns are genuinely shared OS Core candidates and which meanings must remain branch-owned before any schema file decision.

## Inputs

Compared inputs:

```text
docs/businessos-reference-adapter-contract-draft-v0.1-status.md
docs/eduos-non-sensitive-adapter-contract-draft-v0.1-status.md
docs/adapter-schema-validator-adapter-contract-decision-v0.1-status.md
```

## Comparison Position

```text
BusinessOS reference adapter contract: drafted
EduOS non-sensitive adapter contract: drafted
cross-branch comparison: closed
BusinessOS schema file decision: pending
EduOS schema file decision: pending
schema file creation: blocked
adapter implementation: blocked
adapter runtime execution: blocked
OS Core package creation: blocked
OS Core repository creation: blocked
BusinessOS code extraction: blocked
EduOS runtime: blocked
EduOS repository creation: blocked
academic data: blocked
Classroom_LMS_SIS_integration: blocked
Public AI private runtime access: blocked
```

## Executive Comparison

The two drafts share a real branch adapter pattern.

Shared OS Core candidate patterns:

- explicit branch identity
- explicit supported family registry
- explicit role registry posture
- explicit dashboard or page registry posture
- approval policy declaration
- protected source declaration
- evidence visibility declaration
- notification and delivery posture
- readiness and runtime check posture
- scheduler visibility posture
- governance rule pack posture
- command summary posture
- deny-by-default public boundary
- validation without sensitive data
- rollback to branch-local posture
- no runtime authority from validation

BusinessOS-owned meaning:

- finance, operations, support, governance, command center, and executive labels
- BusinessOS dashboard page names
- BusinessOS approval source modules
- BusinessOS evidence source labels
- Daily Close and distribution packet meaning
- notification recipient and template meaning
- private demo and pilot methodology
- release readiness and runtime expectations tied to BusinessOS

EduOS-owned meaning:

- academic roles and role visibility language
- academic command center concepts
- academic close concepts
- academic evidence concepts
- guardian communication concepts
- student support concepts
- assessment, attendance, guardian, student, teacher, and counselor labels
- Classroom/LMS/SIS posture
- academic privacy and sensitive education data denial rules

## Family Comparison

| Family | Shared OS Core Candidate | BusinessOS-Owned | EduOS-Owned | Shared Runtime Allowed |
| --- | --- | --- | --- | --- |
| identity | branch identity fields, version, owner, rollback | `businessos_reference`, private reference branch | `eduos_non_sensitive`, future local-only branch | no |
| dashboard | page registry shape, access posture, mutation default | private BusinessOS dashboard pages | conceptual EduOS academic pages | no |
| approvals | status/priority/source policy shape, approval gates | pilot expansion, notification delivery, privileged access | assessment release, guardian communication, intervention review | no |
| protected sources | explicit protected source registry | BusinessOS operational and delivery sources | academic governance and student support sources | no |
| evidence | evidence category registry, visibility rules | Command Center, alerts, approvals, briefs, Daily Close | academic close, assessment review, support case, intervention plan | no |
| notifications | queue/delivery policy, credential denial, public denial | internal notification outbox and email-ready posture | guardian communication planning posture | no |
| readiness | branch readiness check posture | system-check, release-readiness, dashboard response, area freshness | skeleton scope, no academic data, no runtime, no repo creation | no |
| runtime | runtime status as evidence only | quick/standard/full smoke and runtime stability | runtime blocked, no database, no dashboard | no |
| scheduler | scheduled job visibility and public execution denial | scheduled daily close visibility | future academic close concept only | no |
| governance | rule pack declaration and severity posture | sensitivity rules and BusinessOS governance labels | student privacy and academic sensitivity concepts | no |
| command_center | summary posture and advisory boundary | BusinessOS command synthesis | academic health/support/governance concepts | no |
| demo_pilot | branch-owned methodology and evidence limits | private demo and pilot methodology | not applicable in current EduOS draft | no |
| public_boundary | deny-by-default public boundary and sanitized handoff | no public DB/report/CLI/approval/delivery/scheduler access | no public student/teacher/guardian/grade/attendance/access | no |

## Minimum Common Contract

A future shared adapter schema decision should preserve this minimum common contract:

- explicit adapter identity
- explicit branch identity
- explicit branch visibility
- explicit branch owner
- explicit supported families
- explicit branch-owned labels
- explicit role or conceptual-role posture
- explicit page or conceptual-page posture
- explicit approval and protected source posture
- explicit evidence visibility posture
- explicit notification delivery posture
- explicit readiness and runtime posture
- explicit public boundary denial
- validation without private records, secrets, credentials, or runtime commands
- rollback to branch-local or local-only posture
- no adapter execution authority
- no implementation authority
- no Public AI private runtime authority

## Shared Core Candidate Decision

This comparison supports a future shared schema shape for adapter contracts.

Allowed next design decisions:

```text
BusinessOS Reference Adapter Schema File Decision v0.1
EduOS Non-Sensitive Adapter Schema File Decision v0.1
```

Still not allowed:

```text
schema file creation
adapter implementation
adapter runtime execution
OS Core package creation
OS Core repository creation
BusinessOS code extraction
EduOS runtime
EduOS repository creation
academic data
Classroom/LMS/SIS integration
Public AI private runtime access
```

## Blockers Before Schema File Creation

Schema file creation still requires a separate decision because these questions remain open:

- exact schema file location and naming
- whether both branches should share one schema format or branch-specific schemas
- required root fields versus optional branch fields
- allowed placeholder registries
- synthetic fixture policy for schema validation
- report output policy for cross-branch validation
- whether future config files can live under `config/adapters/`
- how to prevent branch-owned labels from becoming universal OS Core labels
- how to keep EduOS non-sensitive and local-only
- how to keep Public AI outside private runtime

## Extraction Gate Impact

This block satisfies:

```text
BusinessOS contract compared: yes
EduOS contract compared: yes
shared adapter pattern identified: yes
branch-owned meanings identified: yes
schema file decision readiness improved: yes
```

It does not satisfy:

```text
BusinessOS schema file creation: no
EduOS schema file creation: no
adapter implementation: no
adapter runtime execution: no
OS Core package creation: no
OS Core repository creation: no
BusinessOS code extraction: no
EduOS runtime implementation approval: no
EduOS repository creation approval: no
Public AI runtime approval: no
```

## Recommended Next Blocks

Recommended sequence:

```text
BusinessOS Reference Adapter Schema Contract Alignment v0.1 (closed)
EduOS Non-Sensitive Adapter Schema Contract Alignment v0.1 (closed)
Adapter Schema File Cross-Validation Plan v0.1
```

Adapter execution, OS Core packaging, EduOS runtime, academic data, Classroom/LMS/SIS integration, and Public AI private runtime access remain separate and blocked.

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: comparison_only
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: comparison_only
Notification delivery: unchanged
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Adapter implementation: blocked
Adapter runtime execution: blocked
Schema file creation: blocked
Academic data: blocked
Classroom_LMS_SIS_integration: blocked
Implementation authority: none
Runtime authority: none
```

## Validation

Validation for this block:

```text
documentation ASCII check
python cli.py adapter-schema-fixture-run
py_compile
unittest tests.test_adapter_schema_validator
unittest tests.test_adapter_schema_cli
system-check
release-readiness
runtime-stability
quick smoke
```

Expected result:

```text
adapter-schema-fixture-run: passed
unittest: passed
py_compile: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

This comparison is the bridge between contract drafting and schema file decisions. It confirms that BusinessOS and EduOS can share adapter shape, while their domain meaning, data, runtime, dashboards, and approvals remain branch-owned.
