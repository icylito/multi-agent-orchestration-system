# Agents

This directory contains Ollama Modelfiles — the definitions that turn a base language model into a role-locked, governed AI agent.

---

## What a Modelfile Is

An Ollama Modelfile is a plain text file that defines:
- which base model to load (`FROM`)
- what system prompt to inject before every conversation (`SYSTEM`)

Think of it as a job description permanently baked into the model session. When an agent is created from a Modelfile, every conversation it has starts with that system prompt already loaded — it cannot ignore it.

---

## Agent Roster

| File | Model | Role |
|------|-------|------|
| `Manager.Modelfile` | qwen3:14b | Orchestrates the team. Plans, delegates, gates, approves, rejects. |
| `ManagerGPTOSS.Modelfile` | gpt-oss:20b | Alternative manager — stronger at practical sprint planning. |
| `Coder.Modelfile` | qwen3:14b | Implementation. Writes, edits, debugs, runs code. |
| `Reviewer.Modelfile` | deepseek-r1:14b | Quality gate. Reviews architecture, security, maintainability. |
| `Tester.Modelfile` | qwen3:14b | Testing and debugging. Root cause analysis, no fake "tests passed". |
| `Scraper.Modelfile` | qwen3:14b | Research. Finds and structures public web data ethically. |
| `Organizer.Modelfile` | qwen3:14b | Memory and documentation. Writes summaries, maintains logs. |

---

## Shared Rules (All Agents)

Every agent has the same top-level priority stack:

```
1. SAFETY_RULES.md        — cannot be overridden by anything
2. Role Lock              — never drift into another agent's job
3. SYSTEM documents       — read before every major action
4. User request           — execute within the above constraints
5. Optimization prefs     — style and preferences, lowest priority
```

**No agent is allowed to:**
- claim a file was written without writing it
- claim tests passed without running them
- delete logs or overwrite archived handoffs
- hallucinate tool names or capabilities
- drift outside their assigned role

---

## Manager Agent — Detail

The Manager is the most complex agent in the system. It never writes code directly. Its job is:

- understand the user's goal
- ask clarification questions until confidence ≥ 95%
- break work into small sprint tasks
- assign each task to the correct specialist
- define acceptance criteria per task
- verify output from specialists
- reject weak work and request revision
- approve work and move to the next task

**Confidence rule:**
- ≥ 95% → proceed with the safest clear plan
- < 95% → stop and ask 2–4 clarification questions, mark one as RECOMMENDED

**Auto-continue rule:**  
After 2 minutes with no user response, the Manager may auto-continue **only** for safe, reversible, low-risk decisions. It must **never** auto-continue for: deleting files, overwriting credentials, deploying to production, or any destructive operation.

**Handoff format** (every agent-to-agent transfer must use this):
```
TASK ID:
FROM:
TO:
GOAL:
CONTEXT:
FILES / AREAS INVOLVED:
EXPECTED OUTPUT:
ACCEPTANCE CRITERIA:
KNOWN RISKS:
CONFIDENCE:
NEXT STEP:
```

---

## Reviewer Agent — Detail

Uses `deepseek-r1:14b` rather than qwen3. Deepseek R1 was chosen for this role because it produces more structured, critical output — better at instruction-following for review-format tasks.

**Confidence scoring:**
- 95–100% → approve
- 80–94% → approve with concerns
- below 80% → reject / request revision

**Output format:**
```
1. Summary
2. What Was Reviewed
3. Issues Found
4. Risk Level
5. Required Changes
6. Confidence Score
7. Approval Status
```

---

## How to Register Agents with Ollama

```bash
cd agents/

ollama create manager     -f Manager.Modelfile
ollama create managergpt  -f ManagerGPTOSS.Modelfile
ollama create coder       -f Coder.Modelfile
ollama create reviewer    -f Reviewer.Modelfile
ollama create tester      -f Tester.Modelfile
ollama create scraper     -f Scraper.Modelfile
ollama create organizer   -f Organizer.Modelfile
```

After registration, list all models:
```bash
ollama list
```

---

## VRAM Loading

Agents do not run simultaneously. The RTX 3080 has 10 GB VRAM — enough for one 14B model at a time (quantized). The system is designed around this:

1. Agent A loads into VRAM
2. Agent A does its job and writes structured output
3. Agent A unloads
4. Agent B loads into VRAM
5. Agent B reads Agent A's output from disk (via the relay handoff system)
6. Agent B continues

This is not a workaround. It is correct architecture for constrained single-GPU environments.
