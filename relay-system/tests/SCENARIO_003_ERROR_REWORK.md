# Scenario 003 — Error Logging and Rework Flow

This scenario tests how the relay system handles failure.

Purpose:
Verify that the relay system:
- logs errors
- records suspected causes
- does not claim success after failure
- creates a clear rework path
- keeps failure history visible

---

# Scenario Mode

Experimental Mode.

During this scenario:
- failure is simulated
- no real app is broken
- no real API keys are used
- no deletion or destructive action is allowed

---

# Agents Involved

Initial Agent:
coder

Debugging Agent:
tester

Decision Agent:
manager

Documentation Agent:
organizer

---

# Expected Flow

1. Start task as coder
2. Coder logs attempted work
3. Coder logs an error
4. Tester logs diagnosis
5. Manager logs rework request
6. System status confirms latest activity
7. Error log contains failure record

---

# Commands

## 1. Start task

relay --start-task \
  --task-id SCENARIO-003 \
  --goal "Validate error logging and rework flow" \
  --agent coder

## 2. Log coder attempt

relay --log-action \
  --agent coder \
  --task-id SCENARIO-003 \
  --action "Attempted simulated implementation" \
  --result "Implementation failed during simulated runtime check" \
  --confidence 60

## 3. Log error

relay --log-error \
  --agent coder \
  --task-id SCENARIO-003 \
  --error "Simulated syntax/runtime error during implementation" \
  --suspected-cause "Incomplete or incorrect generated code"

## 4. Tester diagnosis

relay --log-action \
  --agent tester \
  --task-id SCENARIO-003 \
  --action "Diagnosed simulated implementation failure" \
  --result "Tester confirmed the task should not be approved and needs rework" \
  --confidence 90

## 5. Manager rework request

relay --log-action \
  --agent manager \
  --task-id SCENARIO-003 \
  --action "Created rework requirement" \
  --result "Manager requires coder to fix the failed implementation before review continues" \
  --confidence 95

## 6. Check status

relay --status

---

# Expected Output

The relay system should show:
- error recorded in logs/errors.jsonl
- activity log contains coder failed attempt
- activity log contains tester diagnosis
- activity log contains manager rework request
- no approval event is required
- no task is falsely completed

---

# Pass Criteria

Scenario passes if:
1. All commands run without Python errors.
2. errors.jsonl exists.
3. SCENARIO-003 error record exists.
4. Tester diagnosis exists in activity log.
5. Manager rework request exists in activity log.
6. System does not create fake approval.

---

# Failure Criteria

Scenario fails if:
- Python error occurs
- error log is missing
- failure is not recorded
- task is treated as completed without rework
