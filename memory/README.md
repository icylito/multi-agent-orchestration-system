# Memory

This directory is the persistent knowledge store for the agent system.

---

## Structure

```
memory/
├── permanent/    # Long-term memory — survives between sessions
└── working/      # Short-term memory — active sprint context
```

---

## permanent/

Stores knowledge that must survive across sessions and sprints:

- Architecture decisions and the reasoning behind them
- Approved workflows and patterns
- User preferences (how the user likes work done, what they reject)
- Project requirements and locked scope
- Long-term strategy

**Written by:** Organizer Agent  
**Read by:** Manager Agent (before planning), any agent that needs project history

---

## working/

Stores context that is relevant now but will be replaced next sprint:

- Current sprint plan and task list
- Temporary notes from an active session
- Active task assignments
- In-progress debugging notes

**Written by:** Organizer Agent during active sprints  
**Cleared by:** Organizer Agent at the start of a new sprint (old working memory moves to `permanent/` if worth keeping, or is discarded)

---

## Memory Policy

The full policy is in `SYSTEM/MEMORY_POLICY.md`. The short version:

- If a decision matters beyond the current sprint → write to `permanent/`
- If it's only useful right now → write to `working/`
- If it's a command or debugging history → write to `logs/`
- Never delete permanent memory without Manager approval
- Working memory can be cleared at sprint boundaries
