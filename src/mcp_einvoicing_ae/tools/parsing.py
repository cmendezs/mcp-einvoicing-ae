"""PINT AE UBL 2.1 invoice parsing tool for UAE e-invoices.

Reuses mcp_einvoicing_core.wire_formats.EN16931UBLParser directly (see
models/invoice.py's module docstring), returning the EN 16931 core field set
only. AE-specific extensions are not extracted: core's parser has no mapping
for AEParty.trade_license_number (PartyLegalEntity/CompanyID,
schemeAgencyID="TL"), and the parsed result is the base ``EN16931Invoice``
model, not a re-validated ``AEInvoice``/``AEParty`` — TRN format checking
(``TaxIdentifier.validate_ae_trn``) is not re-applied to parsed content.
[NEED: bespoke AE extraction] before trade_license_number can round-trip
through this tool.
"""

from __future__ import annotations

from typing import Annotated

from mcp_einvoicing_core.wire_formats import EN16931UBLParser

_AE_EXTENSIONS_NOT_PARSED_WARNING = (
    "AE-EXTENSIONS-NOT-PARSED: trade_license_number and other AE-specific "
    "fields are not extracted by this tool; only the EN 16931 core field set "
    "is returned, and TRN format is not re-validated."
)


async def parse_invoice_ae(
    xml_content: Annotated[str, "Raw PINT AE UBL 2.1 XML invoice content"],
) -> dict[str, object]:
    """Parse a PINT AE UBL 2.1 XML invoice into a structured dict.

    Accepts a PINT AE billing or self-billing UBL 2.1 document (Invoice or
    CreditNote root) and extracts the EN 16931 core field set (header,
    parties, lines, tax breakdown, totals). AE-specific extensions beyond the
    EN 16931 base are not extracted — see module docstring.

    Returns ``{"success": true, "invoice": {...}, "warnings": [...]}`` on
    success, or ``{"success": false, "error": "..."}`` on parse failure.
    """
    from lxml import etree  # noqa: PLC0415

    try:
        raw = xml_content.encode("utf-8") if isinstance(xml_content, str) else xml_content
        invoice = EN16931UBLParser().parse(raw)
        return {
            "success": True,
            "invoice": invoice.model_dump(mode="json"),
            "warnings": [_AE_EXTENSIONS_NOT_PARSED_WARNING],
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
