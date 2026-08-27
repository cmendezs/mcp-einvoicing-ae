"""UAE PINT AE invoice + Peppol AE TDD validation — subclasses BaseDocumentValidator.

Two independent validation surfaces, since the TDD is a distinct document
type from a PINT AE invoice (see models/tdd.py):

- ``validate_invoice_ae``: runs two bundled Schematron rule sets against a
  PINT AE billing/self-billing UBL 2.1 document — the profile's UBL
  structural rules (``pint_ubl_billing``/``pint_ubl_selfbilling``) and the
  ``ibr-*-ae`` jurisdiction rules (``pint_jurisdiction_ae``, shared by both
  variants — confirmed byte-identical, see validators/schematron.py). Results
  from both rule sets are combined into one response.
- ``validate_tdd_ae``: runs the ``peppol_ae_tdd`` Schematron only.
  Schema-level (XSD) validation is not available — ``peppol-tdd-1.0.0.xsd``
  imports the base OASIS ``UnqualifiedDataTypes-2`` schema, which was not
  supplied (see validators/schematron.py's ``tdd_xsd_validator`` docstring and
  context-library/countries/ae.md). Every TDD result carries an explicit
  warning naming this gap rather than silently omitting the check.

Requires the ``xslt2`` optional extra (``saxonche``) — all four bundled
stylesheets are XSLT 2.0. Without it, every validate call returns an explicit
"unavailable" result (``valid=False``, an error naming the missing extra)
rather than a silent pass, matching mcp-einvoicing-be's pattern.
"""

from __future__ import annotations

import logging
from typing import Annotated, cast

from mcp_einvoicing_core import BaseDocumentValidator, DocumentValidationResult
from mcp_einvoicing_core.schematron import BaseStructuredValidator

from mcp_einvoicing_ae.models.invoice import AEProfileVariant
from mcp_einvoicing_ae.validators.schematron import SchematronValidator, StylesheetKey

_log = logging.getLogger(__name__)

_XSLT2_UNAVAILABLE = (
    "AE-VALIDATION-UNAVAILABLE: no Schematron validator could be loaded in "
    "this environment. Install mcp-einvoicing-ae[xslt2] (saxonche) to enable "
    "validation."
)

_TDD_XSD_NOT_RUN_WARNING = (
    "TDD-XSD-NOT-RUN: schema-level (XSD) validation was not performed — "
    "peppol-tdd-1.0.0.xsd imports the base OASIS UnqualifiedDataTypes-2 "
    "schema, which has not been supplied under specs/. Only Schematron-level "
    "validation ran. See "
    "mcp_einvoicing_ae.validators.schematron.tdd_xsd_validator."
)

_UBL_STYLESHEET_BY_VARIANT: dict[str, StylesheetKey] = {
    "billing": "pint_ubl_billing",
    "selfbilling": "pint_ubl_selfbilling",
}


def _load(stylesheet_key: StylesheetKey) -> tuple[BaseStructuredValidator | None, str | None]:
    """Load a bundled Schematron validator, returning (validator, error_message)."""
    try:
        return SchematronValidator(stylesheet_key), None
    except ImportError as exc:
        _log.warning("Schematron stylesheet %s requires saxonche: %s", stylesheet_key, exc)
        return None, str(exc)
    except (ValueError, FileNotFoundError) as exc:
        _log.warning("Failed to load Schematron stylesheet %s: %s", stylesheet_key, exc)
        return None, str(exc)


class AEDocumentValidator(BaseDocumentValidator):
    """UAE document validator: PINT AE invoices and Peppol AE TDD documents."""

    def get_schema_version(self) -> str:
        return "PINT AE v1.0.4 / Peppol AE TDD v1.0.3"

    def validate(self, document_content: str | bytes) -> DocumentValidationResult:
        xml_bytes = (
            document_content.encode("utf-8")
            if isinstance(document_content, str)
            else document_content
        )
        return self._validate_invoice(xml_bytes, variant="billing")

    def _validate_invoice(self, xml_bytes: bytes, variant: str) -> DocumentValidationResult:
        ubl_key = _UBL_STYLESHEET_BY_VARIANT[variant]
        ubl_validator, ubl_error = _load(ubl_key)
        jurisdiction_validator, jurisdiction_error = _load("pint_jurisdiction_ae")

        if ubl_validator is None and jurisdiction_validator is None:
            return DocumentValidationResult(
                valid=False,
                errors=[_XSLT2_UNAVAILABLE],
                warnings=[],
                metadata={"variant": variant, "engine": "unavailable"},
            )

        errors: list[str] = []
        warnings: list[str] = []
        rulesets_run: list[str] = []

        if ubl_validator is not None:
            result = ubl_validator.validate(xml_bytes)
            errors.extend(f"{m.rule_id}: {m.text}" for m in result.errors)
            warnings.extend(f"{m.rule_id}: {m.text}" for m in result.warnings)
            rulesets_run.append(ubl_key)
        else:
            warnings.append(f"UBL-RULES-NOT-RUN: {ubl_error}")

        if jurisdiction_validator is not None:
            result = jurisdiction_validator.validate(xml_bytes)
            errors.extend(f"{m.rule_id}: {m.text}" for m in result.errors)
            warnings.extend(f"{m.rule_id}: {m.text}" for m in result.warnings)
            rulesets_run.append("pint_jurisdiction_ae")
        else:
            warnings.append(f"JURISDICTION-RULES-NOT-RUN: {jurisdiction_error}")

        return DocumentValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata={"variant": variant, "engine": "schematron-xslt", "rulesets": rulesets_run},
        )

    def _validate_tdd(self, xml_bytes: bytes) -> DocumentValidationResult:
        tdd_validator, tdd_error = _load("peppol_ae_tdd")
        if tdd_validator is None:
            return DocumentValidationResult(
                valid=False,
                errors=[
                    _XSLT2_UNAVAILABLE
                    if tdd_error and "saxonche" in tdd_error
                    else f"TDD-SCHEMATRON-LOAD-FAILED: {tdd_error}"
                ],
                warnings=[],
                metadata={"engine": "unavailable"},
            )

        result = tdd_validator.validate(xml_bytes)
        return DocumentValidationResult(
            valid=result.is_valid,
            errors=[f"{m.rule_id}: {m.text}" for m in result.errors],
            warnings=[
                _TDD_XSD_NOT_RUN_WARNING,
                *(f"{m.rule_id}: {m.text}" for m in result.warnings),
            ],
            metadata={"engine": "schematron-xslt", "scope": "schematron-only"},
        )

    async def validate_invoice_ae(
        self,
        xml: Annotated[str, "Raw PINT AE UBL 2.1 XML invoice content"],
        variant: Annotated[
            AEProfileVariant,
            "PINT AE profile variant: 'billing' (default) or 'selfbilling'",
        ] = "billing",
    ) -> dict[str, object]:
        """Validate a PINT AE UBL 2.1 invoice against bundled Schematron rules.

        Runs the profile's UBL structural rules
        (pint_ubl_billing/pint_ubl_selfbilling) plus the ibr-*-ae jurisdiction
        rules (pint_jurisdiction_ae, shared by both variants). Returns a
        combined result with per-rule error/warning messages and the list of
        rule sets actually run in ``rulesets``.
        """
        xml_bytes = xml.encode("utf-8") if isinstance(xml, str) else xml
        result = self._validate_invoice(xml_bytes, variant)
        return cast(dict[str, object], result.to_dict())

    async def validate_tdd_ae(
        self,
        xml: Annotated[str, "Raw Peppol AE Tax Data Document (TDD) XML content"],
    ) -> dict[str, object]:
        """Validate a Peppol AE Tax Data Document (TDD) against its Schematron rules.

        Schematron-level only — schema (XSD) validation is unavailable (see
        module docstring); every result carries an explicit warning naming
        that limitation rather than silently skipping it.
        """
        xml_bytes = xml.encode("utf-8") if isinstance(xml, str) else xml
        result = self._validate_tdd(xml_bytes)
        return cast(dict[str, object], result.to_dict())
