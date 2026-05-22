from app.core.state_manager import load_state


def print_status():
    state = load_state()

    if not state:
        print("No latest run state found.")
        return

    print("=== Latest Orchestra Run ===")
    print(f"Run ID: {state.get('run_id')}")
    print(f"Status: {state.get('status')}")
    print(f"Task: {state.get('task')}")
    print(f"Patched Files: {state.get('patched_files')}")

    test_result = state.get("test_result")
    if test_result:
        print(f"Test Status: {test_result.get('status')}")
        print(f"Test Return Code: {test_result.get('returncode')}")

    review = state.get("review")
    if review:
        first_line = review.splitlines()[0] if review.splitlines() else review
        print(f"Review: {first_line}")

    memory_summary = state.get("memory_summary")
    if memory_summary:
        print("\nMemory Summary:")
        print(memory_summary[:1000])
