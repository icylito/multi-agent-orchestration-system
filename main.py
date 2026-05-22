from app.core.pipeline import run_pipeline


def main():
    print("=== Orchestra V2 Queue Mode ===")
    print("Type 'exit' to stop.\n")

    while True:
        user_task = input("Enter task: ").strip()

        if user_task.lower() in {"exit", "quit", "q"}:
            print("Exiting Orchestra V2.")
            break

        if not user_task:
            continue

        use_manager_answer = input("Use Manager for planning? Default is no. (y/n): ").strip().lower()
        use_manager = use_manager_answer == "y"

        run_pipeline(user_task=user_task, use_manager=use_manager)

        print("\n=== Task complete. Ready for next task. ===\n")


if __name__ == "__main__":
    main()
