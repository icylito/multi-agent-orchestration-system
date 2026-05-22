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


def add_task(
    title: str,
    dependencies: Optional[List[str]] = None,
    goal: Optional[str] = None,
    constraints: Optional[List[str]] = None,
    priority: str = "normal",
    execution_mode: str = "direct",
) -> Dict:
    queue = load_queue()
    dependencies = dependencies or []
    constraints = constraints or []

    invalid_dependencies = [
        dep for dep in dependencies
        if not task_exists(dep)
    ]

    if invalid_dependencies:
        return {
            "status": "ERROR",
            "message": f"Invalid dependencies: {invalid_dependencies}"
        }

    task_id = f"task-{len(queue['tasks']) + 1}"

    task = {
        "id": task_id,
        "title": title,
        "goal": goal or title,
        "constraints": constraints,
        "priority": priority,
        "execution_mode": execution_mode,
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




def task_exists(task_id: str) -> bool:
    return get_task(task_id) is not None


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


def clear_queue():
    queue = _empty_queue()
    save_queue(queue)
    return queue


def queue_status():
    queue = load_queue()
    tasks = queue["tasks"]

    counts = {
        "pending": 0,
        "completed": 0,
        "failed": 0,
        "running": 0,
    }

    for task in tasks:
        status = task.get("status", "pending")
        counts[status] = counts.get(status, 0) + 1

    next_task = get_next_ready_task()

    return {
        "total": len(tasks),
        "counts": counts,
        "next_ready": next_task,
    }


def export_queue():
    return load_queue()


def import_queue(queue_data):
    is_valid, message = validate_queue_data(queue_data)

    if not is_valid:
        return {
            "status": "ERROR",
            "message": message
        }

    save_queue(queue_data)

    return {
        "status": "SUCCESS",
        "message": f"Imported {len(queue_data['tasks'])} tasks"
    }


def validate_queue_data(queue_data):
    if not isinstance(queue_data, dict):
        return False, "Queue data must be a dictionary"

    tasks = queue_data.get("tasks")

    if not isinstance(tasks, list):
        return False, "Queue data must contain a tasks list"

    seen_ids = set()

    for task in tasks:
        if not isinstance(task, dict):
            return False, "Each task must be a dictionary"

        required = ["id", "title", "goal", "constraints", "priority", "execution_mode", "status", "dependencies", "result", "error"]

        for key in required:
            if key not in task:
                return False, f"Task missing required key: {key}"

        if task["id"] in seen_ids:
            return False, f"Duplicate task id: {task['id']}"

        seen_ids.add(task["id"])

        if not isinstance(task["dependencies"], list):
            return False, f"Dependencies must be list for {task['id']}"

    for task in tasks:
        for dep in task["dependencies"]:
            if dep not in seen_ids:
                return False, f"Invalid dependency {dep} for {task['id']}"

    return True, "Queue data is valid"


def format_queue_table():
    tasks = list_tasks()

    if not tasks:
        return "Queue is empty."

    lines = []
    lines.append("ID | Status | Priority | Mode | Dependencies | Title")
    lines.append("---|--------|----------|------|--------------|------")

    for task in tasks:
        deps = ",".join(task.get("dependencies", [])) or "-"
        lines.append(
            f"{task.get('id')} | "
            f"{task.get('status')} | "
            f"{task.get('priority', 'normal')} | "
            f"{task.get('execution_mode', 'direct')} | "
            f"{deps} | "
            f"{task.get('title')}"
        )

    return "\n".join(lines)
