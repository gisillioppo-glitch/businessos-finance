# OS Core Demo Pilot Boundary Readiness v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This note classifies the current BusinessOS private demo and private pilot methodology as OS Core candidates, BusinessOS-specific go-to-market logic, future EduOS analogs, and extraction conditions.

The goal is not to extract demo or pilot code yet. The goal is to make the operating method reusable without copying BusinessOS-specific sales language or pilot assumptions into future branches.

## Product Meaning

BusinessOS now has a controlled path from readiness to private demo to pilot execution:

- release readiness
- private demo package
- private demo script
- personalized demo script
- private demo dry run
- private demo final review
- private pilot intake
- private pilot plan
- private pilot start gate
- owner confirmation
- daily pilot rhythm
- pilot evidence review
- pilot exit decision
- pilot expansion preparation
- pilot expansion decision
- pilot expansion approval request

This is no longer a loose demo process. It is becoming a repeatable institutional adoption methodology.

## Boundary Classification

Classification: OS Core methodology candidate with BusinessOS-specific content.

Current implementation remains inside BusinessOS.

Future extraction should separate:

- reusable readiness-to-demo gate shape
- reusable demo package structure
- reusable demo script structure
- reusable audience personalization pattern
- reusable pilot intake and plan structure
- reusable owner confirmation chain
- reusable daily pilot evidence rhythm
- reusable exit and expansion decision gates
- branch-specific demo copy, pilot workflows, evidence requirements, and owner roles

## OS Core Demo Candidates

These patterns are candidates for eventual shared OS Core behavior:

- private demo readiness gate
- private demo package artifact
- scripted demo run-of-show
- audience-specific demo emphasis
- demo dry run validation
- final go/no-go demo review
- safe-to-show and do-not-show boundary lists
- dashboard page proof path
- demo command list generation

## OS Core Pilot Candidates

These patterns are candidates for eventual shared OS Core behavior:

- pilot intake artifact
- pilot owner and workflow definition
- 14-day pilot plan shape
- pilot start gate
- owner confirmation packet
- daily pilot tracker
- day-by-day operating rhythm
- evidence completeness review
- exit decision recommendations
- expansion preparation
- expansion decision review
- expansion approval request handoff

## BusinessOS-Specific Demo Pilot Logic

These parts should remain BusinessOS-specific unless later generalized carefully:

- finance/operations/governance/support demo narrative
- BusinessOS private demo proof path
- pilot workflows tied to business operations
- pilot expansion language tied to enterprise workflows
- dashboard pages specific to BusinessOS modules
- command examples tied to BusinessOS CLI labels
- evidence requirements tied to BusinessOS reports
- owner roles and audience modes using BusinessOS vocabulary

## Future EduOS Analogs

EduOS may eventually reuse the same adoption method with different branch content:

- school readiness-to-demo gate
- academic demo package
- director/administrator demo script
- teacher operations demo script
- school pilot intake
- first academic workflow pilot plan
- school owner confirmation
- daily academic pilot tracker
- student-risk evidence review
- academic intervention pilot exit decision
- school expansion preparation
- district or department expansion approval request

These are analogs only. EduOS implementation should not be added inside BusinessOS.

## Extraction Conditions

Before demo or pilot methodology moves to shared OS Core:

- artifact generators must accept branch-specific configuration
- audience modes must be branch-configurable
- demo page lists must come from a branch page registry
- command lists must come from branch capabilities
- pilot workflows must be supplied by branch adapters
- evidence requirements must be policy-driven
- owner confirmation roles must be branch-specific
- expansion decisions must remain advisory until approval-gated
- protected approval requests must remain isolated from demo-safe approval commands
- public/private show boundaries must be explicit for each branch

## Current Readiness Assessment

Demo package pattern readiness: high

Demo script pattern readiness: high

Pilot intake and plan readiness: high

Pilot daily rhythm readiness: medium

Pilot expansion gate readiness: high

BusinessOS demo/pilot specialization: keep in BusinessOS

EduOS implementation: planning only, not inside BusinessOS

## Boundaries

This block does not:

- create EduOS
- extract shared OS Core packages
- change demo behavior
- change pilot behavior
- approve pilot expansion
- enable external delivery
- expose private demo or pilot artifacts publicly
- alter approval gates

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
