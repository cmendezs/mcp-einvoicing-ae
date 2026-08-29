"""Tests for parse_invoice_ae."""

from pathlib import Path

import pytest

from mcp_einvoicing_ae.tools.parsing import parse_invoice_ae

_SPECS_ROOT = Path(__file__).parent.parent / "specs"
_STANDARD_INVOICE = _SPECS_ROOT / "pint-ae" / "trn-invoice" / "example" / "Standard tax invoice.xml"


@pytest.mark.skipif(not _STANDARD_INVOICE.exists(), reason="specs/ not present in this checkout")
async def test_parse_standard_invoice_succeeds() -> None:
    xml = _STANDARD_INVOICE.read_text(encoding="utf-8")
    result = await parse_invoice_ae(xml_content=xml)
    assert result["success"] is True
    assert result["invoice"]["invoice_number"]


@pytest.mark.skipif(not _STANDARD_INVOICE.exists(), reason="specs/ not present in this checkout")
async def test_parse_round_trips_ae_extensions() -> None:
    """AE-SC-3: document_uuid, profile_execution_id, and trade_license_number
    (both parties) must round-trip through parse, not be silently dropped."""
    xml = _STANDARD_INVOICE.read_text(encoding="utf-8")
    result = await parse_invoice_ae(xml_content=xml)
    assert result["success"] is True
    invoice = result["invoice"]
    assert invoice["document_uuid"] == "f12f329f-6430-4399-b661-7c5cd9c3a9e6"
    assert invoice["profile_execution_id"] == "00000000"
    assert invoice["seller"]["trade_license_number"]
    assert invoice["buyer"]["trade_license_number"]


async def test_parse_malformed_xml_reports_failure() -> None:
    result = await parse_invoice_ae(xml_content="<Invoice><unclosed></Invoice>")
    assert result["success"] is False
    assert "error" in result


async def test_parse_non_invoice_xml_reports_failure() -> None:
    result = await parse_invoice_ae(xml_content="<NotAnInvoice/>")
    assert result["success"] is False
    assert "error" in result
