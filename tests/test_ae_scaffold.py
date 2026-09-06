"""Smoke tests for the mcp-einvoicing-ae scaffold.

These assert only that the package imports and exposes a server instance.
Behavioural tests arrive with the first tools, once the specification under
specs/ unblocks them.

Version-slot consistency (__version__ vs. pyproject.toml vs. server.json) is
covered by test_metadata.py, not here, to keep this file free of a hardcoded
version literal that could silently drift out of sync again.
"""

from mcp_einvoicing_ae.server import main, mcp


def test_server_exposes_a_runnable_entry_point() -> None:
    assert mcp is not None
    assert callable(main)
