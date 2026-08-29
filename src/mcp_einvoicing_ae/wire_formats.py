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
    (AEParty.trade_license_number, BTAE-11/12/15/16) — mirrors
    mcp_invoicenow_sg.wire_formats.SGUBLSerializer's CompanyID pattern for
    SGParty.uen.

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
                customization_id_el.addnext(pe_el)
        return self._to_bytes(root)

    def _build_party(self, parent: etree._Element, wrapper: str, party: EN16931Party) -> None:
        super()._build_party(parent, wrapper, party)
        if not (isinstance(party, AEParty) and party.trade_license_number):
            return
        wrapper_el = parent.find(_q(wrapper))
        if wrapper_el is None:
            return
        party_el = wrapper_el.find(_q("Party"))
        if party_el is None:
            return
        legal = party_el.find(_q("PartyLegalEntity"))
        if legal is None:
            return
        company_id = etree.SubElement(legal, _q("CompanyID", _CBC))
        company_id.text = party.trade_license_number
        company_id.set("schemeAgencyID", "TL")
