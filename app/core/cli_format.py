def format_task_result(result, action=None):
    if not isinstance(result, dict):
        return str(result)

    if result.get("status") == "ERROR":
        return f"ERROR: {result.get('message')}"

    if "tasks" in result:
        return "Queue cleared."

    task_id = result.get("id")
    title = result.get("title")
    status = result.get("status")

    if task_id and title:
        if action == "add":
            return f"Added {task_id}: {title}"
        if action == "complete":
            return f"Marked {task_id} as completed."
        if action == "fail":
            return f"Marked {task_id} as failed."
        if action == "retry":
            return f"Reset {task_id} to pending."

        return f"{task_id}: {title} [{status}]"

    return str(result)
