# Icylito Multi-Agent Orchestration System

A locally-hosted AI orchestration runtime built on constrained hardware.  
Specialized agents run in sequence, pass structured context through a shared handoff layer, and are governed by a full protocol directory before a single line of application code was written.

---

## Why This Exists

Final semester of a CS.AI degree. The Final Year Project — a customer churn prediction and retention strategy tool — was stored on a single SSD. That SSD got corrupted. Everything was gone.

Two options:

- **Rebuild manually from scratch** — time-consuming, deadline-constrained, no leverage
- **Build a system that maximizes downtime** — agents run tasks autonomously in the background while life continues, compounding progress without requiring constant attention

The second option was chosen. A multi-agent system that could delegate work, run during idle time, and pick up where it left off made more sense than grinding through a manual rebuild. The system became the project.

---

The hardware constraint (RTX 3080, 10 GB VRAM) shaped the architecture directly: agents load one at a time, do one job, write structured output, then unload. The next agent reads from where the last one left off. Constrained hardware, clean design.

The governance layer — 15 protocol documents written *before* any application code — exists for the same reason. A system without defined rules produces undefined behaviour.

---

## Architecture Overview

```
User / Orchestrator
        │
        ▼
  Manager Agent  ←────────────────────────────────────┐
  (planning, delegation, confidence gating)           │
        │                                             │
   assigns task                               Reviewer rejects
        │                                             │
        ▼                                             │
  Specialist Agent  ──── writes output ──────────────►│
  (Coder / Tester / Scraper / Organizer)              │
        │                                             │
  writes handoff file                        Reviewer approves
        │                                             │
        ▼                                             │
  Relay System  ──── logs event ──────────────────────┘
  (relay.py, state.jsonl, activity.jsonl)
        │
  next agent reads handoff and continues
```

**The key constraint:** agents do not run simultaneously. Each model loads into VRAM, does its job, and unloads before the next model loads. Context is preserved between turns through structured handoff files, not in-memory state.

---

## Project Structure

```
saas-project/
├── SYSTEM/                  # Governance layer — rules before code
│   ├── ACCEPTANCE_CRITERIA.md
│   ├── AGENT_RULES.md
│   ├── AGENT_TOOL_USAGE.md
│   ├── CLARIFICATION_PROTOCOL.md
│   ├── HANDOFF_PROTOCOL.md
│   ├── MEMORY_POLICY.md
│   ├── PROJECT_STRUCTURE.md
│   ├── README_SYSTEM.md
│   ├── RELAY_SYSTEM_PROTOCOL.md
│   ├── RELAY_SYSTEM_PROTOCOL_SKILL.md
│   ├── SAFETY_RULES.md
│   ├── SCENARIO_PROTOCOL.md
│   ├── SPRINT_PROTOCOL.md
│   ├── SYSTEM_WORKFLOW.md
│   └── USER_PROFILE.md
│
├── agents/                  # Agent model definitions (Ollama Modelfiles)
│   ├── Manager.Modelfile
│   ├── ManagerGPTOSS.Modelfile
│   ├── Coder.Modelfile
│   ├── Reviewer.Modelfile
│   ├── Tester.Modelfile
│   ├── Scraper.Modelfile
│   └── Organizer.Modelfile
│
├── app/                     # Orchestrator runtime
│   └── orchestrator/
│       ├── main.py          # Entry point — loads agent, calls Ollama, logs to relay
│       ├── ollama_client.py # HTTP client for Ollama /api/chat
│       ├── relay_bridge.py  # Subprocess bridge to relay.py
│       ├── context/
│       │   └── project_context.md   # Persistent project context injected into every agent call
│       └── prompts/
│           ├── manager.md   # Manager agent system prompt
│           └── reviewer.md  # Reviewer agent system prompt
│
├── relay-system/            # The nervous system — logs, handoffs, state
│   ├── scripts/
│   │   └── relay.py         # CLI tool for all relay operations
│   ├── config/
│   │   └── agents.json      # Agent registry and relay rules
│   ├── handoffs/
│   │   ├── latest-handoff.md          # Always the most recent handoff
│   │   ├── handoff-index.jsonl        # Index of all handoffs
│   │   └── archive/                   # Timestamped handoff history
│   ├── logs/
│   │   ├── activity.jsonl   # All system events
│   │   ├── rate-limit.jsonl # Rate-limit / capacity events
│   │   └── errors.jsonl     # Error log
│   ├── state/
│   │   └── state.jsonl      # Active agent and task state (append-only)
│   ├── tests/               # Scenario test scripts
│   └── README.md
│
├── memory/
│   ├── permanent/           # Long-term memory (architecture decisions, user preferences)
│   └── working/             # Short-term memory (active sprint notes, session context)
│
├── external/
│   └── churn-fastapi-base/  # Reference FastAPI churn prediction service (FYP base)
│
├── docs/                    # Reserved for expanded documentation
├── logs/                    # Top-level system log directory
├── backups/                 # Backup storage
├── rebuild/                 # Rebuild workspace
│
├── SYSTEM_WORKFLOW.md       # High-level workflow definition
├── api_schema.json          # API schema specification
├── icylito_story_and_system.md  # Full project story, vision, and design rationale
└── README.md                # This file
```

---

## Agent Roster

| Agent | Model | Role |
|-------|-------|------|
| **Manager** | qwen3:14b | Brain and orchestrator. Plans, delegates, gates decisions at 95% confidence. Never drifts into implementation. |
| **ManagerGPTOSS** | gpt-oss:20b | Alternative manager variant. Stronger at practical reasoning and sprint planning. |
| **Coder** | qwen3:14b | Writes, edits, debugs, and runs code. Acts directly — no hand-holding. |
| **Reviewer** | deepseek-r1:14b | Reviews architecture, security, maintainability. Approves at ≥95% confidence, rejects below 80%. |
| **Tester** | qwen3:14b | Runs tests, identifies root causes, logs results. Never claims tests passed without running them. |
| **Scraper** | qwen3:14b | Finds and structures public web data. Respects robots.txt, rate limits, and legality. |
| **Organizer** | qwen3:14b | Documents decisions, maintains memory files, writes summaries and logs. |

All agents share one rule: **read `./SYSTEM` before acting**. The SYSTEM directory is the operational constitution.

---

## The Relay System

The relay is the nervous system of the project. Without it, agents have no way to communicate failure state, pass context between turns, or recover from errors.

It is a single Python script (`relay-system/scripts/relay.py`) with a CLI interface:

```bash
# Initialize the relay
relay --init

# Start a task
relay --start-task --task-id SPRINT-001 --goal "Rebuild auth module" --agent manager

# Log an agent action
relay --log-action --agent coder --task-id SPRINT-001 \
  --action "Created auth.py" --result "File written" --confidence 90

# Simulate a capacity limit (triggers emergency handoff protocol)
relay --simulate-rate --agent coder --task-id SPRINT-001 --percent 95

# Create a handoff to the next agent
relay --create-handoff --task-id SPRINT-001 \
  --from-agent coder --to-agent tester \
  --summary "Auth module written. Tests needed." --confidence 90

# Validate that the receiving agent understands the handoff
relay --validate-handoff --agent tester --validation-confidence 90

# Continue relay with a new active agent
relay --continue-relay --agent tester

# Check current system status
relay --status
```

**All logs are append-only.** Nothing is deleted. Nothing is overwritten. Every handoff is archived with a timestamp.

---

## The SYSTEM Governance Layer

Before implementation began, 15 governance documents were written. This is the order they are applied:

1. `SAFETY_RULES.md` — constraints no agent can violate (no deleting logs, no overwriting archives, no fake progress)
2. `AGENT_RULES.md` — behavioral rules: role lock, confidence scoring, no hallucination
3. `CLARIFICATION_PROTOCOL.md` — how agents ask questions before acting (never assume below 95%)
4. `HANDOFF_PROTOCOL.md` — the exact format context must take when passed between agents
5. `ACCEPTANCE_CRITERIA.md` — what "done" means: verification, validation, confidence score, documentation
6. `SPRINT_PROTOCOL.md` — how work is organized into small, testable cycles
7. `RELAY_SYSTEM_PROTOCOL.md` — how the relay layer coordinates agent turns
8. `MEMORY_POLICY.md` — what goes into permanent vs working memory and why
9. `SCENARIO_PROTOCOL.md` — how agents handle edge cases and unexpected failures
10. `AGENT_TOOL_USAGE.md` — which tools each agent is allowed to use
11. `PROJECT_STRUCTURE.md` — the canonical folder structure agents must maintain
12. `SYSTEM_WORKFLOW.md` — end-to-end workflow from user request to approved output
13. `USER_PROFILE.md` — persistent context about the user the system serves
14. `README_SYSTEM.md` — index and entry point for the governance layer
15. `RELAY_SYSTEM_PROTOCOL_SKILL.md` — relay skill reference for agent use

---

## Hardware

| Component | Spec |
|-----------|------|
| CPU | Intel i9-12900K |
| GPU | RTX 3080 (10 GB VRAM) |
| RAM | 32 GB DDR5 6000 MHz CL30 |
| OS | Ubuntu (WSL2 on Windows) |

The 10 GB VRAM constraint is intentional architecture: agents load one at a time. This is not a workaround — it is the correct approach for constrained local inference.

---

## How to Run

### Prerequisites

- [Ollama](https://ollama.com) installed and running
- Models pulled: `qwen3:14b`, `deepseek-r1:14b` (and optionally `gpt-oss:20b`)
- Python 3.10+

### Pull models

```bash
ollama pull qwen3:14b
ollama pull deepseek-r1:14b
```

### Register agents with Ollama

```bash
cd agents/
ollama create manager -f Manager.Modelfile
ollama create coder -f Coder.Modelfile
ollama create reviewer -f Reviewer.Modelfile
ollama create tester -f Tester.Modelfile
ollama create scraper -f Scraper.Modelfile
ollama create organizer -f Organizer.Modelfile
```

### Initialize the relay system

```bash
cd relay-system/scripts/
python3 relay.py --init
```

### Run a task

```bash
cd app/orchestrator/
python3 main.py --agent manager --task "Plan the first sprint for the rebuild."
```

---

## Current Status

**Architecture:** Validated. Turn-based loading, handoff-based context passing, and role-specialized agents are structurally sound and have been tested via scenario runs (see `relay-system/tests/`).

**Known gap:** The logging and inter-agent communication layer is not yet complete. When something breaks, agents do not have explicit instructions on how to write failure state in a format other agents can parse. This is the primary item being worked on.

**What has worked:** The system successfully cloned the FYP GitHub backup autonomously. The relay scenario tests passed. The orchestrator correctly invokes Ollama and logs output to the relay.

---

## What's Next

1. Complete the inter-agent logging format and failure recovery protocol
2. Finish the FYP rebuild (YahyaTel) using the system as proof of concept
3. Implement the hybrid cloud extension — local agents prepare context, cloud model (Claude / Codex) executes, state is exported before hitting rate limits, passed to next cloud model
4. Contribute to Arabic NLP tooling
5. Build toward a fully private, locally-hosted personal AI assistant

---

---

*Built by Icylito — May 2026*  
*Living document — updated as the system develops*
