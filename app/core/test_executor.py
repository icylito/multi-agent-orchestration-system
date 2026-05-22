import re
from app.core.command_runner import run_command


def extract_command(test_plan: str):
    # Inline backtick command
    match = re.search(r"Minimal Test Command:\s*`([^`]+)`", test_plan)
    if match:
        return match.group(1).strip()

    # Plain text after Minimal Test Command:
    match = re.search(r"Minimal Test Command:\s*(.+)", test_plan)
    if match:
        command = match.group(1).strip()
        command = command.replace("```", "").strip()
        return command

    # Fallback fenced command
    fenced = re.findall(r"```(?:bash|python)?\n?(.*?)```", test_plan, re.DOTALL)
    if fenced:
        return fenced[0].strip()

    return None


def execute_test_plan(test_plan: str):
    command = extract_command(test_plan)

    if not command:
        return {
            "status": "BLOCKED",
            "stdout": "",
            "stderr": "No executable command found in test plan.",
            "returncode": "N/A",
        }

    return run_command(command)
