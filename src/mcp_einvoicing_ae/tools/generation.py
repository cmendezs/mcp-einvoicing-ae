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
from mcp_einvoicing_ae.models.tdd import AETaxDataDocument
from mcp_einvoicing_ae.standards.pint_ae import CUSTOMIZATION_IDS, PROFILE_IDS
from mcp_einvoicing_ae.tdd_wire_format import AETDDSerializer
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

    async def generate_tdd_ae(
        self,
        tdd_data: Annotated[
            dict[str, Any], "Tax Data Document fields matching the AETaxDataDocument schema"
        ],
    ) -> dict[str, object]:
        """Generate a Peppol AE Tax Data Document (``pxs:TaxData``) XML from structured data.

        The TDD is the 5th-corner report sent to the tax authority (via the
        reporting service provider, C5) for each issued or received PINT AE
        invoice. It carries its own namespace (``urn:peppol:schema:taxdata:1.0``),
        a summary of the reported invoice, and the full source invoice embedded
        in ``pxs:SourceDocument``. This tool builds the document only: sending it
        is a Peppol access-point function (the TDD travels over the Peppol network
        in an SBDH whose Sender/Receiver match ``ReportingParty``/``ReceivingParty``).

        Rules enforced before emitting (TDD Schematron ibr-tdd-*): exactly one
        reported transaction, reported-document identifiers and amounts present,
        a source document present, a timezone on ``issue_time``, a mandatory
        reporters representative, and receiver scheme ``0242``.

        Returns a dict with:
        - ``xml``: the generated ``pxs:TaxData`` XML string
        - ``customization_id``: the CustomizationID applied
        - ``profile_id``: the ProfileID applied
        """
        try:
            tdd = AETaxDataDocument.model_validate(tdd_data)
            xml_string = AETDDSerializer().serialize(tdd).decode("utf-8")
        except DocumentGenerationError:
            raise
        except Exception as exc:
            raise DocumentGenerationError(str(exc)) from exc
        return {
            "xml": xml_string,
            "customization_id": tdd.customization_id,
            "profile_id": tdd.profile_id,
        }
