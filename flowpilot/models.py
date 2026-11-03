from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Step:
    name: str
    task_type: str
    config: dict[str, Any] = field(default_factory=dict)
    retries: int = 0


@dataclass(frozen=True)
class Workflow:
    name: str
    steps: tuple[Step, ...]
