"""UAE trading party — extends mcp-einvoicing-core's EN16931Party.

Field sources (context-library/countries/ae.md "Party-identifier formats",
retrieved 2026-08-26 from specs/pint-ae/trn-invoice/example/Standard tax invoice.xml):

- TRN (Tax Registration Number): 15-digit numeric, carried in `vat_id`
  (cac:PartyTaxScheme/cbc:CompanyID, IBT-031/IBT-048). Format-validated via
  mcp_einvoicing_core.models.TaxIdentifier.validate_ae_trn() — no check-digit
  algorithm has been confirmed in any supplied source, so only format is checked.
- TIN (Tax Identification Number / Peppol Participant Identifier): the first
  10 digits of the TRN, scheme "0235" (cbc:EndpointID schemeID="0235").
  Auto-derived from `vat_id` when `electronic_address` is not supplied.
- Trade License number: a distinct identifier from the TRN
  (cac:PartyLegalEntity/cbc:CompanyID, schemeAgencyID="TL", IBT-030/IBT-047,
  BTAE-11/12/15/16). Do not conflate with the TRN.
"""

from __future__ import annotations

from mcp_einvoicing_core.en16931 import EN16931Party
from mcp_einvoicing_core.models import TaxIdentifier
from pydantic import Field, field_validator, model_validator

from mcp_einvoicing_ae.standards.pint_ae import PEPPOL_PARTICIPANT_SCHEME


class AEParty(EN16931Party):
    """UAE trading party (seller BG-4 or buyer BG-7).

    ``vat_id`` carries the 15-digit TRN. ``trade_license_number`` is a
    separate identifier (schemeAgencyID="TL") and must not be conflated
    with the TRN.
    """

    vat_id: str = Field(..., description="15-digit TRN (BT-31 / BT-48)")
    trade_license_number: str | None = Field(
        default=None,
        description=(
            "Trade License number issued by the Trade License issuing Authority "
            "(IBT-030 / IBT-047, BTAE-11/12/15/16) — distinct from the TRN."
        ),
    )

    @field_validator("vat_id")
    @classmethod
    def _validate_trn_format(cls, v: str) -> str:
        ok, error = TaxIdentifier.validate_ae_trn(v)
        if not ok:
            raise ValueError(f"Invalid TRN in vat_id: {error}")
        return v

    @model_validator(mode="after")
    def _derive_peppol_participant_id(self) -> AEParty:
        """Default the Peppol participant identifier to the TIN (first 10 digits of the TRN).

        Source: specs/guidelines/UAE-Electronic-Invoicing-Guidelines_V-1.1-01June2026.pdf,
        p.3/p.7: "The TIN is the first 10 digits of the TRN."
        """
        if self.electronic_address is None:
            self.electronic_address = self.vat_id[:10]
        if self.electronic_address_scheme is None:
            self.electronic_address_scheme = PEPPOL_PARTICIPANT_SCHEME
        return self
