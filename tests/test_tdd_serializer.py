"""Tests for the Peppol AE TDD serializer (AE-LC-1).

Schema checks use the OpenPeppol XSD and Schematron kept under ``specs/``. Those files are
reference material only (not bundled in the wheel), so these tests skip when ``specs/`` is
absent. Field values mirror specs/tdd/trn-tdd/example/simple.xml.
"""

from __future__ import annotations

import json
from datetime import UTC, date, time
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
from lxml import etree
from mcp_einvoicing_core import DocumentGenerationError
from mcp_einvoicing_core.schematron import XSDValidator

from mcp_einvoicing_ae.models.tdd import (
    AETaxDataDocument,
    TDDParty,
    TDDReportedDocument,
    TDDReportedTransaction,
)
from mcp_einvoicing_ae.tdd_wire_format import AETDDSerializer
from mcp_einvoicing_ae.tools.generation import AEDocumentGenerator

_SPECS = Path(__file__).resolve().parents[1] / "specs"
_TDD_XSD = _SPECS / "tdd" / "common" / "peppol-tdd-1.0.0.xsd"
_UBL_DIR = _SPECS / "shared" / "ubl-2.1" / "common"
_OASIS = "https://docs.oasis-open.org/ubl/os-UBL-2.1/xsdrt/common/"
_SOURCE_INVOICE = (
    '<ubl:Invoice xmlns:ubl="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"/>'
)

needs_specs = pytest.mark.skipif(
    not (_TDD_XSD.exists() and _UBL_DIR.exists()), reason="specs/ reference files not present"
)


def _tdd(**overrides: Any) -> AETaxDataDocument:
    document = TDDReportedDocument(
        customization_id="urn:peppol:pint:billing-1@ae-1",
        profile_id="urn:peppol:bis:billing",
        document_id="inv1",
        uuid="eca87285-6b30-4691-b4b7-f97da43c1760",
        issue_date=date(2025, 4, 13),
        issue_time=time(12, 34, 56),
        document_type_code="380",
        currency_code="AED",
        supplier_trn="123456789",
        customer_trn="9876543210000",
        tax_amount=Decimal("2.30"),
        tax_exclusive_amount=Decimal("282.90"),
    )
    data: dict[str, Any] = {
        "issue_date": date(2025, 4, 14),
        "issue_time": time(12, 0, 0, tzinfo=UTC),
        "reporter_role": "01",
        "reporting_party": TDDParty(endpoint_id="dummy-sender", endpoint_scheme="0235"),
        "receiving_party": TDDParty(endpoint_id="dummy-receiver", endpoint_scheme="0242"),
        "reporters_representative_id": "dummy-representative",
        "reported_transactions": [
            TDDReportedTransaction(
                transport_header_id="cf510157-2967-460b-806a-a6e63b052164",
                reported_document=document,
                source_document_xml=_SOURCE_INVOICE,
            )
        ],
    }
    data.update(overrides)
    return AETaxDataDocument(**data)


def _xsd_errors(xml: bytes) -> list[str]:
    known = {_OASIS + p.name: str(p) for p in _UBL_DIR.glob("*.xsd")}
    validator = XSDValidator(str(_TDD_XSD), known_imports=known)
    result = validator.validate(xml)
    return [] if result.is_valid else [e.text for e in result.errors]


@needs_specs
def test_generated_tdd_is_xsd_valid() -> None:
    xml = AETDDSerializer().serialize(_tdd())
    assert _xsd_errors(xml) == []


def test_element_order_and_namespace() -> None:
    root = etree.fromstring(AETDDSerializer().serialize(_tdd()))
    assert root.tag == "{urn:peppol:schema:taxdata:1.0}TaxData"
    names = [etree.QName(c).localname for c in root]
    assert names == [
        "CustomizationID",
        "ProfileID",
        "IssueDate",
        "IssueTime",
        "DocumentTypeCode",
        "DocumentScope",
        "ReporterRole",
        "ReportingParty",
        "ReceivingParty",
        "ReportersRepresentative",
        "ReportedTransaction",
    ]


def test_issue_time_carries_z_for_utc() -> None:
    root = etree.fromstring(AETDDSerializer().serialize(_tdd()))
    ns = {"cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"}
    assert root.findtext("cbc:IssueTime", namespaces=ns) == "12:00:00Z"


def test_naive_issue_time_is_rejected() -> None:
    with pytest.raises(DocumentGenerationError, match="ibr-tdd-05"):
        AETDDSerializer().serialize(_tdd(issue_time=time(12, 0, 0)))


def test_representative_is_mandatory() -> None:
    with pytest.raises(ValueError, match="reporters_representative_id"):
        _tdd(reporters_representative_id=None)


def test_receiver_scheme_must_be_spis() -> None:
    with pytest.raises(ValueError, match="ibr-tdd-17"):
        _tdd(receiving_party=TDDParty(endpoint_id="x", endpoint_scheme="0235"))


def test_exactly_one_transaction_required() -> None:
    with pytest.raises(DocumentGenerationError, match="ibr-tdd-09"):
        AETDDSerializer().serialize(_tdd(reported_transactions=[]))


def test_missing_source_document_listed() -> None:
    tx = _tdd().reported_transactions[0].model_copy(update={"source_document_xml": None})
    with pytest.raises(DocumentGenerationError, match="ibr-tdd-23"):
        AETDDSerializer().serialize(_tdd(reported_transactions=[tx]))


def test_missing_amounts_listed() -> None:
    doc = _tdd().reported_transactions[0].reported_document
    assert doc is not None
    tx = TDDReportedTransaction(
        reported_document=doc.model_copy(update={"tax_amount": None, "uuid": None}),
        source_document_xml=_SOURCE_INVOICE,
    )
    with pytest.raises(DocumentGenerationError) as exc:
        AETDDSerializer().serialize(_tdd(reported_transactions=[tx]))
    assert "tax_amount" in str(exc.value) and "uuid" in str(exc.value)


def test_malformed_source_document_rejected() -> None:
    tx = _tdd().reported_transactions[0].model_copy(update={"source_document_xml": "<a>"})
    with pytest.raises(DocumentGenerationError, match="well-formed"):
        AETDDSerializer().serialize(_tdd(reported_transactions=[tx]))


@pytest.mark.asyncio
async def test_generate_tdd_ae_tool_round_trip() -> None:
    payload = json.loads(_tdd().model_dump_json())
    result = await AEDocumentGenerator().generate_tdd_ae(payload)
    assert result["customization_id"] == "urn:peppol:taxdata:ae-1"
    assert result["profile_id"] == "urn:peppol:taxreporting"
    assert "<pxs:TaxData" in str(result["xml"])


@needs_specs
def test_generated_tdd_passes_tdd_schematron() -> None:
    saxonche = pytest.importorskip("saxonche")
    xslt = _SPECS / "tdd" / "trn-tdd" / "schematron" / "peppol-ae-tdd.xslt"
    xml = AETDDSerializer().serialize(_tdd())
    with saxonche.PySaxonProcessor(license=False) as proc:
        compiled = proc.new_xslt30_processor().compile_stylesheet(stylesheet_file=str(xslt))
        out = compiled.transform_to_string(xdm_node=proc.parse_xml(xml_text=xml.decode()))
    failed = [
        a.get("id")
        for a in etree.fromstring(out.encode()).iter(
            "{http://purl.oclc.org/dsdl/svrl}failed-assert"
        )
        if a.get("flag") == "fatal"
    ]
    assert failed == []
