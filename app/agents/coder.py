from app.models.ollama_client import generate
from app.core.handoff_file import read_handoff
from app.core.logger import log_event
from app.core.repository_context import (
    scan_repository,
    find_relevant_files,
    prepare_context_bundle,
)
from app.core.execution_packet import ExecutionPacket
from pathlib import Path

MODEL = "qwen3-coder:30b"


def _extract_keywords(handoff: str):
    words = handoff.replace("#", " ").replace("-", " ").split()

    keywords = []

    for word in words:
        clean = word.strip().lower()

        if len(clean) >= 5:
            keywords.append(clean)

    return list(dict.fromkeys(keywords))[:20]


def _format_context(bundle):
    if not bundle:
        return "NO_CONTEXT"

    parts = []

    for item in bundle:
        parts.append(
            f"\n--- FILE: {item['file']} ---\n{item['content']}\n--- END FILE ---"
        )

    return "\n".join(parts)


def run_coder(feedback: str = ''):
    handoff = read_handoff()

    files = scan_repository(".")
    keywords = _extract_keywords(handoff)

    relevant_files = find_relevant_files(files, keywords)[:5]

    bundle = prepare_context_bundle(relevant_files)

    context = _format_context(bundle)

    prompt = f"""
You are the Coder agent.

Rules:
- Never invent methods/classes/files
- Never redesign architecture
- Use ONLY provided repository context
- If blocked, say BLOCKED clearly

Handoff:
{handoff}

Reviewer Feedback:
{feedback if feedback else 'NO_FEEDBACK'}

Repository Context:
{context}

Respond with actual content, not headings only.

Required format:

Status: READY or BLOCKED

Summary:
Write a concrete summary of what you will change.

Proposed Changes:
Provide full updated file content using this exact format:

--- FILE: path/to/file.py ---
full file content here
--- END FILE ---

Rules:
- Do not use markdown code fences.
- Do not use ```python blocks.
- Do not describe changes instead of giving file blocks.
- If you cannot provide full updated file content in FILE blocks, respond BLOCKED and explain why.
"""

    response = generate(prompt, model=MODEL)

    status = "READY"

    if "BLOCKED" in response.upper():
        status = "BLOCKED"

    packet = ExecutionPacket(
        agent="Coder",
        status=status,
        summary="Coder execution completed",
        relevant_files=relevant_files,
        proposed_changes=response,
    )

    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/latest_coder_packet.json").write_text(packet.to_json(), encoding="utf-8")

    log_event(
        "Coder",
        "run_coder",
        status,
        str(relevant_files)
    )

    return packet
