"""Tests for mcp_einvoicing_ae.server — id adapter and Peppol tool registration."""

from mcp_einvoicing_ae.server import _ae_id_adapter, mcp


def test_id_adapter_derives_tin_from_bare_trn() -> None:
    assert _ae_id_adapter("198765432102003") == "0235:1987654321"


def test_id_adapter_passes_through_scheme_qualified_identifier() -> None:
    assert _ae_id_adapter("0235:1987654321") == "0235:1987654321"


def test_peppol_lookup_plugin_registered() -> None:
    """AE-LC-2: core's Peppol participant-lookup plugin must be mounted."""
    assert "peppol" in mcp.registered_plugins
    assert "ae" in mcp.registered_plugins
