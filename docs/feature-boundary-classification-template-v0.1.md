# Feature Boundary Classification Template v0.1

Date: 2026-05-12

## Purpose

This template standardizes how new BusinessOS blocks record their boundary classification.

Use it when creating a new status document or closing a feature block. It keeps the OS Core boundary, BusinessOS-specific scope, future EduOS scope, and Public AI boundary visible without slowing down implementation.

## When To Use

Use this template for:

- new dashboard pages
- new CLI commands
- new reports
- new workflow modules
- new approval, evidence, readiness, notification, or scheduler capabilities
- architecture and doctrine documents that affect future extraction
- any block that touches private data, public surfaces, or external delivery

For very small documentation-only changes, include at least the compact classification record.

## Compact Classification Record

Copy this block into future status documents:

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

## Full Status Document Template

Use this full version for meaningful feature blocks:

```text
# [Block Name] v0.1

## Product Meaning

[Explain what this block makes possible in plain product language.]

## Boundary Classification

- Primary boundary:
- Secondary boundary:
- Private data touched:
- Public surface touched:
- Approval required:
- Evidence generated:
- Audit generated:
- Reusable core candidate:
- Extraction timing:

## Current Capabilities

- [Capability 1]
- [Capability 2]
- [Capability 3]

## Safety Boundary

[Explain what this block does not do, what it does not expose, and what remains controlled elsewhere.]

## Integration

- CLI:
- Dashboard:
- Reports:
- Database:
- Governance:
- Notifications:
- Public surface:

## Validation

- Passed:
- Passed:
- Passed:

## Git Closure

- Commit:
- Tag:
- Push:
- Final Git status:

## Next Step

[Recommended next block.]
```

## Boundary Field Guide

### Primary boundary

Pick one:

```text
OS Core candidate
BusinessOS-specific
Future EduOS-specific
Public AI boundary
Shared candidate, not core yet
Documentation / architecture
```

Use the most direct owner. A dashboard page showing BusinessOS-only data is usually BusinessOS-specific. A dashboard pattern that could become a shell standard may have a secondary shared candidate classification.

### Secondary boundary

Use when the feature has a relevant cross-boundary relationship.

Examples:

```text
BusinessOS dashboard visibility
OS Core evidence pattern
Public AI separation requirement
Future EduOS reference only
Shared report export pattern
```

### Private data touched

Use:

```text
yes
no
read-only
sanitized only
```

If yes, name the data area in the Safety Boundary or Integration section.

### Public surface touched

Use:

```text
yes
no
public docs only
landing only
sanitized export only
```

If yes, confirm that private runtime data is not exposed.

### Approval required

Use:

```text
yes
no
future
read-only only
```

If yes, specify whether approval is required before state mutation, external delivery, public exposure, or executive action.

### Evidence generated

Use:

```text
yes
no
report only
future
```

If evidence is generated, name the report or artifact.

### Audit generated

Use:

```text
yes
no
future
existing audit only
```

If no audit is generated for a mutating feature, explain why.

### Reusable core candidate

Use:

```text
yes
no
partial
not yet
```

Mark `partial` when the shape is reusable but the current implementation still contains BusinessOS language or assumptions.

### Extraction timing

Use one concise phrase:

```text
not planned
after EduOS validates same pattern
after second vertical repeats pattern
after security hardening
after public/private boundary review
remain BusinessOS-specific
```

## Example: Dashboard Page

```text
Boundary classification:
- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared dashboard pattern candidate
- Private data touched: read-only
- Public surface touched: no
- Approval required: no
- Evidence generated: report only
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats pattern
```

## Example: Approval Workflow

```text
Boundary classification:
- Primary boundary: OS Core candidate
- Secondary boundary: BusinessOS-specific decision context
- Private data touched: yes
- Public surface touched: no
- Approval required: yes
- Evidence generated: yes
- Audit generated: yes
- Reusable core candidate: yes
- Extraction timing: after EduOS validates same pattern
```

## Example: Landing Page Change

```text
Boundary classification:
- Primary boundary: Public AI boundary
- Secondary boundary: BusinessOS lead intake
- Private data touched: no
- Public surface touched: yes
- Approval required: no
- Evidence generated: no
- Audit generated: no
- Reusable core candidate: no
- Extraction timing: keep outside private runtime
```

## Closeout Checklist

Before closing a block, confirm:

- the boundary classification is included in the status document
- private data exposure is explicitly described
- public surface impact is explicitly described
- approval and audit behavior are clear
- validation matches the risk level of the block
- commit, push, and tag are complete
- only intended files were staged
- `BussinessOS Avance.pdf` remains untracked and untouched

## Operating Rule

Every block should now answer:

```text
Where does this belong?
What does it touch?
What does it expose?
What does it prove?
When, if ever, should it become core?
```

