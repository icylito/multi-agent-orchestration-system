from app.core.patch_parser import extract_file_blocks
from app.core.patch_applier import apply_patch


def execute_patch(coder_output: str):
    patches = extract_file_blocks(coder_output)

    results = []

    for patch in patches:
        result = apply_patch(
            patch["file"],
            patch["content"]
        )

        result["file"] = patch["file"]
        results.append(result)

    return results


def get_successfully_patched_files(patch_results):
    return [
        result["file"]
        for result in patch_results
        if result.get("status") == "SUCCESS" and "file" in result
    ]
