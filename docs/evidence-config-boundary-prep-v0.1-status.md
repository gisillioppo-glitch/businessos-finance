# Evidence Config Boundary Prep v0.1

Date: 2026-05-27

## Status

Closed for architecture validation.

## Purpose

This block prepares the configuration boundary for the BusinessOS evidence layer.

The goal is not to change evidence runtime behavior, extract code, create an OS Core package, open EduOS implementation, create shared evidence tables, change daily close behavior, expose private reports, or send external delivery. The goal is to identify which evidence constants and branch-specific meanings must become configurable before evidence can move closer to shared OS Core.

## Current Hard-Coded Evidence Inputs

Current BusinessOS evidence constants:

```text
EVIDENCE_REPORTS:
- Command Center -> command_center
- Executive Alerts -> executive_alerts
- Approval Decisions -> approval_decisions
- Governance Brief -> governance_brief
- Support Brief -> support_brief
- Daily Finance Brief -> daily_brief

DEPARTMENT_REPORTS:
- Executive -> Command Center, Executive Alerts, Approval Decisions, Governance Brief, Support Brief, Daily Finance Brief
- Finance -> Daily Finance Brief, Command Center, Executive Alerts
- Operations -> Command Center, Executive Alerts, Approval Decisions
- Governance -> Governance Brief, Approval Decisions, Executive Alerts
- Support -> Support Brief, Executive Alerts, Command Center
```

Current BusinessOS branch-owned values also include:

- `Executive Evidence Index` title
- `Executive Daily Close` title
- `Daily Close Distribution` title
- `email_ready_queue` delivery mode
- `BusinessOS Daily Close` message subject
- distribution message body copy
- business department names
- business access levels
- report file prefixes
- evidence purpose copy
- dashboard labels
- pilot evidence narrative

## Config Boundary Decision

Evidence should move toward config boundary before extraction.

Decision:

```text
evidence statuses: future OS Core default
evidence item shape: future OS Core default
evidence registry: branch config
report prefixes: branch config
evidence labels: branch config
evidence purpose copy: branch config
close packet title/copy: branch config
distribution recipient mapping: branch config
distribution message copy: branch config
sensitivity and visibility rules: branch config
notification handoff: branch adapter
external disclosure: approval-gated branch policy
```

## Proposed Future Config Shape

Future branch config may use a shape like:

```text
branch_id: businessos
evidence:
  statuses:
    - available
    - missing
    - stale
    - blocked
  evidence_items:
    - item_id: command_center
      label: Command Center
      file_prefix: command_center
      purpose: Unified executive system summary.
      required: true
      freshness_rule: same_day
      sensitivity_level: internal
      visibility_scope:
        - admin
        - executive
    - item_id: approval_decisions
      label: Approval Decisions
      file_prefix: approval_decisions
      purpose: Approval outcomes, decisions, and justifications.
      required: true
      freshness_rule: same_day
      sensitivity_level: restricted
      visibility_scope:
        - admin
        - executive
        - governance
  close_packet:
    title: Executive Daily Close
    evidence_index_label: Executive Evidence Index
  distribution:
    delivery_mode: email_ready_queue
    recipient_groups:
      Executive:
        reports:
          - Command Center
          - Executive Alerts
          - Approval Decisions
          - Governance Brief
          - Support Brief
          - Daily Finance Brief
      Finance:
        reports:
          - Daily Finance Brief
          - Command Center
          - Executive Alerts
    message:
      subject_template: BusinessOS Daily Close - {date}
      body_template_id: businessos_daily_close_summary
```

This shape is not implemented in this block.

## Migration Order

Future safe order:

1. Document config shape.
2. Add BusinessOS-only evidence config module or file.
3. Keep current constants as compatibility defaults.
4. Add read-only config accessor.
5. Add targeted tests for default evidence registry.
6. Move evidence registry lookups behind config accessor.
7. Move distribution department mappings behind config accessor.
8. Move subject/body template lookup behind config accessor.
9. Keep report filenames unchanged.
10. Keep notification queue behavior unchanged.
11. Keep database schema unchanged.
12. Keep dashboard behavior unchanged.
13. Validate with evidence-index, daily-close, daily-close-distribution, system-check, release-readiness, runtime-stability, and quick smoke.

## Do Not Move Yet

Do not move these in the next code block without explicit approval:

- evidence report generation mechanics
- daily close export behavior
- daily close distribution queue behavior
- notification outbox schema
- people/user schema
- dashboard evidence pages
- pilot evidence logic
- EduOS evidence analogs
- OS Core shared package
- Public AI evidence access
- external delivery

## Required Future Tests

Future config boundary tests should prove:

- default BusinessOS evidence items remain unchanged
- all expected evidence items resolve to the same report prefixes
- existing available/missing behavior remains unchanged
- daily close references the same evidence index path
- distribution recipients receive the same report sets
- notification queue handoff is unchanged
- audit events remain present
- private evidence remains unavailable to public surfaces
- report output remains stable for the sample DB

## Extraction Impact

This prep reduces extraction risk by separating:

- OS Core evidence mechanics
- BusinessOS evidence meaning
- future EduOS evidence meaning
- Public AI denial boundary
- disclosure approval boundary

It does not make extraction ready yet.

## Current Readiness

```text
evidence contract readiness: drafted
config boundary readiness: prepared
runtime config implementation: not_started
code extraction readiness: blocked
EduOS evidence implementation: blocked
Public AI evidence disclosure: blocked
external delivery authority: blocked
```

## Recommended Next Blocks

```text
Evidence Config Boundary Implementation v0.1 (closed)
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
Approval behavior: config_boundary_prep_only
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

This block prepares the next engineering move. The next safe implementation would add a BusinessOS-only evidence config boundary while keeping current behavior exactly the same.
