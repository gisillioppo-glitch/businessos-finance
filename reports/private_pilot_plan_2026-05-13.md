# Private Pilot Plan MVP v0.1

Date: 2026-05-13

## Pilot Plan Summary

Plan status: pilot_plan_ready_with_warnings
Intake status: pilot_candidate_with_warnings
Pilot length: 14 days
Pilot owner: Executive Owner
Primary workflow: Executive Daily Close
Recommended module: Executive Daily Close
Recommendation reason: Start with controlled evidence and daily operating rhythm while naming readiness warnings clearly.
First action: Confirm warning context with the executive owner, then start with Executive Daily Close.

## Pilot Roles

| Role | Type | Responsibility |
| --- | --- | --- |
| Executive Owner | Maximum Authority | Owns final decision and reviews daily close evidence. |
| Pilot Operator | Operations / Admin | Runs CLI/dashboard checks and captures evidence. |
| Governance Reviewer | Governance / Compliance | Reviews sensitive items, approvals, and boundaries. |
| Support Owner | Support Manager | Tracks incidents, questions, and pilot friction. |

## 14-Day Pilot Timeline

| Days | Phase | Objective | Evidence |
| --- | --- | --- | --- |
| Day 1 | Kickoff and boundary confirmation | Confirm owner, scope, protected data boundary, and pilot success criteria. | Signed pilot scope and owner confirmation. |
| Days 2-3 | Baseline observation | Run BusinessOS against current operating data and capture starting evidence. | Initial command center, daily close, and readiness artifacts. |
| Days 4-7 | Daily close rhythm | Use Executive Daily Close as the primary operating rhythm and verify owner review. | Daily close reports, notification outbox, and evidence index. |
| Days 8-10 | Governance and approval review | Review sensitive findings, approvals, escalation paths, and human-control rules. | Approval decisions, sensitivity findings, and audit logs. |
| Days 11-13 | Executive value review | Compare daily rhythm, visibility, and decision quality against baseline pain points. | Pilot review notes and readiness reports. |
| Day 14 | Exit decision | Decide whether to extend, expand, pause, or close the pilot. | Pilot exit decision and recommended next module. |

## Daily Operating Rhythm

- Run or verify Executive Daily Close.
- Review Command Center health and highest risk.
- Review notification outbox and delivery approval status.
- Review governance sensitivity and approval items.
- Record owner feedback and next action for the following day.

## Success Criteria

- Executive owner reviews at least 5 daily close artifacts during the pilot.
- BusinessOS identifies at least one useful risk, action, or follow-up that would otherwise be manual.
- No sensitive data or credential boundary is violated.
- Pilot users can explain the value of the command layer in one sentence.
- Exit decision is made with evidence, not only opinion.

## Exit Decisions

- Extend pilot: keep same workflow for another 14 days.
- Expand pilot: add one adjacent workflow or department.
- Convert to implementation: define production hardening requirements.
- Pause: resolve readiness/security gaps before continuing.
- Close: archive evidence and mark no current fit.

## Pilot Boundaries

- Do not promise public production deployment during the private pilot.
- Do not expose raw finance.db, credentials, local files, or repository internals.
- Do not enable real email delivery without SMTP credentials, approval gate, and dry-run review.
- Do not broaden the pilot beyond one workflow until success criteria are reviewed.

## Suggested Operator Note

Keep the pilot narrow. The first goal is not to automate everything; it is to prove that BusinessOS can create a trustworthy daily operating rhythm with evidence, ownership, and safe escalation.
