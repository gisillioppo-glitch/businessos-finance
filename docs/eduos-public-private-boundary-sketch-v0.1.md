# EduOS Public Private Boundary Sketch v0.1

Date: 2026-05-23

## Status

Closed for MVP validation.

## Purpose

This document sketches the public/private boundary for future EduOS work before any EduOS repository, runtime, dashboard, database, or Public AI implementation is opened.

The goal is to define what can safely exist on a public EduOS surface, what must remain inside a protected private EduOS environment, and how public interest should be handed off without exposing academic records.

## Current Decision

```text
EduOS public/private boundary: sketched
EduOS public site: not opened
EduOS Public AI: not opened
EduOS private runtime: not opened
EduOS repository: not opened
```

EduOS may now be discussed as a future branch with a clear boundary doctrine.

EduOS implementation remains closed.

## Boundary Doctrine

EduOS public surfaces may explain the product, collect non-sensitive institutional interest, and route qualified leads.

EduOS private surfaces may operate academic workflows, evidence, approvals, support, guardian communication, and command center synthesis.

The public layer must never become a shadow academic system.

## Public Surface Allowed

Future public EduOS surfaces may include:

- product explanation
- school or district interest intake
- non-sensitive demo request fields
- role-neutral branch education
- public feature overview
- safe pilot expectation setting
- approved screenshots or mockups
- public FAQ
- sanitized public proof points
- handoff into protected private intake

Allowed public questions may include:

- institution type
- approximate size band
- role of requester
- broad workflow pain points
- current LMS/SIS category
- demo interest
- preferred contact channel

Public intake must avoid student, teacher, guardian, assessment, disciplinary, support, or private school records.

## Public Surface Prohibited

Future public EduOS surfaces must not:

- access student records
- access teacher records
- access guardian records
- access course rosters
- access attendance records
- access grades
- access assessment content
- access intervention plans
- access academic integrity cases
- expose private evidence
- expose private dashboard pages
- expose live academic status
- execute approvals
- send guardian communications
- mutate academic workflows
- claim live institutional readiness from private runtime
- summarize private EduOS reports
- connect directly to Classroom, LMS, SIS, Drive, or private documents

Public EduOS must be deny-by-default for protected academic data.

## Private Surface Required

The following must remain private:

- Academic Command Center
- student support signals
- intervention plans
- assessment review queues
- grade-change reviews
- academic integrity workflows
- guardian communications
- private notifications
- academic evidence packets
- academic close
- approvals
- role-based dashboards
- LMS/SIS adapter outputs
- private audit logs
- system integrity and readiness reports

Private EduOS should require protected operator access before viewing or acting on any sensitive academic workflow.

## Public AI Boundary

Future EduOS Public AI may:

- explain EduOS at a high level
- answer public product questions
- collect non-sensitive school interest
- clarify public/private separation
- route a demo request
- explain that private operations require protected access
- summarize public intake fields into a sanitized handoff packet

Future EduOS Public AI must not:

- inspect private academic data
- connect to private EduOS runtime
- connect to BusinessOS runtime
- query LMS/SIS systems
- generate guardian messages from private context
- diagnose individual students
- recommend interventions for named students
- summarize private reports
- expose evidence
- approve decisions
- execute commands
- mutate workflows

Public AI should refuse or redirect any request for protected student, assessment, guardian, staff, or school-specific operational data.

## Public-To-Private Handoff

Public intake should create only a sanitized lead or demo packet.

Conceptual handoff fields:

```text
request_id
institution_type
size_band
requester_role
high_level_need
current_system_category
demo_interest
contact_channel
consent_to_contact
created_at
```

The handoff packet must not include:

- student names
- teacher names
- guardian names
- grades
- attendance records
- assessment content
- intervention details
- academic integrity details
- private files
- screenshots of private systems
- secrets or credentials

## LMS/SIS Boundary

EduOS may eventually integrate with systems such as:

- Google Classroom
- Canvas
- Moodle
- Schoology
- PowerSchool
- SIS platforms
- Drive or document repositories
- Sheets or CSV imports

Those systems must connect only through private adapters.

Public EduOS must not request credentials, tokens, exports, rosters, grades, or live system access.

## Screenshot And Demo Asset Boundary

Public assets may include:

- approved product mockups
- synthetic data screenshots
- public architecture diagrams
- high-level workflow diagrams
- sanitized demo clips

Public assets must not include:

- real student records
- real guardian communication
- real teacher performance data
- live dashboard status
- private evidence packets
- private report contents
- unapproved school names
- screenshots from protected private environments

## BusinessOS Separation

EduOS public/private boundary work must not:

- expose BusinessOS private runtime
- reuse BusinessOS finance data
- copy BusinessOS private reports into EduOS public surfaces
- merge BusinessOS landing and EduOS public surfaces
- route EduOS public intake into BusinessOS operational workflows without explicit private review

BusinessOS remains the private reference system. EduOS remains a future branch.

## Implementation Guardrails

This sketch does not:

- create EduOS code
- create an EduOS repository
- create a public EduOS website
- create Public AI
- create private EduOS dashboards
- create academic database schema
- connect to LMS/SIS platforms
- move BusinessOS code
- expose private files
- alter BusinessOS runtime

## Readiness Impact

This block moves EduOS from:

```text
public/private boundary: required
```

to:

```text
public/private boundary: sketched
```

It makes a docs-only EduOS shell safer because the shell can carry boundary doctrine before any implementation begins.

## Recommended Next Blocks

```text
EduOS Docs-Only Shell v0.1
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
