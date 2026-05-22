from app.agents.manager import create_handoff
from app.agents.coder import run_coder
from app.agents.reviewer import review_output
from app.agents.tester import run_tester
from app.core.handoff_file import read_handoff


def main():
    print("=== Orchestra V2 ===")

    user_task = input("Enter task: ")

    print("\n[Manager] Creating handoff...\n")
    handoff = create_handoff(user_task)
    print(handoff)

    print("\n[Coder] Generating implementation...\n")
    coder_output = run_coder()
    print(coder_output)

    print("\n[Reviewer] Validating output...\n")
    review = review_output(read_handoff(), coder_output)
    print(review)

    if review.strip().startswith("PASS"):
        print("\n[Tester] Creating validation test...\n")
        test_plan = run_tester(user_task, review)
        print(test_plan)
    else:
        print("\n[Tester] Skipped because reviewer did not PASS.")


if __name__ == "__main__":
    main()
