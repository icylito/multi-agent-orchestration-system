# App — Orchestrator Runtime

This directory contains the Python application that connects the user, the agents, and the relay system.

---

## What It Does

When you run `main.py`, it:

1. Loads the specified agent's configuration (model name, temperature, system prompt)
2. Injects persistent project context from `context/project_context.md`
3. Sends the task to the Ollama API and gets a response
4. Logs the task start and agent response to the relay system
5. Prints the task ID, agent name, model, and response

This is the glue layer. It does not define agent behavior (that lives in `agents/`) and it does not manage state (that lives in `relay-system/`). It connects them.

---

## File Structure

```
app/
└── orchestrator/
    ├── main.py              # Entry point
    ├── ollama_client.py     # HTTP client for Ollama API
    ├── relay_bridge.py      # Subprocess bridge to relay.py
    ├── context/
    │   └── project_context.md   # Persistent context injected into all agent calls
    └── prompts/
        ├── manager.md       # Manager agent system prompt (lightweight version)
        └── reviewer.md      # Reviewer agent system prompt (lightweight version)
```

---

## Files

### `main.py`

Entry point. Accepts two arguments:
- `--agent` (default: `manager`) — which agent to activate
- `--task` (required) — the task text to send

Currently wired for `manager` and `reviewer` agents. Extend the `AGENTS` dict to add more.

**Example:**
```bash
cd app/orchestrator/
python3 main.py --agent manager --task "Plan the rebuild sprint."
python3 main.py --agent reviewer --task "Review the auth module plan."
```

**Output:**
```
=== TASK ID ===
ORCH-7F3A9B2C

=== AGENT ===
manager

=== MODEL ===
qwen3:14b

=== RESPONSE ===
[agent response here]
```

Each task gets a unique ID (`ORCH-` prefix + 8 hex chars). This ID is used across all relay logs to trace the full history of a task.

---

### `ollama_client.py`

A minimal HTTP client for the Ollama `/api/chat` endpoint. Uses Python's standard library only — no third-party packages required.

- Default base URL: `http://localhost:11434/api`
- Timeout: 300 seconds (5 minutes — large models are slow)
- Non-streaming: waits for the full response before returning

**What it sends:**
```json
{
  "model": "qwen3:14b",
  "messages": [
    {"role": "system", "content": "<agent system prompt>"},
    {"role": "system", "content": "<persistent project context>"},
    {"role": "user", "content": "<task text>"}
  ],
  "stream": false,
  "options": {"temperature": 0.2}
}
```

Low temperature (0.1–0.2) is intentional. These agents are supposed to follow rules and produce structured output — creativity is not the goal.

---

### `relay_bridge.py`

Calls `relay.py` as a subprocess from within Python. This keeps the relay system as a standalone CLI tool (usable independently) while allowing the orchestrator to log events programmatically.

Two methods are currently used:
- `start_task(task_id, goal, agent)` — tells the relay a new task has started
- `log_action(agent, task_id, action, result, confidence)` — logs what the agent did and returned

---

### `context/project_context.md`

Persistent context injected as a second system message into every agent call. This is what allows agents to have project knowledge without being retrained.

Currently contains: YahyaTel FYP context — the project the system is being used to rebuild.

**To update:** edit this file directly. The next agent call will pick up the new context automatically.

---

### `prompts/manager.md` and `prompts/reviewer.md`

Lightweight system prompts used by the orchestrator when calling agents via the API directly (as opposed to using the Ollama Modelfiles). These are shorter versions of the full agent system prompts in `agents/`.

---

## How to Run

```bash
# Make sure Ollama is running
ollama serve

# Make sure the relay is initialized
cd relay-system/scripts/
python3 relay.py --init

# Run the orchestrator
cd app/orchestrator/
python3 main.py --agent manager --task "Your task here"
```

---

## Extending

To add a new agent to the orchestrator:

1. Add an entry to the `AGENTS` dict in `main.py`:
```python
AGENTS = {
    "manager": {...},
    "reviewer": {...},
    "coder": {
        "model": "qwen3:14b",
        "prompt": "prompts/coder.md",
        "temperature": 0.2
    }
}
```

2. Create the corresponding prompt file in `prompts/`.
3. Make sure the model is pulled in Ollama: `ollama pull qwen3:14b`
