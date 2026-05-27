# OS Core Evidence Contract Draft v0.1

Date: 2026-05-27

## Status

Drafted for architecture validation.

## Purpose

This document defines the first formal evidence contract for future OS Core.

The goal is not to extract `app/evidence`, create an OS Core package, change BusinessOS daily close behavior, open EduOS implementation, create shared evidence tables, expose private reports publicly, or enable external delivery. The goal is to define the branch-neutral evidence contract that future shared code would need to satisfy.

## Contract Identity

```text
contract_name: os_core_evidence_packet
contract_version: v0.1
owning_layer: future OS Core
source_reference: BusinessOS app/evidence
current_state: contract_draft_only
extraction_allowed: no
```

## Contract Purpose

The evidence contract controls private institutional proof packages.

It should answer:

```text
What evidence is expected?
What evidence exists?
What evidence is missing?
How fresh is the evidence?
Who may see it?
What close packet summarizes it?
What distribution packet prepares it?
What audit event proves the evidence lifecycle?
What branch owns the domain meaning?
```

## Branch-Neutral Evidence Item Shape

Future evidence items should support this neutral shape:

```text
evidence_id:
label:
purpose:
file_prefix:
report_path:
status:
required:
freshness_rule:
sensitivity_level:
visibility_scope:
branch_id:
branch_context:
source_module:
source_reference_id:
```

Current BusinessOS supports most of this shape, except:

- `evidence_id`
- `required`
- `freshness_rule`
- `sensitivity_level`
- `visibility_scope`
- `branch_id`
- `branch_context`
- explicit source reference metadata

These are future contract fields, not current migration requirements.

## Evidence Status Contract

Minimum evidence statuses:

```text
available
missing
stale
blocked
```

Rules:

- `available` means the evidence artifact exists and satisfies freshness rules
- `missing` means the expected artifact is absent
- `stale` means the artifact exists but is outside the allowed freshness window
- `blocked` means visibility, approval, or sensitivity rules prevent use
- branch adapters may display branch-specific copy
- branch adapters may not invent unregistered statuses

Current BusinessOS uses `available` and `missing`. `stale` and `blocked` are future contract states.

## Evidence Registry Contract

OS Core should not hard-code BusinessOS evidence items as universal.

Shared core should support a branch registry:

```text
branch_id:
evidence_items:
  - item_id:
    label:
    purpose:
    file_prefix:
    required:
    freshness_rule:
    sensitivity_level:
    visibility_scope:
    allowed_distribution_roles:
```

BusinessOS may register:

- command center summary
- executive alerts
- approval decisions
- governance brief
- support brief
- daily finance brief
- executive evidence index
- executive daily close
- daily close distribution
- pilot evidence packets

Future EduOS may later register, only after approval:

- school daily close
- student progress evidence packet
- teacher intervention evidence
- assessment review evidence
- guardian communication evidence
- director review packet
- LMS/SIS/Classroom adapter evidence

## Evidence Index Contract

Evidence index generation must:

- resolve the report date
- load branch evidence registry
- compute expected evidence items
- resolve report paths without public exposure
- calculate available count
- calculate missing count
- calculate stale count when freshness rules exist
- calculate blocked count when visibility rules prevent use
- write audit event for view/export when a database connection exists
- return a structured summary and item list

Evidence index generation must not:

- expose private report contents publicly
- bypass visibility rules
- send external notifications
- approve disclosure
- mutate source workflow state
- require EduOS academic data before EduOS is approved

## Close Packet Contract

Close packet generation should support this neutral shape:

```text
close_packet_id:
date:
branch_id:
completed_steps:
total_steps:
evidence_available:
evidence_missing:
evidence_stale:
evidence_blocked:
close_steps:
evidence_index_reference:
report_path:
```

Close step shape:

```text
step_id:
name:
status:
detail:
required:
source_module:
```

Rules:

- close packets summarize evidence, not raw private content
- close steps must be branch-configurable before extraction
- missing required evidence may block readiness or pilot continuation
- close packet export must create audit evidence
- close packet visibility does not authorize external disclosure

## Distribution Packet Contract

Distribution packet generation should support this neutral shape:

```text
distribution_packet_id:
date:
branch_id:
delivery_mode:
recipients_count:
packages:
evidence_index_reference:
report_path:
```

Recipient package shape:

```text
recipient_identity:
recipient_role:
recipient_group:
visibility_scope:
evidence_items:
status:
missing_count:
message_subject:
message_body:
```

Rules:

- distribution may prepare packages
- distribution may queue internal notifications only through a branch-approved handoff
- distribution must not send external delivery by itself
- disclosure outside the private branch requires explicit policy and approval
- branch adapters own recipient selection, message copy, and role labels

## Evidence Authority Contract

The authority rule is:

```text
Evidence visibility is not disclosure authority.
```

Non-authorities:

- dashboard display
- CLI index output
- daily close report generation
- distribution packet creation
- notification queue visibility
- Public AI
- demo script wording
- pilot recommendation

These surfaces may show or prepare evidence context. They do not disclose private evidence outside the protected branch.

## Sensitivity And Visibility Contract

Each evidence item should define:

```text
sensitivity_level:
visibility_scope:
public_visibility:
requires_approval_for_external_disclosure:
allowed_internal_roles:
redaction_required:
```

Default rule:

```text
Private evidence remains private unless explicitly sanitized, allowlisted, and approved for disclosure.
```

## Audit Contract

Required audit events:

```text
evidence_index_viewed
evidence_index_exported
daily_close_exported
daily_close_distribution_viewed
daily_close_distribution_exported
```

Optional branch events:

```text
evidence_registry_loaded
evidence_freshness_checked
evidence_visibility_blocked
evidence_distribution_queued
evidence_disclosure_denied
```

Audit metadata should include:

- report date
- branch id
- report path
- evidence counts
- missing count
- stale count when available
- blocked count when available
- recipient count when relevant
- queued notification count when relevant

## Branch Adapter Boundary

OS Core may own:

- evidence item shape
- status semantics
- date-scoped lookup
- evidence count summary
- close packet shape
- close step shape
- distribution packet shape
- sensitivity and visibility hooks
- audit event requirements
- public/private denial rule

Branch adapters must own:

- evidence registry
- report prefixes
- branch labels
- branch roles
- close step definitions
- recipient selection
- distribution copy
- dashboard labels
- branch-specific readiness meaning
- branch-specific evidence sensitivity

## BusinessOS Adapter Responsibilities

BusinessOS remains responsible for:

- executive evidence labels
- finance, operations, governance, support, approval, alert, and command center report names
- daily close wording
- department-to-report mapping
- business user roles
- notification subject/body copy
- pilot evidence narrative
- current SQLite table ownership
- current dashboard page behavior

## Future EduOS Adapter Responsibilities

EduOS may later define:

- academic evidence item registry
- teacher/director/guardian role labels
- student progress evidence rules
- assessment evidence rules
- school daily close labels
- LMS/SIS/Classroom evidence adapters
- school-specific visibility and sensitivity rules

EduOS evidence implementation is not opened by this contract.

## Public AI Boundary

Public AI may:

- explain that evidence packets exist
- describe non-sensitive public product concepts
- collect public interest or intake context
- route requests inward

Public AI must not:

- read private evidence reports
- list private evidence items
- summarize daily close artifacts
- disclose report paths containing private state
- generate evidence packets
- queue distribution
- send external delivery
- inspect private pilot evidence
- access EduOS academic evidence

## Validation Contract

Current BusinessOS validation:

```text
python cli.py evidence-index
python cli.py daily-close
python cli.py daily-close-distribution
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Future contract validation should add targeted checks for:

- registry loading
- available evidence detection
- missing evidence detection
- stale evidence detection
- required evidence blocking
- visibility denial
- distribution packet generation
- notification handoff without external send
- audit on view/export
- Public AI denial boundary

## Rollback Rule

Until extraction is explicitly approved:

```text
Keep evidence code inside BusinessOS.
Keep BusinessOS report ownership unchanged.
Keep EduOS evidence implementation blocked.
Keep OS Core package creation blocked.
```

If future contract design creates instability, rollback by returning to:

```text
BusinessOS-only evidence index
BusinessOS-only daily close
BusinessOS-only distribution packet
documentation-only OS Core evidence contract
no shared package
no shared database
```

## Current Readiness

```text
BusinessOS evidence packet maturity: high
BusinessOS daily close maturity: high
BusinessOS distribution maturity: medium
OS Core contract design readiness: ready
Evidence config boundary readiness: next
Code extraction readiness: blocked
EduOS evidence implementation readiness: blocked
Public AI evidence disclosure authority: blocked
```

## Recommended Next Blocks

```text
Evidence Config Boundary Prep v0.1 (closed)
Evidence Config Boundary Implementation v0.1
Evidence Registry Contract Tests v0.1
OS Core Approval Extraction Readiness Review v0.1
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
Approval behavior: contract_only
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
system-check
release-readiness
runtime-stability
quick smoke
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

This contract gives evidence a reusable institutional shape without moving private evidence out of BusinessOS. The right next move is evidence configuration boundary preparation, not extraction.
