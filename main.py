import argparse

from app.core.pipeline import run_pipeline
from app.core.status_reporter import print_status
from app.agents.planner import create_plan
from app.core.task_queue import add_task, list_tasks, get_next_ready_task, mark_completed, mark_failed


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
    parser.add_argument("--queue-add", type=str, help="Add a task to the queue")
    parser.add_argument("--queue-list", action="store_true", help="List queued tasks")
    parser.add_argument("--queue-next", action="store_true", help="Show next ready task")
    parser.add_argument("--queue-complete", type=str, help="Mark task completed by ID")
    parser.add_argument("--queue-fail", type=str, help="Mark task failed by ID")
    parser.add_argument("--plan", type=str, help="Create a non-executing plan for a larger task")

    args = parser.parse_args()

    if args.status:
        print_status()
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

    if args.plan:
        print(create_plan(args.plan))
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
