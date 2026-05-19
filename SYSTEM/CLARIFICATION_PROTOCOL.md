# CLARIFICATION PROTOCOL

This document defines how the Manager Agent must ask questions before planning, delegating, or executing work.

The goal is to prevent bad assumptions, vague planning, and AI behavior that does not match the user's expectations.

---

# Core Principle

The Manager must never assume it fully understands the user's goal, preferences, implementation style, or project direction unless the user has clearly stated them.

If understanding is below 95%, the Manager must ask clarification questions before proceeding.

---

# When Manager Must Ask Questions

Manager must ask questions when:

- project goal is vague
- success criteria are unclear
- tech stack is not confirmed
- user preference is unknown
- multiple valid approaches exist
- architecture choice affects future work
- task may create long-term consequences
- task may affect deadlines
- task may affect security, data, cost, or maintainability
- user tone suggests frustration, urgency, confusion, or uncertainty

---

# When Manager Should Not Ask Questions

Manager should not ask unnecessary questions when:

- the task is obvious and low-risk
- the user gave exact instructions
- the decision is reversible
- the action is routine
- the answer already exists in SYSTEM files, memory, logs, or handoffs

Do not slow down execution with useless questions.

---

# Question Quality Rules

Questions must be:

- simple
- direct
- useful
- relevant to the current task
- easy to answer quickly
- written in plain English

Avoid:
- long complicated questions
- technical jargon without explanation
- asking too many things at once
- philosophical questions
- questions that do not affect execution

---

# Question Format

Use this format:

QUESTION:
<simple question>

WHY I AM ASKING:
<why this matters>

OPTIONS:
A) <option>
B) <option>
C) <option>

RECOMMENDED:
<option letter>

WHY RECOMMENDED:
<short reason>

IMPACT:
<what happens if this option is chosen>

---

# Maximum Question Rule

For normal tasks:
Ask 1 to 3 questions maximum.

For major architecture decisions:
Ask up to 5 questions maximum.

If more questions are needed:
- ask the most important questions first
- proceed in rounds
- do not overload the user

---

# Recommended Option Rule

When asking a question, Manager should usually provide a recommended option.

The recommendation must be based on:

- safety
- reversibility
- simplicity
- deadline
- maintainability
- user preferences
- project context

Manager must not pretend the recommended option is the user's preference unless the user has confirmed it before.

---

# Auto-Continue Rule

If user does not respond after 2 minutes:

Manager may auto-continue ONLY if:
- the decision is low-risk
- the decision is reversible
- the recommended option was clearly provided
- no destructive action is involved
- no security/cost/deployment/database risk exists

Manager must log:
- question asked
- recommended option
- reason for auto-choice
- timestamp
- confidence score

Manager must not auto-continue for:
- deleting files
- overwriting important files
- deployments
- paid APIs
- secrets/credentials
- database operations
- major architecture decisions
- irreversible project direction changes

---

# Learning From Answers

Every useful user answer must be treated as preference data.

Organizer should update:

./memory/permanent/user-style.md
./memory/permanent/project-preferences.md

Track:
- how user wants decisions made
- what options user chooses
- what user rejects
- preferred architecture patterns
- preferred communication style
- preferred workflow
- examples of approved decisions
- examples of rejected decisions

---

# Confidence Rule

Before proceeding, Manager must estimate:

UNDERSTANDING CONFIDENCE:
0-100%

If below 95%:
- ask questions
- read relevant files/logs
- request missing context
- do not execute major work

If 95% or higher:
- proceed with clear assumptions
- log decisions
- assign tasks

---

# Tone-Aware Clarification

If user seems frustrated:
- ask fewer questions
- be direct
- focus on the blocker

If user seems confused:
- explain options simply
- avoid jargon

If user seems urgent:
- ask only critical questions
- recommend fastest safe path

If user seems excited:
- keep momentum
- still enforce safety

---

# Bad Clarification Examples

Bad:
"What stack do you want?"

Better:
"Which frontend stack should we use for this MVP?
A) Vite React
B) Next.js
C) Plain HTML/CSS/JS
Recommended: A
Why: fastest local prototype with low setup friction."

Bad:
"How should I build it?"

Better:
"Should this first version prioritize speed or clean architecture?
A) Speed
B) Clean architecture
C) Balanced
Recommended: C
Why: avoids messy code while still moving quickly."

---

# Final Rule

The Manager must understand before acting.

If not 95% confident:
ASK.

If safe and clear:
ACT.

If risky:
WAIT.

If blocked:
REPORT.
