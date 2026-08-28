"""Tests for AEDocumentValidator.validate_invoice_ae / validate_tdd_ae.

v0.2.0 replaced the two bundled PINT AE stylesheets in validate_invoice_ae
with core's shared CEN EN16931 base Schematron, and validate_tdd_ae now
always reports "unavailable" (no substitute for the removed peppol_ae_tdd
Schematron) — see mcp_einvoicing_ae/validators/schematron.py and
tools/validation.py module docstrings for why.
"""

from pathlib import Path

import pytest

from mcp_einvoicing_ae.tools import validation as validation_module
from mcp_einvoicing_ae.tools.validation import (
    EN16931_BASE_KNOWN_LIMITATIONS_WARNING,
    EN16931_BASE_ONLY_SCOPE_WARNING,
    AEDocumentValidator,
)

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


async def test_validate_invoice_ae_billing_runs_en16931_base() -> None:
    xml = _STANDARD_INVOICE.read_text(encoding="utf-8")
    result = await _validator.validate_invoice_ae(xml=xml, variant="billing")
    assert isinstance(result["valid"], bool)
    assert isinstance(result["errors"], list)
    assert result["variant"] == "billing"
    assert result["rulesets_run"] == ["en16931_base"]
    assert result["scope"] == "en16931-base-only"
    assert any(EN16931_BASE_ONLY_SCOPE_WARNING == w for w in result["warnings"])
    assert any(EN16931_BASE_KNOWN_LIMITATIONS_WARNING == w for w in result["warnings"])


async def test_validate_invoice_ae_selfbilling_variant() -> None:
    xml = _SELF_BILLING_INVOICE.read_text(encoding="utf-8")
    result = await _validator.validate_invoice_ae(xml=xml, variant="selfbilling")
    assert result["variant"] == "selfbilling"
    assert result["rulesets_run"] == ["en16931_base"]


async def test_validate_invoice_ae_flags_known_br_co_09_limitation() -> None:
    """The bundled example's TRNs carry no ISO country prefix — BR-CO-09
    is expected to fire; this is disclosed, not silently hidden."""
    xml = _STANDARD_INVOICE.read_text(encoding="utf-8")
    result = await _validator.validate_invoice_ae(xml=xml, variant="billing")
    assert any("BR-CO-09" in e for e in result["errors"])


async def test_validate_invoice_ae_unavailable_when_base_validator_cannot_load(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise() -> None:
        raise ImportError("saxonche not installed")

    monkeypatch.setattr(validation_module, "en16931_base_validator", _raise)
    validator = AEDocumentValidator()
    xml = _STANDARD_INVOICE.read_text(encoding="utf-8")
    result = await validator.validate_invoice_ae(xml=xml, variant="billing")
    assert result["valid"] is False
    assert any("AE-VALIDATION-UNAVAILABLE" in e for e in result["errors"])


async def test_validate_tdd_ae_always_unavailable() -> None:
    xml = _TDD_SIMPLE.read_text(encoding="utf-8")
    result = await _validator.validate_tdd_ae(xml=xml)
    assert result["valid"] is False
    assert any("TDD-VALIDATION-UNAVAILABLE" in e for e in result["errors"])
    assert result["engine"] == "unavailable"


def test_get_schema_version() -> None:
    assert "PINT AE" in _validator.get_schema_version()
    assert "TDD" in _validator.get_schema_version()
