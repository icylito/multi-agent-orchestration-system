from app.agents.manager import create_handoff
from app.core.direct_handoff import create_direct_handoff
from app.agents.coder import run_coder
from app.agents.reviewer import review_output
from app.agents.tester import run_tester
from app.agents.memory_gatekeeper import run_memory_gatekeeper
from app.core.handoff_file import read_handoff
from app.core.execute_patch import execute_patch, get_successfully_patched_files
from app.core.test_executor import execute_test_plan
from app.core.rollback import rollback_many
from app.core.state_manager import save_state
from app.core.patch_parser import extract_file_blocks
from app.core.diff_preview import create_diff_bundle


MAX_REVIEW_RETRIES = 1


def run_pipeline(
    user_task: str,
    use_manager: bool = False,
    auto_apply: bool = False,
    auto_test: bool = False,
    constraints=None,
    priority="normal",
):
    constraints = constraints or []

    state = {
        "run_id": None,
        "status": "STARTED",
        "task": user_task,
        "constraints": constraints,
        "priority": priority,
        "handoff": None,
        "coder_packet": None,
        "review": None,
        "review_attempts": [],
        "patch_results": None,
        "patched_files": [],
        "test_plan": None,
        "test_result": None,
        "rollback_results": None,
        "memory_summary": None,
    }

    save_state(state)

    if use_manager:
        print("\n[Manager] Creating handoff...\n")
        handoff = create_handoff(user_task)
        state["status"] = "MANAGER_HANDOFF_CREATED"
    else:
        print("\n[DirectHandoff] Creating direct handoff...\n")
        handoff = create_direct_handoff(
            user_task=user_task,
            constraints=constraints,
            priority=priority,
        )
        state["status"] = "DIRECT_HANDOFF_CREATED"

    state["handoff"] = handoff
    save_state(state)
    print(handoff)

    feedback = ""
    coder_packet = None
    review = ""

    for attempt in range(MAX_REVIEW_RETRIES + 1):
        print(f"\n[Coder] Generating implementation packet... attempt {attempt + 1}\n")
        coder_packet = run_coder(feedback=feedback)
        state["coder_packet"] = coder_packet.to_dict()
        state["status"] = f"CODER_COMPLETED_ATTEMPT_{attempt + 1}"
        save_state(state)
        print(coder_packet.to_json())

        print("\n[Reviewer] Validating output...\n")
        review = review_output(read_handoff(), coder_packet.proposed_changes)
        state["review"] = review
        state["review_attempts"].append({
            "attempt": attempt + 1,
            "review": review,
        })
        state["status"] = f"REVIEW_COMPLETED_ATTEMPT_{attempt + 1}"
        save_state(state)
        print(review)

        if review.strip().startswith("PASS"):
            break

        if review.strip().startswith("NEEDS_REVISION") and attempt < MAX_REVIEW_RETRIES:
            feedback = review
            print("\n[RetryLoop] Reviewer requested revision. Sending feedback to coder.")
            continue

        print("\n[Tester] Skipped because reviewer did not PASS.")
        state["status"] = "REVIEW_NOT_PASS"
        save_state(state)
        _finalize_memory(state)
        return state

    if not review.strip().startswith("PASS"):
        print("\n[Tester] Skipped because reviewer did not PASS.")
        state["status"] = "REVIEW_NOT_PASS"
        save_state(state)
        _finalize_memory(state)
        return state

    patches = extract_file_blocks(coder_packet.proposed_changes)

    print("\n[DiffPreview] Proposed changes:\n")
    if patches:
        print(create_diff_bundle(patches))
    else:
        print("No patchable FILE blocks found.")

    apply_choice = "y" if auto_apply else input("\nReviewer passed. Apply proposed patch? (y/n): ").strip().lower()

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

    run_choice = "y" if auto_test else input("\nRun tester command? (y/n): ").strip().lower()

    if run_choice == "y":
        print("\n[TestExecutor] Running test...\n")
        test_result = execute_test_plan(test_plan)
        state["test_result"] = test_result
        state["status"] = "TEST_EXECUTED"
        save_state(state)
        print(test_result)

        if test_result.get("status") == "FAILED":
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

    _finalize_memory(state)
    return state


def _finalize_memory(state):
    print("\n[MemoryGatekeeper] Saving run summary...\n")
    summary = run_memory_gatekeeper(state)
    state["memory_summary"] = summary
    save_state(state)
    print(summary)
