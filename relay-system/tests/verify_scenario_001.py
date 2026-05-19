#!/usr/bin/env python3

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

required_files = [
    BASE / "config" / "agents.json",
    BASE / "logs" / "activity.jsonl",
    BASE / "logs" / "rate-limit.jsonl",
    BASE / "state" / "state.jsonl",
    BASE / "handoffs" / "handoff-index.jsonl",
    BASE / "handoffs" / "latest-handoff.md",
]

archive_dir = BASE / "handoffs" / "archive"


def read_jsonl(path):
    if not path.exists():
        return []

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    records = []

    for line in lines:
        if line.strip():
            records.append(json.loads(line))

    return records


def check_required_files():
    missing = []

    for file_path in required_files:
        if not file_path.exists():
            missing.append(str(file_path))

    return missing


def check_archive_exists():
    if not archive_dir.exists():
        return False

    return any(archive_dir.glob("*SCENARIO-001*coder_to_tester.md"))


def check_activity_log():
    records = read_jsonl(BASE / "logs" / "activity.jsonl")
    events = [record.get("event") for record in records]

    return {
        "TASK_STARTED": "TASK_STARTED" in events,
        "AGENT_ACTION": "AGENT_ACTION" in events,
        "HANDOFF_CREATED": "HANDOFF_CREATED" in events,
        "HANDOFF_VALIDATION": "HANDOFF_VALIDATION" in events,
        "RELAY_CONTINUED": "RELAY_CONTINUED" in events,
    }


def check_rate_log():
    records = read_jsonl(BASE / "logs" / "rate-limit.jsonl")

    return any(
        record.get("task_id") == "SCENARIO-001"
        and record.get("status") == "CRITICAL_95"
        for record in records
    )


def check_state_log():
    records = read_jsonl(BASE / "state" / "state.jsonl")

    return any(
        record.get("event") == "ACTIVE_AGENT_CHANGED"
        and record.get("active_agent") == "tester"
        for record in records
    )


def main():
    failures = []

    missing_files = check_required_files()
    if missing_files:
        failures.append(f"Missing required files: {missing_files}")

    if not check_archive_exists():
        failures.append("Missing archived SCENARIO-001 handoff file.")

    activity_checks = check_activity_log()
    for event, passed in activity_checks.items():
        if not passed:
            failures.append(f"Missing activity event: {event}")

    if not check_rate_log():
        failures.append("Missing CRITICAL_95 rate-limit record for SCENARIO-001.")

    if not check_state_log():
        failures.append("Missing ACTIVE_AGENT_CHANGED state record to tester.")

    print("Scenario 001 Verification")
    print("-------------------------")

    if failures:
        print("STATUS: FAILED")
        print("")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("STATUS: PASSED")
    print("")
    print("All required relay files, logs, handoffs, and state changes exist.")


if __name__ == "__main__":
    main()
