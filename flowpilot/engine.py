import logging
from dataclasses import dataclass
from time import perf_counter

from flowpilot.models import Workflow
from flowpilot.tasks import run_task

logger = logging.getLogger("flowpilot")


@dataclass(frozen=True)
class StepResult:
    name: str
    success: bool
    attempts: int
    duration_seconds: float
    error: str | None = None


@dataclass(frozen=True)
class WorkflowResult:
    name: str
    success: bool
    steps: tuple[StepResult, ...]


def run_workflow(workflow: Workflow) -> WorkflowResult:
    results: list[StepResult] = []
    logger.info(
        "Starting workflow '%s' (%d steps)", workflow.name, len(workflow.steps)
    )

    for step in workflow.steps:
        started = perf_counter()
        error = None
        attempts = 0

        for attempt in range(step.retries + 1):
            attempts += 1
            try:
                logger.info("Running step '%s' (attempt %d)", step.name, attempts)
                run_task(step.task_type, step.config)
                error = None
                break
            except Exception as exc:
                error = str(exc)
                logger.warning("Step '%s' failed: %s", step.name, error)

        duration = perf_counter() - started
        result = StepResult(step.name, error is None, attempts, duration, error)
        results.append(result)
        if error is not None:
            logger.error("Workflow stopped after failed step '%s'", step.name)
            return WorkflowResult(workflow.name, False, tuple(results))

    logger.info("Workflow '%s' completed successfully", workflow.name)
    return WorkflowResult(workflow.name, True, tuple(results))
