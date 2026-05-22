from pathlib import Path


def apply_patch(file_path: str, content: str):
    path = Path(file_path)

    if not path.exists():
        return {
            "status": "ERROR",
            "message": f"File does not exist: {file_path}"
        }

    backup_path = path.with_suffix(path.suffix + ".bak")

    # Backup current file
    backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

    # Write new content
    path.write_text(content, encoding="utf-8")

    return {
        "status": "SUCCESS",
        "message": f"Patched {file_path}",
        "backup": str(backup_path)
    }
