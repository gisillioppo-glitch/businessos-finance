# Private Pilot Intake MVP v0.1

Date: 2026-05-13

## Pilot Intake Status

Intake status: pilot_candidate_with_warnings
Release readiness: ready_with_warnings
Private demo dry run: ready_with_warnings
Recommended starting module: Executive Daily Close
Recommendation reason: Start with controlled evidence and daily operating rhythm while naming readiness warnings clearly.

## Diagnostic Questions

1. What daily executive process currently requires the most manual follow-up?
2. Who owns finance, operations, governance, support, and daily close decisions?
3. Which decisions should never execute without approval?
4. What evidence does leadership need at the end of each day?
5. Which notifications should be internal-only versus externally delivered?
6. What data must stay private during the pilot?
7. What would make the pilot successful after 14 days?

## Candidate Pilot Modules

| Module | Fit | Suggested Owner | Risk |
| --- | --- | --- | --- |
| Executive Daily Close | Best first pilot when leadership needs daily evidence, notifications, and operating rhythm. | Executive Owner | Medium |
| Approvals + Governance Sensitivity | Best first pilot when the organization needs control over sensitive actions and decision approvals. | Governance / Executive Owner | High |
| Command Center Dashboard | Best first pilot when the organization needs unified visibility before automation. | Executive Owner | Medium |
| Support + Assistance | Best first pilot when internal help, escalation, and incident follow-up are fragmented. | Support Manager | Medium |

## Pilot Readiness Criteria

- Private demo dry run is not blocked.
- Release readiness has no failed checks.
- Pilot scope is limited to one primary workflow.
- Maximum Authority owner is identified.
- Sensitive files, credentials, and private database remain outside public surface.
- Real external email delivery remains disabled until explicitly configured and approved.

## Pilot Boundaries

- Do not promise public production deployment during the private pilot.
- Do not expose raw finance.db, credentials, local files, or repository internals.
- Do not enable real email delivery without SMTP credentials, approval gate, and dry-run review.
- Do not broaden the pilot beyond one workflow until success criteria are reviewed.

## Suggested Close

If the organization agrees with the recommended starting module, define a 14-day private pilot with one executive owner, one workflow, daily evidence review, and no public deployment commitment.
