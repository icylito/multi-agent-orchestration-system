from app.models.ollama_client import generate
from app.core.logger import log_event

MODEL = "qwen3-coder:30b"


def run_tester(task: str, review: str) -> str:
    prompt = f"""
You are the Tester agent in a disciplined orchestration system.

Your responsibilities:
- Suggest minimal validation tests
- Verify accepted implementations
- Do not redesign architecture
- Do not create new frameworks
- Keep tests simple and practical

Task:
{task}

Reviewer Result:
{review}

Respond with:
1. Test Goal
2. Minimal Test Command
3. Expected Result
"""

    response = generate(prompt, model=MODEL)

    log_event(
        agent="Tester",
        action="run_tester",
        status="SUCCESS"
    )

    return response
