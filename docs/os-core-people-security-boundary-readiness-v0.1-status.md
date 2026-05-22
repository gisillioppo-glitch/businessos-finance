# OS Core People Security Boundary Readiness v0.1

Date: 2026-05-22

## Status

Closed for MVP validation.

## Product Meaning

OS Core People Security Boundary Readiness identifies which identity, access level, role, and dashboard access-control capabilities are reusable OS Core candidates before opening EduOS. It separates the domain-neutral institutional identity layer from BusinessOS-specific roles, departments, dashboard pages, and demo navigation.

## Boundary Classification

- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS people and dashboard access specialization
- Private data touched: no
- Public surface touched: no
- Approval required: no
- Evidence generated: documentation only
- Audit generated: no
- Reusable core candidate: yes
- Extraction timing: before EduOS implementation, after role/page configuration hardening

## Scope

- Classify people records, user status, access levels, role validation, and dashboard navigation access.
- Mark branch-specific roles and page lists as required before OS Core extraction.
- Define EduOS people/security analogs without implementing EduOS logic in BusinessOS.
- Define extraction conditions before moving people/security logic into a future shared OS Core package.
- Update the institutional extraction map and README.

## OS Core People And Security Candidates

These patterns are reusable across BusinessOS, EduOS, and future verticals:

- institutional user identity records
- normalized email identity key
- active, inactive, pending, suspended status lifecycle
- access level model
- manager or hierarchy reference
- duplicate user protection
- audit log on user creation and duplicate skip
- credential validation boundary
- role-based dashboard page allowlist
- default role resolution
- private dashboard protection

## BusinessOS-Specific People And Security Logic

These should remain in BusinessOS until another vertical proves the same shape:

- Executive Owner, Finance Manager, Operations Manager, and Support Manager defaults
- Finance, Operations, Support, and Executive departments
- current BusinessOS dashboard page names
- private demo and pilot navigation pages
- business role labels and current access assumptions
- local MVP login wording and dashboard UX assumptions

## Future EduOS People And Security Analogs

EduOS may later reuse the core people/security layer for:

- student identity records
- teacher and coordinator roles
- director or school administrator roles
- guardian or family contact relationships
- academic department or grade-level groupings
- student-record access controls
- role-based dashboards for school operations

These are planning analogs only. Do not implement EduOS people or security logic inside BusinessOS.

## Extraction Conditions

People and security logic can move toward shared OS Core when:

- role labels are branch-configurable
- department/group labels are branch-configurable
- dashboard page access lists are configuration-driven
- access levels are mapped to branch-specific role policies
- identity schema separates core user fields from vertical profile fields
- authentication settings remain environment-protected
- tests prove a future branch can define its own roles and page allowlist

## Current Readiness Assessment

```text
Identity record core readiness: high
User status lifecycle readiness: high
Access level readiness: medium
Dashboard access control readiness: medium
BusinessOS people specialization: high
EduOS implementation readiness: planning only
Extraction recommendation: not yet; prepare role and page configuration first
```

## Boundaries

- No OS Core package extraction in this block.
- No EduOS implementation.
- No login behavior change.
- No dashboard access behavior change.
- No user data mutation.
- No public exposure of private people or access-control artifacts.

## Validation

Run:

```bash
python cli.py system-check
python cli.py release-readiness
python cli.py runtime-stability
python scripts/smoke_test.py quick
```
