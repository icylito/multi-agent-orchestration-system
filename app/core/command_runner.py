import subprocess
from typing import Dict


ALLOWED_PREFIXES = [
    "python -c",
    "python - <<'PY'",
    "grep ",
    "cat ",
    "head ",
    "tail ",
    "ls ",
    "find ",
    "sed -n",
]


def is_allowed(command: str) -> bool:
    stripped = command.strip()
    return any(stripped.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def run_command(command: str) -> Dict[str, str]:
    if not is_allowed(command):
        return {
            "status": "BLOCKED",
            "stdout": "",
            "stderr": f"Command not allowed: {command}",
            "returncode": "N/A",
        }

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=30,
    )

    return {
        "status": "SUCCESS" if result.returncode == 0 else "FAILED",
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": str(result.returncode),
    }
