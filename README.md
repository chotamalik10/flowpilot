# FlowPilot

**A local-first workflow automation platform with a command-line interface and an installable app-style dashboard.**

FlowPilot is a Python workflow runner for repeatable, configuration-driven tasks. Use the CLI for developer workflows or launch the local dashboard to create and execute workflows visually. Both interfaces use the same execution engine.

> **Project status:** Alpha. The current release provides a working workflow engine, JSON workflow validation, a responsive local dashboard, installable PWA shell, and a safe starter task.

## What you get

- **App-style dashboard:** responsive layout for desktop, tablet, and mobile.
- **Installable experience:** add FlowPilot to a supported device's home screen / app launcher.
- **Visual workspace:** overview cards, workflow builder, and saved automation library.
- **Shared engine:** workflows created in the dashboard can also be run from the CLI.
- **Workflow validation:** catch malformed JSON, duplicate step names, and invalid retry settings.
- **Execution reporting:** per-step status, attempts, duration, and errors.
- **Local-first operation:** dashboard binds to 127.0.0.1 by default.
- **No runtime dependencies:** core server and engine use the Python standard library.

## Dashboard and app mode

~~~bash
python -m pip install -e .
flowpilot serve
~~~

Open **http://127.0.0.1:8765** in your browser. On supported browsers, use the browser's **Install app** option or **Add to Home Screen** to launch FlowPilot in an app-style window.

The offline app shell can cache the dashboard interface. Workflow data and execution still require the local Python server to be running. The server is intentionally restricted to localhost; do not expose it directly to a public network.

## Download ZIP

Get the complete source as a ZIP from GitHub:

- [Download latest source ZIP](https://github.com/chotamalik10/flowpilot/archive/refs/heads/main.zip)
- [Browse repository files](https://github.com/chotamalik10/flowpilot)

The ZIP contains the source code. It is not a standalone Windows installer; install Python and follow the setup below.

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
.venv\Scripts\Activate.ps1
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
│   ├── dashboard/
│   │   ├── icons/         # App icons
│   │   ├── index.html
│   │   ├── styles.css
│   │   ├── app.js
│   │   ├── manifest.webmanifest
│   │   └── service-worker.js
│   ├── cli.py
│   ├── engine.py
│   ├── server.py
│   ├── models.py
│   ├── tasks.py
│   └── workflow.py
├── tests/
├── workflows/
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
- [x] Responsive dashboard and workflow creation / execution
- [x] Installable PWA shell and app icons
- [ ] File organizer task with preview / dry-run
- [ ] Persistent execution history
- [ ] Scheduling and recurring workflows
- [ ] Plugin system and custom task registration
- [ ] YAML workflow support

## License

MIT. See LICENSE.
