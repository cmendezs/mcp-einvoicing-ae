"""PINT AE / Peppol AE TDD Schematron validator for mcp-einvoicing-ae.

Extends mcp_einvoicing_core.SchematronValidator with a stylesheet key map for
the UAE rule sets. All XSLT files are bundled inside the package under
``mcp_einvoicing_ae/rules/`` (copied from the user-supplied ``specs/`` at
2026-08-27; the licensing blocker on OpenPeppol Schematron redistribution
(CORE-PEPPOL-SCHEMATRON-1) does not apply here since these files were
supplied directly, not fetched — see context-library/decisions and
context-library/countries/ae.md "Known gaps and open items").

Bundled rule sources (from mcp-einvoicing-ae/specs/, retrieved 2026-08-26):
- PINT AE billing / self-billing: same compiled UBL/PINT structural rules for
  both Invoice and CreditNote document types within a profile (confirmed
  byte-identical between trn-invoice/ and trn-creditnote/ on 2026-08-27), so
  only one stylesheet per profile is bundled.
- The `ibr-*-ae` jurisdiction-aligned rules are identical between the billing
  and self-billing profiles (confirmed byte-identical on 2026-08-27) — a
  single bundled stylesheet covers both.
- Peppol AE TDD: its own single Schematron, distinct namespace/document.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from mcp_einvoicing_core.schematron import (
    BaseStructuredValidator,
    SaxonSchematronValidator,
    ValidationMessage,
    ValidationResult,
    load_schematron_validator,
)
from mcp_einvoicing_core.schematron import (
    XSDValidator as _CoreXSDValidator,
)

__all__ = [
    "SchematronValidator",
    "SaxonSchematronValidator",
    "ValidationMessage",
    "ValidationResult",
    "tdd_xsd_validator",
]

_RULES_DIR = Path(__file__).parent.parent / "rules"

StylesheetKey = Literal[
    "pint_ubl_billing",
    "pint_ubl_selfbilling",
    "pint_jurisdiction_ae",
    "peppol_ae_tdd",
]

_STYLESHEET_MAP: dict[str, Path] = {
    "pint_ubl_billing": _RULES_DIR / "pint-ubl-billing.xslt",
    "pint_ubl_selfbilling": _RULES_DIR / "pint-ubl-selfbilling.xslt",
    "pint_jurisdiction_ae": _RULES_DIR / "pint-jurisdiction-ae.xslt",
    "peppol_ae_tdd": _RULES_DIR / "peppol-ae-tdd.xslt",
}

_TDD_XSD_PATH = _RULES_DIR / "peppol-tdd-1.0.0.xsd"


def SchematronValidator(stylesheet_key: StylesheetKey) -> BaseStructuredValidator:  # noqa: N802
    """Factory: return the right validator backend for a bundled stylesheet key.

    Delegates version detection and backend dispatch to core's
    ``load_schematron_validator()``.

    Raises:
        ValueError:        If the key is unknown.
        FileNotFoundError: If the XSLT file is missing from the package.
        ImportError:       If an XSLT 2.0+ stylesheet is requested without
                           the optional ``saxonche`` extra installed.
    """
    stylesheet_path = _STYLESHEET_MAP.get(stylesheet_key)
    if stylesheet_path is None:
        raise ValueError(
            f"Unknown stylesheet key: {stylesheet_key!r}. Valid keys: {sorted(_STYLESHEET_MAP)}"
        )
    return load_schematron_validator(stylesheet_path)


def tdd_xsd_validator() -> _CoreXSDValidator:
    """Return an ``XSDValidator`` for the Peppol AE Tax Data Document schema.

    The TDD is not a UBL invoice and is not covered by the EN 16931/PINT
    Schematron rules above — schema-level (XSD) validation plus its own
    ``peppol_ae_tdd`` Schematron are the two checks available for it.

    Currently raises ``ValueError``: ``peppol-tdd-1.0.0.xsd`` imports the base
    OASIS ``UnqualifiedDataTypes-2`` schema, which was not included in any
    supplied ZIP (see context-library/countries/ae.md "Wire format caps and
    constraints", still `[NEED:]` as of 2026-08-27). lxml cannot compile the
    schema standalone until that base schema is supplied. Schematron-level
    validation via ``SchematronValidator("peppol_ae_tdd")`` is unaffected —
    it operates on the XML directly and does not require XSD compilation.
    """
    return _CoreXSDValidator(_TDD_XSD_PATH)
