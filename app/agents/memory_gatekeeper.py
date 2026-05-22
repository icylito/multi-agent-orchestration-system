from pathlib import Path
from app.models.ollama_client import generate
from app.core.logger import log_event

MODEL = "qwen3-coder:30b"
MEMORY_PATH = Path("memory/working/latest_summary.md")


def run_memory_gatekeeper(state: dict) -> str:
    prompt = f"""
You are the MemoryGatekeeper agent.

Your job:
- Summarize only useful project memory from this run
- Do not save temporary noise
- Do not save full logs unless necessary
- Capture architecture decisions, working features, bugs, and next steps

Run State:
{state}

Respond in markdown with:
# Summary
# Important Decisions
# Working Features
# Problems Found
# Next Steps
"""

    response = generate(prompt, model=MODEL)

    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_PATH.write_text(response, encoding="utf-8")

    log_event(
        agent="MemoryGatekeeper",
        action="save_latest_summary",
        status="SUCCESS"
    )

    return response
