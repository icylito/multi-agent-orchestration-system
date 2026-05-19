# RELAY SYSTEM PROTOCOL

This document defines how agents must use the local relay/orchestration system.

The relay system is located at:

./relay-system/

It provides:
- append-only logging
- task tracking
- rate-limit simulation
- emergency handoff creation
- handoff validation
- relay continuation
- scenario testing
- relay status inspection

The relay system is currently in EXPERIMENTAL MODE.

---

# Primary Commands

Agents may use:

relay --status

relay --start-task

relay --log-action

relay --simulate-rate

relay --create-handoff

relay --validate-handoff

relay --continue-relay

relay --log-error

Agents may also use:

relayctl status
relayctl active
relayctl latest-handoff
relayctl run-tests
relayctl emergency <agent> <task_id>

---

# When to Use Relay

Use relay when:
- starting a structured task
- logging meaningful progress
- recording agent actions
- simulating or handling rate/capacity limits
- creating handoffs between agents
- validating handoff understanding
- continuing work under another agent
- logging errors/debugging events
- checking current relay state

---

# Required Relay Logging

Every meaningful agent action should be logged.

Use:

relay --log-action \
  --agent <agent> \
  --task-id <task_id> \
  --action "<what was done>" \
  --result "<result>" \
  --confidence <0-100>

Do not log vague entries.

Bad:
"Worked on project."

Good:
"Created handoff validation test and confirmed low-confidence fallback behavior."

---

# Emergency Handoff Rule

If an agent reaches or simulates 95% capacity/rate usage:

1. Stop active work.
2. Trigger emergency status:

relayctl emergency <agent> <task_id>

3. Ask active agent for a detailed checkpoint.
4. Create a handoff:

relay --create-handoff \
  --task-id <task_id> \
  --from-agent <from_agent> \
  --to-agent <to_agent> \
  --summary "<detailed checkpoint>" \
  --confidence <confidence>

5. Receiving agent validates understanding:

relay --validate-handoff \
  --agent <agent> \
  --validation-confidence <confidence>

6. Continue only if allowed by current mode.

---

# Experimental Mode Rules

During Experimental Mode:
- 90% confidence is acceptable for mechanical testing.
- No real Claude/ChatGPT API relay is active.
- No real API keys are required.
- No autonomous overnight execution is active.
- Scenario tests may simulate rate limits and handoffs.

---

# Production Mode Rules

Later, Production Mode should require:
- 95% confidence for continuation
- Manager approval
- Tester/Reviewer verification
- stricter fallback logic
- real provider adapters only after approval

---

# Low-Confidence Rule

If handoff validation is below required confidence:

- do not continue blindly
- record CLARIFICATION_REQUIRED
- Manager must intervene
- read logs, memory, and latest handoff
- ask user if required

---

# Error Rule

If an error occurs:

relay --log-error \
  --agent <agent> \
  --task-id <task_id> \
  --error "<error>" \
  --suspected-cause "<cause>"

Then Manager must decide:
- rework
- clarification
- retry
- stop

---

# Test Suite Rule

Before trusting changes to the relay system, run:

relayctl run-tests

All scenarios must pass before considering the relay system stable.

Current scenarios:
- Scenario 001: Basic handoff success
- Scenario 002: Low-confidence fallback
- Scenario 003: Error logging and rework flow

---

# Safety Rules

Agents must not:
- delete relay logs
- delete archived handoffs
- overwrite historical logs
- fake relay events
- claim tests passed without running verifier
- bypass Manager approval for risky actions

---

# Relay Files

Important files:

./relay-system/logs/activity.jsonl
Main append-only activity log.

./relay-system/logs/rate-limit.jsonl
Rate/capacity status log.

./relay-system/logs/errors.jsonl
Error/debug log.

./relay-system/state/state.jsonl
Append-only state history.

./relay-system/handoffs/latest-handoff.md
Most recent handoff.

./relay-system/handoffs/archive/
Historical handoff archive.

./relay-system/tests/
Scenario documentation, runners, and verifiers.

---

# Final Rule

The relay system is the coordination memory layer.

Agents must use it to preserve context, prevent lost progress, and avoid unsafe blind continuation.
