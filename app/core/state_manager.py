import json
from datetime import datetime
from pathlib import Path

STATE_PATH = Path("relay-system/state/latest_run.json")
RUNS_DIR = Path("relay-system/state/runs")


def save_state(state: dict):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.utcnow().isoformat()
    state["updated_at"] = now

    if "run_id" not in state or not state["run_id"]:
        safe_time = now.replace(":", "-").replace(".", "-")
        state["run_id"] = f"run-{safe_time}"

    latest_json = json.dumps(state, indent=2)

    STATE_PATH.write_text(latest_json, encoding="utf-8")

    archive_path = RUNS_DIR / f"{state['run_id']}.json"
    archive_path.write_text(latest_json, encoding="utf-8")


def load_state():
    if not STATE_PATH.exists():
        return {}

    return json.loads(STATE_PATH.read_text(encoding="utf-8"))
