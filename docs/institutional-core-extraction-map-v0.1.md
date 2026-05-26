# Institutional Core Extraction Map v0.1

Date: 2026-05-12

## Purpose

This document maps the current BusinessOS implementation into reusable OS Core, BusinessOS-specific domain logic, future EduOS-specific domain logic, Public AI boundary logic, and shared platform candidates.

The goal is not to extract code yet. The goal is to understand which parts of BusinessOS are becoming the repeatable pattern for future OS branches.

## Strategic Position

BusinessOS remains the first live branch and reference implementation of the OS Software System.

Current doctrine:

```text
BusinessOS -> harden -> identify reusable core -> design OS Platform -> design EduOS -> implement EduOS
```

BusinessOS should continue maturing until the core pattern is stable enough to duplicate. EduOS should not be opened as a rushed clone or loose module inside BusinessOS.

## Current BusinessOS Module Map

```text
app/
|-- actions
|-- alerts
|-- approvals
|-- assistance
|-- audit
|-- command_center
|-- dashboard
|-- db
|-- demo
|-- evidence
|-- governance
|-- ingest
|-- notifications
|-- operations
|-- people
|-- readiness
|-- reports
|-- rules
|-- scheduler
|-- security
|-- support
`-- system
```

## Classification Summary

| Area | Current Module(s) | Classification | Future Direction |
| --- | --- | --- | --- |
| Audit trail | `audit` | OS Core candidate | Shared append-only activity layer. |
| Security | `security` | OS Core candidate | Shared role/session/access boundary. |
| People and roles | `people` | OS Core candidate | Shared institutional identity model. |
| Approvals | `approvals` | OS Core candidate | Shared approval-gated action layer. |
| Governance | `governance` | OS Core candidate | Shared sensitivity and policy layer. |
| Notifications | `notifications` | OS Core candidate | Shared internal/external delivery control. |
| Evidence | `evidence` | OS Core candidate | Shared evidence packet and review layer. |
| Readiness | `readiness` | OS Core candidate | Shared release/demo/pilot readiness logic. |
| System checks | `system` | OS Core candidate | Shared integrity and runtime stability checks. |
| Scheduler | `scheduler` | OS Core candidate | Shared controlled recurring job layer. |
| Dashboard shell | `dashboard` | Shared UI candidate | Shared shell with vertical-specific pages. |
| Command center | `command_center` | Shared pattern candidate | Shared executive synthesis pattern. |
| Demo and pilot | `demo` | Shared go-to-market candidate | Shared private demo/pilot methodology. |
| Reports | `reports` | Shared utility candidate | Shared report history/export utilities. |
| Database connection | `db` | Shared utility candidate | Shared persistence conventions, not final schema. |
| Finance actions/rules | `actions`, `rules`, `ingest` | BusinessOS-specific | Enterprise finance and operating rules. |
| Operations | `operations` | BusinessOS-specific with shared pattern | Business workflow model; pattern may transfer. |
| Support | `support` | BusinessOS-specific with shared pattern | Incident model; pattern may transfer. |

## OS Core Candidates

These modules are likely reusable across BusinessOS, EduOS, and future verticals once hardened.

### Audit

Current role:

- records traceable events
- supports governance review
- supports readiness and system checks

Future OS Core role:

- shared event timeline
- append-only audit behavior
- role-aware audit visibility
- incident and evidence linkage

Extraction condition:

- audit events must support domain-neutral event types and metadata.

### Security

Current role:

- protects the private dashboard
- defines allowed dashboard pages by role
- separates public landing from private runtime

Future OS Core role:

- shared role validation
- access boundaries per OS branch
- protected mode foundation
- public/private route separation
- branch-specific dashboard page allowlists
- environment-protected authentication settings

Extraction condition:

- roles must be generalized beyond BusinessOS labels
- dashboard page access lists must become configuration-driven
- authentication settings must remain environment-protected
- public/private route rules must be branch-neutral

Current readiness:

- login boundary: medium readiness
- dashboard allowlist shape: medium readiness
- public/private separation: high readiness
- BusinessOS page specialization: keep in BusinessOS
- EduOS implementation: planning only, not inside BusinessOS

### People

Current role:

- maintains internal users
- tracks roles, departments, status, access levels

Future OS Core role:

- shared institutional identity layer
- branch-specific role extensions
- access-level enforcement
- user status lifecycle
- hierarchy or manager relationship support
- duplicate identity protection

Extraction condition:

- role labels must become branch-configurable
- department or group labels must become branch-configurable
- access levels must map to branch-specific role policies
- identity schema must separate core user fields from vertical profile fields

Current readiness:

- identity record: high readiness
- user status lifecycle: high readiness
- access level model: medium readiness
- BusinessOS default users: keep in BusinessOS
- EduOS implementation: planning only, not inside BusinessOS

EduOS adaptation:

- student
- teacher
- director
- guardian or family contact
- academic coordinator

### Approvals

Current role:

- handles pending, approved, rejected, and cancelled approval requests
- supports approval reports and briefings
- integrates with notification delivery approval
- protects controlled pilot expansion requests from generic demo approval commands

Future OS Core role:

- shared approval-gated execution model
- sensitive action approval workflow
- justification and rationale tracking
- protected request source policies for demo-safe and automation-safe operation

Extraction condition:

- approval types must become configurable per branch
- protected source modules must become policy-driven rather than hard-coded
- role labels must become branch-configurable
- dashboard and report language must separate core approval status from vertical context

Current readiness:

- lifecycle primitive: high readiness
- request creation and deduplication: high readiness
- generic dashboard visibility: medium readiness
- BusinessOS pilot expansion specialization: keep in BusinessOS
- EduOS implementation: planning only, not inside BusinessOS

Future EduOS analog:

- academic policy exceptions
- grade or assessment change approvals
- restricted student record access
- intervention plan approvals
- guardian or director acknowledgement

### Governance

Current role:

- evaluates findings
- evaluates sensitivity rules
- supports governance brief and KPIs

Future OS Core role:

- shared policy and sensitivity engine
- branch-specific rule packs
- escalation and protected mode triggers
- audit-log based finding detection
- domain-neutral severity and justification checks

Extraction condition:

- sensitivity rule packs must become branch-configurable
- source modules and table mappings must become configurable per vertical
- privileged access levels must become branch-configurable
- finding types must be domain-neutral with branch-specific labels
- report language must separate core governance status from vertical content

Current readiness:

- governance findings: high readiness
- sensitivity rule shape: high readiness
- rule-pack configurability: medium readiness
- dashboard visibility: medium readiness
- BusinessOS governance specialization: keep in BusinessOS
- EduOS implementation: planning only, not inside BusinessOS

BusinessOS rule pack examples:

- budget approval
- sensitive operation
- overdue operational task

EduOS rule pack examples:

- grade modification
- restricted assessment behavior
- academic integrity event
- restricted student record access
- guardian communication policy check

### Evidence

Current role:

- builds executive evidence index
- generates daily close
- generates daily close distribution

Future OS Core role:

- shared evidence packet model
- review chain support
- repeatability evidence
- owner review artifacts
- expected evidence item registry
- date-based close and evidence packet generation

Extraction condition:

- evidence item definitions must become configurable by vertical
- close steps must become configuration-driven
- distribution recipients must become branch-configurable
- report labels must be separated from evidence mechanics
- report language must separate core evidence status from vertical content

Current readiness:

- evidence index: high readiness
- daily close shape: high readiness
- distribution packet: medium readiness
- dashboard visibility: medium readiness
- BusinessOS evidence specialization: keep in BusinessOS
- EduOS implementation: planning only, not inside BusinessOS

Future EduOS analog:

- school daily close
- student progress evidence packet
- teacher intervention evidence
- academic risk review packet
- assessment change evidence
- guardian communication evidence

### Notifications

Current role:

- notification outbox
- delivery approvals
- secure email delivery adapter
- delivery status transitions

Future OS Core role:

- shared internal notification queue
- external delivery approval gate
- delivery mode policy
- dry-run and disabled delivery safety modes
- branch-neutral delivery status reporting

Extraction condition:

- real delivery adapters must remain credential-protected and approval-gated
- recipient roles and departments must become branch-configurable
- message templates must be separated from delivery mechanics
- channel policy must be configurable per vertical
- report language must separate core delivery status from vertical content

Current readiness:

- outbox lifecycle: high readiness
- delivery approval gate: high readiness
- secure email adapter: medium readiness
- dashboard visibility: medium readiness
- BusinessOS daily close specialization: keep in BusinessOS
- EduOS implementation: planning only, not inside BusinessOS

Future EduOS analog:

- director daily school close distribution
- teacher intervention notifications
- guardian communication approvals
- assessment or grade-change approval notices
- academic risk escalation notifications

### Readiness and System

Current role:

- release readiness
- system integrity
- runtime stability
- scheduled daily close status visibility

Future OS Core role:

- shared validation framework
- branch-specific readiness check registry
- quick/standard/full validation profiles
- controlled recurring job status model
- public/private runtime boundary checks
- branch-neutral local artifact policy

Extraction condition:

- checks must be modular and declarative enough for BusinessOS, EduOS, and Public AI
- required modules, tables, reports, dashboard pages, and public paths must become branch-configurable
- scheduled jobs must be registered through a generic job registry
- known local artifacts must be policy-driven
- smoke profile limits must be configurable per branch

Current readiness:

- system integrity shape: high readiness
- release readiness shape: high readiness
- runtime stability shape: high readiness
- scheduler status visibility: medium readiness
- BusinessOS runtime specialization: keep in BusinessOS
- EduOS implementation: planning only, not inside BusinessOS

Future EduOS analog:

- EduOS module presence checks
- student/course/teacher table readiness checks
- school daily close artifact freshness
- academic evidence packet freshness
- scheduled academic close or intervention review status

### Dashboard and Command Center

Current role:

- protected private dashboard shell
- role-aware navigation
- read-only operating views
- command center executive synthesis
- dashboard visibility for readiness, integrity, notifications, approvals, evidence, pilot, and demo surfaces

Future OS Core role:

- shared protected dashboard shell
- branch-configurable page registry
- role-aware page visibility
- reusable read-only status page patterns
- shared executive synthesis layout
- branch-specific command center adapters
- public/private UI boundary enforcement

Extraction condition:

- page registry must become branch-configurable
- role allowlists must be policy-driven or data-driven
- labels, groups, and page copy must remain branch-specific
- KPI and status components must accept neutral data objects
- command center aggregation must accept branch-specific adapters
- action buttons must remain governance-gated and disabled by default in read-only views
- report loaders must avoid hard-coded BusinessOS report names in core code

Current readiness:

- dashboard shell readiness: medium
- command center pattern readiness: medium
- read-only status page pattern readiness: high
- role-aware private access readiness: medium
- BusinessOS page specialization: keep in BusinessOS
- EduOS implementation: planning only, not inside BusinessOS

Future EduOS analog:

- school dashboard shell
- academic command center
- student risk status
- course progress status
- teacher workload status
- guardian communication status
- intervention approval status
- school daily close status
- academic evidence packet status

### Demo and Pilot Methodology

Current role:

- private demo readiness gate
- private demo package and script
- demo personalization by audience
- private demo dry run and final review
- private pilot intake and plan
- pilot start gate and owner confirmation
- daily pilot evidence rhythm
- pilot exit, expansion preparation, expansion decision, and approval request handoff

Future OS Core role:

- shared readiness-to-demo methodology
- shared demo package structure
- shared demo script and audience emphasis pattern
- shared pilot intake and plan structure
- shared owner confirmation chain
- shared pilot evidence rhythm
- shared exit and expansion decision gates
- branch-specific workflows, evidence, copy, and owner roles

Extraction condition:

- artifact generators must accept branch-specific configuration
- audience modes must be branch-configurable
- demo page lists must come from a branch page registry
- command lists must come from branch capabilities
- pilot workflows must be supplied by branch adapters
- evidence requirements must be policy-driven
- owner confirmation roles must be branch-specific
- expansion decisions must remain advisory until approval-gated
- protected approval requests must remain isolated from demo-safe approval commands

Current readiness:

- demo package pattern readiness: high
- demo script pattern readiness: high
- pilot intake and plan readiness: high
- pilot daily rhythm readiness: medium
- pilot expansion gate readiness: high
- BusinessOS demo/pilot specialization: keep in BusinessOS
- EduOS implementation: planning only, not inside BusinessOS

Future EduOS analog:

- school readiness-to-demo gate
- academic demo package
- director or administrator demo script
- teacher operations demo script
- school pilot intake
- first academic workflow pilot plan
- school owner confirmation
- daily academic pilot tracker
- student-risk evidence review
- academic intervention pilot exit decision
- school expansion preparation
- district or department expansion approval request

## BusinessOS-Specific Domain Logic

These areas should remain inside BusinessOS unless later generalized carefully.

Domain adapter doctrine:

- OS Core should provide reusable operating patterns.
- BusinessOS should provide enterprise business domain meaning.
- EduOS should later provide academic domain meaning.
- Domain logic should adapt to core patterns, not become core by default.

### Finance

Includes:

- transactions
- cash flow
- expense ratio
- expense concentration
- financial anomalies
- finance recommended actions

Why BusinessOS-specific:

- directly tied to enterprise financial operations
- not a natural EduOS core primitive

Potential shared pattern:

- domain risk rules
- action generation
- brief generation
- neutral rule result schema
- branch-specific thresholds and wording

### Operations

Includes:

- operations tasks
- escalation rules
- operations brief

Why partially reusable:

- workflow/task concepts are universal
- actual task types and escalation logic are vertical-specific
- statuses, owners, and evidence links may become shared patterns
- task categories and urgency rules must remain branch-specific

Future EduOS analog:

- academic workflows
- assignment workflow
- attendance workflow
- intervention workflow

### Support

Includes:

- support incidents
- incident status
- support brief
- support report

Why partially reusable:

- incident management is universal
- incident categories and severity rules change by vertical
- support status lifecycle may become a shared pattern
- incident language and response criteria must remain branch-specific

Future EduOS analog:

- student support requests
- teacher support
- academic incident
- safety or conduct incident

### Rules, Actions, and Domain Briefs

Includes:

- financial rule evaluation
- recommended action lifecycle
- domain brief generation
- report export shape
- command center domain summaries

Why partially reusable:

- rule registries, result schemas, actions, and briefs are reusable shapes
- source data, thresholds, vocabulary, and risk meaning are vertical-specific

Future EduOS analog:

- academic risk rules
- intervention recommendations
- course or student brief generation
- academic evidence summaries
- director command center domain summaries

Extraction condition:

- rule inputs must be branch-specific adapters
- rule outputs must use neutral severity/result structures
- action statuses must remain generic
- domain wording must be branch-owned
- command center must consume neutral summaries rather than hard-coded BusinessOS modules

## EduOS Future Domain Map

EduOS should be a separate OS branch, not a module inside BusinessOS.

Future EduOS modules may include:

- students
- teachers
- courses
- subjects
- assignments
- assessments
- grading governance
- academic integrity
- learning support
- restricted assessment mode
- subject intelligence modes
- family/guardian communication
- academic evidence index
- director command center

Shared patterns to reuse from BusinessOS:

- people and role structure
- governance sensitivity rules
- approvals
- audit logging
- dashboard shell
- evidence packets
- readiness checks
- notification approval gate
- pilot methodology
- command center synthesis

BusinessOS patterns to adapt, not copy:

- finance rules become academic performance/integrity rules
- operations tasks become academic workflows
- support incidents become academic/student support incidents
- daily close becomes academic daily/weekly institutional close

## Public AI Boundary Map

Public AI should remain isolated from private OS runtime.

Allowed:

- product explanation
- public Q&A
- lead qualification
- demo guidance
- intake routing
- high-level education about OS branches

Not allowed:

- private DB access
- private reports access
- approval execution
- workflow mutation
- sensitive internal artifact exposure
- credential use
- user impersonation

Future Public AI modules may include:

- public product assistant
- demo request assistant
- lead qualification assistant
- OS branch explainer
- controlled intake summarizer

Boundary doctrine:

```text
Public AI routes interest inward; it does not operate the private OS core.
```

Public AI may:

- explain BusinessOS or future OS branches at a high level
- answer public product questions
- qualify interest using non-sensitive questions
- collect demo request context
- route qualified interest to private intake
- explain public/private boundaries
- summarize non-sensitive public form responses

Public AI must not:

- access private databases
- read private reports
- execute CLI commands
- approve or reject approval requests
- mutate workflows
- trigger notification delivery
- inspect secrets or credentials
- impersonate users
- expose internal evidence packets
- present private runtime status as public live truth

Future OS Core or OS Platform role:

- public/private route separation
- public intake schema
- public lead qualification schema
- public assistant refusal rules
- public-to-private handoff packet
- sensitive data denial policy
- branch-aware product explanation
- public artifact allowlist
- private runtime denylist

Extraction condition:

- public routes must be separate from private runtime routes
- public assistant permissions must be deny-by-default
- private file, DB, report, and dashboard access must be impossible from public context
- public copy must be branch-specific
- intake schema must be branch-configurable
- private handoff packets must be sanitized
- public proof assets must be allowlisted
- public status claims must be based on approved public artifacts, not live private state

## Extraction Readiness Levels

| Level | Meaning | Action |
| --- | --- | --- |
| L0 | BusinessOS-only | Keep inside BusinessOS. |
| L1 | Shared pattern candidate | Document pattern, do not extract yet. |
| L2 | Core candidate | Prepare config/domain separation. |
| L3 | Extractable core | Ready to move into `os-core` or shared package. |
| L4 | Shared platform service | Can serve multiple OS branches. |

## Current Extraction Readiness

| Module | Level | Reason |
| --- | --- | --- |
| `audit` | L2 | Strong shared pattern, needs domain-neutral metadata. |
| `security` | L2 | Shared access pattern, needs branch-aware roles. |
| `people` | L2 | Shared identity pattern, needs vertical role extension. |
| `approvals` | L2 | Shared approval gate, needs configurable approval types. |
| `governance` | L2 | Shared policy engine, needs branch-specific rule packs. |
| `notifications` | L2 | Shared queue/delivery gate, needs adapter boundaries. |
| `evidence` | L2 | Shared evidence model, needs configurable evidence registry. |
| `readiness` | L2 | Shared validation pattern, needs check registry. |
| `system` | L2 | Shared integrity/runtime pattern, needs branch registry. |
| `dashboard` | L1 | Shared visual shell, still tightly coupled to BusinessOS pages. |
| `demo` | L1 | Shared methodology, currently BusinessOS/private-pilot specific. |
| `command_center` | L1 | Shared executive synthesis pattern, current data is BusinessOS-specific. |
| `actions` | L0 | Finance action model is BusinessOS-specific. |
| `rules` | L0 | Current rules are financial/BusinessOS-specific. |
| `ingest` | L0 | CSV finance ingestion is BusinessOS-specific. |
| `operations` | L1 | Workflow pattern reusable, current domain is BusinessOS. |
| `support` | L1 | Incident pattern reusable, current domain is BusinessOS. |

## Recommended Next Steps

1. Continue hardening BusinessOS as the reference implementation.
2. Avoid opening EduOS implementation until BusinessOS core patterns are stable.
3. Add branch-aware configuration only when a second branch is ready to consume it.
4. Keep documenting shared patterns before extracting code.
5. Use the OS Platform Map before opening EduOS implementation.

## Immediate Follow-Up Blocks

Recommended sequence:

```text
EduOS Skeleton Publish Readiness Checklist v0.1
EduOS Skeleton Repo Naming Decision v0.1
```

## Operator Note

This map is architectural. It does not move code, create EduOS, or split repositories. It defines what BusinessOS is teaching us about the reusable OS pattern.
