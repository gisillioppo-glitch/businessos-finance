# OS Core Approval Extraction Readiness Review v0.1

Date: 2026-05-27

## Status

Closed for architecture validation.

## Purpose

This block reviews whether the BusinessOS approval layer is ready to move from contract/config/test readiness into shared OS Core extraction.

The goal is not to extract `app/approvals`, create an OS Core package, change approval runtime behavior, open EduOS implementation, create shared approval tables, expose approval data publicly, or grant dashboard approval authority. The goal is to make the extraction decision explicit after approvals gained a contract, config boundary, and automated tests.

## Review Inputs

This review follows:

```text
docs/os-core-candidate-contract-review-approvals-v0.1-status.md
docs/os-core-approval-contract-draft-v0.1.md
docs/approval-config-boundary-prep-v0.1-status.md
docs/approval-config-boundary-implementation-v0.1-status.md
docs/os-core-approval-contract-test-plan-v0.1.md
docs/approval-config-boundary-tests-v0.1-status.md
docs/os-core-extraction-contract-draft-v0.1.md
```

It also considers the evidence boundary work because action-producing approvals depend on evidence rules:

```text
docs/os-core-evidence-contract-draft-v0.1.md
docs/evidence-config-boundary-implementation-v0.1-status.md
docs/evidence-registry-contract-tests-v0.1-status.md
```

## Decision

```text
decision: defer_extraction
contract_design_status: ready
config_boundary_status: implemented
test_boundary_status: implemented
extraction_allowed_now: no
next_safe_step: branch_adapter_contract_review
```

Approvals are now ready for deeper platform design, but not for code extraction.

## Why Extraction Is Deferred

Extraction remains deferred because:

- BusinessOS approval runtime still owns the SQLite table directly.
- approval role labels are still branch language.
- approval type meaning is branch-owned and not yet adapterized.
- evidence requirements are documented but not enforced by a shared contract.
- dashboard visibility vs approval authority is documented but not contract-tested.
- Public AI denial is documented but not contract-tested against a public surface.
- notification delivery and pilot expansion approval gates still depend on BusinessOS source modules.
- EduOS approval implementation remains blocked.
- no shared OS Core package boundary exists yet.

## Readiness Strengths

Approvals are stronger than before because:

- branch-neutral lifecycle is drafted.
- request creation shape is documented.
- status update shape is documented.
- authority rule is documented.
- audit expectations are documented.
- BusinessOS config boundary exists.
- config is read-only.
- approval types, statuses, priorities, and protected source modules are covered by tests.
- duplicate request behavior is covered by tests.
- audit on create/update is covered by tests.
- protected `pilot_expansion` source behavior is covered by tests.
- evidence now has its own contract/config/test boundary for future evidence-backed approvals.

## Extraction Gate Review

| Gate | Status | Notes |
| --- | --- | --- |
| Contract documented | pass | Approval contract draft exists. |
| Boundary classification documented | pass | Approval status docs include boundary classification. |
| BusinessOS source behavior validated | pass | Approval tests and approval-report pass. |
| Future branch consumer named | pass_with_blocker | EduOS is named, but implementation remains blocked. |
| Domain adapter boundary documented | partial | Branch-owned approval types are identified, but adapter contract is not drafted. |
| Sensitive data denied by default | pass | No public approval access exists. |
| Approval behavior documented | pass | Authority and lifecycle rules are documented. |
| Evidence behavior documented | partial | Evidence contract exists, but approval evidence enforcement is not implemented. |
| Audit behavior documented | pass | Audit requirements and tests exist. |
| Config shape drafted | pass | BusinessOS config boundary is implemented. |
| Validation command identified | pass | Targeted tests and quick smoke exist. |
| Rollback plan identified | pass | Keep approvals BusinessOS-only. |

## Required Before Extraction Can Reopen

Before approval code extraction can be reconsidered:

1. Draft branch adapter contract for approvals.
2. Define approval evidence requirement enforcement.
3. Add lifecycle contract tests beyond config defaults.
4. Add dashboard authority boundary tests or documented static checks.
5. Add Public AI denial checks for approval data.
6. Define shared package boundary without moving code.
7. Confirm EduOS approval implementation remains blocked or separately approved.
8. Confirm rollback from shared contract to BusinessOS-only remains possible.

## Allowed Next Moves

Allowed:

- documentation-only branch adapter contract review
- approval lifecycle contract tests
- Public AI denial documentation checks
- dashboard authority boundary documentation checks
- OS Core package opening decision as a no-code decision

Not allowed:

- moving `app/approvals` out of BusinessOS
- creating shared approval tables
- adding EduOS approval runtime
- exposing approval records publicly
- letting dashboard display approve requests
- letting Public AI approve requests
- enabling external action without approval evidence

## Current Readiness Assessment

```text
approval contract readiness: ready
approval config boundary readiness: implemented
approval test boundary readiness: implemented
approval extraction readiness: deferred
shared OS Core package readiness: blocked
EduOS approval implementation readiness: blocked
Public AI approval access: blocked
```

## Recommended Next Blocks

```text
OS Core Approval Branch Adapter Contract v0.1 (drafted)
Approval Lifecycle Contract Tests v0.1 (closed)
Public AI Approval Denial Check v0.1
OS Core Package Opening Decision v0.1
EduOS Skeleton Approval Decision Revisit v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: partially
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none
Runtime behavior: none_changed
Approval behavior: extraction_review_only
Notification delivery: unchanged
Remote publish: none
Code extraction: blocked
```

## Validation

Expected validation for this block:

```text
documentation ASCII check
python -m unittest tests.test_approval_config_boundary
python cli.py approval-report
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected result:

```text
approval tests: passed
approval-report: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

Approvals are now mature enough for platform contract design, but not mature enough for extraction. This is good: BusinessOS keeps stability while OS Core gains a clearer map.
