import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("relay-system/logs/activity.jsonl")


def log_event(agent: str, action: str, status: str, details: str = "") -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent": agent,
        "action": action,
        "status": status,
        "details": details,
    }

    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
