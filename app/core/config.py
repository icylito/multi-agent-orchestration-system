import json
from pathlib import Path

CONFIG_PATH = Path("relay-system/config/settings.json")


def load_config():
    if not CONFIG_PATH.exists():
        return {}

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_config_value(path: str, default=None):
    config = load_config()
    current = config

    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]

    return current
