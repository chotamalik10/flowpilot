import argparse
import logging
from pathlib import Path

from flowpilot.engine import run_workflow
from flowpilot.server import serve
from flowpilot.workflow import WorkflowValidationError, load_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flowpilot",
        description="Build and run safe, configuration-driven workflows.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Execute a workflow JSON file.")
    run_parser.add_argument("workflow", help="Path to a workflow JSON file.")
    run_parser.add_argument("--verbose", action="store_true", help="Show detailed logs.")
    validate_parser = subparsers.add_parser("validate", help="Validate a workflow file.")
    validate_parser.add_argument("workflow", help="Path to a workflow JSON file.")
    list_parser = subparsers.add_parser("list", help="List saved dashboard workflows.")
    list_parser.add_argument("--directory", default="workflows", help="Workflow directory.")
    serve_parser = subparsers.add_parser("serve", help="Launch the local web dashboard.")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Local bind host.")
    serve_parser.add_argument("--port", type=int, default=8765, help="Dashboard port.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "serve":
        try:
            serve(args.host, args.port)
        except (OSError, ValueError) as exc:
            print(f"Server error: {exc}")
            return 2
        return 0
    if args.command == "list":
        directory = Path(args.directory)
        files = sorted(directory.glob("*.json")) if directory.is_dir() else []
        if not files:
            print(f"No workflows found in {directory}.")
            return 0
        for file in files:
            try:
                workflow = load_workflow(file)
                print(f"{workflow.name}  |  {len(workflow.steps)} step(s)  |  {file}")
            except WorkflowValidationError as exc:
                print(f"INVALID  |  {file}: {exc}")
        return 0
    try:
        workflow = load_workflow(args.workflow)
    except WorkflowValidationError as exc:
        print(f"Workflow error: {exc}")
        return 2
    if args.command == "validate":
        print(f"VALID: {workflow.name} ({len(workflow.steps)} step(s))")
        return 0
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )
    result = run_workflow(workflow)
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
