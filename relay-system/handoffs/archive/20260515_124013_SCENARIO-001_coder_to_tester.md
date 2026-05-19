# Agent Handoff

TASK ID: SCENARIO-001
FROM: coder
TO: tester
STATUS: HANDOFF_CREATED
CONFIDENCE SCORE: 90
CREATED AT: 2026-05-15T12:40:13.063983+00:00

---

## SUMMARY

Coder completed simulated work and hit a simulated 95% rate limit. Tester should validate the relay logs, state, and handoff continuity.

---

## RECEIVING AGENT REQUIREMENT

The receiving agent must confirm understanding before continuing.

If understanding confidence is 95% or higher:
- continue the task
- log the next action

If understanding confidence is below 95%:
- stop
- ask Manager for clarification
- read logs or memory before continuing

---

## SAFETY NOTE

This file is historical context.
Do not delete old handoffs.
Do not overwrite archived handoff files.
