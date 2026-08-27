"""Tests for the bundled PINT AE / Peppol AE TDD Schematron and XSD validators.

All four bundled stylesheets are XSLT 2.0 (confirmed 2026-08-27), so real
validation requires the optional `saxonche` extra — skipped when absent,
mirroring mcp-einvoicing-de's test_schematron_backend.py pattern.
"""

import importlib.util
from pathlib import Path

import pytest

from mcp_einvoicing_ae.validators.schematron import SchematronValidator, tdd_xsd_validator

_SAXON_AVAILABLE = importlib.util.find_spec("saxonche") is not None

_SPECS_ROOT = Path(__file__).parent.parent / "specs"
_STANDARD_INVOICE = _SPECS_ROOT / "pint-ae" / "trn-invoice" / "example" / "Standard tax invoice.xml"
_SELF_BILLING_INVOICE = (
    _SPECS_ROOT / "pint-ae-self-billing" / "trn-invoice" / "example" / "Self Billing.xml"
)
_TDD_SIMPLE = _SPECS_ROOT / "tdd" / "trn-tdd" / "example" / "simple.xml"


def test_unknown_stylesheet_key_raises() -> None:
    with pytest.raises(ValueError, match="Unknown stylesheet key"):
        SchematronValidator("not-a-real-key")  # type: ignore[arg-type]


@pytest.mark.skipif(not _SAXON_AVAILABLE, reason="saxonche extra not installed")
class TestBundledStylesheetsLoad:
    def test_pint_ubl_billing_loads(self) -> None:
        SchematronValidator("pint_ubl_billing")

    def test_pint_ubl_selfbilling_loads(self) -> None:
        SchematronValidator("pint_ubl_selfbilling")

    def test_pint_jurisdiction_ae_loads(self) -> None:
        SchematronValidator("pint_jurisdiction_ae")

    def test_peppol_ae_tdd_loads(self) -> None:
        SchematronValidator("peppol_ae_tdd")


@pytest.mark.skipif(not _SAXON_AVAILABLE, reason="saxonche extra not installed")
@pytest.mark.skipif(not _STANDARD_INVOICE.exists(), reason="specs/ not present in this checkout")
def test_jurisdiction_rules_run_against_standard_invoice() -> None:
    validator = SchematronValidator("pint_jurisdiction_ae")
    result = validator.validate(_STANDARD_INVOICE.read_bytes(), profile="pint-ae-billing")
    # Not asserting is_valid — the bundled example is a documentation fixture,
    # not guaranteed schematron-clean. Asserting the validator runs to
    # completion and returns a real ValidationResult is the useful check here.
    assert result is not None
    assert isinstance(result.errors, list)
    assert isinstance(result.warnings, list)


def test_tdd_xsd_validator_raises_without_base_oasis_schema() -> None:
    """peppol-tdd-1.0.0.xsd imports the base OASIS UnqualifiedDataTypes-2 schema,
    which was not included in any supplied ZIP (see context-library/countries/ae.md
    "Wire format caps and constraints" -- still `[NEED:]` as of 2026-08-27). lxml
    cannot compile the TDD schema standalone until that base schema is supplied.
    This test documents the current failure mode rather than silently skipping it.
    """
    with pytest.raises(ValueError, match="Failed to parse XSD schema"):
        tdd_xsd_validator()
