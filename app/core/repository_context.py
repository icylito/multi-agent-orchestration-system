from pathlib import Path


IMPORTANT_FILES = [
    "app/core/execution_controller.py",
    "app/core/config.py",
    "app/core/logger.py",
    "relay-system/config/settings.json",
    "relay-system/handoffs/active_handoff.md",
]


def scan_repository(root: str = "."):
    root_path = Path(root)
    return [str(path) for path in root_path.rglob("*") if path.is_file()]


def find_relevant_files(files, keywords):
    relevant = []

    # Always include important files if they exist
    for important in IMPORTANT_FILES:
        if important in files and important not in relevant:
            relevant.append(important)

    for file in files:
        lower = file.lower()
        if any(keyword.lower() in lower for keyword in keywords):
            if file not in relevant:
                relevant.append(file)

    return relevant


def load_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}"


def prepare_context_bundle(file_paths):
    bundle = []

    for path in file_paths:
        bundle.append({
            "file": path,
            "content": load_file_content(path)
        })

    return bundle
