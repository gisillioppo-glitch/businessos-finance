# Private Demo Script / Sketch MVP v0.1

Date: 2026-05-14

## Demo Purpose

Present BusinessOS as a private institutional AI operating system that helps leaders see, close, and govern daily operations from one protected command layer.

## Readiness Context

Release readiness: ready
Passed checks: 14
Warning checks: 0
Failed checks: 0

## Pre-Demo Checklist

- Run python cli.py system-check.
- Run python cli.py release-readiness.
- Run python cli.py runtime-stability.
- Run python cli.py session-handoff before changing chat or pausing.
- Run python scripts/smoke_test.py quick before demo checkpoints.
- Confirm the private dashboard responds at http://localhost:8501.
- Confirm Git status has no unexpected changes beyond BussinessOS Avance.pdf.
- Confirm finance.db, .env, and Streamlit secrets are not in the public surface.

## Demo Commands

| Purpose | Command |
| --- | --- |
| Pre-demo readiness | `python cli.py release-readiness` |
| System health | `python cli.py system-check` |
| Daily close | `python cli.py daily-close` |
| Notification outbox | `python cli.py notifications` |
| Private dashboard | `streamlit run app/dashboard/main.py` |

## Demo Arc

| Segment | Timebox | Screen | Talk Track | Proof |
| --- | --- | --- | --- | --- |
| Opening | 2 min | Public landing / product positioning | BusinessOS is a private institutional AI operating system for leaders who need one protected view across finance, operations, governance, support, decisions, and daily close. | Show public landing only as product surface, not private internals. |
| Private Command Center | 4 min | Dashboard | This is the executive command layer. The system synthesizes operational signals and turns fragmented module data into next-best executive moves. | Show overall health, risk, executive brief, module snapshot. |
| Operating Modules | 6 min | Finance, Operations, Governance, Support | The value is not one module. The value is the connected operating loop: finance creates signals, operations turns them into work, governance controls sensitivity, and support manages incidents. | Show each page briefly; avoid deep raw data. |
| Human Control Layer | 5 min | Assistance, Approvals, People, Sensitivity | BusinessOS keeps humans in control. It routes help, approvals, access and sensitive findings instead of letting automation bypass institutional governance. | Show approval queue, people access layer, sensitivity rules. |
| Daily Close and Evidence | 6 min | Daily Close, Notifications, Scheduled Close | At the end of the day, the system closes the loop: it gathers evidence, prepares executive distribution, queues notifications, and tracks what happened to those messages. | Show daily close status, notification statuses, scheduled close page. |
| Trust and Readiness | 4 min | System Integrity, Release Readiness | Before presenting or operating, BusinessOS can check itself. This is what makes the product feel like an operating system instead of a dashboard. | Show system-check and release-readiness reports/pages. |
| Close | 3 min | Dashboard / Command Center | The promise is simple: fewer fragmented tools, better executive visibility, safer decisions, and daily operating rhythm with evidence. | Ask what workflow they would want BusinessOS to close first in their organization. |

## Dashboard Pages Available

- Dashboard
- Alerts
- Finance
- Operations
- Governance
- Sensitivity
- Support
- Assistance
- Approvals
- Daily Close
- Notifications
- Delivery Approval
- Secure Email
- Scheduled Close
- System Integrity
- Runtime Stability
- Surface Audit
- Boundary Index
- Session Handoff
- Demo Readiness
- Demo Package
- Demo Script
- Pilot Plan
- Pilot Tracker
- Pilot Exit
- Pilot Day 1
- Pilot Day 2
- Pilot Day 3
- Pilot Day 4
- Pilot Day 5
- People

## Do Not Show

- finance.db raw contents.
- .env, credentials, tokens, local secrets, Streamlit secrets.
- Private implementation internals unless explicitly requested in a technical review.
- Untracked local artifacts such as BussinessOS Avance.pdf.
- Real external email sending as if production-ready; keep it positioned as protected/dry-run unless configured.

## Known Risks To Name Honestly

- Dashboard auth is still local MVP auth and should remain private.
- Email delivery is protected and should stay disabled/dry-run until credentials and approvals are configured.
- The data set is demo-scale, not production-scale.
- Release readiness may show warnings during active development blocks before commit.

## Closing Questions

- Which daily executive process would you want automated first?
- Who needs to receive the daily close in your organization?
- Which actions should always require approval before execution?
- What would make this trustworthy enough for a private pilot?

## Suggested Closing Statement

BusinessOS is not just a dashboard. It is an operating rhythm: detect, prioritize, approve, close the day, package evidence, notify owners, and verify system integrity before the next decision cycle.
