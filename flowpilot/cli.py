import argparse
import logging

from flowpilot.engine import run_workflow
from flowpilot.workflow import WorkflowValidationError, load_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flowpilot",
        description="Run safe, configuration-driven workflows.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run a workflow JSON file.")
    run_parser.add_argument("workflow", help="Path to a workflow JSON file.")
    run_parser.add_argument(
        "--verbose", action="store_true", help="Show detailed execution logs."
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )
    try:
        workflow = load_workflow(args.workflow)
        result = run_workflow(workflow)
    except WorkflowValidationError as exc:
        print(f"Workflow error: {exc}")
        return 2

    passed = sum(step.success for step in result.steps)
    print(f"\nWorkflow: {result.name}")
    print(f"Result: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Steps: {passed}/{len(result.steps)} succeeded")
    for step in result.steps:
        status = "PASS" if step.success else "FAIL"
        print(
            f"  [{status}] {step.name} — {step.attempts} attempt(s), "
            f"{step.duration_seconds:.3f}s"
        )
        if step.error:
            print(f"         Error: {step.error}")
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
