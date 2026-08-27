"""Tests for AETaxDataDocument.

Field values below are drawn from specs/tdd/trn-tdd/example/simple.xml.
"""

from datetime import date, time

from mcp_einvoicing_ae.models.tdd import (
    TDD_NAMESPACE,
    AETaxDataDocument,
    TDDParty,
    TDDReportedDocument,
    TDDReportedTransaction,
)
from mcp_einvoicing_ae.standards.pint_ae import TDD_CUSTOMIZATION_ID, TDD_PROFILE_ID


def test_defaults_match_observed_customization_and_profile_id() -> None:
    tdd = AETaxDataDocument(
        issue_date=date(2025, 4, 14),
        issue_time=time(12, 0, 0),
        reporter_role="01",
        reporting_party=TDDParty(endpoint_id="dummy-sender"),
        receiving_party=TDDParty(endpoint_id="dummy-receiver", endpoint_scheme="0242"),
    )
    assert tdd.customization_id == TDD_CUSTOMIZATION_ID == "urn:peppol:taxdata:ae-1"
    assert tdd.profile_id == TDD_PROFILE_ID == "urn:peppol:taxreporting"
    assert TDD_NAMESPACE == "urn:peppol:schema:taxdata:1.0"


def test_reported_transaction_with_reported_document() -> None:
    reported_doc = TDDReportedDocument(
        customization_id="urn:peppol:pint:billing-1@ae-1",
        profile_id="urn:peppol:bis:billing",
        document_id="inv1",
        issue_date=date(2025, 4, 13),
        issue_time=time(12, 34, 56),
        document_type_code="380",
        currency_code="AED",
        supplier_trn="123456789",
        customer_trn="9876543210000",
    )
    transaction = TDDReportedTransaction(
        transport_header_id="cf510157-2967-460b-806a-a6e63b052164",
        reported_document=reported_doc,
    )
    tdd = AETaxDataDocument(
        issue_date=date(2025, 4, 14),
        issue_time=time(12, 0, 0),
        reporter_role="01",
        reporting_party=TDDParty(endpoint_id="dummy-sender"),
        receiving_party=TDDParty(endpoint_id="dummy-receiver", endpoint_scheme="0242"),
        reported_transactions=[transaction],
    )
    assert len(tdd.reported_transactions) == 1
    assert tdd.reported_transactions[0].reported_document.document_type_code == "380"
