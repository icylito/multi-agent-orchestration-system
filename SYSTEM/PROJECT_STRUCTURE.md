# PROJECT STRUCTURE RULES

This document defines how all agents must use the project folders.

## Root Folder: ~/saas-project

This is the main workspace. All project work must stay inside this folder unless the user explicitly says otherwise.

Agents must not write random files into the root unless the file is a core project file such as README.md, package.json, or SYSTEM_WORKFLOW.md.

---

## ./agents

Purpose:
Stores Ollama Modelfiles and agent definitions.

Allowed contents:
- Manager.Modelfile
- Coder.Modelfile
- Tester.Modelfile
- Reviewer.Modelfile
- Organizer.Modelfile
- Scraper.Modelfile
- future agent prompt files

Rules:
- Only modify these files when changing agent behavior.
- Do not store project code here.
- Do not store temporary logs here.

---

## ./app

Purpose:
Main application/codebase folder.

Allowed contents:
- frontend code
- backend code
- APIs
- database files/config
- package files
- source code
- tests

Rules:
- All production/project code should go here.
- Coder Agent works mostly here.
- Tester Agent tests mostly here.
- Reviewer Agent reviews mostly here.

---

## ./memory/permanent

Purpose:
Long-term knowledge that should survive across sessions.

Allowed contents:
- architecture decisions
- approved workflows
- user preferences
- project requirements
- final design decisions
- business strategy
- API decisions
- database decisions

Example files:
- architecture.md
- project-requirements.md
- user-style.md
- approved-decisions.md
- tech-stack.md

Rules:
- Only store high-value long-term information.
- Do not store temporary thoughts here.
- Organizer Agent is responsible for keeping this clean.

---

## ./memory/working

Purpose:
Temporary active work memory.

Allowed contents:
- current sprint plan
- today's tasks
- active TODOs
- rough notes
- experiment notes
- incomplete ideas
- handoff notes

Example files:
- current-sprint.md
- active-todos.md
- session-summary.md
- agent-handoffs.md

Rules:
- Temporary but useful.
- Can be cleaned or summarized later.
- Organizer Agent should move important items to permanent memory when approved.

---

## ./logs

Purpose:
Execution history and debugging records.

Allowed contents:
- command outputs
- failed attempts
- test results
- error logs
- build logs
- debugging history

Example files:
- debug.md
- test-results.md
- command-history.md
- failed-attempts.md

Rules:
- Tester Agent must record important failures here.
- Coder Agent may log important command outputs here.
- Do not store final decisions here.

---

## ./backups

Purpose:
Manual backups and snapshots.

Allowed contents:
- copied files before risky edits
- exported configs
- archived versions
- emergency restore points

Rules:
- Before risky changes, create a backup here.
- Do not use as normal project storage.
- Do not delete backups without user approval.

---

# Agent Responsibility by Folder

Manager:
- Reads SYSTEM files
- Coordinates all folders
- Approves movement of important info into permanent memory

Coder:
- Works mainly in ./app
- May write logs to ./logs
- Must not edit SYSTEM unless instructed

Tester:
- Works mainly in ./app
- Writes test/debug info into ./logs

Reviewer:
- Reviews ./app, ./memory/permanent, and SYSTEM rules
- Does not make major edits unless asked

Organizer:
- Owns ./memory/permanent
- Owns ./memory/working
- Keeps documentation clean

Scraper:
- Saves research summaries into ./memory/working first
- Important verified research may later move into ./memory/permanent

# Final Rule

Before creating a file, every agent must ask:
1. Is this code? Put it in ./app.
2. Is this long-term knowledge? Put it in ./memory/permanent.
3. Is this temporary work? Put it in ./memory/working.
4. Is this command/debug output? Put it in ./logs.
5. Is this an agent definition? Put it in ./agents.
6. Is this a backup? Put it in ./backups.
