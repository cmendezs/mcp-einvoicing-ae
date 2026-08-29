"""Tests for AEDocumentGenerator.generate_invoice_ae.

Fixture values mirror test_models_invoice.py's _base_kwargs (drawn from
specs/pint-ae/trn-invoice/example/Standard tax invoice.xml).
"""

from datetime import date
from decimal import Decimal

import pytest
from mcp_einvoicing_core import DocumentGenerationError
from mcp_einvoicing_core.en16931 import EN16931Address, EN16931Tax

from mcp_einvoicing_ae.models.invoice import AE_STANDARD_VAT_RATE, AEInvoiceLine
from mcp_einvoicing_ae.models.party import AEParty
from mcp_einvoicing_ae.standards.pint_ae import CUSTOMIZATION_IDS, PROFILE_IDS
from mcp_einvoicing_ae.tools.generation import AEDocumentGenerator

_gen = AEDocumentGenerator()

_SELLER_ADDRESS = EN16931Address(
    line_one="Street Name", city="Sharjah", postcode="00000", country_code="AE"
)
_BUYER_ADDRESS = EN16931Address(
    line_one="Street Name", city="Abu Dhabi", postcode="00000", country_code="AE"
)


def _invoice_data() -> dict:
    return {
        "invoice_number": "AE-01TEST",
        "invoice_date": date(2025, 2, 6),
        "document_uuid": "f12f329f-6430-4399-b661-7c5cd9c3a9e6",
        "profile_execution_id": "00000000",
        "seller": AEParty(
            name="Party Trade Name",
            address=_SELLER_ADDRESS,
            vat_id="198765432102003",
            trade_license_number="112345678900003",
        ),
        "buyer": AEParty(
            name="Noor Electronics",
            address=_BUYER_ADDRESS,
            vat_id="134567890123003",
            trade_license_number="112345679000001",
        ),
        "line_items": [
            AEInvoiceLine(
                line_id="1",
                name="Item Name",
                quantity=Decimal("2000"),
                unit_code="H87",
                unit_price=Decimal("4.9"),
                line_net_amount=Decimal("10486"),
                tax_category="S",
                tax_rate=AE_STANDARD_VAT_RATE,
            )
        ],
        "sum_of_line_net_amounts": Decimal("10486"),
        "tax_exclusive_amount": Decimal("10643.29"),
        "tax_total": Decimal("532.16"),
        "tax_inclusive_amount": Decimal("11175.45"),
        "amount_due": Decimal("11175.50"),
        "tax_lines": [
            EN16931Tax(
                category="S",
                rate=AE_STANDARD_VAT_RATE,
                taxable_amount=Decimal("10643.29"),
                tax_amount=Decimal("532.16"),
            )
        ],
    }


async def test_generate_billing_default() -> None:
    result = await _gen.generate_invoice_ae(invoice_data=_invoice_data())
    assert isinstance(result["xml"], str)
    assert result["customization_id"] == CUSTOMIZATION_IDS["billing"]
    assert result["profile_id"] == PROFILE_IDS["billing"]
    assert "AE-01TEST" in result["xml"]
    assert "198765432102003" in result["xml"]


async def test_generate_emits_ae_mandatory_elements() -> None:
    """AE-SC-1/AE-SC-3: cbc:UUID, cbc:ProfileExecutionID, per-line
    cac:ItemPriceExtension, and PartyLegalEntity/CompanyID (schemeAgencyID=TL)
    must all be present in generated output."""
    result = await _gen.generate_invoice_ae(invoice_data=_invoice_data())
    xml = result["xml"]
    assert "<cbc:UUID>f12f329f-6430-4399-b661-7c5cd9c3a9e6</cbc:UUID>" in xml
    assert "<cbc:ProfileExecutionID>00000000</cbc:ProfileExecutionID>" in xml
    assert "<cac:ItemPriceExtension>" in xml
    assert 'schemeAgencyID="TL"' in xml
    assert "112345678900003" in xml


async def test_generate_selfbilling_variant() -> None:
    result = await _gen.generate_invoice_ae(invoice_data=_invoice_data(), variant="selfbilling")
    assert result["customization_id"] == CUSTOMIZATION_IDS["selfbilling"]
    assert result["profile_id"] == PROFILE_IDS["selfbilling"]
    assert CUSTOMIZATION_IDS["selfbilling"] in result["xml"]


async def test_generate_wraps_validation_failure() -> None:
    data = _invoice_data()
    data["tax_lines"] = []
    with pytest.raises(DocumentGenerationError, match="BR-CO-18"):
        await _gen.generate_invoice_ae(invoice_data=data)


def test_get_format_name_and_country_code() -> None:
    assert _gen.get_format_name() == "UBL-2.1"
    assert _gen.get_country_code() == "AE"
