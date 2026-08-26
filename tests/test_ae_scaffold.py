"""Smoke tests for the mcp-einvoicing-ae scaffold.

These assert only that the package imports and exposes a server instance.
Behavioural tests arrive with the first tools, once the specification under
specs/ unblocks them.
"""

import mcp_einvoicing_ae
from mcp_einvoicing_ae.server import main, mcp


def test_version_matches_pyproject() -> None:
    assert mcp_einvoicing_ae.__version__ == "0.1.0"


def test_server_exposes_a_runnable_entry_point() -> None:
    assert mcp is not None
    assert callable(main)
