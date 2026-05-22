from pathlib import Path
import difflib


def create_diff(file_path: str, new_content: str):
    path = Path(file_path)

    if not path.exists():
        return f"ERROR: File does not exist: {file_path}"

    old_lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"{file_path} (current)",
        tofile=f"{file_path} (proposed)",
    )

    return "".join(diff)


def create_diff_bundle(patches):
    diffs = []

    for patch in patches:
        diffs.append(create_diff(patch["file"], patch["content"]))

    return "\n".join(diffs)
