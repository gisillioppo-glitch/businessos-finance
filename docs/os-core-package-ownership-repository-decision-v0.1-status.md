# OS Core Package Ownership and Repository Decision v0.1

Date: 2026-05-29

## Status

Closed for ownership and repository planning.

## Purpose

This block decides the planning posture for future OS Core package ownership and repository creation.

The goal is not to create an `os-core` package, initialize a repository, create a remote, move BusinessOS code, open shared runtime, implement an adapter, or open EduOS runtime. The goal is to define who owns the future package decision and what must be true before repository work is allowed.

## Decision Summary

```text
future_package_name: os-core
ownership_posture: platform_owned_private_core
repository_posture: deferred_pending_explicit_approval
initial_visibility_if_created: private
package_creation: blocked
repository_creation: blocked
remote_push: blocked
code_extraction: blocked
shared_runtime: blocked
adapter_implementation: blocked
EduOS_runtime: blocked
Public_AI_private_runtime_access: blocked
```

OS Core is approved as a planning concept only.

OS Core is not approved as a code package or repository in this block.

## Ownership Decision

Future OS Core should be owned by the platform layer, not by BusinessOS or EduOS individually.

```text
owner_layer: OS Platform
reference_branch: BusinessOS
future_consumer_branch: EduOS
public_surface_role: denied_private_runtime_access
```

BusinessOS remains the live reference branch.

EduOS remains a future consumer with a local-only skeleton.

Public AI remains outside private runtime authority.

## Repository Decision

Repository creation is deferred.

If approved later, the future repository should be:

```text
repo_name: os-core
visibility: private
remote_creation: requires_explicit_approval
initial_contents: contracts_docs_config_only
runtime_code: blocked_until_extraction_approval
branch_adapters: blocked_until_schema_validator_approval
public_distribution: blocked
```

No `git init`, remote creation, GitHub repository creation, package folder, or package publication is approved here.

## Allowed Future Initial Contents

If repository creation is explicitly approved later, the first repository may include only:

- README
- proprietary notice
- contracts documentation
- adapter schema documentation
- non-sensitive config examples
- validation planning documentation
- no-op placeholders only if separately approved

It must not include:

- copied BusinessOS private runtime code
- BusinessOS database files
- private reports
- secrets
- Streamlit secrets
- notification credentials
- EduOS academic data
- executable shared runtime
- live adapters
- package publishing config

## Package Ownership Rules

Future OS Core ownership must follow these rules:

- OS Core owns branch-neutral operating contracts only.
- Branches own meaning, labels, thresholds, copy, and domain rules.
- BusinessOS owns finance, operations, support, and pilot language.
- EduOS owns academic labels and education domain rules.
- Public AI owns no private runtime authority.
- Adapter contracts are required before any branch can consume core behavior.
- Approval gates are required before action-producing shared behavior.
- Evidence and audit behavior must remain explicit.
- Rollback must return behavior to branch-only operation.

## Repository Creation Blockers

Repository creation remains blocked while any are true:

- explicit repository approval has not been granted
- package ownership has not been accepted by the operator
- adapter schema validator has not been implemented or approved
- BusinessOS reference schema has not been approved
- EduOS non-sensitive adapter posture has not been approved
- extraction candidate tests are incomplete
- public/private boundary enforcement is not validated
- shared runtime would need private BusinessOS data
- shared runtime would imply EduOS implementation
- Public AI would gain private runtime authority

## Future Approval Gate

A future repository approval request must answer:

```text
repo_name:
repo_visibility:
owner:
initial_contents:
excluded_contents:
first_commit_scope:
remote_creation_approved:
package_creation_approved:
runtime_code_approved:
adapter_code_approved:
BusinessOS_code_copy_approved:
EduOS_runtime_approved:
Public_AI_access_approved:
rollback_rule:
validation_before_push:
```

Default answer for runtime, adapter, BusinessOS copy, EduOS runtime, and Public AI access remains `no`.

## BusinessOS Impact

BusinessOS remains unchanged.

This decision does not:

- move BusinessOS code
- change CLI commands
- change dashboard pages
- change database schema
- change reports
- create shared imports
- create shared package dependencies
- expose private runtime

BusinessOS continues as the validated private institutional OS branch.

## EduOS Impact

EduOS remains local-only and non-sensitive.

This decision does not approve:

- EduOS repository creation
- EduOS runtime
- EduOS database
- EduOS dashboard
- EduOS adapters
- EduOS approvals
- EduOS notification delivery
- academic records
- Classroom, LMS, or SIS integration

EduOS may later consume OS Core only after adapter contracts and repository/package gates are approved.

## Public AI Impact

Public AI remains outside private runtime authority.

Blocked:

- private DB access
- private report access
- CLI execution
- approval decisions
- workflow mutation
- notification delivery
- scheduler execution
- live private status claims

Allowed later only as public-boundary planning:

- public claims allowlist
- public denial policy
- intake handoff shape
- sanitized explanation of high-level concepts

## Relationship to Validator Plan

The adapter schema validator plan remains a prerequisite to any implementation.

Recommended dependency order:

```text
package ownership decision
adapter schema validator implementation decision
BusinessOS reference adapter schema planning
EduOS non-sensitive adapter schema planning
repository creation approval
package skeleton approval
code extraction approval
```

This block completes the ownership decision only.

## Extraction Gate Impact

This decision satisfies one planning gate:

```text
OS Core package ownership and repository posture decided: yes
```

It does not satisfy:

```text
OS Core package creation: no
OS Core repository creation: no
remote repository push: no
adapter schema validator implementation: no
adapter implementation: no
code extraction approval: no
EduOS runtime implementation approval: no
Public AI runtime approval: no
```

## Approved Next Blocks

Recommended sequence:

```text
EduOS Skeleton Approval Decision Revisit v0.1
OS Core Adapter Schema Validator Implementation Decision v0.1 (closed)
BusinessOS Reference Adapter Schema Planning v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: no
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none
Approval behavior: ownership_decision_only
Notification delivery: unchanged
Remote publish: blocked
Repository creation: blocked
Package creation: blocked
Code extraction: blocked
Adapter implementation: blocked
Schema validator implementation: blocked
Ownership posture: decided_for_planning
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

This decision keeps OS Core moving from idea toward platform governance without opening a repository too early. The package now has a future owner and repository posture, but no runtime authority.
