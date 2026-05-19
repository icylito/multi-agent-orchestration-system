#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

CONFIG_DIR = BASE / "config"
LOGS_DIR = BASE / "logs"
HANDOFFS_DIR = BASE / "handoffs"
ARCHIVE_DIR = BASE / "handoffs" / "archive"
STATE_DIR = BASE / "state"

ACTIVITY_LOG = LOGS_DIR / "activity.jsonl"
RATE_LOG = LOGS_DIR / "rate-limit.jsonl"
ERROR_LOG = LOGS_DIR / "errors.jsonl"
STATE_LOG = STATE_DIR / "state.jsonl"
HANDOFF_INDEX = HANDOFFS_DIR / "handoff-index.jsonl"


def now():
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs():
    for folder in [CONFIG_DIR, LOGS_DIR, HANDOFFS_DIR, ARCHIVE_DIR, STATE_DIR]:
        folder.mkdir(parents=True, exist_ok=True)


def append_jsonl(path, data):
    data["timestamp"] = now()
    with open(path, "a", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")


def read_last_jsonl(path):
    if not path.exists():
        return None

    lines = path.read_text(encoding="utf-8").strip().splitlines()

    if not lines:
        return None

    return json.loads(lines[-1])


def init_system():
    ensure_dirs()

    agents_config = {
        "agents": {
            "manager": "brain/orchestrator",
            "coder": "implementation",
            "tester": "testing/debugging",
            "reviewer": "quality review",
            "organizer": "memory/docs/logs",
            "scraper": "research/web data"
        },
        "rules": {
            "append_only": True,
            "no_delete": True,
            "no_overwrite_old_logs": True,
            "critical_rate_limit_percent": 95
        }
    }

    config_path = CONFIG_DIR / "agents.json"

    if not config_path.exists():
        config_path.write_text(
            json.dumps(agents_config, indent=2),
            encoding="utf-8"
        )

    append_jsonl(ACTIVITY_LOG, {
        "event": "SYSTEM_INIT",
        "message": "Relay system initialized",
        "base_path": str(BASE)
    })

    append_jsonl(STATE_LOG, {
        "event": "STATE_INIT",
        "active_agent": None,
        "current_task": None,
        "rate_status": "UNKNOWN"
    })

    print("Relay system initialized successfully.")
    print(f"Location: {BASE}")


def start_task(task_id, goal, agent):
    ensure_dirs()

    append_jsonl(ACTIVITY_LOG, {
        "event": "TASK_STARTED",
        "task_id": task_id,
        "goal": goal,
        "active_agent": agent
    })

    append_jsonl(STATE_LOG, {
        "event": "ACTIVE_TASK_UPDATED",
        "task_id": task_id,
        "goal": goal,
        "active_agent": agent,
        "rate_status": "SAFE"
    })

    print("Task started successfully.")
    print(f"Task ID: {task_id}")
    print(f"Goal: {goal}")
    print(f"Active Agent: {agent}")


def log_action(agent, task_id, action, result, confidence):
    ensure_dirs()

    append_jsonl(ACTIVITY_LOG, {
        "event": "AGENT_ACTION",
        "agent": agent,
        "task_id": task_id,
        "action": action,
        "result": result,
        "confidence": confidence
    })

    print("Agent action logged.")
    print(f"Agent: {agent}")
    print(f"Task ID: {task_id}")
    print(f"Confidence: {confidence}%")


def simulate_rate(agent, task_id, percent):
    ensure_dirs()

    if percent >= 95:
        status = "CRITICAL_95"
    elif percent >= 80:
        status = "WARNING"
    else:
        status = "SAFE"

    append_jsonl(RATE_LOG, {
        "event": "RATE_STATUS_CHECK",
        "agent": agent,
        "task_id": task_id,
        "percent": percent,
        "status": status
    })

    append_jsonl(STATE_LOG, {
        "event": "RATE_STATUS_UPDATED",
        "active_agent": agent,
        "task_id": task_id,
        "percent": percent,
        "rate_status": status
    })

    print(f"Rate status: {status} ({percent}%)")

    if status == "CRITICAL_95":
        print("\nEMERGENCY HANDOFF REQUIRED")
        print("Ask the active agent:")
        print("""
You are at 95% limit. Stop active work now.
Give a detailed checkpoint of everything you have done.

Use this format:
WHAT I DID:
FILES CHANGED:
COMMANDS RUN:
ERRORS:
CURRENT STATE:
WHAT IS UNFINISHED:
NEXT RECOMMENDED STEP:
WARNINGS:
CONFIDENCE:
""")


def create_handoff(task_id, from_agent, to_agent, summary, confidence):
    ensure_dirs()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{stamp}_{task_id}_{from_agent}_to_{to_agent}.md"
    archive_path = ARCHIVE_DIR / filename
    latest_path = HANDOFFS_DIR / "latest-handoff.md"

    content = f"""# Agent Handoff

TASK ID: {task_id}
FROM: {from_agent}
TO: {to_agent}
STATUS: HANDOFF_CREATED
CONFIDENCE SCORE: {confidence}
CREATED AT: {now()}

---

## SUMMARY

{summary}

---

## RECEIVING AGENT REQUIREMENT

The receiving agent must confirm understanding before continuing.

If understanding confidence is 95% or higher:
- continue the task
- log the next action

If understanding confidence is below 95%:
- stop
- ask Manager for clarification
- read logs or memory before continuing

---

## SAFETY NOTE

This file is historical context.
Do not delete old handoffs.
Do not overwrite archived handoff files.
"""

    archive_path.write_text(content, encoding="utf-8")
    latest_path.write_text(content, encoding="utf-8")

    append_jsonl(HANDOFF_INDEX, {
        "event": "HANDOFF_CREATED",
        "task_id": task_id,
        "from_agent": from_agent,
        "to_agent": to_agent,
        "archive_file": str(archive_path),
        "latest_file": str(latest_path),
        "confidence": confidence
    })

    append_jsonl(ACTIVITY_LOG, {
        "event": "HANDOFF_CREATED",
        "task_id": task_id,
        "from_agent": from_agent,
        "to_agent": to_agent,
        "handoff_file": str(archive_path),
        "confidence": confidence
    })

    print("Handoff created successfully.")
    print(f"Archive: {archive_path}")
    print(f"Latest: {latest_path}")


def validate_handoff(agent, confidence):
    ensure_dirs()

    if confidence >= 95:
        decision = "APPROVED_CONTINUE"
    else:
        decision = "CLARIFICATION_REQUIRED"

    append_jsonl(ACTIVITY_LOG, {
        "event": "HANDOFF_VALIDATION",
        "agent": agent,
        "confidence": confidence,
        "decision": decision
    })

    print("Handoff validation complete.")
    print(f"Agent: {agent}")
    print(f"Confidence: {confidence}%")
    print(f"Decision: {decision}")


def continue_relay(agent):
    ensure_dirs()

    latest_handoff = read_last_jsonl(HANDOFF_INDEX)

    if not latest_handoff:
        print("No handoff exists. Cannot continue relay.")
        return

    append_jsonl(ACTIVITY_LOG, {
        "event": "RELAY_CONTINUED",
        "agent": agent,
        "handoff_used": latest_handoff
    })

    append_jsonl(STATE_LOG, {
        "event": "ACTIVE_AGENT_CHANGED",
        "active_agent": agent,
        "handoff_used": latest_handoff
    })

    print("Relay continued successfully.")
    print(f"New active agent: {agent}")


def log_error(agent, task_id, error, suspected_cause):
    ensure_dirs()

    append_jsonl(ERROR_LOG, {
        "event": "ERROR_RECORDED",
        "agent": agent,
        "task_id": task_id,
        "error": error,
        "suspected_cause": suspected_cause
    })

    print("Error logged.")
    print(f"Agent: {agent}")
    print(f"Task ID: {task_id}")


def status():
    ensure_dirs()

    latest_state = read_last_jsonl(STATE_LOG)
    latest_rate = read_last_jsonl(RATE_LOG)
    latest_activity = read_last_jsonl(ACTIVITY_LOG)
    latest_handoff = read_last_jsonl(HANDOFF_INDEX)

    print("\nRelay System Status")
    print("-------------------")
    print(f"Base: {BASE}")

    print("\nLatest State:")
    print(json.dumps(latest_state, indent=2) if latest_state else "None")

    print("\nLatest Rate:")
    print(json.dumps(latest_rate, indent=2) if latest_rate else "None")

    print("\nLatest Activity:")
    print(json.dumps(latest_activity, indent=2) if latest_activity else "None")

    print("\nLatest Handoff:")
    print(json.dumps(latest_handoff, indent=2) if latest_handoff else "None")


def main():
    parser = argparse.ArgumentParser(description="Local AI Relay System MVP")

    parser.add_argument("--init", action="store_true")
    parser.add_argument("--start-task", action="store_true")
    parser.add_argument("--log-action", action="store_true")
    parser.add_argument("--simulate-rate", action="store_true")
    parser.add_argument("--create-handoff", action="store_true")
    parser.add_argument("--validate-handoff", action="store_true")
    parser.add_argument("--continue-relay", action="store_true")
    parser.add_argument("--log-error", action="store_true")
    parser.add_argument("--status", action="store_true")

    parser.add_argument("--task-id")
    parser.add_argument("--goal")
    parser.add_argument("--agent")
    parser.add_argument("--from-agent")
    parser.add_argument("--to-agent")
    parser.add_argument("--action")
    parser.add_argument("--result")
    parser.add_argument("--summary")
    parser.add_argument("--error")
    parser.add_argument("--suspected-cause")
    parser.add_argument("--confidence", type=int)
    parser.add_argument("--validation-confidence", type=int)
    parser.add_argument("--percent", type=int)

    args = parser.parse_args()

    if args.init:
        init_system()

    elif args.start_task:
        start_task(
            task_id=args.task_id,
            goal=args.goal,
            agent=args.agent
        )

    elif args.log_action:
        log_action(
            agent=args.agent,
            task_id=args.task_id,
            action=args.action,
            result=args.result,
            confidence=args.confidence
        )

    elif args.simulate_rate:
        simulate_rate(
            agent=args.agent,
            task_id=args.task_id,
            percent=args.percent
        )

    elif args.create_handoff:
        create_handoff(
            task_id=args.task_id,
            from_agent=args.from_agent,
            to_agent=args.to_agent,
            summary=args.summary,
            confidence=args.confidence
        )

    elif args.validate_handoff:
        validate_handoff(
            agent=args.agent,
            confidence=args.validation_confidence
        )

    elif args.continue_relay:
        continue_relay(
            agent=args.agent
        )

    elif args.log_error:
        log_error(
            agent=args.agent,
            task_id=args.task_id,
            error=args.error,
            suspected_cause=args.suspected_cause
        )

    elif args.status:
        status()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
