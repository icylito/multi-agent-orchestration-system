import re
from app.core.command_runner import run_command


def clean_command(command: str):
    command = command.strip()
    command = command.replace("```bash", "").replace("```python", "").replace("```", "").strip()

    # Remove markdown bullet/number prefix
    command = re.sub(r"^\s*[-*]\s*", "", command)
    command = re.sub(r"^\s*\d+\.\s*", "", command)

    return command.strip()


def extract_command(test_plan: str):
    # Inline backtick after Minimal Test Command
    match = re.search(r"Minimal Test Command:\s*`([^`]+)`", test_plan, re.IGNORECASE)
    if match:
        return clean_command(match.group(1))

    # Fenced code block anywhere
    fenced = re.findall(r"```(?:bash|python)?\n?(.*?)```", test_plan, re.DOTALL | re.IGNORECASE)
    if fenced:
        return clean_command(fenced[0])

    # Plain text after Minimal Test Command
    match = re.search(r"Minimal Test Command:\s*(.+)", test_plan, re.IGNORECASE)
    if match:
        return clean_command(match.group(1))

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
