from app.models.ollama_client import generate
from app.core.logger import log_event
from app.core.repository_context import prepare_context_bundle

MODEL = "qwen3-coder:30b"


def run_tester(task: str, review: str, relevant_files=None) -> str:
    relevant_files = relevant_files or []
    context = prepare_context_bundle(relevant_files[:5])

    formatted_context = "\n".join(
        f"\n--- FILE: {item['file']} ---\n{item['content']}\n--- END FILE ---"
        for item in context
    )

    prompt = f"""
You are the Tester agent.

Rules:
- Use ONLY the repository context.
- Do not assume Node.js, Java, pytest, or any framework unless shown in context.
- If no executable test is possible, say BLOCKED.
- Provide a Python command only if the repo is Python.
- Do not use markdown code fences.
- Minimal Test Command must be one single-line command.
- If validating text above a target line, use grep -B.
- If validating text below a target line, use grep -A.
- If validating text above a line, use grep -B.
- If validating text below a line, use grep -A.

Task:
{task}

Reviewer Result:
{review}

Repository Context:
{formatted_context}

Respond with:
1. Status: READY or BLOCKED
2. Test Goal
3. Minimal Test Command: provide ONE executable shell command on a single line, no markdown fences
4. Expected Result
"""

    response = generate(prompt, model=MODEL)
    log_event("Tester", "run_tester", "SUCCESS")
    return response
