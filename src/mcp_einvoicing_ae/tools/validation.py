"""UAE PINT AE invoice + Peppol AE TDD validation — subclasses BaseDocumentValidator.

Two independent validation surfaces, since the TDD is a distinct document
type from a PINT AE invoice (see models/tdd.py):

- ``validate_invoice_ae``: runs core's shared, licensing-clean CEN EN16931
  base Schematron (``en16931_base_schematron_validator()`` — the same
  artifact ``mcp-einvoicing-be`` v0.8.0 / ``mcp-ksef-pl`` v0.6.0 consume)
  against a PINT AE billing/self-billing UBL 2.1 document. v0.1.0 ran two
  self-compiled OpenPeppol-derived stylesheets here instead
  (``pint_ubl_billing``/``pint_ubl_selfbilling`` plus ``pint_jurisdiction_ae``)
  with no confirmed redistribution rights — removed in v0.2.0. See
  ``validators/schematron.py`` module docstring for the full licensing
  history and why the PINT-AE jurisdiction (``ibr-*-ae``) rules have no
  substitute. Every result carries ``EN16931_BASE_ONLY_SCOPE_WARNING`` and
  ``EN16931_BASE_KNOWN_LIMITATIONS_WARNING``.
- ``validate_tdd_ae``: v0.1.0 ran the ``peppol_ae_tdd`` Schematron here.
  Removed in v0.2.0 for the same licensing reason, and unlike the invoice
  path, core provides no substitute artifact for TDD (a distinct Peppol
  document type, not an EN16931 UBL invoice) — this now always returns an
  explicit ``engine="unavailable"`` result.

Requires the ``xslt2`` optional extra (``saxonche``) for
``validate_invoice_ae`` — core's bundled EN16931 base Schematron is XSLT.
Without it, ``validate_invoice_ae`` returns an explicit "unavailable" result
(``valid=False``, an error naming the missing extra) rather than a silent
pass, matching ``mcp-einvoicing-be``'s pattern.
"""

from __future__ import annotations

import logging
from typing import Annotated, cast

from mcp_einvoicing_core import BaseDocumentValidator, DocumentValidationResult
from mcp_einvoicing_core.schematron import BaseStructuredValidator

from mcp_einvoicing_ae.models.invoice import AEProfileVariant
from mcp_einvoicing_ae.validators.schematron import en16931_base_validator

_log = logging.getLogger(__name__)

_XSLT2_UNAVAILABLE = (
    "AE-VALIDATION-UNAVAILABLE: core's bundled EN16931 base Schematron "
    "validator could not be loaded in this environment. Install "
    "mcp-einvoicing-ae[xslt2] (saxonche) to enable validation."
)

_TDD_VALIDATION_UNAVAILABLE = (
    "TDD-VALIDATION-UNAVAILABLE: v0.1.0's peppol_ae_tdd Schematron and "
    "peppol-tdd-1.0.0.xsd were removed in v0.2.0 — self-compiled OpenPeppol-"
    "derived content with no confirmed redistribution rights (see "
    "validators/schematron.py and "
    "context-library/decisions/peppol-schematron-artifact.md in the root "
    "monorepo). Core provides no substitute TDD validation artifact. No "
    "Peppol AE Tax Data Document validation is currently available."
)

# Added to every validate_invoice_ae result: the CEN EN16931 base Schematron
# checks structural + arithmetic/totals rules only, not the PINT-AE
# jurisdiction overlay (ibr-*-ae rules, removed in v0.2.0 — see
# validators/schematron.py).
EN16931_BASE_ONLY_SCOPE_WARNING = (
    "EN16931-BASE-ONLY-SCOPE: this validates the CEN EN16931 base rules "
    "(structural + arithmetic/totals) only. PINT-AE jurisdiction-specific "
    "rules (ibr-*-ae) are NOT checked — this is not a full PINT AE "
    "conformance result. See "
    "context-library/decisions/peppol-schematron-artifact.md."
)

# Added to every validate_invoice_ae result: BR-CO-09 is expected to fire on
# every genuine AE invoice (UAE TRNs carry no ISO 3166-1 alpha-2 prefix) —
# see validators/schematron.py module docstring for the confirmed evidence.
EN16931_BASE_KNOWN_LIMITATIONS_WARNING = (
    "EN16931-BASE-KNOWN-LIMITATION: BR-CO-09 (VAT identifier must carry an "
    "ISO 3166-1 alpha-2 country prefix) is expected to fire on every "
    "genuine AE invoice — UAE Tax Registration Numbers are bare numerics "
    "with no country prefix, an EU-rule-vs-non-EU-identifier mismatch, not "
    "a defect in the invoice data. See validators/schematron.py."
)


def _load_base_validator() -> tuple[BaseStructuredValidator | None, str | None]:
    try:
        return en16931_base_validator(), None
    except ImportError as exc:
        _log.warning("Core's EN16931 base Schematron requires saxonche: %s", exc)
        return None, str(exc)


class AEDocumentValidator(BaseDocumentValidator):
    """UAE document validator: PINT AE invoices and Peppol AE TDD documents."""

    def __init__(self) -> None:
        self._base_schematron, self._base_schematron_error = _load_base_validator()

    def get_schema_version(self) -> str:
        return "PINT AE v1.0.4 (EN16931 base only) / Peppol AE TDD (unavailable)"

    def validate(self, document_content: str | bytes) -> DocumentValidationResult:
        xml_bytes = (
            document_content.encode("utf-8")
            if isinstance(document_content, str)
            else document_content
        )
        return self._validate_invoice(xml_bytes, variant="billing")

    def _validate_invoice(self, xml_bytes: bytes, variant: str) -> DocumentValidationResult:
        if self._base_schematron is None:
            return DocumentValidationResult(
                valid=False,
                errors=[_XSLT2_UNAVAILABLE],
                warnings=[],
                metadata={"variant": variant, "engine": "unavailable"},
            )

        result = self._base_schematron.validate(xml_bytes)
        return DocumentValidationResult(
            valid=result.is_valid,
            errors=[f"{m.rule_id}: {m.text}" for m in result.errors],
            warnings=[
                EN16931_BASE_ONLY_SCOPE_WARNING,
                EN16931_BASE_KNOWN_LIMITATIONS_WARNING,
                *(f"{m.rule_id}: {m.text}" for m in result.warnings),
            ],
            metadata={
                "variant": variant,
                "engine": "schematron-xslt",
                "scope": "en16931-base-only",
                "rulesets_run": ["en16931_base"],
            },
        )

    def _validate_tdd(self, xml_bytes: bytes) -> DocumentValidationResult:  # noqa: ARG002
        return DocumentValidationResult(
            valid=False,
            errors=[_TDD_VALIDATION_UNAVAILABLE],
            warnings=[],
            metadata={"engine": "unavailable"},
        )

    async def validate_invoice_ae(
        self,
        xml: Annotated[str, "Raw PINT AE UBL 2.1 XML invoice content"],
        variant: Annotated[
            AEProfileVariant,
            "PINT AE profile variant: 'billing' (default) or 'selfbilling'",
        ] = "billing",
    ) -> dict[str, object]:
        """Validate a PINT AE UBL 2.1 invoice against the CEN EN16931 base Schematron.

        Checks the CEN EN16931 base rules (structural + arithmetic/totals,
        ~50 BR-* rules) via core's bundled, licensing-clean Schematron. Does
        NOT check the PINT-AE jurisdiction overlay (ibr-*-ae rules) — the
        result's metadata.scope is "en16931-base-only", and
        EN16931_BASE_ONLY_SCOPE_WARNING is always included. BR-CO-09 is
        expected to fire on every genuine AE invoice (see
        EN16931_BASE_KNOWN_LIMITATIONS_WARNING, always included) since UAE
        TRNs carry no ISO country prefix. This is not a full PINT AE
        conformance check; a document that passes may still be rejected by a
        real Peppol Access Point. See
        context-library/decisions/peppol-schematron-artifact.md for why.
        Returns a structured result with per-rule error and warning messages.
        The ``variant`` parameter is accepted for interface stability with
        v0.1.0 but does not change which rules run — the CEN base rules are
        identical for both billing and self-billing profiles.
        """
        xml_bytes = xml.encode("utf-8") if isinstance(xml, str) else xml
        result = self._validate_invoice(xml_bytes, variant)
        return cast(dict[str, object], result.to_dict())

    async def validate_tdd_ae(
        self,
        xml: Annotated[str, "Raw Peppol AE Tax Data Document (TDD) XML content"],
    ) -> dict[str, object]:
        """Validate a Peppol AE Tax Data Document (TDD).

        Always returns an explicit "unavailable" result — see module
        docstring and _TDD_VALIDATION_UNAVAILABLE for why no TDD validation
        is currently available.
        """
        xml_bytes = xml.encode("utf-8") if isinstance(xml, str) else xml
        result = self._validate_tdd(xml_bytes)
        return cast(dict[str, object], result.to_dict())
