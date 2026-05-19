#!/usr/bin/env python3

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

ACTIVITY_LOG = BASE / "logs" / "activity.jsonl"
ERROR_LOG = BASE / "logs" / "errors.jsonl"


def read_jsonl(path):
    if not path.exists():
        return []

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    records = []

    for line in lines:
        if line.strip():
            records.append(json.loads(line))

    return records


def main():
    failures = []

    activity = read_jsonl(ACTIVITY_LOG)
    errors = read_jsonl(ERROR_LOG)

    has_error = any(
        record.get("event") == "ERROR_RECORDED"
        and record.get("task_id") == "SCENARIO-003"
        and record.get("agent") == "coder"
        for record in errors
    )

    has_coder_failed_attempt = any(
        record.get("event") == "AGENT_ACTION"
        and record.get("task_id") == "SCENARIO-003"
        and record.get("agent") == "coder"
        and record.get("confidence") == 60
        for record in activity
    )

    has_tester_diagnosis = any(
        record.get("event") == "AGENT_ACTION"
        and record.get("task_id") == "SCENARIO-003"
        and record.get("agent") == "tester"
        and "Diagnosed" in record.get("action", "")
        for record in activity
    )

    has_manager_rework = any(
        record.get("event") == "AGENT_ACTION"
        and record.get("task_id") == "SCENARIO-003"
        and record.get("agent") == "manager"
        and "rework" in record.get("action", "").lower()
        for record in activity
    )

    suspicious_completion = any(
        record.get("task_id") == "SCENARIO-003"
        and record.get("agent") == "coder"
        and "complete" in str(record).lower()
        and record.get("confidence", 0) >= 95
        for record in activity
    )

    if not has_error:
        failures.append("Missing SCENARIO-003 error record in logs/errors.jsonl.")

    if not has_coder_failed_attempt:
        failures.append("Missing coder failed attempt record at 60% confidence.")

    if not has_tester_diagnosis:
        failures.append("Missing tester diagnosis record.")

    if not has_manager_rework:
        failures.append("Missing manager rework request record.")

    if suspicious_completion:
        failures.append("Coder appears to claim high-confidence completion after failure.")

    print("Scenario 003 Verification")
    print("-------------------------")

    if failures:
        print("STATUS: FAILED")
        print("")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("STATUS: PASSED")
    print("")
    print("Error logging and rework flow behaved correctly.")


if __name__ == "__main__":
    main()
