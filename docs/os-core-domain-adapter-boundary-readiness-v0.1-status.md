# OS Core Domain Adapter Boundary Readiness v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This note classifies the current BusinessOS domain modules as branch-specific adapters around reusable OS patterns.

The goal is not to extract domain code yet. The goal is to prevent BusinessOS finance, operations, support, rules, and actions from being copied directly into EduOS or a future shared OS Core.

## Product Meaning

BusinessOS now has enough institutional infrastructure to show a clear split:

- OS Core candidates provide shared operating behavior
- BusinessOS domain adapters provide enterprise business meaning
- future EduOS domain adapters should provide academic meaning

This split protects the future OS Platform from becoming a renamed BusinessOS clone.

## Boundary Classification

Classification: branch-specific domain adapters with reusable OS patterns.

Current implementation remains inside BusinessOS.

Future extraction should separate:

- reusable rule evaluation shape
- reusable action recommendation shape
- reusable task/workflow shape
- reusable incident/support shape
- reusable brief/report shape
- branch-specific data models
- branch-specific language
- branch-specific risk semantics
- branch-specific thresholds

## OS Core Pattern Candidates

These patterns are candidates for eventual shared OS Core behavior:

- domain rule registry
- rule result schema
- action recommendation lifecycle
- task/workflow lifecycle
- incident/support lifecycle
- risk severity normalization
- status normalization
- owner/assignee linkage
- domain brief generation shape
- domain report export shape
- audit logging for domain events
- evidence linkage for domain decisions

## BusinessOS-Specific Domain Logic

These parts should remain BusinessOS-specific:

- transactions
- cash flow interpretation
- expense ratio logic
- expense concentration logic
- finance anomaly language
- finance recommended action copy
- operations task categories
- operations escalation rules
- support incident categories
- business support severity rules
- BusinessOS command center wording tied to finance/ops/support

## Future EduOS Domain Analogs

EduOS may eventually use the same adapter pattern with different domain content:

- student records
- course records
- attendance signals
- assignment workflows
- assessment workflows
- academic risk rules
- academic integrity findings
- student support incidents
- teacher support workflows
- guardian communication tasks
- intervention recommendations
- academic command center language

These are analogs only. EduOS implementation should not be added inside BusinessOS.

## Extraction Conditions

Before domain adapters move toward shared OS Core:

- rule inputs must be branch-specific adapters
- rule outputs must use a neutral severity/result schema
- action recommendation status must remain generic
- task and incident statuses must be normalized
- domain copy must be owned by branch configuration
- thresholds must be branch-specific policy
- report labels must be branch-specific
- dashboard pages must read from branch adapters
- command center synthesis must consume neutral summaries
- private data schemas must not be forced into a shared core package

## Current Readiness Assessment

Rule evaluation shape readiness: medium

Action recommendation lifecycle readiness: medium

Operations/task pattern readiness: medium

Support/incident pattern readiness: medium

Brief/report shape readiness: high

BusinessOS domain specialization: keep in BusinessOS

EduOS implementation: planning only, not inside BusinessOS

## Boundaries

This block does not:

- create EduOS
- extract shared OS Core packages
- change finance behavior
- change operations behavior
- change support behavior
- change database schema
- alter command center decisions
- expose private data publicly

## Validation

Validation expected for this block:

```text
docs ASCII check
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```

Expected result:

```text
system-check: passed
release-readiness: ready
runtime-stability: runtime_stable
quick smoke: passed
```
