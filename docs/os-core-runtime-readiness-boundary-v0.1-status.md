# OS Core Runtime Readiness Boundary v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Product Meaning

OS Core Runtime Readiness Boundary identifies which system integrity, release readiness, runtime stability, and scheduler capabilities are reusable OS Core candidates before opening EduOS. It separates domain-neutral operational health checks from BusinessOS-specific reports, dashboard pages, landing checks, and daily close expectations.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS runtime and release readiness specialization
- Private data touched: no
- Public surface touched: no
- Approval required: no
- Evidence generated: documentation only
- Audit generated: no
- Reusable core candidate: yes
- Extraction timing: before EduOS implementation, after check registry and schedule configuration hardening

## Scope

- Classify system integrity checks, release readiness gates, runtime stability review, and scheduled close visibility.
- Mark check registries and scheduled jobs as configuration candidates before OS Core extraction.
- Define EduOS runtime/readiness analogs without implementing EduOS logic in BusinessOS.
- Define extraction conditions before moving runtime readiness logic into a future shared OS Core package.
- Update the institutional extraction map and README.

## OS Core Runtime Readiness Candidates

These patterns are reusable across BusinessOS, EduOS, and future verticals:

- module presence checks
- database table readiness checks
- report freshness and latest-artifact checks
- public/private secret boundary checks
- known local artifact handling
- boundary classification coverage checks
- dashboard local response checks
- release readiness status aggregation
- runtime stability status aggregation
- smoke profile size and heavy-command guardrails
- controlled recurring job status visibility

## BusinessOS-Specific Runtime Readiness Logic

These should remain in BusinessOS until another vertical proves the same shape:

- BusinessOS module list
- BusinessOS report prefix list
- Finance database and table expectations
- BusinessOS daily close artifact requirement
- public landing and lead intake file checks
- current dashboard page list
- executive daily close scheduler naming
- BusinessOS demo/pilot readiness language

## Future EduOS Runtime Readiness Analogs

EduOS may later reuse the core runtime readiness layer for:

- EduOS module presence checks
- student/course/teacher table readiness checks
- school daily close artifact freshness
- academic evidence packet freshness
- private school dashboard response checks
- public/private school data boundary checks
- scheduled academic close or intervention review status
- EduOS smoke profile size and heavy-command guardrails

These are planning analogs only. Do not implement EduOS runtime readiness logic inside BusinessOS.

## Extraction Conditions

Runtime readiness logic can move toward shared OS Core when:

- required modules are branch-configurable
- required tables are branch-configurable
- required report prefixes are branch-configurable
- dashboard page checks are configuration-driven
- public/private path checks accept branch-specific public surfaces
- scheduled jobs are registered through a generic job registry
- known local artifacts are policy-driven
- smoke profile limits are configurable per branch
- tests prove a future branch can define its own checks without editing BusinessOS-specific code

## Current Readiness Assessment

```text
System integrity shape readiness: high
Release readiness shape readiness: high
Runtime stability shape readiness: high
Scheduler status visibility readiness: medium
BusinessOS runtime specialization: high
EduOS implementation readiness: planning only
Extraction recommendation: not yet; prepare check registry and job configuration first
```

## Boundaries

- No OS Core package extraction in this block.
- No EduOS implementation.
- No check behavior change.
- No scheduler behavior change.
- No dashboard behavior change.
- No public exposure of private runtime artifacts.

## Validation

Run:

```bash
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```
