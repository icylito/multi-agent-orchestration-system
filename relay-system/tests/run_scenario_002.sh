#!/usr/bin/env bash

set -e

echo "Running Scenario 002 — Low-Confidence Handoff Fallback"

relay --start-task \
  --task-id SCENARIO-002 \
  --goal "Validate low-confidence handoff fallback" \
  --agent coder

relay --log-action \
  --agent coder \
  --task-id SCENARIO-002 \
  --action "Performed unclear simulated implementation work" \
  --result "Work was incomplete and context may be insufficient" \
  --confidence 75

relay --simulate-rate \
  --agent coder \
  --task-id SCENARIO-002 \
  --percent 95

relay --create-handoff \
  --task-id SCENARIO-002 \
  --from-agent coder \
  --to-agent tester \
  --summary "Coder hit simulated 95% limit, but the handoff contains incomplete context. Tester should validate understanding and request clarification if confidence is too low." \
  --confidence 75

relay --validate-handoff \
  --agent tester \
  --validation-confidence 70

relay --status

echo "Scenario 002 completed."
echo "Expected result: CLARIFICATION_REQUIRED"
