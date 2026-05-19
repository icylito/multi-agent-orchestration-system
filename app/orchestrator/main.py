import argparse
import uuid
from pathlib import Path

from ollama_client import OllamaClient
from relay_bridge import RelayBridge


AGENTS = {
    "manager": {
        "model": "qwen3:14b",
        "prompt": "prompts/manager.md",
        "temperature": 0.2
    },
    "reviewer": {
        "model": "deepseek-r1:latest",
        "prompt": "prompts/reviewer.md",
        "temperature": 0.1
    }
}


def load_agent(agent_name):
    if agent_name not in AGENTS:
        raise ValueError(f"Unknown agent: {agent_name}")

    config = AGENTS[agent_name]
    prompt_path = Path(__file__).parent / config["prompt"]

    return {
        "name": agent_name,
        "model": config["model"],
        "temperature": config["temperature"],
        "system_prompt": prompt_path.read_text(encoding="utf-8")
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", default="manager")
    parser.add_argument("--task", required=True)
    args = parser.parse_args()

    task_id = f"ORCH-{uuid.uuid4().hex[:8].upper()}"

    agent = load_agent(args.agent)
    ollama = OllamaClient()
    relay = RelayBridge()

    relay.start_task(
        task_id=task_id,
        goal=args.task,
        agent=agent["name"]
    )

    context_path = Path(__file__).parent / "context" / "project_context.md"

    persistent_context = ""

    if context_path.exists():
        persistent_context = context_path.read_text(encoding="utf-8")

    messages = [
        {
            "role": "system",
            "content": agent["system_prompt"]
        },
        {
            "role": "system",
            "content": f"Persistent Project Context:\n\n{persistent_context}"
        },
        {
            "role": "user",
            "content": args.task
        }
  ]
    output = ollama.chat(
        model=agent["model"],
        messages=messages,
        temperature=agent["temperature"]
    )

    relay.log_action(
        agent=agent["name"],
        task_id=task_id,
        action="Generated manager response from Ollama",
        result=output,
        confidence=90
    )

    print("\n=== TASK ID ===")
    print(task_id)

    print("\n=== AGENT ===")
    print(agent["name"])

    print("\n=== MODEL ===")
    print(agent["model"])

    print("\n=== RESPONSE ===")
    print(output)


if __name__ == "__main__":
    main()
