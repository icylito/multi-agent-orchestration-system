from pathlib import Path


def rollback_file(file_path: str):
    path = Path(file_path)
    backup_path = path.with_suffix(path.suffix + ".bak")

    if not backup_path.exists():
        return {
            "status": "ERROR",
            "message": f"No backup found for {file_path}"
        }

    path.write_text(backup_path.read_text(encoding="utf-8"), encoding="utf-8")

    return {
        "status": "SUCCESS",
        "message": f"Rolled back {file_path} from {backup_path}"
    }


def rollback_many(file_paths):
    return [rollback_file(file_path) for file_path in file_paths]
