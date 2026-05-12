# OS Core Boundary Checklist v0.1

Date: 2026-05-12

## Purpose

This checklist turns the Institutional Core Extraction Map into an operating decision tool.

Use it before adding a new feature, moving logic between modules, or deciding whether a BusinessOS capability should later become part of the reusable OS Core.

The goal is not to extract the core yet. The goal is to keep every new block placed in the right boundary while BusinessOS continues maturing.

## Boundary Options

Every new capability should be classified into one primary boundary:

```text
1. OS Core
2. BusinessOS-specific
3. Future EduOS-specific
4. Public AI boundary
5. Shared candidate, not core yet
```

If the boundary is unclear, mark it as shared candidate and keep it inside BusinessOS until the pattern repeats in another vertical.

## Fast Decision Rule

Use this first:

```text
If the capability would still make sense in EduOS, LegalOS, HealthOS, or another future branch without changing its purpose, it may be OS Core.

If it depends on finance, operations, support, business reporting, pilot sales motion, or enterprise demo language, it is BusinessOS-specific for now.

If it talks to public users, public marketing pages, lead capture, or external AI-facing surfaces, it belongs at the Public AI boundary.
```

## OS Core Checklist

A capability is an OS Core candidate when most of these are true:

- It protects institutional trust.
- It manages roles, permissions, approvals, evidence, audits, notifications, readiness, or system health.
- It can operate without finance-specific terminology.
- It supports multiple future verticals with the same purpose.
- It has stable inputs and outputs that do not depend on a single business domain.
- It strengthens control, traceability, continuity, or governance.
- It can be tested without loading domain-specific sample data.
- It should remain private and internal by default.

Examples from current BusinessOS:

```text
audit
security
people
approvals
governance
notifications
evidence
readiness
system
scheduler
```

Decision:

```text
If yes to most checks, build it as a domain-neutral pattern even if it currently lives inside BusinessOS.
```

## BusinessOS-Specific Checklist

A capability is BusinessOS-specific when most of these are true:

- It depends on finance, operations, support, business owners, executive reporting, or company operating rhythm.
- It uses business-specific KPIs or statuses.
- It creates value primarily for a private company operating system.
- It depends on BusinessOS tables, workflows, language, demo flow, or pilot methodology.
- It would need meaningful rewriting to serve EduOS or another vertical.
- It supports the current product maturity path rather than a platform-level primitive.

Examples from current BusinessOS:

```text
finance rules
operations tasks
support incidents
daily close content
private demo package
private pilot flow
business release readiness language
```

Decision:

```text
Keep it in BusinessOS. Do not extract it until another vertical proves the same shape exists.
```

## Future EduOS Checklist

A capability belongs in future EduOS planning when most of these are true:

- It is about learning, students, teachers, courses, lessons, assessments, progress, or academic operations.
- It needs education-specific roles and institutional policies.
- It would reuse OS Core controls but replace the business domain model.
- It should not be implemented inside BusinessOS except as a note or placeholder.

Potential future EduOS examples:

```text
student progress review
teacher assistance queue
course evidence packet
academic approval workflow
learning risk alerts
school daily close
```

Decision:

```text
Document the idea, but do not build it in BusinessOS yet.
```

## Public AI Boundary Checklist

A capability belongs at the Public AI boundary when most of these are true:

- It is public-facing.
- It handles marketing, landing pages, lead intake, demos, public questions, or external user onboarding.
- It can be separated from private institutional data.
- It must not expose internal database records, reports, evidence, decisions, or audit logs.
- It may use public AI interaction but should only receive sanitized context.
- It should live outside the private repo when it becomes a public surface.

Examples from current ecosystem:

```text
landing website
lead intake
public demo request
public AI explainer
external product FAQ
```

Decision:

```text
Keep public surfaces separate from the private OS runtime. Never move sensitive logic into public code.
```

## Shared Candidate, Not Core Yet

Use this category when a capability looks reusable but is not proven enough.

Common signs:

- It has a reusable shape but current language is BusinessOS-specific.
- It may become platform logic after EduOS validates the same pattern.
- It is useful in more than one module but not yet more than one vertical.
- Extracting now would slow BusinessOS without clear platform benefit.

Examples:

```text
command center synthesis
dashboard page pattern
report export convention
demo readiness flow
pilot operating rhythm
```

Decision:

```text
Keep it inside BusinessOS, name the reusable pattern, and avoid hard-coding new domain assumptions.
```

## Feature Intake Questions

Before starting a new block, answer these:

```text
What boundary owns this?
What data does it touch?
Is the data private, public, or sanitized?
Does it require approval before action?
Does it create evidence or audit history?
Does it need dashboard visibility?
Does it need CLI visibility?
Does it introduce external delivery or public exposure?
Would this still make sense in EduOS?
Is this a feature, a control, or a platform primitive?
```

## Extraction Discipline

Do:

- build in small validated blocks
- keep OS Core candidates domain-neutral where practical
- document boundary decisions
- validate with py_compile, targeted command, quick smoke, or full smoke depending on risk
- commit, push, and tag completed blocks
- stage only explicit files

Do not:

- extract core too early
- add EduOS logic inside BusinessOS
- mix public landing code with private runtime logic
- expose private reports, audit logs, evidence, database paths, or secrets
- use broad staging commands when local files are present
- treat one successful BusinessOS pattern as platform core before repetition proves it

## Recommended Classification Record

For future status documents, use this compact record:

```text
Boundary classification:
- Primary boundary:
- Secondary boundary:
- Private data touched:
- Public surface touched:
- Approval required:
- Evidence generated:
- Audit generated:
- Reusable core candidate:
- Extraction timing:
```

Example:

```text
Boundary classification:
- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS dashboard visibility
- Private data touched: yes
- Public surface touched: no
- Approval required: no
- Evidence generated: report only
- Audit generated: no
- Reusable core candidate: yes
- Extraction timing: after EduOS validates same pattern
```

## Current Rule For BusinessOS

BusinessOS remains the live reference branch.

The operating rule is:

```text
Harden BusinessOS first.
Name reusable patterns as they stabilize.
Keep public AI separate.
Do not open EduOS implementation until the OS Core boundary is clearer.
Extract only after repeated patterns prove themselves.
```

## Completion Criteria

This checklist is complete when:

- new features can be classified before implementation
- OS Core candidates have a conservative decision rule
- BusinessOS-specific logic remains protected from premature extraction
- EduOS remains future-facing, not accidentally embedded
- Public AI boundaries are explicit
- the checklist can be reused in future block status documents

