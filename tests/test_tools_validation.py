"""Tests for AEDocumentValidator.validate_invoice_ae / validate_tdd_ae.

Uses the real bundled Schematron stylesheets against the supplied example
documents (saxonche is installed in this workspace venv — confirmed via
tests/test_validators_schematron.py). Not asserting `valid=True` for the
bundled examples: they are documentation fixtures, not guaranteed
schematron-clean (same stance as test_validators_schematron.py). The useful
assertions here are that both rule sets actually run and that the combined
result/warnings shape is correct — including the "unavailable" fallback path
when a stylesheet fails to load.
"""

from pathlib import Path

import pytest

from mcp_einvoicing_ae.tools import validation as validation_module
from mcp_einvoicing_ae.tools.validation import AEDocumentValidator

_validator = AEDocumentValidator()

_SPECS_ROOT = Path(__file__).parent.parent / "specs"
_STANDARD_INVOICE = _SPECS_ROOT / "pint-ae" / "trn-invoice" / "example" / "Standard tax invoice.xml"
_SELF_BILLING_INVOICE = (
    _SPECS_ROOT / "pint-ae-self-billing" / "trn-invoice" / "example" / "Self Billing.xml"
)
_TDD_SIMPLE = _SPECS_ROOT / "tdd" / "trn-tdd" / "example" / "simple.xml"

pytestmark = pytest.mark.skipif(
    not _STANDARD_INVOICE.exists(), reason="specs/ not present in this checkout"
)


async def test_validate_invoice_ae_billing_runs_both_rulesets() -> None:
    xml = _STANDARD_INVOICE.read_text(encoding="utf-8")
    result = await _validator.validate_invoice_ae(xml=xml, variant="billing")
    assert isinstance(result["valid"], bool)
    assert isinstance(result["errors"], list)
    assert result["variant"] == "billing"
    assert result["rulesets"] == ["pint_ubl_billing", "pint_jurisdiction_ae"]


async def test_validate_invoice_ae_selfbilling_variant() -> None:
    xml = _SELF_BILLING_INVOICE.read_text(encoding="utf-8")
    result = await _validator.validate_invoice_ae(xml=xml, variant="selfbilling")
    assert result["variant"] == "selfbilling"
    assert result["rulesets"] == ["pint_ubl_selfbilling", "pint_jurisdiction_ae"]


async def test_validate_invoice_ae_unavailable_when_stylesheets_cannot_load(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(_key: str) -> None:
        raise ImportError("saxonche not installed")

    monkeypatch.setattr(validation_module, "SchematronValidator", _raise)
    xml = _STANDARD_INVOICE.read_text(encoding="utf-8")
    result = await _validator.validate_invoice_ae(xml=xml, variant="billing")
    assert result["valid"] is False
    assert any("AE-VALIDATION-UNAVAILABLE" in e for e in result["errors"])


async def test_validate_tdd_ae_flags_xsd_not_run() -> None:
    xml = _TDD_SIMPLE.read_text(encoding="utf-8")
    result = await _validator.validate_tdd_ae(xml=xml)
    assert isinstance(result["valid"], bool)
    assert any("TDD-XSD-NOT-RUN" in w for w in result["warnings"])


def test_get_schema_version() -> None:
    assert "PINT AE" in _validator.get_schema_version()
    assert "TDD" in _validator.get_schema_version()
