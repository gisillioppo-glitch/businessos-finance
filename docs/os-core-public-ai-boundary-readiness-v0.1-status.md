# OS Core Public AI Boundary Readiness v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This note classifies the Public AI boundary around BusinessOS, future OS branches, and future EduOS.

The goal is not to implement a public AI assistant yet. The goal is to define what a public AI surface may explain, collect, route, and summarize without operating the private OS runtime.

## Product Meaning

BusinessOS now has a mature private institutional operating surface. That increases the risk of accidentally letting a public surface imply or perform private operations.

This boundary keeps the public layer useful without making it operationally dangerous.

## Boundary Classification

Classification: public intake and explanation boundary.

Current implementation remains outside the private BusinessOS runtime.

Future Public AI should separate:

- public explanation
- lead qualification
- demo request intake
- branch education
- controlled intake summarization
- private runtime operations
- private data access
- approval execution
- workflow mutation

## Allowed Public AI Behavior

Public AI may:

- explain BusinessOS at a high level
- explain the OS branch concept
- answer public product questions
- qualify interest using non-sensitive questions
- collect demo request context
- route qualified interest to private intake
- explain public boundaries
- summarize non-sensitive public form responses
- describe what a private demo may cover
- clarify that private operations require protected access

## Prohibited Public AI Behavior

Public AI must not:

- access `finance.db`
- read private reports
- expose dashboard pages
- expose private dashboard screenshots unless approved for public use
- execute CLI commands
- approve or reject approval requests
- mutate workflows
- trigger notification delivery
- inspect secrets
- use credentials
- impersonate users
- reveal internal evidence packets
- summarize private daily close artifacts
- present stale private status as live public truth

## OS Core Public Boundary Candidates

These patterns may become shared OS Core/public-platform behavior:

- public/private route separation
- public intake schema
- public lead qualification schema
- public assistant refusal rules
- public-to-private handoff packet
- sensitive data denial policy
- branch-aware product explanation
- safe demo expectation setting
- public artifact allowlist
- private runtime denylist

## BusinessOS-Specific Public Logic

These parts should remain BusinessOS-specific:

- finance/operations/governance/support product language
- BusinessOS landing copy
- BusinessOS lead intake fields
- BusinessOS demo positioning
- BusinessOS pilot qualification wording
- BusinessOS public proof assets

## Future EduOS Public Analogs

EduOS may eventually use the same public boundary pattern with academic content:

- EduOS public explanation
- school demo request intake
- director or administrator qualification questions
- teacher workflow interest routing
- guardian communication expectation setting
- public academic OS explainer
- safe handoff into private EduOS intake

These are analogs only. EduOS implementation should not be added inside BusinessOS.

## Extraction Conditions

Before Public AI boundary behavior moves toward shared OS Core or OS Platform:

- public routes must be separate from private runtime routes
- public assistant permissions must be deny-by-default
- private file, DB, report, and dashboard access must be impossible from public context
- public copy must be branch-specific
- intake schema must be branch-configurable
- private handoff packets must be sanitized
- public proof assets must be allowlisted
- public status claims must be based on approved public artifacts, not live private state
- escalation into private OS must require protected operator review

## Current Readiness Assessment

Public/private repository split readiness: high

Public surface checklist readiness: high

Lead intake readiness: medium

Public AI assistant readiness: not implemented

Private runtime isolation doctrine readiness: high

BusinessOS public specialization: keep outside private runtime

EduOS implementation: planning only, not inside BusinessOS

## Boundaries

This block does not:

- create Public AI
- create EduOS
- expose private data publicly
- connect an AI assistant to private runtime
- change landing behavior
- change lead intake behavior
- change credentials or secrets
- change repository split

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
