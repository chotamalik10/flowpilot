import typing


Task = typing.Callable[[dict[str, typing.Any]], None]


def print_task(config: dict[str, typing.Any]) -> None:
    message = config.get("message")
    if not isinstance(message, str):
        raise TypeError("'print' task requires a string 'message'.")
    print(message)


TASKS: dict[str, Task] = {
    "print": print_task,
}


def run_task(task_type: str, config: dict[str, typing.Any]) -> None:
    task = TASKS.get(task_type)
    if task is None:
        available = ", ".join(sorted(TASKS))
        raise ValueError(
            f"Unknown task type '{task_type}'. Available tasks: {available}"
        )
    task(config)
