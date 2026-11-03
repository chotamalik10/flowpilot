# FlowPilot

**A local-first workflow automation platform with a command-line interface and a browser dashboard.**

FlowPilot is a Python workflow runner for repeatable, configuration-driven tasks. Use the CLI for developer workflows or launch the local dashboard to create and execute workflows visually. Both interfaces use the same execution engine.

> **Project status:** Alpha. The current release provides a working workflow engine, JSON workflow validation, a local dashboard, and a safe starter task.

## What you get

- **Dual interface:** terminal CLI and browser-based control center.
- **Shared engine:** workflows created in the dashboard can also be run from the CLI.
- **Workflow validation:** catch malformed JSON, duplicate step names, and invalid retry settings.
- **Execution reporting:** per-step status, attempts, duration, and errors.
- **Retry support:** configure retries for individual steps.
- **Local-first operation:** dashboard binds to 127.0.0.1 by default.
- **No runtime dependencies:** core server and engine use the Python standard library.

## Dashboard

Start the dashboard:

~~~bash
python -m pip install -e .
flowpilot serve
~~~

Open **http://127.0.0.1:8765** in your browser. From the dashboard you can create workflows, view saved workflows, and run them.

The server is intentionally restricted to localhost. Do not expose it directly to a public network.

## Quick start

Requires Python 3.10 or newer.

~~~bash
git clone https://github.com/chotamalik10/flowpilot.git
cd flowpilot
python -m venv .venv
~~~

Activate the environment:

**Windows PowerShell**
~~~powershell
.venv\\Scripts\\Activate.ps1
~~~

**macOS / Linux**
~~~bash
source .venv/bin/activate
~~~

Install:

~~~bash
python -m pip install -e ".[dev]"
~~~

## CLI commands

~~~bash
flowpilot --help
flowpilot serve
flowpilot list
flowpilot validate examples/hello.json
flowpilot run examples/hello.json
flowpilot run examples/hello.json --verbose
~~~

You can also use the module form:

~~~bash
python -m flowpilot serve
python -m flowpilot run examples/hello.json
~~~

## Workflow format

~~~json
{
  "name": "hello-world",
  "steps": [
    {
      "name": "welcome",
      "type": "print",
      "message": "Hello from FlowPilot!",
      "retries": 0
    }
  ]
}
~~~

Each step has a unique name, a registered task type, and task-specific configuration. The built-in print task is intended for safe first-run verification.

## Project structure

~~~text
flowpilot/
├── .github/workflows/ci.yml
├── examples/
├── flowpilot/
│   ├── dashboard/       # Browser UI (HTML, CSS, JavaScript)
│   ├── cli.py           # Terminal interface
│   ├── engine.py        # Shared execution engine
│   ├── server.py        # Local dashboard API
│   ├── models.py
│   ├── tasks.py
│   └── workflow.py
├── tests/
├── workflows/           # Local saved workflows
├── pyproject.toml
└── README.md
~~~

## Development

~~~bash
python -m pip install -e ".[dev]"
pytest
ruff check .
~~~

GitHub Actions runs the test and lint suite across supported Python versions.

## Security model

- The dashboard binds to localhost only; non-local bind addresses are rejected.
- Request bodies are size-limited.
- Workflow filenames are validated before access.
- Workflow definitions select registered task types; they do not execute arbitrary shell commands or Python source.
- The initial dashboard is designed for trusted local use and does not include user authentication. Keep it on your own machine.

## Roadmap

- [x] Shared workflow engine and CLI
- [x] JSON workflow validation and retry support
- [x] Local browser dashboard and workflow creation
- [x] Dashboard workflow execution and activity feedback
- [ ] File organizer task with preview / dry-run
- [ ] Persistent execution history
- [ ] Scheduling and recurring workflows
- [ ] Plugin system and custom task registration
- [ ] YAML workflow support

## License

MIT. See LICENSE.
