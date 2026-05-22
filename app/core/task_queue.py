import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

QUEUE_PATH = Path("relay-system/state/task_queue.json")


def _now():
    return datetime.utcnow().isoformat()


def _empty_queue():
    return {
        "tasks": []
    }


def load_queue() -> Dict:
    if not QUEUE_PATH.exists():
        return _empty_queue()

    return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))


def save_queue(queue: Dict) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(queue, indent=2), encoding="utf-8")


def add_task(title: str, dependencies: Optional[List[str]] = None) -> Dict:
    queue = load_queue()
    dependencies = dependencies or []

    task_id = f"task-{len(queue['tasks']) + 1}"

    task = {
        "id": task_id,
        "title": title,
        "status": "pending",
        "dependencies": dependencies,
        "created_at": _now(),
        "updated_at": _now(),
        "result": None,
        "error": None,
    }

    queue["tasks"].append(task)
    save_queue(queue)

    return task


def list_tasks() -> List[Dict]:
    return load_queue()["tasks"]


def get_task(task_id: str) -> Optional[Dict]:
    for task in list_tasks():
        if task["id"] == task_id:
            return task
    return None


def _dependency_completed(queue: Dict, dependency_id: str) -> bool:
    for task in queue["tasks"]:
        if task["id"] == dependency_id:
            return task["status"] == "completed"
    return False


def get_next_ready_task() -> Optional[Dict]:
    queue = load_queue()

    for task in queue["tasks"]:
        if task["status"] != "pending":
            continue

        dependencies = task.get("dependencies", [])

        if all(_dependency_completed(queue, dep) for dep in dependencies):
            return task

    return None


def update_task_status(task_id: str, status: str, result=None, error=None) -> Optional[Dict]:
    queue = load_queue()

    for task in queue["tasks"]:
        if task["id"] == task_id:
            task["status"] = status
            task["updated_at"] = _now()
            task["result"] = result
            task["error"] = error
            save_queue(queue)
            return task

    return None


def mark_completed(task_id: str, result=None):
    return update_task_status(task_id, "completed", result=result)


def mark_failed(task_id: str, error=None):
    return update_task_status(task_id, "failed", error=error)
