#!/usr/bin/env bash

set -e

echo "Running Scenario 001 — Basic Handoff Test"

relay --start-task \
  --task-id SCENARIO-001 \
  --goal "Validate basic relay handoff flow" \
  --agent coder

relay --log-action \
  --agent coder \
  --task-id SCENARIO-001 \
  --action "Performed simulated implementation work" \
  --result "Simulated work completed for relay testing" \
  --confidence 90

relay --simulate-rate \
  --agent coder \
  --task-id SCENARIO-001 \
  --percent 95

relay --create-handoff \
  --task-id SCENARIO-001 \
  --from-agent coder \
  --to-agent tester \
  --summary "Coder completed simulated work and hit a simulated 95% rate limit. Tester should validate the relay logs, state, and handoff continuity." \
  --confidence 90

relay --validate-handoff \
  --agent tester \
  --validation-confidence 90

relay --continue-relay \
  --agent tester

relay --status

echo "Scenario 001 completed."
