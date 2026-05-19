# HANDOFF PROTOCOL

This document defines how agents must communicate task progress, results, blockers, and next actions.

Every agent handoff must be structured.
No vague handoffs.
No "done" without evidence.
No approval without verification.

---

# Required Handoff Format

Every handoff must use this format:

TASK ID:
FROM:
TO:
ROLE:
GOAL:
STATUS:
SUMMARY:
FILES CREATED:
FILES MODIFIED:
COMMANDS RUN:
TESTS RUN:
RESULTS:
ERRORS / BLOCKERS:
CONFIDENCE SCORE:
RECOMMENDED NEXT STEP:
NEEDS USER APPROVAL:

---

# Field Rules

## TASK ID
A short unique identifier.

Example:
SPRINT-001-CODER-LOGIN

## FROM
The agent sending the handoff.

Example:
Coder Agent

## TO
The next responsible agent.

Example:
Tester Agent

## ROLE
The role of the sending agent.

Example:
Implementation

## GOAL
What this task was supposed to accomplish.

## STATUS
Must be one of:

- NOT STARTED
- IN PROGRESS
- COMPLETED
- BLOCKED
- NEEDS REVIEW
- NEEDS TESTING
- REWORK REQUIRED
- APPROVED
- REJECTED

## SUMMARY
Plain English explanation of what happened.

## FILES CREATED
List files created.
If none, write: None.

## FILES MODIFIED
List files modified.
If none, write: None.

## COMMANDS RUN
List commands run.
If none, write: None.

## TESTS RUN
List tests/checks run.
If none, write: Not run.

## RESULTS
What happened after execution/testing/review.

## ERRORS / BLOCKERS
Any issue preventing completion.
If none, write: None.

## CONFIDENCE SCORE
Estimate from 0 to 100%.

Confidence below 95% requires either:
- rework
- clarification
- further testing
- reviewer approval

## RECOMMENDED NEXT STEP
What should happen next.

## NEEDS USER APPROVAL
Must be Yes or No.

Use Yes for:
- destructive changes
- deleting files
- production deployment
- secret handling
- payment/API billing changes
- irreversible architecture decisions
- major tech stack changes

---

# Handoff Rules

1. Every task must end with a handoff.
2. Coder must hand off to Tester or Reviewer.
3. Tester must hand off to Manager.
4. Reviewer must hand off to Manager.
5. Organizer must hand off to Manager after documentation updates.
6. Scraper must hand off to Manager or Organizer.
7. Manager decides approval, rework, or next sprint.
8. No agent may mark final completion except Manager.
9. No agent may hide errors.
10. If confidence is below 95%, the task is not final-approved.

---

# Example Handoff

TASK ID: SPRINT-001-CODER-SETUP
FROM: Coder Agent
TO: Tester Agent
ROLE: Implementation
GOAL: Create initial React app structure inside ./app.
STATUS: NEEDS TESTING
SUMMARY: Created Vite React app and installed dependencies.
FILES CREATED:
- ./app/package.json
- ./app/src/App.jsx
FILES MODIFIED:
- None
COMMANDS RUN:
- npm create vite@latest app -- --template react
- npm install
TESTS RUN:
- Not run
RESULTS:
Project scaffold created successfully.
ERRORS / BLOCKERS:
None
CONFIDENCE SCORE: 90%
RECOMMENDED NEXT STEP:
Tester should run npm install and npm run build inside ./app.
NEEDS USER APPROVAL: No
