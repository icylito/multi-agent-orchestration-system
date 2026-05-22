from app.agents.manager import create_handoff
from app.agents.coder import run_coder
from app.agents.reviewer import review_output
from app.agents.tester import run_tester
from app.core.handoff_file import read_handoff
from app.core.execute_patch import execute_patch
from app.core.test_executor import execute_test_plan


def main():
    print("=== Orchestra V2 ===")

    user_task = input("Enter task: ")

    print("\n[Manager] Creating handoff...\n")
    handoff = create_handoff(user_task)
    print(handoff)

    print("\n[Coder] Generating implementation packet...\n")
    coder_packet = run_coder()
    print(coder_packet.to_json())

    print("\n[Reviewer] Validating output...\n")
    review = review_output(read_handoff(), coder_packet.proposed_changes)
    print(review)

    if review.strip().startswith("PASS"):
        apply_choice = input("\nReviewer passed. Apply proposed patch? (y/n): ").strip().lower()

        if apply_choice == "y":
            print("\n[PatchExecutor] Applying patch...\n")
            patch_results = execute_patch(coder_packet.proposed_changes)
            for result in patch_results:
                print(result)
        else:
            print("\n[PatchExecutor] Skipped by user.")

        print("\n[Tester] Creating validation test...\n")
        test_plan = run_tester(user_task, review, coder_packet.relevant_files)
        print(test_plan)

        run_choice = input("\nRun tester command? (y/n): ").strip().lower()
        if run_choice == "y":
            print("\n[TestExecutor] Running test...\n")
            test_result = execute_test_plan(test_plan)
            print(test_result)
    else:
        print("\n[Tester] Skipped because reviewer did not PASS.")


if __name__ == "__main__":
    main()
