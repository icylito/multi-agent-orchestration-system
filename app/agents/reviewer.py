from app.models.ollama_client import generate
from app.core.logger import log_event

MODEL = "qwen3-coder:30b"


def review_output(handoff: str, coder_output: str) -> str:
    if "Status: BLOCKED" in coder_output or "BLOCKED" in coder_output[:200]:
        verdict = "BLOCKED\nCoder did not implement because required context or files were missing."
        log_event("Reviewer", "review_output", "BLOCKED")
        return verdict

    prompt = f"""
You are the Reviewer agent.

Your responsibilities:
- Detect fake systems/classes/methods
- Detect architecture drift
- Verify handoff compliance
- Reject unnecessary redesigns
- PASS only if the coder produced grounded implementation changes

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

    log_event("Reviewer", "review_output", "SUCCESS")
    return response
