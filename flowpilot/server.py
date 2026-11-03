"""Local-only HTTP server for the FlowPilot web dashboard."""
from __future__ import annotations

import json
import re
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from flowpilot.engine import run_workflow
from flowpilot.workflow import WorkflowValidationError, load_workflow

PROJECT_ROOT = Path.cwd()
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"
DASHBOARD_DIR = Path(__file__).with_name("dashboard")
SAFE_NAME = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$")


def _json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = "FlowPilot/1.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[dashboard] {self.address_string()} - {fmt % args}")

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload: Any) -> None:
        self._send(status, _json_bytes(payload), "application/json; charset=utf-8")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health":
            self._json(200, {"status": "ok", "name": "FlowPilot"})
            return
        if path == "/api/workflows":
            WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
            items = []
            for file in sorted(WORKFLOWS_DIR.glob("*.json")):
                try:
                    workflow = load_workflow(file)
                    items.append({
                        "name": workflow.name,
                        "file": file.name,
                        "steps": len(workflow.steps),
                    })
                except WorkflowValidationError as exc:
                    items.append({"name": file.stem, "file": file.name, "error": str(exc)})
            self._json(200, {"workflows": items})
            return
        if path in {"/", "/index.html"}:
            target = DASHBOARD_DIR / "index.html"
            self._send(200, target.read_bytes(), "text/html; charset=utf-8")
            return
        if path == "/styles.css":
            self._send(200, (DASHBOARD_DIR / "styles.css").read_bytes(), "text/css; charset=utf-8")
            return
        if path == "/app.js":
            self._send(200, (DASHBOARD_DIR / "app.js").read_bytes(), "text/javascript; charset=utf-8")
            return
        self._json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 256_000:
                self._json(400, {"error": "Request body must be between 1 and 256 KB."})
                return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            self._json(400, {"error": "Request body must be valid JSON."})
            return

        if path == "/api/workflows":
            self._create_workflow(payload)
            return
        if path.startswith("/api/run/"):
            filename = path.removeprefix("/api/run/")
            if not SAFE_NAME.fullmatch(filename.removesuffix(".json")) or not filename.endswith(".json"):
                self._json(400, {"error": "Invalid workflow filename."})
                return
            target = WORKFLOWS_DIR / filename
            if not target.is_file():
                self._json(404, {"error": "Workflow not found."})
                return
            try:
                result = run_workflow(load_workflow(target))
                self._json(200 if result.success else 422, {
                    "name": result.name,
                    "success": result.success,
                    "error": None if result.success else "One or more workflow steps failed.",
                    "steps": [asdict(step) for step in result.steps],
                })
            except WorkflowValidationError as exc:
                self._json(422, {"error": str(exc)})
            return
        self._json(404, {"error": "Not found"})

    def _create_workflow(self, payload: Any) -> None:
        if not isinstance(payload, dict):
            self._json(400, {"error": "Workflow must be a JSON object."})
            return
        name = payload.get("name")
        if not isinstance(name, str) or not name.strip():
            self._json(400, {"error": "Workflow name is required."})
            return
        slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip()).strip("-_").lower()[:64]
        if not slug or not SAFE_NAME.fullmatch(slug):
            self._json(400, {"error": "Workflow name must contain letters or numbers."})
            return
        WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
        target = WORKFLOWS_DIR / f"{slug}.json"
        if target.exists():
            self._json(409, {"error": "A workflow with this name already exists."})
            return
        temporary = WORKFLOWS_DIR / f".{slug}.tmp"
        try:
            temporary.write_bytes(_json_bytes(payload))
            workflow = load_workflow(temporary)
            temporary.replace(target)
        except (WorkflowValidationError, OSError) as exc:
            temporary.unlink(missing_ok=True)
            self._json(400, {"error": str(exc)})
            return
        self._json(201, {
            "name": workflow.name,
            "file": target.name,
            "steps": len(workflow.steps),
        })


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    if host not in {"127.0.0.1", "localhost"}:
        raise ValueError("For safety, the dashboard currently binds to localhost only.")
    WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((host, port), DashboardHandler)
    print(f"FlowPilot dashboard: http://{host}:{port}")
    print("Press Ctrl+C to stop the local server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down FlowPilot...")
    finally:
        server.server_close()
