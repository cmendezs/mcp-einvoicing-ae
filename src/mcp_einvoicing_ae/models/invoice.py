"""UAE invoice models — extend mcp-einvoicing-core EN16931 base types.

PINT AE (billing + self-billing) is a UBL 2.1 CIUS of EN 16931-1:2017 (confirmed
by CustomizationID/ProfileID inspection — see context-library/countries/ae.md
"Invoice-tree pathway"). Unlike some country packages, AEInvoice does not need a
bespoke serializer: PINT AE's structural fields map directly onto
mcp_einvoicing_core.wire_formats.EN16931UBLSerializer/EN16931UBLParser (which
read CustomizationID from `profile` and ProfileID from `business_process`), so
`profile` here holds the real BT-24 URN rather than a package-local friendly
key. `variant` is a convenience input that resolves to the right `profile` /
`business_process` / default `invoice_type_code` when the caller does not want
to look up raw URNs themselves.

Field/rule citations: context-library/countries/ae.md, context-library/formats/pint-ae.md
(mcp-einvoicing monorepo), and specs/pint-ae/trn-invoice/example/Standard tax invoice.xml.
"""

from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import Any, ClassVar, Literal

from mcp_einvoicing_core.en16931 import EN16931Invoice, EN16931LineItem
from pydantic import model_validator

from mcp_einvoicing_ae.models.party import AEParty
from mcp_einvoicing_ae.standards.pint_ae import (
    CUSTOMIZATION_IDS,
    DEFAULT_INVOICE_TYPE_CODE,
    PROFILE_IDS,
)

AEProfileVariant = Literal["billing", "selfbilling"]


class AEVatCategory(StrEnum):
    """UNCL5305 VAT category codes observed in PINT AE examples.

    Source: context-library/countries/ae.md "Currency and VAT rates" —
    category letters S, AE, E, O, Z appear in supplied example filenames
    (Doc-level-allowance-AE-category.xml, etc.), mapped against the
    Aligned-TaxCategoryCodes.gc codelist. The full semantics of each code
    beyond the letter itself are `[NEED:]` per that file — read
    specs/pint-ae/trn-invoice/codelist/Aligned-TaxCategoryCodes.gc directly
    before relying on anything beyond the bare code value.
    """

    STANDARD = "S"
    REVERSE_CHARGE = "AE"
    EXEMPT = "E"
    NOT_SUBJECT = "O"
    ZERO_RATED = "Z"


# Standard UAE VAT rate (ibr-190-ae): 5.00%. See context-library/countries/ae.md
# "Currency and VAT rates" for the citation. Reduced/zero-rate statutory basis
# remains [NEED:] there — only the standard-rate numeric value is used here.
AE_STANDARD_VAT_RATE = Decimal("5.00")


class AEInvoiceLine(EN16931LineItem):
    """PINT AE invoice line (BG-25), narrowing `tax_category` to the observed UNCL5305 set."""

    tax_category: AEVatCategory = AEVatCategory.STANDARD


class AEInvoice(EN16931Invoice):
    """UAE e-invoice — PINT AE billing or self-billing profile.

    `profile` (BT-24) and `business_process` (BT-23) hold the real Peppol URNs
    directly (see module docstring for why), copied verbatim from
    context-library/formats/pint-ae.md's Profile URNs table:

        billing:      urn:peppol:pint:billing-1@ae-1     / urn:peppol:bis:billing
        selfbilling:  urn:peppol:pint:selfbilling-1@ae-1  / urn:peppol:bis:selfbilling

    `variant` is a convenience constructor input only — pass either `variant`
    or explicit `profile`/`business_process`, not a mix that disagrees.
    """

    _allowed_profiles: ClassVar[frozenset[str]] = frozenset(CUSTOMIZATION_IDS.values())

    variant: AEProfileVariant | None = None
    seller: AEParty
    buyer: AEParty
    line_items: list[AEInvoiceLine]  # type: ignore[assignment]
    currency_code: str = "AED"

    @model_validator(mode="before")
    @classmethod
    def _resolve_variant(cls, data: Any) -> Any:
        """Fill `profile`/`business_process`/`invoice_type_code` from `variant` when unset.

        Runs before field validation so EN16931Invoice's own validators
        (_require_tax_lines, _check_profile_urn) see a fully populated instance.
        """
        if not isinstance(data, dict):
            return data
        variant: AEProfileVariant = data.get("variant") or "billing"
        data = dict(data)
        data.setdefault("profile", CUSTOMIZATION_IDS[variant])
        data.setdefault("business_process", PROFILE_IDS[variant])
        data.setdefault("invoice_type_code", DEFAULT_INVOICE_TYPE_CODE[variant])
        data.setdefault("variant", variant)
        return data
