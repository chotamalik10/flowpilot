from pathlib import Path

import pytest

from flowpilot.server import DASHBOARD_DIR, serve


def test_dashboard_assets_are_packaged():
    assert (DASHBOARD_DIR / "index.html").is_file()
    assert (DASHBOARD_DIR / "styles.css").is_file()
    assert (DASHBOARD_DIR / "app.js").is_file()


def test_server_refuses_non_local_binding():
    with pytest.raises(ValueError, match="localhost"):
        serve("0.0.0.0", 8765)


def test_workflow_storage_is_not_a_required_source_file():
    # The dashboard creates this directory when the server starts.
    assert Path("flowpilot/server.py").is_file()
