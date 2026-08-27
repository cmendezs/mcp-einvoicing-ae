"""Tests for AEParty — TRN validation and Peppol participant ID derivation.

TRN values are the exact examples from
specs/pint-ae/trn-invoice/example/Standard tax invoice.xml.
"""

import pytest
from mcp_einvoicing_core.en16931 import EN16931Address
from pydantic import ValidationError

from mcp_einvoicing_ae.models.party import AEParty

_ADDRESS = EN16931Address(
    line_one="Street Name", city="Sharjah", postcode="00000", country_code="AE"
)


def test_valid_trn_accepted() -> None:
    party = AEParty(name="Party Trade Name", address=_ADDRESS, vat_id="198765432102003")
    assert party.vat_id == "198765432102003"


def test_invalid_trn_rejected() -> None:
    with pytest.raises(ValidationError, match="15 digits"):
        AEParty(name="Party Trade Name", address=_ADDRESS, vat_id="12345")


def test_peppol_participant_id_derived_from_trn() -> None:
    party = AEParty(name="Buyer Trade Name", address=_ADDRESS, vat_id="134567890123003")
    assert party.electronic_address == "1345678901"
    assert party.electronic_address_scheme == "0235"


def test_explicit_electronic_address_not_overridden() -> None:
    party = AEParty(
        name="Party Trade Name",
        address=_ADDRESS,
        vat_id="198765432102003",
        electronic_address="9999999999",
        electronic_address_scheme="0088",
    )
    assert party.electronic_address == "9999999999"
    assert party.electronic_address_scheme == "0088"


def test_trade_license_number_distinct_from_trn() -> None:
    party = AEParty(
        name="Party Trade Name",
        address=_ADDRESS,
        vat_id="198765432102003",
        trade_license_number="112345678900003",
    )
    assert party.trade_license_number == "112345678900003"
    assert party.trade_license_number != party.vat_id
