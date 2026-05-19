import subprocess
from pathlib import Path


class RelayBridge:
    def __init__(self):
        self.root = Path(__file__).resolve().parents[2]
        self.relay_py = self.root / "relay-system" / "scripts" / "relay.py"

    def run_relay(self, args):
        command = ["python3", str(self.relay_py)] + args

        result = subprocess.run(
            command,
            cwd=str(self.root),
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr or result.stdout)

        return result.stdout

    def start_task(self, task_id, goal, agent):
        return self.run_relay([
            "--start-task",
            "--task-id", task_id,
            "--goal", goal,
            "--agent", agent
        ])

    def log_action(self, agent, task_id, action, result, confidence):
        return self.run_relay([
            "--log-action",
            "--agent", agent,
            "--task-id", task_id,
            "--action", action,
            "--result", result,
            "--confidence", str(confidence)
        ])
