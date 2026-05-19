# MEMORY POLICY

This document defines how the AI system stores, updates, summarizes, and maintains memory.

The goal is:
- preserve important knowledge
- reduce context waste
- improve continuity
- learn user preferences over time
- avoid memory pollution

Memory must remain:
- structured
- relevant
- truthful
- useful
- maintainable

---

# Core Memory Principle

Not all information deserves permanent memory.

Agents must distinguish between:
1. permanent knowledge
2. temporary work
3. logs/debugging
4. user behavior/preferences
5. failed experiments

The Organizer Agent is responsible for maintaining memory quality.

---

# Memory Locations

## Permanent Memory

Location:
./memory/permanent/

Purpose:
Long-term project intelligence.

Stores:
- architecture decisions
- approved workflows
- project requirements
- tech stack decisions
- API decisions
- database structure decisions
- user preferences
- important research
- stable business logic
- approved coding standards

Example files:
- architecture.md
- approved-decisions.md
- tech-stack.md
- user-style.md
- ai-team-workflow.md

---

## Working Memory

Location:
./memory/working/

Purpose:
Temporary active project memory.

Stores:
- active sprint plans
- temporary tasks
- rough notes
- active bugs
- incomplete ideas
- handoff notes
- short-term experiments
- session summaries

Example files:
- current-sprint.md
- active-todos.md
- session-summary.md
- handoffs.md

Working memory may later:
- be cleaned
- summarized
- promoted into permanent memory

---

## Logs

Location:
./logs/

Purpose:
Historical operational record.

Stores:
- command history
- debugging output
- failures
- test results
- crashes
- rollback events
- execution traces

Logs are NOT permanent memory.

---

# User Profile Memory

Location:
./SYSTEM/USER_PROFILE.md
and
./memory/permanent/user-style.md

Purpose:
Help the system adapt to the user over time.

Track:
- communication style
- preferred detail level
- preferred workflow
- frustration triggers
- priorities
- approval patterns
- coding preferences
- architecture preferences
- AI workflow expectations

Example:
- user prefers direct answers
- user dislikes fluff
- user values execution over explanation
- user prefers structured systems
- user wants strong role enforcement

---

# Tone Detection Rules

Agents should estimate user tone during important interactions.

Possible tones:
- focused
- excited
- frustrated
- confused
- urgent
- angry
- uncertain

Behavior adaptation:
- frustrated → reduce fluff and solve directly
- urgent → prioritize execution
- confused → simplify explanations
- excited → maintain momentum while staying grounded
- uncertain → provide options and recommendation

Tone estimates are suggestions, not facts.

Never overreact emotionally.

---

# Memory Promotion Rules

Information should move from working memory to permanent memory ONLY if:
- repeatedly useful
- architecturally important
- approved by Manager
- important to user preferences
- required across future sessions

Avoid storing:
- random temporary thoughts
- low-value noise
- duplicate information
- unverified assumptions

---

# Memory Cleanup Rules

Organizer Agent should:
- reduce duplication
- archive outdated notes
- summarize large logs
- merge repetitive ideas
- maintain readability

Memory quality matters more than memory quantity.

---

# Session Summary Rules

At session end:
Organizer should update:
./memory/working/session-summary.md

Summary should include:
- completed tasks
- failed tasks
- important decisions
- unresolved blockers
- confidence concerns
- next recommended actions

---

# Confidence & Truthfulness Rules

Memory must:
- separate facts from assumptions
- preserve uncertainty honestly
- avoid fabricated conclusions
- preserve important context

Never store fake confidence.

---

# Retrieval Rules

Before major work:
Manager should review:
- relevant permanent memory
- active sprint memory
- recent logs if needed

Avoid blindly re-reading everything.

Prioritize:
- relevance
- recency
- importance

---

# Long-Term Learning Goal

Over time, the system should better understand:
- how the user works
- how the user thinks
- what the user values
- what output quality the user expects
- how to reduce unnecessary clarification

The goal is adaptation WITHOUT losing structure, safety, or truthfulness.

---

# Final Rule

Memory exists to improve future execution.

If memory becomes noisy, duplicated, vague, or bloated:
execution quality will decline.

Maintain high signal quality.
