"""PINT AE UBL 2.1 invoice parsing tool for UAE e-invoices.

Reuses mcp_einvoicing_core.wire_formats.EN16931UBLParser for the EN 16931
core field set, then re-extracts the AE-specific extensions core's generic
parser has no mapping for (document_uuid, profile_execution_id,
trade_license_number per party) directly from the raw XML via targeted
XPath, and re-validates the merged result as an AEInvoice — restoring the
same TRN-format and tax-rate checks a fresh AEInvoice construction gets,
and round-tripping trade_license_number end to end.

Note: EN16931UBLParser._extract builds and returns EN16931Invoice inline
with no reusable intermediate dict to subclass/extend (unlike the
serializer, which exposes hookable _build_* methods) — see
mcp_einvoicing_core.wire_formats module docstring. Re-scanning the raw XML
separately for the handful of AE-specific elements is simpler and more
robust than duplicating that method.
"""

from __future__ import annotations

from typing import Annotated

from mcp_einvoicing_core.wire_formats import UBL_NSMAP, EN16931UBLParser
from mcp_einvoicing_core.xml_utils import safe_fromstring

from mcp_einvoicing_ae.models.invoice import AEInvoice

_NSMAP = {"cbc": UBL_NSMAP["cbc"], "cac": UBL_NSMAP["cac"]}


def _extract_ae_extensions(root) -> dict[str, str | None]:  # noqa: ANN001
    """Pull the AE-specific elements core's generic parser doesn't map."""

    def text(xpath: str) -> str | None:
        results = root.xpath(xpath, namespaces=_NSMAP)
        el = results[0] if results else None
        return el.text.strip() if el is not None and el.text else None

    return {
        "document_uuid": text("cbc:UUID"),
        "profile_execution_id": text("cbc:ProfileExecutionID"),
        "seller_trade_license_number": text(
            "cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/"
            'cbc:CompanyID[@schemeAgencyID="TL"]'
        ),
        "buyer_trade_license_number": text(
            "cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/"
            'cbc:CompanyID[@schemeAgencyID="TL"]'
        ),
    }


async def parse_invoice_ae(
    xml_content: Annotated[str, "Raw PINT AE UBL 2.1 XML invoice content"],
) -> dict[str, object]:
    """Parse a PINT AE UBL 2.1 XML invoice into a structured dict.

    Accepts a PINT AE billing or self-billing UBL 2.1 document (Invoice or
    CreditNote root), extracts the EN 16931 core field set plus the AE
    extensions (document_uuid, profile_execution_id, trade_license_number),
    and re-validates the merged result as an AEInvoice — so TRN format and
    tax-rate/category consistency are re-checked on parsed content, not just
    on freshly constructed invoices.

    Returns ``{"success": true, "invoice": {...}}`` on success, or
    ``{"success": false, "error": "..."}`` on parse or validation failure.
    """
    from lxml import etree  # noqa: PLC0415

    try:
        raw = xml_content.encode("utf-8") if isinstance(xml_content, str) else xml_content
        base_invoice = EN16931UBLParser().parse(raw)
        root = safe_fromstring(raw)
        extensions = _extract_ae_extensions(root)

        data = base_invoice.model_dump(mode="json")
        data["document_uuid"] = extensions["document_uuid"]
        data["profile_execution_id"] = extensions["profile_execution_id"]
        data["seller"]["trade_license_number"] = extensions["seller_trade_license_number"]
        data["buyer"]["trade_license_number"] = extensions["buyer_trade_license_number"]

        invoice = AEInvoice.model_validate(data)
        return {
            "success": True,
            "invoice": invoice.model_dump(mode="json"),
        }
    except etree.XMLSyntaxError as exc:
        return {
            "success": False,
            "error": f"XML parse error: {exc}",
        }
    except Exception as exc:
        return {
            "success": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
