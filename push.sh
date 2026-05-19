#!/bin/bash

echo "=== Cleaning up partial .git if it exists ==="
rm -rf .git

echo "=== Initializing git ==="
git init
git config user.email "yfaisal74@gmail.com"
git config user.name "Icylito"
git branch -M main

echo "=== Staging files ==="
git add .

echo "=== Status check (FYP_2 should NOT appear) ==="
git status

echo "=== Committing ==="
git commit -m "feat: initial commit — multi-agent-orchestration-system

- Turn-based local AI agent runtime on RTX 3080 (10GB VRAM)
- 7 specialized agents: Manager, Coder, Reviewer, Tester, Scraper, Organizer
- Relay system: append-only logs, handoff archive, state tracking (relay.py)
- Full SYSTEM governance layer: 15 protocol documents written before code
- Orchestrator runtime: main.py, ollama_client.py, relay_bridge.py
- .gitignore: excludes external/FYP_2 (.venv 1.1GB), __pycache__, secrets
- Added: README.md, agents/README.md, app/README.md, memory/README.md
- Added: docs/GITHUB_PUSH_PREP.md"

echo "=== Adding remote and pushing ==="
git remote add origin https://github.com/icylito/multi-agent-orchestration-system.git
git push -u origin main

echo "=== Done! Check https://github.com/icylito/multi-agent-orchestration-system ==="
