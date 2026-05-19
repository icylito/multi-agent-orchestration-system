#!/usr/bin/env bash

set -e

echo "Running Scenario 003 — Error Logging and Rework Flow"

relay --start-task \
  --task-id SCENARIO-003 \
  --goal "Validate error logging and rework flow" \
  --agent coder

relay --log-action \
  --agent coder \
  --task-id SCENARIO-003 \
  --action "Attempted simulated implementation" \
  --result "Implementation failed during simulated runtime check" \
  --confidence 60

relay --log-error \
  --agent coder \
  --task-id SCENARIO-003 \
  --error "Simulated syntax/runtime error during implementation" \
  --suspected-cause "Incomplete or incorrect generated code"

relay --log-action \
  --agent tester \
  --task-id SCENARIO-003 \
  --action "Diagnosed simulated implementation failure" \
  --result "Tester confirmed the task should not be approved and needs rework" \
  --confidence 90

relay --log-action \
  --agent manager \
  --task-id SCENARIO-003 \
  --action "Created rework requirement" \
  --result "Manager requires coder to fix the failed implementation before review continues" \
  --confidence 95

relay --status

echo "Scenario 003 completed."
echo "Expected result: error logged + manager rework required"
