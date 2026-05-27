# OS Core Candidate Contract Review - Evidence v0.1

Date: 2026-05-27

## Status

Closed for architecture validation.

## Purpose

This block applies `docs/os-core-contract-checklist-v0.1.md` to the current BusinessOS evidence, daily close, and daily close distribution layer.

The goal is not to extract evidence code, create an OS Core package, change daily close behavior, open EduOS implementation, create shared evidence tables, expose private evidence publicly, or enable external delivery. The goal is to decide whether evidence can move from general OS Core candidate into detailed contract design.

## Candidate

```text
candidate_name: evidence
source_module: app/evidence
contract_family: evidence_packet
current_readiness_level: L2
proposed_outcome: pass_for_contract_design
consumer_branch: future EduOS, after approval
businessos_behavior_validated: yes
eduos_implementation_required: no
public_surface_involved: no
private_data_touched: yes
branch_adapter_required: yes
approval_required: no for read-only evidence, yes for action-producing distribution or disclosure
audit_required: yes
evidence_required: yes
config_required: yes
validation_command: python cli.py evidence-index
rollback_rule: keep evidence BusinessOS-only
```

## Review Outcome

```text
Outcome: pass_for_contract_design
Extraction allowed now: no
```

Evidence passes the checklist for detailed contract design because the current BusinessOS layer already has a reusable institutional evidence packet shape:

- expected evidence registry
- evidence availability checks
- missing evidence counts
- date-based report lookup
- daily close summary generation
- close step status rows
- distribution packet preparation
- role-aware recipient packaging
- notification queue handoff
- audit log on evidence index view/export
- audit log on daily close export
- audit log on distribution view/export

Evidence does not pass for code extraction yet because evidence items, labels, report prefixes, close step language, recipient rules, and delivery copy are still BusinessOS-specific.

## Fast Gate

| Question | Result | Notes |
| --- | --- | --- |
| Branch-neutral purpose | pass | Evidence packets and daily close are reusable institutional patterns. |
| BusinessOS language removable | pass_with_work | Executive, finance, support, governance, and Daily Close labels remain branch wording. |
| Branch-specific meaning adapter-owned | partial | Evidence reports and department package rules are still code-level constants. |
| Private data denied by default | pass | Evidence artifacts remain inside private reports and dashboard surfaces. |
| Public AI operational access blocked | pass | Public AI has no evidence report access or disclosure authority. |
| Approval behavior defined | partial | Read-only evidence needs no approval; disclosure and delivery need approval gates. |
| Validation without new sensitive data | pass | Existing CLI and smoke checks validate current behavior. |
| Rollback path clear | pass | Keep evidence code inside BusinessOS. |

## Contract Strengths

Current strengths:

- `EVIDENCE_REPORTS` defines an expected evidence item registry.
- evidence status is reduced to branch-neutral `available` or `missing`.
- daily close reports summarize completed steps, evidence available, and evidence missing.
- distribution packages separate recipients, evidence items, subject, body, and status.
- distribution queues notifications rather than sending external email directly.
- evidence index, daily close, and distribution export audit events.
- dashboard and CLI can show evidence state without granting mutation authority.
- quick smoke validates evidence-adjacent readiness through system, release, runtime, and daily close schedule checks.

## Contract Gaps

The following gaps block extraction:

- evidence labels are hard-coded in `EVIDENCE_REPORTS`
- report prefixes are BusinessOS-specific
- evidence purposes use executive/business wording
- daily close report title and summary are BusinessOS-specific
- close steps are provided by BusinessOS runtime, not a shared contract
- distribution departments and recipient rules are BusinessOS-specific
- email subject/body copy is BusinessOS-specific
- notification handoff is present, but delivery approval is not part of an evidence contract
- evidence sensitivity and visibility rules are implied, not contract-defined
- freshness rules exist in system/readiness checks, but not as an evidence contract
- tests do not yet isolate evidence registry, missing evidence, or distribution package behavior

## Required Contract Design

Before evidence can move toward shared OS Core, define:

```text
evidence_contract_name:
evidence_contract_version:
branch_id:
evidence_item_registry:
evidence_item_required_fields:
evidence_statuses:
evidence_freshness_rule:
evidence_visibility_rule:
evidence_sensitivity_rule:
close_packet_shape:
close_step_shape:
distribution_packet_shape:
recipient_selector_adapter:
notification_handoff_rule:
disclosure_approval_rule:
public_ai_denial_rule:
audit_event_rules:
validation_profile:
rollback_rule:
```

## Branch Adapter Boundary

Shared OS Core should own:

- evidence item shape
- available/missing status semantics
- date-scoped packet lookup
- close packet structure
- close step structure
- distribution packet structure
- visibility rule hooks
- sensitivity rule hooks
- audit event requirements
- public/private denial rule

BusinessOS should own:

- executive evidence labels
- finance, operations, governance, support, and command center report names
- daily close wording
- department-to-report mapping
- business recipient roles
- notification subject/body copy
- pilot evidence narrative

Future EduOS should own only after approval:

- academic evidence labels
- student progress evidence
- teacher intervention evidence
- assessment review evidence
- guardian communication evidence
- director review packets
- school role visibility rules
- LMS/SIS/Classroom adapter evidence mapping

## Evidence Authority Rule

The future contract should preserve this rule:

```text
Evidence visibility is not disclosure authority.
Dashboard visibility is not export authority.
Distribution packet creation is not external delivery authority.
Public AI is never evidence disclosure authority.
Only an approved, policy-allowed disclosure path can expose private evidence outside the protected branch.
```

## Recommended Follow-Up

```text
OS Core Evidence Contract Draft v0.1
Evidence Config Boundary Prep v0.1
Evidence Registry Contract Tests v0.1
OS Core Approval Extraction Readiness Review v0.1
```

## Boundary Classification

```text
OS Core candidate: yes
BusinessOS-specific: partially
EduOS-specific: planning_only
Public AI boundary: deny_by_default
Sensitive data exposure: none_new
Runtime behavior: none_changed
Approval behavior: review_only
Notification delivery: none_changed
Remote publish: none
Code extraction: blocked
```

## Validation

Expected validation for this block:

```text
documentation ASCII check
python cli.py evidence-index
python cli.py daily-close
python cli.py daily-close-distribution
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected result:

```text
evidence-index: passed
daily-close: passed
daily-close-distribution: passed
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```

## Operator Note

This review makes evidence the next OS Core candidate ready for detailed contract drafting. It does not authorize extraction. BusinessOS remains the live reference branch, and EduOS evidence remains planning-only.
