from pathlib import Path

HANDOFF_PATH = Path("relay-system/handoffs/active_handoff.md")


def write_handoff(content: str) -> None:
    HANDOFF_PATH.parent.mkdir(parents=True, exist_ok=True)
    HANDOFF_PATH.write_text(content, encoding="utf-8")


def read_handoff() -> str:
    if not HANDOFF_PATH.exists():
        return ""
    return HANDOFF_PATH.read_text(encoding="utf-8")
