#!/usr/bin/env python3

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

ACTIVITY_LOG = BASE / "logs" / "activity.jsonl"
HANDOFF_INDEX = BASE / "handoffs" / "handoff-index.jsonl"
ARCHIVE_DIR = BASE / "handoffs" / "archive"


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
    handoffs = read_jsonl(HANDOFF_INDEX)

    has_handoff = any(
        record.get("task_id") == "SCENARIO-002"
        and record.get("event") == "HANDOFF_CREATED"
        for record in handoffs
    )

    has_archive = any(
        ARCHIVE_DIR.glob("*SCENARIO-002*coder_to_tester.md")
    )

    has_low_conf_validation = any(
        record.get("event") == "HANDOFF_VALIDATION"
        and record.get("agent") == "tester"
        and record.get("confidence") == 70
        and record.get("decision") == "CLARIFICATION_REQUIRED"
        for record in activity
    )

    has_bad_approval = any(
        record.get("event") == "HANDOFF_VALIDATION"
        and record.get("agent") == "tester"
        and record.get("confidence") == 70
        and record.get("decision") == "APPROVED_CONTINUE"
        for record in activity
    )

    if not has_handoff:
        failures.append("Missing SCENARIO-002 handoff index record.")

    if not has_archive:
        failures.append("Missing archived SCENARIO-002 handoff file.")

    if not has_low_conf_validation:
        failures.append("Missing CLARIFICATION_REQUIRED validation for tester at 70% confidence.")

    if has_bad_approval:
        failures.append("Low-confidence handoff was incorrectly approved.")

    print("Scenario 002 Verification")
    print("-------------------------")

    if failures:
        print("STATUS: FAILED")
        print("")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("STATUS: PASSED")
    print("")
    print("Low-confidence handoff correctly required clarification.")


if __name__ == "__main__":
    main()
