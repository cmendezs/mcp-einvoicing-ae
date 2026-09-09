"""UBL 2.1 serializer for AEInvoice — PINT AE (billing + self-billing).

Reuses mcp_einvoicing_core.wire_formats.EN16931UBLSerializer wholesale and
adds the AE-specific elements core cannot derive on its own:

  - cbc:UUID (BTAE-07, ibr-193-ae) and cac:ItemPriceExtension per line
    (BTAE-10/BTAE-08, ibr-104-ae/ibr-194-ae) now come natively from core
    v1.25.0 (EN16931Invoice.document_uuid and the opt-in
    _emit_item_price_extension flag) — no override needed here beyond
    setting the flag.
  - cbc:ProfileExecutionID (BTAE-02, ibr-154-ae) — a sibling inserted
    immediately after cbc:ProfileID, mirroring how core emits cbc:UUID as a
    sibling of cbc:ID.
  - cac:PartyLegalEntity/cbc:CompanyID with schemeAgencyID="TL"
    (AEParty.trade_license_number, BTAE-11/12/15/16) now comes from core's
    opt-in _get_party_legal_entity_company_id hook (v1.32.0, CORE-6) —
    mirrors mcp_invoicenow_sg.wire_formats.SGUBLSerializer's identical
    override for SGParty.uen. Previously a package-local _build_party
    override duplicating core's element traversal; see
    audit/2026-09-audit-core.md.

Placement confirmed against
specs/pint-ae/trn-invoice/example/Standard tax invoice.xml and the UBL 2.1
Invoice schema sequence (CustomizationID -> ProfileID -> ID -> UUID ->
IssueDate).
"""

from __future__ import annotations

from lxml import etree
from mcp_einvoicing_core.en16931 import EN16931Invoice, EN16931Party
from mcp_einvoicing_core.wire_formats import UBL_NSMAP, EN16931UBLSerializer

from mcp_einvoicing_ae.models.invoice import AEInvoice
from mcp_einvoicing_ae.models.party import AEParty

_CAC = UBL_NSMAP["cac"]
_CBC = UBL_NSMAP["cbc"]


def _q(local: str, ns: str = _CAC) -> str:
    return f"{{{ns}}}{local}"


class AEUBLSerializer(EN16931UBLSerializer):
    """Serialize an AEInvoice to UBL 2.1 XML bytes (PINT AE billing/self-billing)."""

    #: BTAE-10/BTAE-08 (ibr-104-ae/ibr-194-ae) — see core's
    #: EN16931UBLSerializer._build_item_price_extension docstring for the
    #: placement/amount derivation confirmed against the AE example fixture.
    _emit_item_price_extension = True

    def serialize(self, invoice: EN16931Invoice) -> bytes:
        root = self._build_root(invoice)
        # cbc:ProfileExecutionID (BTAE-02), sibling immediately after
        # cbc:ProfileID per the UBL 2.1 Invoice schema sequence.
        if isinstance(invoice, AEInvoice) and invoice.profile_execution_id:
            pe_el = etree.Element(_q("ProfileExecutionID", _CBC))
            pe_el.text = invoice.profile_execution_id
            profile_id_el = root.find(_q("ProfileID", _CBC))
            if profile_id_el is not None:
                profile_id_el.addnext(pe_el)
            else:
                # business_process (-> ProfileID) is optional in core; AEInvoice
                # always sets it via _resolve_variant, but fall back to a
                # position right after CustomizationID if it's ever absent.
                customization_id_el = root.find(_q("CustomizationID", _CBC))
                if customization_id_el is not None:
                    customization_id_el.addnext(pe_el)
        return self._to_bytes(root)

    def _get_party_legal_entity_company_id(
        self, party: EN16931Party
    ) -> tuple[str, str | None] | None:
        """AEParty.trade_license_number, schemeAgencyID="TL" (BTAE-11/12/15/16)."""
        if isinstance(party, AEParty) and party.trade_license_number:
            return (party.trade_license_number, "TL")
        return None
