import json
from datetime import datetime
from pathlib import Path

STATE_PATH = Path("relay-system/state/latest_run.json")


def save_state(state: dict):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    state["updated_at"] = datetime.utcnow().isoformat()

    STATE_PATH.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8"
    )


def load_state():
    if not STATE_PATH.exists():
        return {}

    return json.loads(STATE_PATH.read_text(encoding="utf-8"))
