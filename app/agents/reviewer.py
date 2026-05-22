from app.models.ollama_client import generate
from app.core.logger import log_event
from pathlib import Path

MODEL = "qwen3-coder:30b"


def review_output(handoff: str, coder_output: str) -> str:
    upper = coder_output.upper()

    if "BLOCKED" in upper[:500]:
        verdict = "BLOCKED\nCoder did not implement because required context or files were missing."
        log_event("Reviewer", "review_output", "BLOCKED")
        return verdict

    placeholder_phrases = [
        "1. Status\n2. Summary\n3. Proposed Changes",
        "Proposed Changes",
    ]

    if coder_output.strip() in placeholder_phrases or len(coder_output.strip()) < 80:
        verdict = "NEEDS_REVISION\nCoder output is placeholder or too short. No grounded implementation was provided."
        log_event("Reviewer", "review_output", "NEEDS_REVISION")
        return verdict

    if "--- FILE:" not in coder_output or "--- END FILE ---" not in coder_output:
        verdict = "NEEDS_REVISION\nCoder output does not include required FILE blocks for patch application."
        log_event("Reviewer", "review_output", "NEEDS_REVISION")
        return verdict

    prompt = f"""
You are the Reviewer agent.

Rules:
- PASS only if coder produced concrete grounded code changes.
- NEEDS_REVISION if output is placeholder, generic, or missing actual code.
- FAIL if coder invented non-existent files, languages, methods, or systems.
- Reject Node.js/Java/other language assumptions unless repository context proves them.
- Verify handoff compliance.

Handoff:
{handoff}

Coder Output:
{coder_output}

Respond ONLY with:
PASS
or
NEEDS_REVISION
or
FAIL

Then explain briefly why.
"""

    response = generate(prompt, model=MODEL)

    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/latest_review.txt").write_text(response, encoding="utf-8")

    log_event("Reviewer", "review_output", "SUCCESS")
    return response
