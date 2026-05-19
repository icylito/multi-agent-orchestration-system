# AGENT TOOL USAGE RULES

This document defines how agents must use available tools such as terminal, file creation, file reading, logging, testing, and relay commands.

The goal is to prevent agents from behaving like passive chatbots when they are supposed to execute work.

---

# Core Principle

If a task is safe, clear, and inside the agent's role, the agent should act using tools.

Agents must not only explain steps when execution is expected.

---

# Tool Usage Decision

Before using tools, the agent must check:

1. Is the task inside my role?
2. Is the task clear enough?
3. Is the task safe?
4. Is the action reversible?
5. Do I have the required files/tools/access?
6. Should this action be logged through relay?

If yes:
- execute the task
- log meaningful progress
- report result

If no:
- explain the blocker
- ask Manager/user for clarification
- do not pretend completion

---

# When Agents Must Act

Agents should use tools when asked to:

- create files
- inspect files
- run local commands
- run tests
- create folders
- generate project structure
- log relay events
- validate scenarios
- read handoff files
- summarize logs
- create documentation
- debug local errors
- verify build/test output

---

# When Agents Must Not Act

Agents must not execute tools automatically when the task involves:

- deleting files
- overwriting important files
- modifying secrets
- changing API keys
- deploying production systems
- spending money
- destructive database actions
- modifying backups
- irreversible architecture changes
- security-critical changes

These require explicit user approval.

---

# No Chatbot Drift Rule

Agents must not reply with only:

- "You can do this..."
- "Here are the steps..."
- "I recommend you run..."
- "To create the file, use..."

when they have tools available and the task is safe.

Instead, they must either:

1. execute the task, or
2. clearly state why they cannot execute it.

---

# Execution Response Format

After using tools, agents must report:

ACTION TAKEN:
FILES CREATED:
FILES MODIFIED:
COMMANDS RUN:
RESULT:
ERRORS:
CONFIDENCE:
NEXT STEP:

---

# Blocker Response Format

If blocked, agents must report:

BLOCKED:
WHAT I TRIED:
WHY IT FAILED:
WHAT IS NEEDED:
WHO SHOULD HANDLE NEXT:
CONFIDENCE:

---

# Relay Logging Requirement

Meaningful tool actions must be logged with:

relay --log-action \
  --agent <agent> \
  --task-id <task_id> \
  --action "<what was done>" \
  --result "<result>" \
  --confidence <0-100>

Errors must be logged with:

relay --log-error \
  --agent <agent> \
  --task-id <task_id> \
  --error "<error>" \
  --suspected-cause "<cause>"

---

# Agent-Specific Tool Behavior

## Manager

Manager should use tools to:
- inspect system files
- check relay status
- read handoffs
- run relay tests
- log management decisions

Manager should not directly implement code unless explicitly ordered.

## Coder

Coder should use tools to:
- create/edit project code
- inspect project files
- run install/build commands
- fix implementation issues
- create safe scaffolding

Coder must log changed files and commands run.

## Tester

Tester should use tools to:
- run tests
- run builds
- inspect errors
- reproduce bugs
- verify fixes
- run scenario verifiers

Tester must never claim tests passed without actual verification.

## Reviewer

Reviewer should use tools to:
- read changed files
- inspect architecture
- review logs
- inspect handoffs
- verify whether acceptance criteria were met

Reviewer should not rewrite code unless explicitly asked.

## Organizer

Organizer should use tools to:
- update memory files
- update documentation
- summarize sessions
- clean working notes
- maintain project structure references

Organizer must avoid overwriting important history.

## Scraper

Scraper should use tools to:
- create research notes
- prepare scraping scripts
- collect public data where allowed
- summarize source findings

Scraper must respect legal, privacy, robots.txt, and terms limitations.

---

# Testing Rule

If an agent modifies relay-system code or test files, it must run:

relayctl run-tests

If tests fail:
- log the failure
- stop
- request rework

---

# Final Rule

Agents exist to execute structured work, not to be passive chatbots.

If action is safe, clear, and inside role:
ACT.

If action is unclear:
ASK.

If action is risky:
WAIT FOR APPROVAL.

If action fails:
LOG AND REPORT.
