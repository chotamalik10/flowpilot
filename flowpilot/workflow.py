import json
from pathlib import Path

from flowpilot.models import Step, Workflow


class WorkflowValidationError(ValueError):
    """Raised when a workflow document is invalid."""


def load_workflow(path: str | Path) -> Workflow:
    workflow_path = Path(path)
    try:
        raw = json.loads(workflow_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise WorkflowValidationError(f"Cannot read workflow file: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise WorkflowValidationError(f"Invalid JSON: {exc}") from exc

    if not isinstance(raw, dict):
        raise WorkflowValidationError("Workflow root must be a JSON object.")

    name = raw.get("name")
    steps_data = raw.get("steps")
    if not isinstance(name, str) or not name.strip():
        raise WorkflowValidationError("'name' must be a non-empty string.")
    if not isinstance(steps_data, list) or not steps_data:
        raise WorkflowValidationError("'steps' must be a non-empty array.")

    steps = []
    seen_names = set()
    for index, item in enumerate(steps_data, start=1):
        if not isinstance(item, dict):
            raise WorkflowValidationError(f"Step {index} must be an object.")
        step_name = item.get("name")
        task_type = item.get("type")
        retries = item.get("retries", 0)
        if not isinstance(step_name, str) or not step_name.strip():
            raise WorkflowValidationError(f"Step {index} needs a non-empty 'name'.")
        if step_name in seen_names:
            raise WorkflowValidationError(f"Duplicate step name: {step_name}")
        if not isinstance(task_type, str) or not task_type.strip():
            raise WorkflowValidationError(f"Step '{step_name}' needs a non-empty 'type'.")
        if not isinstance(retries, int) or isinstance(retries, bool) or retries < 0:
            raise WorkflowValidationError(
                f"Step '{step_name}' retries must be a non-negative integer."
            )
        config = {
            key: value for key, value in item.items()
            if key not in {"name", "type", "retries"}
        }
        steps.append(Step(step_name, task_type, config, retries))
        seen_names.add(step_name)

    return Workflow(name=name, steps=tuple(steps))
