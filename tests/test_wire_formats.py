"""Tests for AEUBLSerializer (mcp_einvoicing_ae.wire_formats)."""

from datetime import date
from decimal import Decimal

from lxml import etree
from mcp_einvoicing_core.en16931 import EN16931Address, EN16931Tax

from mcp_einvoicing_ae.models.invoice import AE_STANDARD_VAT_RATE, AEInvoice, AEInvoiceLine
from mcp_einvoicing_ae.models.party import AEParty
from mcp_einvoicing_ae.wire_formats import AEUBLSerializer

_ADDRESS = EN16931Address(
    line_one="Street Name", city="Sharjah", postcode="00000", country_code="AE"
)
_CBC = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
_CAC = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
_NS = {"cbc": _CBC, "cac": _CAC}


def _invoice(**overrides) -> AEInvoice:
    seller_kwargs = overrides.pop("seller_kwargs", {})
    buyer_kwargs = overrides.pop("buyer_kwargs", {})
    kwargs = {
        "invoice_number": "AE-01TEST",
        "invoice_date": date(2025, 2, 6),
        "document_uuid": "f12f329f-6430-4399-b661-7c5cd9c3a9e6",
        "profile_execution_id": "00000000",
        "seller": AEParty(
            name="Party Trade Name",
            address=_ADDRESS,
            vat_id="198765432102003",
            trade_license_number="112345678900003",
            **seller_kwargs,
        ),
        "buyer": AEParty(
            name="Noor Electronics",
            address=_ADDRESS,
            vat_id="134567890123003",
            **buyer_kwargs,
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
    kwargs.update(overrides)
    return AEInvoice(**kwargs)


def test_company_id_omitted_when_trade_license_number_unset() -> None:
    """Buyer has no trade_license_number in this fixture — no CompanyID under
    its PartyLegalEntity, while the seller (which does set it) gets one."""
    xml = AEUBLSerializer().serialize(_invoice())
    root = etree.fromstring(xml)
    buyer_legal = root.find("cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity", _NS)
    assert buyer_legal is not None
    assert buyer_legal.find("cbc:CompanyID", _NS) is None

    seller_legal = root.find("cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity", _NS)
    company_id = seller_legal.find("cbc:CompanyID", _NS)
    assert company_id is not None
    assert company_id.text == "112345678900003"
    assert company_id.get("schemeAgencyID") == "TL"


def test_item_price_extension_math_matches_fixture() -> None:
    """line_net_amount=10486, tax_rate=5 -> vat=524.3, payable=11010.3,
    matching specs/pint-ae/trn-invoice/example/Standard tax invoice.xml."""
    xml = AEUBLSerializer().serialize(_invoice())
    root = etree.fromstring(xml)
    ipe = root.find("cac:InvoiceLine/cac:ItemPriceExtension", _NS)
    assert ipe is not None
    assert Decimal(ipe.find("cbc:Amount", _NS).text) == Decimal("11010.3")
    assert Decimal(ipe.find("cac:TaxTotal/cbc:TaxAmount", _NS).text) == Decimal("524.3")


def test_profile_execution_id_sibling_of_profile_id() -> None:
    xml = AEUBLSerializer().serialize(_invoice())
    root = etree.fromstring(xml)
    children = [etree.QName(c.tag).localname for c in root if etree.QName(c.tag).namespace == _CBC]
    assert children.index("ProfileID") < children.index("ProfileExecutionID") < children.index("ID")


def test_uuid_and_profile_execution_id_values() -> None:
    xml = AEUBLSerializer().serialize(_invoice())
    root = etree.fromstring(xml)
    assert root.find("cbc:UUID", _NS).text == "f12f329f-6430-4399-b661-7c5cd9c3a9e6"
    assert root.find("cbc:ProfileExecutionID", _NS).text == "00000000"
