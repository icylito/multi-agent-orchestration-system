# SCENARIO PROTOCOL

This document defines how the AI team creates, tests, reviews, and learns from scenarios.

Scenarios are used to train the system behavior without changing model weights.

They act as operational examples that show:
- what should happen
- what should not happen
- what fallback should trigger
- how agents should respond
- how the Manager should decide

---

# Core Principle

Scenarios are practical behavior tests.

They help the system improve by creating repeatable examples of:
- success flows
- failure flows
- edge cases
- low-confidence situations
- rate-limit handoffs
- debugging paths
- clarification paths
- rework loops

---

# Scenario Location

All scenario files must be stored in:

./relay-system/tests/

Scenario documentation files:

SCENARIO_XXX_NAME.md

Scenario runner files:

run_scenario_XXX.sh

Scenario verifier files:

verify_scenario_XXX.py

---

# Scenario File Requirements

Every scenario documentation file must include:

1. Scenario title
2. Purpose
3. Mode
4. Agents involved
5. Expected flow
6. Commands
7. Expected output
8. Pass criteria
9. Failure criteria
10. Notes / future improvements

---

# Scenario Types

The system should support these scenario types:

## Success Scenario
Tests a normal successful workflow.

Example:
Basic handoff works.

## Failure Scenario
Tests that errors are logged and rework is created.

Example:
Coder creates broken code, Tester rejects it.

## Low-Confidence Scenario
Tests that the system stops instead of continuing blindly.

Example:
Receiving agent only understands 70%.

## Clarification Scenario
Tests that Manager asks useful questions before acting.

Example:
User gives vague project request.

## Safety Scenario
Tests that dangerous actions require approval.

Example:
Agent attempts to delete a file.

## Rate-Limit Scenario
Tests emergency handoff behavior.

Example:
Agent reaches simulated 95% capacity.

## Tool-Usage Scenario
Tests that agents use tools instead of only explaining.

Example:
Coder must create a file instead of telling user how.

---

# Scenario Naming Rule

Use this format:

SCENARIO_001_BASIC_HANDOFF.md
SCENARIO_002_LOW_CONFIDENCE_HANDOFF.md
SCENARIO_003_ERROR_REWORK.md

Runner:

run_scenario_001.sh

Verifier:

verify_scenario_001.py

---

# Scenario Runner Rule

Every scenario should have a shell runner when possible.

Runner must:
- execute the scenario steps
- stop on errors
- print clear progress
- avoid destructive actions
- use relay commands
- not require API keys unless explicitly approved

---

# Scenario Verifier Rule

Every scenario should have a verifier when possible.

Verifier must:
- inspect logs/state/handoffs
- confirm expected events exist
- confirm wrong behavior did not happen
- return PASSED or FAILED
- exit with non-zero status when failed

---

# Learning From Scenarios

When a scenario passes:
- Organizer may summarize what behavior was validated.

When a scenario fails:
- Manager must analyze why.
- Reviewer may inspect the system rules.
- Coder may fix scripts.
- Tester must rerun verifier.
- Organizer must document the lesson learned.

---

# Scenario Result Logging

After scenario execution, log result with:

relay --log-action \
  --agent tester \
  --task-id <SCENARIO-ID> \
  --action "<what was verified>" \
  --result "<pass/fail summary>" \
  --confidence <confidence>

---

# Scenario Promotion Rule

A scenario becomes a stable behavior example only after:
1. runner works
2. verifier passes
3. Manager approves
4. Organizer documents result
5. test suite includes it when appropriate

---

# Scenario Regression Rule

If future changes break a previously passing scenario:
- stop
- log regression
- identify cause
- fix system
- rerun full test suite

No system change is stable if it breaks existing scenarios.

---

# Final Rule

Scenarios are how the system learns safe behavior over time.

Every important failure, edge case, or repeated confusion should become a scenario.
