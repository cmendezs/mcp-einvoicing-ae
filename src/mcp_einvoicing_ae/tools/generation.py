"""UAE invoice generation — subclasses BaseDocumentGenerator from mcp-einvoicing-core.

AEInvoice reuses mcp_einvoicing_core.wire_formats.EN16931UBLSerializer directly
(see models/invoice.py's module docstring) rather than a package-local UBL
emitter — grepped 2026-08-27: no other country package in the monorepo calls
it directly, so AE is the first real consumer.

Known limitation: only the EN 16931 core field set is emitted.
AEParty.trade_license_number (a genuine PINT AE field, IBT-030/IBT-047) has
no mapping in core's generic serializer and is silently dropped from the
output XML today. [NEED: a bespoke AE serializer override, or a core hook for
country-specific PartyLegalEntity/CompanyID extensions] before
trade_license_number can round-trip through generation. Documented here
rather than fixed silently.

core-state-check: [REUSE: EN16931UBLSerializer from core v1.22.0]
"""

from __future__ import annotations

from typing import Annotated, Any

from mcp_einvoicing_core import BaseDocumentGenerator, DocumentGenerationError
from mcp_einvoicing_core.wire_formats import EN16931UBLSerializer

from mcp_einvoicing_ae.models.invoice import AEInvoice, AEProfileVariant
from mcp_einvoicing_ae.standards.pint_ae import CUSTOMIZATION_IDS, PROFILE_IDS


class AEDocumentGenerator(BaseDocumentGenerator[AEInvoice]):
    """UAE PINT AE UBL 2.1 document generator (billing + self-billing).

    Subclasses ``BaseDocumentGenerator`` and implements ``generate()``.
    Tools are exposed as instance methods so they can be registered on
    ``EInvoicingMCPServer``.
    """

    def get_format_name(self) -> str:
        return "UBL-2.1"

    def get_country_code(self) -> str:
        return "AE"

    def generate(self, document: AEInvoice) -> str:
        """Serialize an ``AEInvoice`` to a UBL 2.1 XML string."""
        return EN16931UBLSerializer().serialize(document).decode("utf-8")

    async def generate_invoice_ae(
        self,
        invoice_data: Annotated[dict[str, Any], "Invoice fields matching the AEInvoice schema"],
        variant: Annotated[
            AEProfileVariant,
            "PINT AE profile variant: 'billing' (default) or 'selfbilling'",
        ] = "billing",
    ) -> dict[str, object]:
        """Generate a PINT AE UBL 2.1 e-invoice XML document from structured data.

        Applies the correct CustomizationID (BT-24) and ProfileID (BT-23) for
        the selected variant. Only the EN 16931 core field set is emitted —
        ``AEParty.trade_license_number`` has no bespoke mapping in core's UBL
        serializer yet and is dropped from the output; see this module's
        docstring.

        Returns a dict with:
        - ``xml``: the generated UBL 2.1 XML string
        - ``customization_id``: the CustomizationID applied (BT-24)
        - ``profile_id``: the ProfileID applied (BT-23)
        """
        try:
            invoice = AEInvoice.model_validate({**invoice_data, "variant": variant})
            xml_string = self.generate(invoice)
        except DocumentGenerationError:
            raise
        except Exception as exc:
            raise DocumentGenerationError(str(exc)) from exc

        return {
            "xml": xml_string,
            "customization_id": CUSTOMIZATION_IDS[variant],
            "profile_id": PROFILE_IDS[variant],
        }
