from app.core.handoff_file import write_handoff
from app.core.logger import log_event


def create_direct_handoff(user_task: str) -> str:
    handoff = f"""# Task
{user_task}

# Constraints
- Use repository context only
- Modify only files that already exist unless explicitly requested
- Do not redesign architecture
- Do not invent methods/classes/files
- Keep changes minimal and focused
- Provide full updated file content using FILE blocks
- If blocked, say BLOCKED clearly

# Expected Output
- Concrete grounded implementation
- Minimal patchable FILE blocks
- No placeholder output
- No markdown code fences

# Notes
- This handoff was created directly from the user task without Manager expansion
- Coder must rely on repository context, not assumptions
"""

    write_handoff(handoff)

    log_event(
        agent="DirectHandoff",
        action="create_direct_handoff",
        status="SUCCESS",
        details=user_task
    )

    return handoff
