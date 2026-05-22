import argparse

from app.core.pipeline import run_pipeline
from app.core.status_reporter import print_status
from app.agents.planner import create_plan
from app.core.task_queue import (
    add_task,
    list_tasks,
    get_next_ready_task,
    mark_completed,
    mark_failed,
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

    parser.add_argument("--queue-add", type=str, help="Add task to queue")
    parser.add_argument("--queue-list", action="store_true", help="List queued tasks")
    parser.add_argument("--queue-next", action="store_true", help="Show next ready task")
    parser.add_argument("--queue-complete", type=str, help="Mark task completed")
    parser.add_argument("--queue-fail", type=str, help="Mark task failed")
    parser.add_argument("--queue-run-next", action="store_true", help="Run next ready queued task")
    parser.add_argument("--queue-run-all", action="store_true", help="Run all ready queued tasks sequentially")

    args = parser.parse_args()

    if args.status:
        print_status()
        return

    if args.plan:
        print(create_plan(args.plan))
        return

    if args.queue_add:
        task = add_task(args.queue_add)
        print(task)
        return

    if args.queue_list:
        for task in list_tasks():
            print(task)
        return

    if args.queue_next:
        print(get_next_ready_task())
        return

    if args.queue_complete:
        print(mark_completed(args.queue_complete))
        return

    if args.queue_fail:
        print(mark_failed(args.queue_fail))
        return


    if args.queue_run_all:
        while True:
            task = get_next_ready_task()

            if not task:
                print("No more ready queued tasks.")
                return

            print(f"Running queued task: {task['id']} - {task['title']}")

            state = run_pipeline(
                user_task=task["title"],
                use_manager=args.manager and not args.no_manager,
                auto_apply=args.auto_apply,
                auto_test=args.auto_test,
            )

            if state.get("test_result", {}).get("status") == "SUCCESS":
                print(mark_completed(task["id"], result=state.get("status")))
                continue

            if state.get("status") in {"PATCH_SKIPPED", "TEST_SKIPPED"}:
                print(mark_completed(task["id"], result=state.get("status")))
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
            use_manager=args.manager and not args.no_manager,
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
