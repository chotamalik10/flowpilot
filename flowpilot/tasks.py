from collections.abc import Callable
from typing import Any


Task = Callable[[dict[str, Any]], None]


def print_task(config: dict[str, Any]) -> None:
    message = config.get("message")
    if not isinstance(message, str):
        raise ValueError("'print' task requires a string 'message'.")
    print(message)


TASKS: dict[str, Task] = {
    "print": print_task,
}


def run_task(task_type: str, config: dict[str, Any]) -> None:
    task = TASKS.get(task_type)
    if task is None:
        available = ", ".join(sorted(TASKS))
        raise ValueError(
            f"Unknown task type '{task_type}'. Available tasks: {available}"
        )
    task(config)
