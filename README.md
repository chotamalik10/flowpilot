# FlowPilot

**A cross-platform workflow automation engine built with Python.**

FlowPilot runs repeatable workflows from JSON configuration, with task execution, retries, structured logs, and a CLI designed for developers.

> Status: Early development — the starter release includes a sequential workflow runner and a safe built-in task.

## Features
- Run multi-step workflows from JSON files
- Built-in `print` task for safe first-run testing
- Per-task retry policy
- Structured execution results and exit codes
- Cross-platform Python support
- Automated tests and GitHub Actions CI

## Quick start
Requires Python 3.10 or newer.

```bash
git clone https://github.com/chotamalik10/flowpilot.git
cd flowpilot
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install:

```bash
python -m pip install -e ".[dev]"
```

Run the example:

```bash
flowpilot run examples/hello.json
```

Or:

```bash
python -m flowpilot.cli run examples/hello.json
```

## Workflow format

```json
{
  "name": "hello-world",
  "steps": [
    {
      "name": "welcome",
      "type": "print",
      "message": "Hello from FlowPilot!"
    }
  ]
}
```

Each step has a unique `name`, a registered task `type`, and task-specific configuration.

## CLI
```text
flowpilot --help
flowpilot run examples/hello.json
```

## Development
```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Roadmap
- [x] Initial workflow schema and CLI
- [x] Sequential task execution
- [x] Retry handling
- [x] Unit tests and CI
- [ ] YAML workflow support
- [ ] Task plugins and custom task registration
- [ ] Scheduling and recurring workflows
- [ ] Workflow state persistence
- [ ] Dry-run mode and richer execution reports

## Safety
FlowPilot only runs explicitly configured task types. The initial release does not execute arbitrary shell commands or Python code from workflow files.

## License
MIT. See [LICENSE](LICENSE).
