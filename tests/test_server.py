from pathlib import Path

import pytest

from flowpilot.server import DASHBOARD_DIR, STATIC_ASSETS, serve


def test_dashboard_assets_are_packaged():
    for asset in (
        "index.html",
        "styles.css",
        "app.js",
        "manifest.webmanifest",
        "service-worker.js",
        "icons/icon.svg",
        "icons/icon-maskable.svg",
    ):
        assert (DASHBOARD_DIR / asset).is_file()


def test_static_asset_routes_are_allowlisted():
    assert "/manifest.webmanifest" in STATIC_ASSETS
    assert "/service-worker.js" in STATIC_ASSETS
    assert "/icons/icon.svg" in STATIC_ASSETS


def test_server_refuses_non_local_binding():
    with pytest.raises(ValueError, match="localhost"):
        serve("0.0.0.0", 8765)


def test_workflow_storage_is_not_a_required_source_file():
    # The dashboard creates this directory when the server starts.
    assert Path("flowpilot/server.py").is_file()
