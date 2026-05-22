from dataclasses import dataclass, asdict
from typing import List, Optional
import json


@dataclass
class ExecutionPacket:
    agent: str
    status: str
    summary: str
    relevant_files: List[str]
    proposed_changes: str
    errors: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)
