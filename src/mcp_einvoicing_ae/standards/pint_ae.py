"""PINT AE profile constants and core profile-registry registration.

URNs copied verbatim from supplied PINT AE example documents — see
`context-library/formats/pint-ae.md` (mcp-einvoicing monorepo) for the full
citation trail. Do not edit a URN here without a corresponding citation update
in that file.
"""

from __future__ import annotations

from mcp_einvoicing_core.profile_registry import profile_registry

# UBL CustomizationID values (BT-24)
CUSTOMIZATION_IDS: dict[str, str] = {
    "billing": "urn:peppol:pint:billing-1@ae-1",
    "selfbilling": "urn:peppol:pint:selfbilling-1@ae-1",
}

# UBL ProfileID values (BT-23)
PROFILE_IDS: dict[str, str] = {
    "billing": "urn:peppol:bis:billing",
    "selfbilling": "urn:peppol:bis:selfbilling",
}

# Default UNCL1001 invoice type code per profile, observed in supplied examples:
# billing uses 380 (Invoice), self-billing uses 389 (Self-billed invoice).
DEFAULT_INVOICE_TYPE_CODE: dict[str, str] = {
    "billing": "380",
    "selfbilling": "389",
}

# Peppol AE Tax Data Document (TDD) — not a UBL invoice, own namespace.
# Observed in specs/tdd/trn-tdd/example/simple.xml.
TDD_CUSTOMIZATION_ID = "urn:peppol:taxdata:ae-1"
TDD_PROFILE_ID = "urn:peppol:taxreporting"
TDD_NAMESPACE = "urn:peppol:schema:taxdata:1.0"

# Peppol participant identifier scheme for UAE (ISO 6523 ICD), observed in
# every supplied example's cbc:EndpointID schemeID attribute.
PEPPOL_PARTICIPANT_SCHEME = "0235"

for _profile_name, _customization_id in CUSTOMIZATION_IDS.items():
    profile_registry.register("AE", _profile_name.upper(), "UBL", _customization_id)
