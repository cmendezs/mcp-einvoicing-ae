"""Schematron validation support for mcp-einvoicing-ae.

v0.1.0 bundled four self-compiled OpenPeppol-derived stylesheets under
``mcp_einvoicing_ae/rules/`` (``pint-ubl-billing.xslt``,
``pint-ubl-selfbilling.xslt``, ``pint-jurisdiction-ae.xslt``,
``peppol-ae-tdd.xslt``, plus ``peppol-tdd-1.0.0.xsd`` for XSD-level TDD
checks). None of the underlying ``.sch``/``.xsd`` sources under ``specs/``
carry a redistribution grant — same finding
``context-library/decisions/peppol-schematron-artifact.md`` already made for
``mcp-einvoicing-be``/``mcp-ksef-pl``'s Peppol BIS 3.0 overlay and
``mcp-invoicenow-sg``'s PINT-SG overlay. v0.1.0's own module docstring argued
this was "moot" here because the files were supplied directly by the user
rather than fetched from the web — that reasoning was wrong: being
user-supplied only means Claude did not autonomously retrieve copyrighted
material (a separate, process-level concern), it says nothing about whether
this project holds redistribution rights to bundle the content into a
published PyPI wheel. All five files are removed in v0.2.0.

What replaces PINT AE structural/jurisdiction validation:
``mcp_einvoicing_core.schematron_artifacts.en16931_base_schematron_validator()``
(core >=1.18.0) — the same licensing-clean, EUPL 1.2-sourced CEN EN16931 base
Schematron (``BR-*`` rules only) that ``mcp-einvoicing-be`` v0.8.0 and
``mcp-ksef-pl`` v0.6.0 already consume. Unlike ``mcp-invoicenow-sg`` (blocked
by an unsourced GST-category-to-UNCL5305 crosswalk), AE has no equivalent
blocker: ``AEInvoice`` uses the ``Aligned-TaxCategoryCodes.gc`` codelist,
which the "Aligned" name itself signals as UNCL5305-derived (confirmed by
example values ``S``/``AE``/``E``/``O``/``Z`` — see
``context-library/countries/ae.md``), and AE's serializer is core's own
``EN16931UBLSerializer`` unmodified, which already emits ``TaxScheme/ID``
as the literal ``"VAT"`` (verified in
``mcp-einvoicing-core/src/mcp_einvoicing_core/wire_formats.py``) — no GST/VAT
rewrite step like SG's ``_gst_to_vat_for_base_validation`` is needed.

Known, permanent scope limitation (not a data bug): ``BR-CO-09`` ("the Seller
VAT identifier... shall have a prefix in accordance with ISO code ISO
3166-1 alpha-2") fires on every genuine AE invoice, because UAE Tax
Registration Numbers (see ``TaxIdentifier.validate_ae_trn()``) are bare
15-digit numerics with no country-code prefix — confirmed directly against
the government-supplied
``specs/pint-ae/trn-invoice/example/Standard tax invoice.xml`` fixture,
whose ``PartyTaxScheme/CompanyID`` values (``198765432102003``,
``134567890123003``) carry no ISO prefix. This is a structural mismatch
between an EU-designed rule and a non-EU jurisdiction, not something a
validation-only data transform can correct (unlike SG's TaxScheme/ID
mismatch, which was a literal renaming and a genuine mapping between clean
equivalents). ``EN16931_BASE_KNOWN_LIMITATIONS_WARNING`` in
``tools/validation.py`` discloses this on every result rather than silently
filtering the finding out of ``errors``.

What is NOT replaced: the PINT-AE jurisdiction overlay (the ``ibr-*-ae``
rules removed with ``pint-jurisdiction-ae.xslt``) and Peppol AE TDD
validation (``peppol-ae-tdd.xslt`` / ``peppol-tdd-1.0.0.xsd``) have no
licensing-clean substitute anywhere in core or elsewhere in this monorepo —
core provides no TDD capability at all (grepped
``context-library/core-state.md``, no match). ``validate_tdd_ae`` in
``tools/validation.py`` now always returns an explicit
``engine="unavailable"`` result rather than silently omitting the check.
Both gaps stay blocked on the same external OpenPeppol licensing question as
``[CORE-PEPPOL-SCHEMATRON-1]`` in ``context-library/roadmap-2026.md``.
"""

from __future__ import annotations

from mcp_einvoicing_core.schematron import BaseStructuredValidator
from mcp_einvoicing_core.schematron_artifacts import en16931_base_schematron_validator

__all__ = ["en16931_base_validator"]


def en16931_base_validator() -> BaseStructuredValidator:
    """Return core's bundled, licensing-clean CEN EN16931 base Schematron validator.

    Raises:
        ImportError: If the optional ``saxonche`` extra (XSLT 3.0 engine) is
            not installed.
    """
    return en16931_base_schematron_validator()
