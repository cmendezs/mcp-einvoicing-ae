"""Tests for AEInvoice / AEInvoiceLine.

Field values below are drawn from
specs/pint-ae/trn-invoice/example/Standard tax invoice.xml and
specs/pint-ae-self-billing/trn-invoice/example/Self Billing.xml.
"""

from datetime import date
from decimal import Decimal

import pytest
from mcp_einvoicing_core.en16931 import EN16931Address, EN16931Tax
from mcp_einvoicing_core.wire_formats import EN16931UBLSerializer
from pydantic import ValidationError

from mcp_einvoicing_ae.models.invoice import AE_STANDARD_VAT_RATE, AEInvoice, AEInvoiceLine
from mcp_einvoicing_ae.models.party import AEParty
from mcp_einvoicing_ae.standards.pint_ae import CUSTOMIZATION_IDS, PROFILE_IDS

_SELLER_ADDRESS = EN16931Address(
    line_one="Street Name", city="Sharjah", postcode="00000", country_code="AE"
)
_BUYER_ADDRESS = EN16931Address(
    line_one="Street Name", city="Abu Dhabi", postcode="00000", country_code="AE"
)


def _seller() -> AEParty:
    return AEParty(
        name="Party Trade Name",
        address=_SELLER_ADDRESS,
        vat_id="198765432102003",
        trade_license_number="112345678900003",
    )


def _buyer() -> AEParty:
    return AEParty(
        name="Noor Electronics",
        address=_BUYER_ADDRESS,
        vat_id="134567890123003",
        trade_license_number="112345679000001",
    )


def _line() -> AEInvoiceLine:
    return AEInvoiceLine(
        line_id="1",
        name="Item Name",
        quantity=Decimal("2000"),
        unit_code="H87",
        unit_price=Decimal("4.9"),
        line_net_amount=Decimal("10486"),
        tax_category="S",
        tax_rate=AE_STANDARD_VAT_RATE,
    )


def _base_kwargs() -> dict:
    return {
        "invoice_number": "AE-01TEST",
        "invoice_date": date(2025, 2, 6),
        "seller": _seller(),
        "buyer": _buyer(),
        "line_items": [_line()],
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


def test_billing_variant_resolves_profile_urns() -> None:
    invoice = AEInvoice(**_base_kwargs())
    assert invoice.profile == CUSTOMIZATION_IDS["billing"]
    assert invoice.business_process == PROFILE_IDS["billing"]
    assert invoice.invoice_type_code == "380"
    assert invoice.currency_code == "AED"


def test_selfbilling_variant_resolves_profile_urns() -> None:
    invoice = AEInvoice(variant="selfbilling", **_base_kwargs())
    assert invoice.profile == CUSTOMIZATION_IDS["selfbilling"]
    assert invoice.business_process == PROFILE_IDS["selfbilling"]
    assert invoice.invoice_type_code == "389"


def test_explicit_profile_overrides_variant_default() -> None:
    kwargs = _base_kwargs()
    invoice = AEInvoice(profile=CUSTOMIZATION_IDS["selfbilling"], **kwargs)
    assert invoice.profile == CUSTOMIZATION_IDS["selfbilling"]


def test_disallowed_profile_urn_rejected() -> None:
    kwargs = _base_kwargs()
    with pytest.raises(ValidationError, match="not in the"):
        AEInvoice(profile="urn:not-a-real-ae-profile", **kwargs)


def test_requires_at_least_one_tax_line() -> None:
    kwargs = _base_kwargs()
    kwargs["tax_lines"] = []
    with pytest.raises(ValidationError, match="BR-CO-18"):
        AEInvoice(**kwargs)


def test_serializes_via_core_ubl_serializer() -> None:
    """AEInvoice reuses core's EN16931UBLSerializer directly (no bespoke AE serializer)."""
    invoice = AEInvoice(**_base_kwargs())
    xml_bytes = EN16931UBLSerializer().serialize(invoice)
    xml = xml_bytes.decode("utf-8")
    assert "urn:peppol:pint:billing-1@ae-1" in xml
    assert "urn:peppol:bis:billing" in xml
    assert "198765432102003" in xml
