# OS Core Approval Boundary Readiness v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Product Meaning

OS Core Approval Boundary Readiness identifies which approval capabilities are now stable enough to treat as reusable OS Core candidates before opening EduOS. It also separates BusinessOS pilot expansion approval logic from domain-neutral approval primitives so future verticals do not inherit business-specific workflow assumptions.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS approval specialization
- Private data touched: no
- Public surface touched: no
- Approval required: no
- Evidence generated: documentation only
- Audit generated: no
- Reusable core candidate: yes
- Extraction timing: before EduOS implementation, after BusinessOS approval workflow hardening

## Scope

- Classify the approval lifecycle into reusable core primitives and BusinessOS-specific specialization.
- Mark demo-safe approval behavior as an OS Core safety requirement.
- Define EduOS approval analogs without implementing EduOS logic in BusinessOS.
- Define extraction conditions before moving approval code into a future shared OS Core package.
- Update the institutional extraction map and README.

## OS Core Approval Candidates

These patterns are reusable across BusinessOS, EduOS, and future verticals:

- approval request schema shape
- pending, approved, rejected, cancelled lifecycle
- approver/requester roles
- approval type and priority
- source module and source reference linkage
- deduplication by title and source reference
- status justification
- audit log on request creation and decision update
- report and dashboard visibility
- demo-safe guardrails that exclude protected request sources

## BusinessOS-Specific Approval Logic

These should remain in BusinessOS until another vertical proves the same shape:

- pilot expansion approval gate prep
- pilot expansion approval request draft
- pilot expansion approval request creation
- pilot expansion dashboard approval pages
- private demo and pilot language
- business daily close delivery approval context
- current executive-owner wording and business role labels

## Future EduOS Approval Analogs

EduOS may later reuse the core approval layer for:

- academic policy exceptions
- grade or assessment change approvals
- restricted student record access
- intervention plan approval
- guardian or director acknowledgement
- external communication approval

These are planning analogs only. Do not implement EduOS approval logic inside BusinessOS.

## Extraction Conditions

Approval logic can move toward shared OS Core when:

- approval types are configurable per vertical
- protected source modules are policy-driven, not hard-coded
- role labels are branch-configurable
- request source metadata is domain-neutral
- dashboard approval views accept branch-specific labels through configuration
- report language separates core status from vertical context
- tests prove default demo flows cannot mutate protected requests

## Current Readiness Assessment

```text
Approval lifecycle core readiness: high
Approval UI core readiness: medium
Approval report core readiness: medium
BusinessOS pilot specialization: high
EduOS implementation readiness: planning only
Extraction recommendation: not yet; prepare config boundary first
```

## Boundaries

- No OS Core package extraction in this block.
- No EduOS implementation.
- No approval status mutation.
- No controlled expansion approval.
- No public exposure of private approval artifacts.
- No dashboard behavior change.

## Validation

Run:

```bash
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```
