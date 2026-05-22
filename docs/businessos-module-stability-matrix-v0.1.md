# BusinessOS Module Stability Matrix v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Purpose

This matrix summarizes BusinessOS module stability, integration maturity, OS Core readiness, and next architectural action before opening EduOS.

The goal is not to extract code or create EduOS yet. The goal is to identify which parts of BusinessOS are stable reference patterns, which parts need adapter work, and which parts must remain BusinessOS-specific.

## Stability Scale

| Level | Meaning | Action |
| --- | --- | --- |
| Stable | Validated repeatedly and integrated across system checks, dashboard, reports, or smoke profile. | Keep hardening; safe as reference pattern. |
| Maturing | Functional and validated, but still coupled to BusinessOS-specific naming, data, or workflow. | Document adapter boundary before extraction. |
| Branch-specific | Correct for BusinessOS but not reusable as-is. | Keep inside BusinessOS. |
| Future-only | Documented as future pattern, not implemented. | Do not build until branch exists. |

## Module Matrix

| Area | Current Module(s) | Stability | OS Core Readiness | Integration Evidence | Next Action |
| --- | --- | --- | --- | --- | --- |
| Audit | `audit` | Stable | L2 | Used across system events, readiness, approvals, and reports. | Prepare domain-neutral metadata later. |
| Security | `security` | Stable | L2 | Private dashboard login, protected config, public/private boundary checks. | Keep branch-aware role policy explicit. |
| People | `people` | Stable | L2 | Dashboard People page and identity/access records. | Generalize role vocabulary only when EduOS branch exists. |
| Approvals | `approvals` | Stable | L2 | Approval lifecycle, protected pilot expansion request guard, reports. | Keep approval types configurable before extraction. |
| Governance | `governance` | Stable | L2 | Governance brief, sensitivity rules, policy controls, audits. | Separate shared policy engine from BusinessOS rule packs. |
| Notifications | `notifications` | Stable | L2 | Outbox, statuses, delivery approval, dashboard visibility. | Keep delivery adapters branch-specific. |
| Evidence | `evidence` | Stable | L2 | Evidence index, daily close, distribution, dashboard visibility. | Move toward configurable evidence registry later. |
| Readiness | `readiness` | Stable | L2 | Release readiness, demo readiness, boundary coverage, dashboard summaries. | Keep checks registry-based before extraction. |
| System/runtime | `system` | Stable | L2 | System integrity, runtime stability, smoke profile guardrails. | Keep branch registry and artifact policy explicit. |
| Scheduler | `scheduler` | Maturing | L2 | Scheduled daily close status, dashboard visibility, smoke coverage. | Generalize recurring job registry later. |
| Dashboard | `dashboard` | Maturing | L1 | Broad private UI with read-only operational pages. | Define branch page registry before extraction. |
| Command center | `command_center` | Maturing | L1 | Executive synthesis across Finance/Ops/Gov/Support. | Convert to neutral summary adapters later. |
| Demo/pilot | `demo` | Stable methodology, BusinessOS-specific content | L1 | Demo package, script, pilot chain, expansion gates. | Keep methodology reusable, content branch-owned. |
| Reports | `reports` | Stable | L1/L2 utility | Daily reports, readiness reports, close artifacts. | Consider shared report history conventions later. |
| Finance actions | `actions` | Branch-specific | L0 | Recommended finance actions and status lifecycle. | Keep inside BusinessOS; extract only generic action lifecycle later. |
| Financial rules | `rules` | Branch-specific | L0 | Financial risk/anomaly rules. | Keep inside BusinessOS; do not copy into EduOS. |
| Ingest | `ingest` | Branch-specific | L0 | CSV finance ingestion. | Keep inside BusinessOS. |
| Operations | `operations` | Maturing | L1 | Ops tasks, escalations, briefs, dashboard pages. | Treat as workflow adapter pattern. |
| Support | `support` | Maturing | L1 | Incidents, support brief, support dashboard. | Treat as incident/support adapter pattern. |
| Public surface | `public` / landing repo | Stable boundary | Platform/public layer | Landing, lead intake, public surface checklist. | Keep public surface separate from private runtime. |

## Integration Health

Current integration posture:

- system-check validates required modules, database tables, reports, boundaries, and coverage
- release-readiness validates demo/release posture
- runtime-stability validates quick/standard/full smoke profile constraints
- dashboard exposes key private operational views
- smoke quick profile validates high-value paths quickly
- boundary classification coverage is complete for status docs

Current operating status:

```text
BusinessOS private OS reference: stable
BusinessOS commercial v1 readiness: maturing
OS Core extraction readiness: medium
EduOS opening readiness: concept-ready, implementation-not-yet
```

## Extraction Risk Summary

Low extraction risk:

- audit event shape
- readiness check shape
- system integrity framework shape
- notification outbox lifecycle
- approval lifecycle
- evidence packet pattern

Medium extraction risk:

- dashboard shell
- command center synthesis
- demo/pilot methodology
- scheduler recurring jobs
- operations workflow model
- support incident model

High extraction risk:

- finance rules
- finance actions
- finance ingest
- BusinessOS-specific copy
- hard-coded report names
- module-specific dashboard page labels

## EduOS Readiness Impact

This matrix indicates EduOS can move to concept architecture soon, but should not begin implementation until:

- branch adapter contracts are clearer
- EduOS domain model is documented separately
- dashboard page registry shape is defined
- command center adapter shape is defined
- private/public boundaries remain explicit
- no BusinessOS finance logic is copied into EduOS

## Recommended Next Blocks

```text
EduOS Opening Readiness Checklist v0.1
EduOS Concept Architecture v0.1
```

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
