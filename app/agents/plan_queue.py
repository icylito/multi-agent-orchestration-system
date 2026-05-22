import json
import re
from pathlib import Path
from app.models.ollama_client import generate
from app.core.logger import log_event

MODEL = "qwen3-coder:30b"
PLANNED_QUEUE_PATH = Path("relay-system/state/planned_queue.json")


def create_plan_queue(user_task: str) -> dict:
    prompt = f"""
You are the Planner agent for Orchestra V2.

Create an MVP-safe task queue for this goal.

Rules:
- Output ONLY valid JSON
- No markdown
- No commentary
- Sequential tasks only unless dependency is truly required
- Use simple task ids: task-1, task-2, task-3
- Each task must be small enough for one pipeline run
- Avoid enterprise-scale features
- Use this exact JSON shape:

{{
  "tasks": [
    {{
      "id": "task-1",
      "title": "Small concrete task",
      "status": "pending",
      "dependencies": [],
      "result": null,
      "error": null
    }}
  ]
}}

Goal:
{user_task}
"""

    response = generate(prompt, model=MODEL)
    data = _parse_json(response)

    PLANNED_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLANNED_QUEUE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

    log_event(
        agent="PlanQueue",
        action="create_plan_queue",
        status="SUCCESS",
        details=user_task
    )

    return data


def _parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\\{.*\\}", text, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))
