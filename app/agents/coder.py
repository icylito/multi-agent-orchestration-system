from app.models.ollama_client import generate
from app.core.handoff_file import read_handoff
from app.core.logger import log_event
from app.core.repository_context import scan_repository, find_relevant_files, prepare_context_bundle

MODEL = "qwen3-coder:30b"


def _extract_keywords(handoff: str):
    words = handoff.replace("#", " ").replace("-", " ").replace(".", " ").split()

    keywords = []

    for word in words:
        clean = word.strip().lower()

        if len(clean) >= 5:
            keywords.append(clean)

    priority_keywords = [
        "execution",
        "controller",
        "retry",
        "handoff",
        "logger",
        "message",
        "routing",
        "agent",
    ]

    return list(dict.fromkeys(priority_keywords + keywords))[:25]


def _format_context(context_bundle):
    if not context_bundle:
        return "NO_RELEVANT_FILES_FOUND"

    parts = []

    for item in context_bundle:
        parts.append(
            f"\n--- FILE: {item['file']} ---\n{item['content']}\n--- END FILE ---"
        )

    return "\n".join(parts)


def run_coder() -> str:
    handoff = read_handoff()

    files = scan_repository(".")
    keywords = _extract_keywords(handoff)
    relevant_files = find_relevant_files(files, keywords)

    # Keep context small for now
    relevant_files = relevant_files[:5]
    context_bundle = prepare_context_bundle(relevant_files)
    repo_context = _format_context(context_bundle)

    prompt = f"""
You are the Coder agent in a disciplined orchestration system.

Rules:
- Use ONLY the repository context provided.
- Modify minimal files.
- Never redesign architecture.
- Never invent methods/classes/files.
- Follow handoff exactly.
- If required files are missing, say BLOCKED and explain what file is missing.
- If no relevant files are found, say BLOCKED.
- Do not produce code based on assumptions.

Handoff:

{handoff}

Repository Context:

{repo_context}

Respond with:
1. Status: READY or BLOCKED
2. Relevant Files Found
3. Understanding
4. Implementation Plan
5. Proposed Code Changes
"""

    response = generate(prompt, model=MODEL)

    log_event(
        agent="Coder",
        action="run_coder",
        status="SUCCESS",
        details=f"relevant_files={relevant_files}"
    )

    return response
