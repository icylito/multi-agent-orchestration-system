from app.models.ollama_client import generate
from app.core.logger import log_event

MODEL = "qwen3-coder:30b"


def create_plan(user_task: str) -> str:
    prompt = f"""
You are the Planner agent for Orchestra V2. You must plan MVP-safe work, not enterprise-scale systems.

Your job:
- Break a larger task into safe subtasks
- Prefer the smallest useful implementation
- Avoid concurrency unless explicitly requested
- Avoid enterprise-scale features unless explicitly requested
- Prefer disk-based JSON persistence for state because Orchestra V2 already uses local state files
- Each subtask should be executable by the current CLI pipeline
- Identify dependencies
- Identify risks
- Recommend execution order
- Do NOT write implementation code
- Do NOT modify files
- Do NOT create patches
- Keep each subtask small enough for one execution pipeline run

Task:
{user_task}

Respond in markdown with:

# Goal
# Subtasks
# Dependencies
# Risks
# Recommended Execution Order
# Out of Scope
# Stop Conditions
"""

    response = generate(prompt, model=MODEL)

    log_event(
        agent="Planner",
        action="create_plan",
        status="SUCCESS",
        details=user_task
    )

    return response
