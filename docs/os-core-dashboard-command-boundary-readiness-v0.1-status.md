# OS Core Dashboard Command Boundary Readiness v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This note classifies the current BusinessOS dashboard and command center surfaces as OS Core candidates, BusinessOS-specific views, future EduOS analogs, and extraction conditions.

The goal is not to extract the dashboard or command center code yet. The goal is to make the UI and executive synthesis boundary clear before opening another OS branch.

## Product Meaning

BusinessOS now has a broad private operating surface:

- executive dashboard shell
- command center summary
- readiness views
- system integrity views
- runtime stability views
- notification views
- approval views
- pilot and demo views
- boundary and surface audit views

This creates enough repeated structure to identify what may become reusable OS interface behavior later.

## Boundary Classification

Classification: OS Core candidate with BusinessOS-specific page content.

Current implementation remains inside BusinessOS.

Future extraction should separate:

- reusable protected dashboard shell
- branch-specific navigation registry
- shared read-only status page patterns
- shared executive synthesis layout
- branch-specific metrics, copy, and domain objects
- governance-controlled action visibility

## OS Core Dashboard Candidates

These patterns are candidates for eventual shared OS Core behavior:

- protected private dashboard shell
- page registry and navigation grouping
- role-aware page visibility
- KPI row and status summary presentation
- read-only evidence table presentation
- status severity display
- latest report loading pattern
- dashboard page loader validation
- public/private surface separation
- dashboard readiness page inclusion checks

## OS Core Command Candidates

These command center patterns are candidates for eventual shared OS Core behavior:

- executive synthesis layer
- health state aggregation
- highest-risk selection
- next-best-move summary
- cross-module evidence references
- report export shape
- command-center audit event shape
- read-only executive operating brief

## BusinessOS-Specific Dashboard Logic

These parts should remain BusinessOS-specific unless later generalized carefully:

- finance dashboard metrics
- operations task language
- support incident language
- governance finding copy tied to BusinessOS controls
- pilot expansion wording
- private demo and pilot sales workflow
- notification subjects tied to daily close
- command center risk wording tied to BusinessOS module names

## Future EduOS Analogs

EduOS may eventually reuse the same UI and synthesis shape with different domain pages:

- school dashboard shell
- academic command center
- student risk status
- course progress status
- teacher workload status
- guardian communication status
- intervention approval status
- school daily close status
- academic evidence packet status

These are analogs only. EduOS implementation should not be added inside BusinessOS.

## Extraction Conditions

Before dashboard or command center behavior moves to shared OS Core:

- page registry must become branch-configurable
- role allowlists must be data-driven or policy-driven
- page labels and group names must be branch-specific configuration
- KPI components must accept neutral status objects
- command center aggregation must accept branch-specific adapters
- executive synthesis wording must be configurable by branch
- action buttons must remain governance-gated and disabled by default in read-only views
- report loaders must avoid hard-coded BusinessOS report names in core code
- UI shell must not expose private data through public routes

## Current Readiness Assessment

Dashboard shell readiness: medium

Command center pattern readiness: medium

Read-only status page pattern readiness: high

Role-aware private access readiness: medium

BusinessOS page specialization: keep in BusinessOS

EduOS implementation: planning only, not inside BusinessOS

## Boundaries

This block does not:

- create EduOS
- extract shared OS Core packages
- change dashboard behavior
- change command center behavior
- add new UI actions
- expose private dashboard content publicly
- alter login or access control

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
