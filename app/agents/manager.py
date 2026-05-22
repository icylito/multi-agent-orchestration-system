from app.models.ollama_client import generate
from app.core.handoff_file import write_handoff
from app.core.logger import log_event

MODEL = "qwen3-coder:30b"


def create_handoff(user_task: str) -> str:
    prompt = f"""
You are the Manager agent in a disciplined orchestration system.

Your job:
- Create a clean implementation handoff
- Do NOT solve the task yourself
- Do NOT redesign architecture
- Keep scope small
- Force the coder to modify minimal files
- Never claim an existing system exists unless repository context proves it
- Prevent fake systems/classes/methods

User task:
{user_task}

Respond ONLY in markdown.

Format:

# Task
# Constraints
# Expected Output
# Notes
"""

    response = generate(prompt, model=MODEL)

    write_handoff(response)

    log_event(
        agent="Manager",
        action="create_handoff",
        status="SUCCESS",
        details=user_task
    )

    return response
