# SPRINT PROTOCOL

This document defines how the AI team executes work using an agile iterative workflow.

The system must prioritize:
- small validated progress
- fast feedback
- safe iteration
- clear ownership
- rework when quality is weak
- deadline awareness

The system must avoid:
- giant uncontrolled tasks
- hidden failures
- fake completions
- unverified assumptions
- chaotic parallel work

---

# Core Sprint Philosophy

A sprint is a small focused execution cycle.

Every sprint must:
1. Have a clear goal
2. Be broken into small tasks
3. Have assigned agents
4. Have acceptance criteria
5. Be testable
6. Be reviewable
7. End with approval or rework

No sprint may continue without Manager approval.

---

# Sprint Lifecycle

## Phase 1 — Goal Understanding

Manager Agent:
- reads the user request
- checks SYSTEM rules
- evaluates confidence
- identifies risks
- asks clarification questions if confidence <95%

If confidence is below 95%:
- Manager must ask questions
- provide suggested answers
- recommend the safest option

---

## Phase 2 — Sprint Planning

Manager creates:
- sprint ID
- sprint goal
- task breakdown
- assigned agents
- expected outputs
- acceptance criteria
- risks
- dependencies

Tasks must remain:
- small
- reversible
- testable
- reviewable

Avoid giant vague tasks.

---

## Phase 3 — Delegation

Manager assigns work.

Example:
- Scraper researches APIs
- Organizer documents requirements
- Coder implements feature
- Tester validates feature
- Reviewer evaluates quality

Manager tracks:
- task ownership
- progress
- blockers
- confidence

---

## Phase 4 — Execution

Assigned agent performs work.

Rules:
- follow HANDOFF_PROTOCOL.md
- follow PROJECT_STRUCTURE.md
- follow SYSTEM_WORKFLOW.md
- log important results
- avoid scope creep
- remain inside assigned role

---

## Phase 5 — Verification

Tester Agent:
- runs tests/builds/checks
- reproduces issues
- validates behavior
- reports failures honestly

Reviewer Agent:
- checks architecture
- checks maintainability
- checks security
- checks quality
- evaluates scalability and readability

---

## Phase 6 — Confidence Evaluation

Manager evaluates:
- tester results
- reviewer results
- handoff quality
- risks
- unresolved assumptions

If confidence >=95%:
- approve sprint task
- continue next task

If confidence <95%:
- reject sprint task
- request rework
- explain exact failure points

---

# Rework Rules

Rework is mandatory when:
- confidence <95%
- testing failed
- reviewer rejects
- requirements not met
- architecture weak
- implementation risky
- undocumented assumptions exist

Rework must:
- identify exact issue
- assign responsible agent
- define correction scope
- avoid rewriting unrelated parts

---

# Sprint Completion Rules

A sprint is COMPLETE only if:
1. Acceptance criteria met
2. Tests passed or issues documented
3. Reviewer approved
4. Manager confidence >=95%
5. Organizer updated memory/docs
6. Handoff finalized

---

# Acceptance Criteria Rules

Every sprint task must define:
- expected output
- success conditions
- validation method
- risk level

Example:
Task: Create login API

Acceptance Criteria:
- endpoint exists
- validation works
- invalid input rejected
- tests pass
- logs generated
- reviewer approves architecture

---

# Blocker Rules

If blocked:
- stop pretending progress
- report exact blocker
- identify missing requirement
- identify responsible next agent
- estimate risk

Never hallucinate success.

---

# User Approval Rules

Mandatory approval required for:
- deleting files
- overwriting important files
- changing secrets
- production deployment
- irreversible architecture decisions
- paid API/service activation
- database destruction
- modifying backups

---

# Session Summary Rules

At sprint end:
Organizer must update:
- ./memory/working/session-summary.md
- ./memory/working/current-sprint.md

If high-value knowledge discovered:
move approved knowledge into:
- ./memory/permanent/

---

# Default Sprint Output Format

SPRINT ID:
SPRINT GOAL:
TASKS:
ASSIGNED AGENTS:
RISKS:
CURRENT STATUS:
CONFIDENCE:
BLOCKERS:
NEXT ACTION:
