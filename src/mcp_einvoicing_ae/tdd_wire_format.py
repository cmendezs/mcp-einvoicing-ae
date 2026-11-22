"""Peppol AE Tax Data Document (TDD) XML serializer.

Turns an :class:`~mcp_einvoicing_ae.models.tdd.AETaxDataDocument` into a
``pxs:TaxData`` document (namespace ``urn:peppol:schema:taxdata:1.0``).

Element order follows ``TaxDataType`` / ``ReportedTransactionType`` /
``ReportedDocumentType`` in ``peppol-tdd-1.0.0.xsd``. Before emitting, the
serializer enforces the cardinality and content rules of the TDD Schematron
(ibr-tdd-*) that the Pydantic model leaves optional, so a document that would
fail them is rejected with an explicit list instead of being emitted. The XSD
and the Schematron are not executed at runtime: they are OpenPeppol artefacts
kept under ``specs/`` for tests only (see ``validate_tdd_ae``).

core-state-check: [NO-CORE-MATCH: the TDD is a distinct Peppol document type;
core's EN16931UBLSerializer covers Invoice/CreditNote only]
"""

from __future__ import annotations

from datetime import time
from decimal import Decimal

from lxml import etree
from mcp_einvoicing_core import DocumentGenerationError

from mcp_einvoicing_ae.models.tdd import (
    TDD_NAMESPACE,
    AETaxDataDocument,
    TDDParty,
    TDDReportedDocument,
    TDDReportedTransaction,
)

_CBC = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
_CAC = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
_CEC = "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"
_NSMAP = {"pxs": TDD_NAMESPACE, "cbc": _CBC, "cac": _CAC, "cec": _CEC}


def _q(ns: str, local: str) -> str:
    return f"{{{ns}}}{local}"


def _add(parent: etree._Element, ns: str, local: str, text: str | None = None) -> etree._Element:
    el = etree.SubElement(parent, _q(ns, local))
    if text is not None:
        el.text = text
    return el


def _format_time(value: time, *, require_tz: bool) -> str:
    """Format as ``HH:MM:SS[.ffffff]`` with ``Z`` or a numeric offset when tz-aware."""
    if value.tzinfo is None:
        if require_tz:
            raise DocumentGenerationError(
                "ibr-tdd-05: the Tax Data Document issue_time must carry a timezone "
                "(use e.g. datetime.time(12, 0, tzinfo=datetime.timezone.utc))"
            )
        return value.isoformat()
    offset = value.utcoffset()
    base = value.replace(tzinfo=None).isoformat()
    if offset is None or offset.total_seconds() == 0:
        return f"{base}Z"
    total = int(offset.total_seconds() // 60)
    sign = "+" if total >= 0 else "-"
    return f"{base}{sign}{abs(total) // 60:02d}:{abs(total) % 60:02d}"


def _amount(value: Decimal) -> str:
    return format(value, "f")


def _reported_document_problems(doc: TDDReportedDocument) -> list[str]:
    checks = {
        "document_id (ibr-tdd-26)": doc.document_id,
        "uuid (ibr-tdd-27)": doc.uuid,
        "currency_code (ibr-tdd-30)": doc.currency_code,
        "supplier_trn (ibr-tdd-44)": doc.supplier_trn,
        "customer_trn": doc.customer_trn,
        "tax_amount (ibr-tdd-35)": doc.tax_amount,
        "tax_exclusive_amount (ibr-tdd-52)": doc.tax_exclusive_amount,
    }
    return [f"reported_document.{name} is required" for name, v in checks.items() if v is None]


def _problems(tdd: AETaxDataDocument) -> list[str]:
    out: list[str] = []
    if len(tdd.reported_transactions) != 1:
        out.append(
            "ibr-tdd-09: exactly one reported transaction is required, "
            f"got {len(tdd.reported_transactions)}"
        )
    for i, tx in enumerate(tdd.reported_transactions):
        if tx.reported_document is None:
            out.append(f"reported_transactions[{i}]: reported_document is required (ibr-tdd-22)")
        else:
            out += [
                f"reported_transactions[{i}].{m}"
                for m in _reported_document_problems(tx.reported_document)
            ]
        if not tx.source_document_xml:
            out.append(f"reported_transactions[{i}]: source_document_xml is required (ibr-tdd-23)")
    return out


def _party(parent: etree._Element, local: str, party: TDDParty) -> None:
    node = _add(parent, TDD_NAMESPACE, local)
    ep = _add(node, _CBC, "EndpointID", party.endpoint_id)
    ep.set("schemeID", party.endpoint_scheme)


def _tax_party(parent: etree._Element, local: str, trn: str, scheme: str) -> None:
    holder = _add(parent, _CAC, local)
    party = _add(holder, _CAC, "Party")
    pts = _add(party, _CAC, "PartyTaxScheme")
    _add(pts, _CBC, "CompanyID", trn)
    ts = _add(pts, _CAC, "TaxScheme")
    _add(ts, _CBC, "ID", scheme)


def _reported_document(parent: etree._Element, doc: TDDReportedDocument) -> None:
    node = _add(parent, TDD_NAMESPACE, "ReportedDocument")
    _add(node, _CBC, "CustomizationID", doc.customization_id)
    _add(node, _CBC, "ProfileID", doc.profile_id)
    _add(node, _CBC, "ID", doc.document_id)
    _add(node, _CBC, "UUID", doc.uuid)
    _add(node, _CBC, "IssueDate", doc.issue_date.isoformat())
    _add(node, _CBC, "IssueTime", _format_time(doc.issue_time, require_tz=False))
    _add(node, TDD_NAMESPACE, "DocumentTypeCode", doc.document_type_code)
    _add(node, _CBC, "DocumentCurrencyCode", doc.currency_code)
    assert doc.supplier_trn is not None and doc.customer_trn is not None  # noqa: S101
    assert doc.tax_amount is not None and doc.tax_exclusive_amount is not None  # noqa: S101
    _tax_party(node, "AccountingSupplierParty", doc.supplier_trn, doc.supplier_tax_scheme)
    _tax_party(node, "AccountingCustomerParty", doc.customer_trn, doc.customer_tax_scheme)
    tt = _add(node, _CAC, "TaxTotal")
    _add(tt, _CBC, "TaxAmount", _amount(doc.tax_amount)).set("currencyID", doc.currency_code or "")
    mt = _add(node, TDD_NAMESPACE, "MonetaryTotal")
    _add(mt, _CBC, "TaxExclusiveAmount", _amount(doc.tax_exclusive_amount)).set(
        "currencyID", doc.currency_code or ""
    )


def _transaction(parent: etree._Element, tx: TDDReportedTransaction) -> None:
    node = _add(parent, TDD_NAMESPACE, "ReportedTransaction")
    if tx.transport_header_id:
        _add(node, TDD_NAMESPACE, "TransportHeaderID", tx.transport_header_id)
    if tx.reported_document is not None:
        _reported_document(node, tx.reported_document)
    if tx.source_document_xml:
        try:
            source = etree.fromstring(
                tx.source_document_xml.encode("utf-8"),
                parser=etree.XMLParser(resolve_entities=False, no_network=True),
            )
        except etree.XMLSyntaxError as exc:
            raise DocumentGenerationError(
                f"source_document_xml is not well-formed XML: {exc}"
            ) from exc
        sd = _add(node, TDD_NAMESPACE, "SourceDocument")
        _add(sd, _CEC, "ExtensionContent").append(source)


class AETDDSerializer:
    """Serialize :class:`AETaxDataDocument` to a ``pxs:TaxData`` XML document."""

    def serialize(self, tdd: AETaxDataDocument) -> bytes:
        """Return UTF-8 XML bytes, or raise ``DocumentGenerationError`` listing every problem."""
        problems = _problems(tdd)
        if problems:
            raise DocumentGenerationError("TDD is incomplete: " + "; ".join(problems))
        root = etree.Element(_q(TDD_NAMESPACE, "TaxData"), nsmap=_NSMAP)
        _add(root, _CBC, "CustomizationID", tdd.customization_id)
        _add(root, _CBC, "ProfileID", tdd.profile_id)
        _add(root, _CBC, "IssueDate", tdd.issue_date.isoformat())
        _add(root, _CBC, "IssueTime", _format_time(tdd.issue_time, require_tz=True))
        _add(root, TDD_NAMESPACE, "DocumentTypeCode", tdd.document_type_code)
        _add(root, TDD_NAMESPACE, "DocumentScope", tdd.document_scope)
        _add(root, TDD_NAMESPACE, "ReporterRole", tdd.reporter_role)
        _party(root, "ReportingParty", tdd.reporting_party)
        _party(root, "ReceivingParty", tdd.receiving_party)
        rep = _add(root, TDD_NAMESPACE, "ReportersRepresentative")
        pid = _add(rep, _CAC, "PartyIdentification")
        _add(pid, _CBC, "ID", tdd.reporters_representative_id).set(
            "schemeID", tdd.reporters_representative_scheme
        )
        for tx in tdd.reported_transactions:
            _transaction(root, tx)
        return etree.tostring(root, xml_declaration=True, encoding="UTF-8", pretty_print=True)
