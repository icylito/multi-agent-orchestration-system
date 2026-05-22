from app.agents.manager import create_handoff
from app.core.direct_handoff import create_direct_handoff
from app.agents.coder import run_coder
from app.agents.reviewer import review_output
from app.agents.tester import run_tester
from app.core.handoff_file import read_handoff
from app.core.execute_patch import execute_patch, get_successfully_patched_files
from app.core.test_executor import execute_test_plan
from app.core.rollback import rollback_many
from app.core.state_manager import save_state


def main():
    print("=== Orchestra V2 ===")

    state = {
        "status": "STARTED",
        "task": None,
        "handoff": None,
        "coder_packet": None,
        "review": None,
        "patch_results": None,
        "patched_files": [],
        "test_plan": None,
        "test_result": None,
        "rollback_results": None,
    }

    user_task = input("Enter task: ")
    state["task"] = user_task
    save_state(state)

    use_manager = input("Use Manager? (y/n): ").strip().lower()

    if use_manager == "y":
        print("\n[Manager] Creating handoff...\n")
        handoff = create_handoff(user_task)
        state["status"] = "MANAGER_HANDOFF_CREATED"
    else:
        print("\n[DirectHandoff] Creating direct handoff...\n")
        handoff = create_direct_handoff(user_task)
        state["status"] = "DIRECT_HANDOFF_CREATED"

    state["handoff"] = handoff
    save_state(state)
    print(handoff)

    print("\n[Coder] Generating implementation packet...\n")
    coder_packet = run_coder()
    state["coder_packet"] = coder_packet.to_dict()
    state["status"] = "CODER_COMPLETED"
    save_state(state)
    print(coder_packet.to_json())

    print("\n[Reviewer] Validating output...\n")
    review = review_output(read_handoff(), coder_packet.proposed_changes)
    state["review"] = review
    state["status"] = "REVIEW_COMPLETED"
    save_state(state)
    print(review)

    if review.strip().startswith("PASS"):
        apply_choice = input("\nReviewer passed. Apply proposed patch? (y/n): ").strip().lower()

        if apply_choice == "y":
            print("\n[PatchExecutor] Applying patch...\n")
            patch_results = execute_patch(coder_packet.proposed_changes)
            patched_files = get_successfully_patched_files(patch_results)

            state["patch_results"] = patch_results
            state["patched_files"] = patched_files
            state["status"] = "PATCH_APPLIED"
            save_state(state)

            for result in patch_results:
                print(result)
        else:
            state["status"] = "PATCH_SKIPPED"
            save_state(state)
            print("\n[PatchExecutor] Skipped by user.")

        print("\n[Tester] Creating validation test...\n")
        test_plan = run_tester(user_task, review, coder_packet.relevant_files)
        state["test_plan"] = test_plan
        state["status"] = "TEST_PLAN_CREATED"
        save_state(state)
        print(test_plan)

        run_choice = input("\nRun tester command? (y/n): ").strip().lower()
        if run_choice == "y":
            print("\n[TestExecutor] Running test...\n")
            test_result = execute_test_plan(test_plan)
            state["test_result"] = test_result
            state["status"] = "TEST_EXECUTED"
            save_state(state)
            print(test_result)

            if test_result.get("status") != "SUCCESS":
                rollback_choice = input("\nTest failed. Rollback applied patch? (y/n): ").strip().lower()
                if rollback_choice == "y":
                    rollback_results = rollback_many(state["patched_files"])
                    state["rollback_results"] = rollback_results
                    state["status"] = "ROLLED_BACK"
                    save_state(state)

                    print("\n[Rollback] Results:")
                    for result in rollback_results:
                        print(result)
        else:
            state["status"] = "TEST_SKIPPED"
            save_state(state)
    else:
        state["status"] = "REVIEW_NOT_PASS"
        save_state(state)
        print("\n[Tester] Skipped because reviewer did not PASS.")


if __name__ == "__main__":
    main()
