"""Regression tests for package metadata consistency (AE-SC-1)."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path

import mcp_einvoicing_ae

_PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def test_version_slot_consistency() -> None:
    pyproject = tomllib.loads((_PACKAGE_ROOT / "pyproject.toml").read_text())
    assert mcp_einvoicing_ae.__version__ == pyproject["project"]["version"], (
        f"__version__={mcp_einvoicing_ae.__version__} drifted from "
        f"pyproject={pyproject['project']['version']}"
    )


def test_server_json_version_matches_pyproject() -> None:
    pyproject = tomllib.loads((_PACKAGE_ROOT / "pyproject.toml").read_text())
    server = json.loads((_PACKAGE_ROOT / "server.json").read_text())
    expected = pyproject["project"]["version"]
    assert server["version"] == expected, (
        f"server.json version={server['version']} drifted from pyproject={expected}"
    )
    pkg_version = server["packages"][0]["version"]
    assert pkg_version == expected, (
        f"server.json packages[0].version={pkg_version} drifted from pyproject={expected}"
    )
