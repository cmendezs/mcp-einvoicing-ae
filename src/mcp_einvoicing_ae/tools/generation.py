"""UAE invoice generation — subclasses BaseDocumentGenerator from mcp-einvoicing-core.

Uses AEUBLSerializer (mcp_einvoicing_ae.wire_formats), which layers the
AE-specific elements (cbc:ProfileExecutionID, PartyLegalEntity/CompanyID
schemeAgencyID="TL") on top of core's EN16931UBLSerializer — see that
module's docstring for the full mapping, including which elements now come
natively from core v1.25.0 (cbc:UUID, cac:ItemPriceExtension).

core-state-check: [REUSE: EN16931UBLSerializer from core v1.25.0]
"""

from __future__ import annotations

from typing import Annotated, Any

from mcp_einvoicing_core import BaseDocumentGenerator, DocumentGenerationError

from mcp_einvoicing_ae.models.invoice import AEInvoice, AEProfileVariant
from mcp_einvoicing_ae.standards.pint_ae import CUSTOMIZATION_IDS, PROFILE_IDS
from mcp_einvoicing_ae.wire_formats import AEUBLSerializer


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
        return AEUBLSerializer().serialize(document).decode("utf-8")

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
        the selected variant. All unconditionally-mandatory PINT AE elements
        are emitted: ``cbc:UUID``, ``cbc:ProfileExecutionID``, per-line
        ``cac:ItemPriceExtension``, and ``PartyLegalEntity/CompanyID``
        (``AEParty.trade_license_number``, when set).

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
