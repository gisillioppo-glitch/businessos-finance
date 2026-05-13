# Private Demo Script / Sketch MVP v0.1

## Product Meaning

The Private Demo Script / Sketch MVP turns the current BusinessOS product state into a guided private demo narrative.

It complements the Private Demo Package by defining what to show, what to say, what commands to run, what not to show, known risks, and closing questions for a controlled presentation.

## Boundary Classification

- Primary boundary: BusinessOS-specific
- Secondary boundary: Shared private demo methodology candidate
- Private data touched: sanitized only
- Public surface touched: no
- Approval required: no
- Evidence generated: yes
- Audit generated: yes
- Reusable core candidate: partial
- Extraction timing: after second vertical repeats private demo script pattern

## Why It Matters

BusinessOS is now large enough that a demo can become confusing if it is improvised. This script protects the product story, avoids exposing internal implementation details, and helps present the system as an institutional operating rhythm rather than disconnected features.

## Current Capabilities

- Adds `python cli.py private-demo-script`.
- Exports `reports/private_demo_script_YYYY-MM-DD.md`.
- Defines the demo arc and timeboxes.
- Defines screen order and talk track.
- Includes demo commands.
- Lists safe dashboard pages to show.
- Lists what not to show.
- Lists known risks to name honestly.
- Includes closing questions for private demo discovery.
- Writes audit logs when exported.
- Adds smoke test coverage.

## Demo Positioning

BusinessOS should be presented as:

```text
A private institutional AI operating system that helps leaders see, close, govern, and communicate daily operations from one protected command layer.
```

## Safety Boundary

The script does not expose secrets, raw database internals, credentials, private repo settings, or local artifacts such as `BussinessOS Avance.pdf`.

## Next Step

Use the script for rehearsal, then refine based on the first private demo conversation.
