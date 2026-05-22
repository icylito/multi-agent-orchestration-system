import argparse

from app.core.pipeline import run_pipeline
from app.core.status_reporter import print_status
from app.core.cli_format import format_task_result
from app.agents.planner import create_plan
from app.agents.plan_queue import create_plan_queue
from app.core.task_queue import (
    add_task,
    list_tasks,
    get_next_ready_task,
    mark_completed,
    mark_failed,
    clear_queue,
    queue_status,
    export_queue,
    import_queue,
    format_queue_table,
    retry_task,
    skip_task,
    validate_queue_data,
)


def interactive_mode():
    print("=== Orchestra V2 Queue Mode ===")
    print("Type 'exit' to stop.\n")

    while True:
        user_task = input("Enter task: ").strip()

        if user_task.lower() in {"exit", "quit", "q"}:
            print("Exiting Orchestra V2.")
            break

        if not user_task:
            continue

        use_manager_answer = input(
            "Use Manager for planning? Default is no. (y/n): "
        ).strip().lower()

        use_manager = use_manager_answer == "y"

        run_pipeline(
            user_task=user_task,
            use_manager=use_manager,
        )

        print("\n=== Task complete. Ready for next task. ===\n")


def main():
    parser = argparse.ArgumentParser(description="Orchestra V2 CLI")

    parser.add_argument("--task", type=str, help="Run a single task")
    parser.add_argument("--manager", action="store_true", help="Use Manager planning")
    parser.add_argument("--no-manager", action="store_true", help="Skip Manager planning")
    parser.add_argument("--auto-apply", action="store_true", help="Automatically apply patches")
    parser.add_argument("--auto-test", action="store_true", help="Automatically run tests")

    parser.add_argument("--status", action="store_true", help="Show latest run status")
    parser.add_argument("--plan", type=str, help="Create a non-executing plan")
    parser.add_argument("--plan-queue", type=str, help="Create a queue JSON from a larger goal")

    parser.add_argument("--queue-add", type=str, help="Add task to queue")
    parser.add_argument("--depends-on", type=str, help="Comma-separated dependency task IDs")
    parser.add_argument("--priority", type=str, default="normal", help="Task priority")
    parser.add_argument("--execution-mode", type=str, default="direct", help="Task execution mode")
    parser.add_argument("--constraint", action="append", default=[], help="Task constraint; can be used multiple times")
    parser.add_argument("--note", type=str, default="", help="Task note")
    parser.add_argument("--tag", action="append", default=[], help="Task tag; can be used multiple times")
    parser.add_argument("--created-by", type=str, default="human", help="Task creator")
    parser.add_argument("--queue-list", action="store_true", help="List queued tasks")
    parser.add_argument("--queue-table", action="store_true", help="Show queue as table")
    parser.add_argument("--queue-next", action="store_true", help="Show next ready task")
    parser.add_argument("--queue-complete", type=str, help="Mark task completed")
    parser.add_argument("--queue-fail", type=str, help="Mark task failed")
    parser.add_argument("--queue-retry", type=str, help="Reset failed task to pending")
    parser.add_argument("--queue-skip", type=str, help="Mark task as skipped")
    parser.add_argument("--queue-run-next", action="store_true", help="Run next ready queued task")
    parser.add_argument("--queue-run-all", action="store_true", help="Run all ready queued tasks sequentially")
    parser.add_argument("--max-tasks", type=int, default=5, help="Maximum queued tasks to run in one run-all session")
    parser.add_argument("--queue-clear", action="store_true", help="Clear all queued tasks")
    parser.add_argument("--yes", action="store_true", help="Confirm destructive actions")
    parser.add_argument("--queue-status", action="store_true", help="Show queue status summary")
    parser.add_argument("--queue-export", action="store_true", help="Print full queue JSON")
    parser.add_argument("--queue-import", type=str, help="Import queue from JSON file")
    parser.add_argument("--queue-validate", action="store_true", help="Validate current queue data")

    args = parser.parse_args()

    if args.status:
        print_status()
        return

    if args.plan:
        print(create_plan(args.plan))
        return

    if args.plan_queue:
        import json
        queue = create_plan_queue(args.plan_queue)
        print(json.dumps(queue, indent=2))
        return

    if args.queue_clear:
        if not args.yes:
            print("Refusing to clear queue without --yes.")
            return

        print(format_task_result(clear_queue()))
        return

    if args.queue_status:
        print(queue_status())
        return

    if args.queue_export:
        import json
        print(json.dumps(export_queue(), indent=2))
        return

    if args.queue_import:
        import json
        from pathlib import Path

        path = Path(args.queue_import)

        if not path.exists():
            print({"status": "ERROR", "message": f"File not found: {args.queue_import}"})
            return

        queue_data = json.loads(path.read_text(encoding="utf-8"))
        print(import_queue(queue_data))
        return

    if args.queue_validate:
        is_valid, message = validate_queue_data(export_queue())
        print({
            "valid": is_valid,
            "message": message
        })
        return

    if args.queue_add:
        dependencies = []
        if args.depends_on:
            dependencies = [dep.strip() for dep in args.depends_on.split(",") if dep.strip()]

        task = add_task(
    title=args.queue_add,
    dependencies=dependencies,
    notes=args.note,
    tags=args.tag,
    created_by=args.created_by,
    priority=args.priority,
    execution_mode=args.execution_mode,
)
        print(format_task_result(task, action='add'))
        return

    if args.queue_list:
        for task in list_tasks():
            print(format_task_result(task, action='add'))
        return

    if args.queue_table:
        print(format_queue_table())
        return

    if args.queue_next:
        print(get_next_ready_task())
        return

    if args.queue_complete:
        print(format_task_result(mark_completed(args.queue_complete), action='complete'))
        return

    if args.queue_fail:
        print(format_task_result(mark_failed(args.queue_fail), action='fail'))
        return

    if args.queue_retry:
        print(format_task_result(retry_task(args.queue_retry), action='retry'))
        return

    if args.queue_skip:
        print(format_task_result(skip_task(args.queue_skip), action='skip'))
        return


    if args.queue_run_all:
        is_valid, message = validate_queue_data(export_queue())

        if not is_valid:
            print({
                "status": "ERROR",
                "message": f"Queue validation failed: {message}"
            })
            return

        tasks_run = 0

        while True:
            if tasks_run >= args.max_tasks:
                print(f"Reached max task limit: {args.max_tasks}")
                return
            task = get_next_ready_task()

            if not task:
                print("No more ready queued tasks.")
                return

            print(f"Running queued task: {task['id']} - {task['title']}")

            state = run_pipeline(
                user_task=task["goal"],
                use_manager=(task.get("execution_mode") == "manager") or (args.manager and not args.no_manager),
                auto_apply=args.auto_apply,
                auto_test=args.auto_test,
                constraints=task.get("constraints", []),
                priority=task.get("priority", "normal"),
            )

            if state.get("test_result", {}).get("status") == "SUCCESS":
                print(mark_completed(task["id"], result=state.get("status")))
                tasks_run += 1
                continue

            if state.get("status") in {"PATCH_SKIPPED", "TEST_SKIPPED"}:
                print(mark_completed(task["id"], result=state.get("status")))
                tasks_run += 1
                continue

            print(mark_failed(task["id"], error=state.get("status")))
            print("Stopping queue execution because a task failed.")
            return

    if args.queue_run_next:
        task = get_next_ready_task()

        if not task:
            print("No ready queued task found.")
            return

        print(f"Running queued task: {task['id']} - {task['title']}")

        state = run_pipeline(
            user_task=task["title"],
            use_manager=(task.get("execution_mode") == "manager") or (args.manager and not args.no_manager),
            auto_apply=args.auto_apply,
            auto_test=args.auto_test,
        )

        if state.get("test_result", {}).get("status") == "SUCCESS":
            print(mark_completed(task["id"], result=state.get("status")))
        elif state.get("status") in {"PATCH_SKIPPED", "TEST_SKIPPED"}:
            print(mark_completed(task["id"], result=state.get("status")))
        else:
            print(mark_failed(task["id"], error=state.get("status")))

        return

    if args.task:
        use_manager = args.manager and not args.no_manager

        run_pipeline(
            user_task=args.task,
            use_manager=use_manager,
            auto_apply=args.auto_apply,
            auto_test=args.auto_test,
        )
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
