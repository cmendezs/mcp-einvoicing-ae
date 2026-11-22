"""Peppol AE Tax Data Document (TDD) model.

The TDD is the UAE's 5th-corner tax-authority reporting document. It is
**not** a UBL Invoice/CreditNote and must not be modeled as a variant of
AEInvoice — own namespace (``urn:peppol:schema:taxdata:1.0``), own root
element (``pxs:TaxData``), own Schematron and XSD.

Field/cardinality source: specs/tdd/common/peppol-tdd-1.0.0.xsd (root element
``TaxData`` / type ``TaxDataType``, `ReportedTransactionType`), cross-checked
against the worked example specs/tdd/trn-tdd/example/simple.xml. Fields below
cover the schema's mandatory (``minOccurs="1"``) elements plus the commonly
populated optional ones seen in the example; this is not a field-for-field
transcription of the full XSD (e.g. `ReportedDocument`'s nested party/tax
detail and `CustomContent` are not modeled) — read the XSD directly before
assuming a field not listed here is unsupported by the format itself.

Transport mechanism: the TDD BIS (``specs/tdd/common/docs/tdd-bis.pdf``, section 1.2)
states that the issuer's service provider (C2) and the receiver's service provider (C3)
each send a TDD to the tax authority's service provider (C5) "by using the Peppol
network", and the compliance document (``tdd-compliance.pdf``) requires the SBDH
``Sender``/``Receiver`` identifiers to equal ``pxs:ReportingParty``/``pxs:ReceivingParty``
``cbc:EndpointID`` (value and ``schemeID``). The TDD therefore travels over the same
Peppol AS4 channel as a PINT AE invoice, enveloped in an SBDH, not over a separate REST
channel. This module models and serializes the document only; submission is a
service-provider (Peppol access point) function, and the C5-to-FTA leg uses a data
format "agreed between them" that no supplied document specifies.
"""

from __future__ import annotations

from datetime import date, time
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from mcp_einvoicing_ae.standards.pint_ae import (
    PEPPOL_PARTICIPANT_SCHEME,
    TDD_CUSTOMIZATION_ID,
    TDD_NAMESPACE,
    TDD_PROFILE_ID,
)

__all__ = [
    "TDD_NAMESPACE",
    "TDDParty",
    "TDDReportedDocument",
    "TDDReportedTransaction",
    "AETaxDataDocument",
]


class TDDParty(BaseModel):
    """Minimal party reference for TDD reporting/receiving parties.

    Source: peppol-tdd-1.0.0.xsd ``ReportingParty``/``ReceivingParty``
    (``cac:PartyType``, only ``cbc:EndpointID`` observed in the supplied
    example — the full ``PartyType`` supports far more, but nothing else was
    populated in any supplied TDD example).
    """

    endpoint_id: str = Field(..., description="cbc:EndpointID value")
    endpoint_scheme: str = Field(
        default=PEPPOL_PARTICIPANT_SCHEME, description="cbc:EndpointID schemeID attribute"
    )


class TDDReportedDocument(BaseModel):
    """Summary of the invoice/credit-note being reported (``pxs:ReportedDocument``).

    Mandatory per XSD: customization_id, profile_id, issue_date, issue_time,
    document_type_code, document_scope is on the parent TaxData, not here.
    Only the fields observed in the supplied example are modeled; the XSD
    additionally allows tax-total and monetary-total detail not transcribed
    here — read peppol-tdd-1.0.0.xsd directly if that detail is needed.
    """

    customization_id: str = Field(..., description="The reported document's own CustomizationID")
    profile_id: str = Field(..., description="The reported document's own ProfileID")
    document_id: str | None = Field(default=None, description="cbc:ID")
    uuid: str | None = Field(default=None, description="cbc:UUID")
    issue_date: date
    issue_time: time
    document_type_code: str = Field(
        ..., description="UNTDID 1001 code of the reported document, e.g. '380'"
    )
    currency_code: str | None = Field(default=None, description="cbc:DocumentCurrencyCode")
    supplier_trn: str | None = Field(
        default=None, description="AccountingSupplierParty/PartyTaxScheme/CompanyID"
    )
    customer_trn: str | None = Field(
        default=None, description="AccountingCustomerParty/PartyTaxScheme/CompanyID"
    )
    supplier_tax_scheme: str = Field(
        default="VAT", description="Supplier PartyTaxScheme/TaxScheme/cbc:ID (ibr-tdd-45)"
    )
    customer_tax_scheme: str = Field(
        default="VAT", description="Customer PartyTaxScheme/TaxScheme/cbc:ID"
    )
    tax_amount: Decimal | None = Field(
        default=None, description="cac:TaxTotal/cbc:TaxAmount in the document currency (ibt-110)"
    )
    tax_exclusive_amount: Decimal | None = Field(
        default=None,
        description="pxs:MonetaryTotal/cbc:TaxExclusiveAmount in the document currency (ibt-109)",
    )


class TDDReportedTransaction(BaseModel):
    """One reported transaction (``pxs:ReportedTransaction``, 0..unbounded).

    ``source_document_xml`` holds the raw embedded UBL invoice/credit-note
    (``pxs:SourceDocument/cec:ExtensionContent``) as a string, unparsed — a
    full round-trip model of the embedded document is out of scope here;
    parse it separately with `AEInvoice`/`EN16931UBLParser` if needed.
    """

    transport_header_id: str | None = Field(
        default=None, description="pxs:TransportHeaderID — correlates to the AS4 transmission"
    )
    reported_document: TDDReportedDocument | None = None
    source_document_xml: str | None = Field(
        default=None, description="Raw embedded source document XML, unparsed"
    )


class AETaxDataDocument(BaseModel):
    """Peppol AE Tax Data Document (``pxs:TaxData``).

    Mandatory fields per peppol-tdd-1.0.0.xsd's ``TaxDataType``:
    CustomizationID, ProfileID, IssueDate, IssueTime, DocumentTypeCode,
    DocumentScope, ReporterRole, ReportingParty, ReceivingParty,
    ReportersRepresentative. ``ReportedTransaction`` is 0..unbounded.
    """

    customization_id: str = Field(default=TDD_CUSTOMIZATION_ID)
    profile_id: str = Field(default=TDD_PROFILE_ID)
    issue_date: date
    issue_time: time
    document_type_code: Literal["S"] = Field(
        default="S",
        description="pxs:DocumentTypeCode — only 'S' observed in supplied examples",
    )
    document_scope: Literal["D"] = Field(
        default="D",
        description="pxs:DocumentScope — only 'D' observed in supplied examples",
    )
    reporter_role: str = Field(..., description="pxs:ReporterRole, e.g. '01'")
    reporting_party: TDDParty
    receiving_party: TDDParty
    reporters_representative_id: str = Field(
        ...,
        min_length=1,
        description=(
            "pxs:ReportersRepresentative/cac:PartyIdentification/cbc:ID — mandatory "
            "(XSD minOccurs=1; Schematron ibr-tdd-19 requires exactly one)."
        ),
    )
    reporters_representative_scheme: Literal["0242"] = Field(
        default="0242",
        description="schemeID of the representative ID; ibr-tdd-21 allows only '0242' (SPIS)",
    )
    reported_transactions: list[TDDReportedTransaction] = Field(default_factory=list)

    @model_validator(mode="after")
    def _receiving_party_is_spis(self) -> AETaxDataDocument:
        """ibr-tdd-17: the receiver endpoint scheme MUST refer to an SPIS ('0242')."""
        if self.receiving_party.endpoint_scheme != "0242":
            raise ValueError(
                "ibr-tdd-17: receiving_party.endpoint_scheme must be '0242' (SPIS), "
                f"got {self.receiving_party.endpoint_scheme!r}"
            )
        return self
