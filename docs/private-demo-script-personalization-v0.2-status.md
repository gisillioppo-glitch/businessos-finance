# Private Demo Script Personalization v0.2

## Product Meaning

Private Demo Script Personalization v0.2 turns the generic private demo script into a more practical operator guide for different private-demo audiences.

The script now helps the presenter adjust emphasis for executives, operations owners, governance reviewers, and pilot evaluators while staying inside the protected BusinessOS boundary.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared demo narrative methodology candidate
- Private data touched: sanitized only
- Public surface touched: no
- Approval required: no
- Evidence generated: yes
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats personalized demo scripting pattern

## Why It Matters

BusinessOS has enough dashboard pages, pilot artifacts, readiness checks, and governance views that a private demo can drift if every audience receives the same narrative.

This block keeps the demo controlled while making it easier to emphasize the right proof path for the person in the room.

## Current Capabilities

- Upgrades `python cli.py private-demo-script` output to v0.2.
- Adds audience personalization modes.
- Adds a personalized proof path for private demos.
- Adds operator cues for live steering.
- Keeps the demo script report inside `reports/private_demo_script_YYYY-MM-DD.md`.
- Extends the private dashboard `Demo Script` page to show the new sections read-only.
- Keeps all sensitive internals, credentials, raw database contents, and local-only artifacts out of the script.

## Audience Modes

- Executive sponsor.
- Operations owner.
- Governance or security reviewer.
- Pilot evaluator.

## Safety Boundary

The personalization does not expose secrets, raw implementation internals, repository settings, production credentials, real email delivery, or local artifacts such as `BussinessOS Avance.pdf`.

The dashboard remains read-only. Operators regenerate the artifact from CLI.

## Validation

```text
py_compile OK
private-demo-script OK
dashboard loader check OK
system-check OK: passed, 57/57
release-readiness OK: ready, 14/14
runtime-stability OK: runtime_stable, 8/8
quick smoke OK: 10 commands
```

Loader check:

```text
exists True
personas 4
proof_steps 6
operator_cues 4
segments 7
```

All targeted and general validation passed.

## Next Step

Use the personalized script during private demo rehearsal, then refine the audience modes after the first real private demo conversation.
