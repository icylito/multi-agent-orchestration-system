# Agent Handoff

TASK ID: SCENARIO-002
FROM: coder
TO: tester
STATUS: HANDOFF_CREATED
CONFIDENCE SCORE: 75
CREATED AT: 2026-05-15T12:46:08.150431+00:00

---

## SUMMARY

Coder hit simulated 95% limit, but the handoff contains incomplete context. Tester should validate understanding and request clarification if confidence is too low.

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
