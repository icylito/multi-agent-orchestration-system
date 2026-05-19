# Scenario 001 — Basic Handoff Test

This scenario tests the basic relay flow.

Purpose:
Verify that the relay system can:
- start a task
- log an agent action
- simulate a 95% limit
- create a handoff
- validate handoff understanding
- continue relay to the next agent
- report status

---

# Scenario Mode

Experimental Mode.

During this scenario:
- 90% confidence is acceptable
- no real API keys are used
- no real Claude/ChatGPT relay is used
- no autonomous execution is used

---

# Agents Involved

Initial Agent:
coder

Receiving Agent:
tester

Organizer:
documents the result

---

# Expected Flow

1. Start task as coder
2. Coder logs action
3. Rate limit simulated at 95%
4. Handoff created from coder to tester
5. Tester validates handoff at 90%
6. Relay continues to tester
7. System status confirms tester as latest active agent

---

# Commands

## 1. Start task

relay --start-task \
  --task-id SCENARIO-001 \
  --goal "Validate basic relay handoff flow" \
  --agent coder

## 2. Log coder action

relay --log-action \
  --agent coder \
  --task-id SCENARIO-001 \
  --action "Performed simulated implementation work" \
  --result "Simulated work completed for relay testing" \
  --confidence 90

## 3. Simulate 95% rate limit

relay --simulate-rate \
  --agent coder \
  --task-id SCENARIO-001 \
  --percent 95

## 4. Create handoff

relay --create-handoff \
  --task-id SCENARIO-001 \
  --from-agent coder \
  --to-agent tester \
  --summary "Coder completed simulated work and hit a simulated 95% rate limit. Tester should validate the relay logs, state, and handoff continuity." \
  --confidence 90

## 5. Validate handoff

relay --validate-handoff \
  --agent tester \
  --validation-confidence 90

## 6. Continue relay

relay --continue-relay \
  --agent tester

## 7. Check status

relay --status

---

# Expected Output

The relay system should show:
- latest state includes tester as active agent
- latest rate status is CRITICAL_95
- latest handoff exists
- activity log includes handoff validation
- no files were deleted
- archived handoff file exists

---

# Pass Criteria

Scenario passes if:
1. All commands run without Python errors.
2. Handoff archive file is created.
3. latest-handoff.md exists.
4. handoff-index.jsonl is updated.
5. state.jsonl records active agent change to tester.
6. relay --status shows latest handoff and latest state.

---

# Failure Criteria

Scenario fails if:
- Python error occurs
- handoff file is not created
- state is not updated
- logs are overwritten instead of appended
- relay status cannot read latest entries
