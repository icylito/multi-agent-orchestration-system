# Relay System MVP

This is the local relay/orchestration system for AI agent handoffs.

It is used to:
- track active tasks
- log agent actions
- simulate rate-limit/capacity events
- create handoff files
- validate handoff confidence
- continue work with another agent
- inspect current relay status

---

# Current Mode

The system is currently in EXPERIMENTAL MODE.

During experimentation:
- 90% confidence handoffs are allowed
- the goal is to test workflow mechanics
- no real cloud API relay is active
- no autonomous overnight execution is active

Later, production mode will require:
- 95% confidence for continuation
- Manager approval
- Tester/Reviewer verification
- safer enforcement rules

---

# Command Shortcut

The relay system can be controlled using:

relay

Example:

relay --status

---

# Main Commands

## Initialize

relay --init

## Start Task

relay --start-task \
  --task-id SPRINT-001 \
  --goal "Test relay MVP" \
  --agent manager

## Log Agent Action

relay --log-action \
  --agent coder \
  --task-id SPRINT-001 \
  --action "Created test output" \
  --result "Action completed" \
  --confidence 90

## Simulate Rate Limit

relay --simulate-rate \
  --agent coder \
  --task-id SPRINT-001 \
  --percent 95

## Create Handoff

relay --create-handoff \
  --task-id SPRINT-001 \
  --from-agent coder \
  --to-agent tester \
  --summary "Coder hit simulated 95% limit and created handoff." \
  --confidence 90

## Validate Handoff

relay --validate-handoff \
  --agent tester \
  --validation-confidence 90

## Continue Relay

relay --continue-relay \
  --agent tester

## Inspect Status

relay --status

---

# Files

## logs/activity.jsonl
Append-only record of system events and agent actions.

## logs/rate-limit.jsonl
Append-only record of simulated or real rate-limit checks.

## logs/errors.jsonl
Append-only record of errors.

## state/state.jsonl
Append-only state history.

## handoffs/latest-handoff.md
Latest readable handoff.

## handoffs/archive/
Archived timestamped handoffs.

## config/agents.json
Agent registry and relay rules.

---

# Safety Rules

The relay system should not:
- delete logs
- overwrite archived handoffs
- hide failed actions
- claim completion without verification
- perform real API calls until explicitly upgraded

---

# Future Upgrades

Planned future phases:
1. Real provider adapters
2. Real rate-limit detection where possible
3. Agent task queue
4. Dashboard UI
5. Cloud AI relay support
6. Overnight supervised automation
