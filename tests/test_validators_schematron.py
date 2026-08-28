"""Tests for the CEN EN16931 base Schematron validator wiring.

v0.1.0 bundled four self-compiled OpenPeppol-derived stylesheets here; v0.2.0
removed them (no confirmed redistribution rights) and wired core's shared
en16931_base_schematron_validator() instead — see
mcp_einvoicing_ae/validators/schematron.py module docstring for the full
history. Requires the optional `saxonche` extra (XSLT 3.0) — skipped when
absent, mirroring mcp-einvoicing-de's test_schematron_backend.py pattern.
"""

import importlib.util
from pathlib import Path

import pytest

from mcp_einvoicing_ae.validators.schematron import en16931_base_validator

_SAXON_AVAILABLE = importlib.util.find_spec("saxonche") is not None

_SPECS_ROOT = Path(__file__).parent.parent / "specs"
_STANDARD_INVOICE = _SPECS_ROOT / "pint-ae" / "trn-invoice" / "example" / "Standard tax invoice.xml"


@pytest.mark.skipif(not _SAXON_AVAILABLE, reason="saxonche extra not installed")
def test_en16931_base_validator_loads() -> None:
    en16931_base_validator()


@pytest.mark.skipif(not _SAXON_AVAILABLE, reason="saxonche extra not installed")
@pytest.mark.skipif(not _STANDARD_INVOICE.exists(), reason="specs/ not present in this checkout")
def test_en16931_base_validator_runs_against_standard_invoice() -> None:
    validator = en16931_base_validator()
    result = validator.validate(_STANDARD_INVOICE.read_bytes())
    # Not asserting is_valid — the bundled example is a documentation fixture,
    # not guaranteed schematron-clean, and BR-CO-09 is a known, permanent
    # false positive for AE's non-EU TRN identifiers (see
    # validators/schematron.py). Asserting the validator runs to completion
    # and returns a real ValidationResult is the useful check here.
    assert result is not None
    assert isinstance(result.errors, list)
    assert isinstance(result.warnings, list)


@pytest.mark.skipif(not _SAXON_AVAILABLE, reason="saxonche extra not installed")
@pytest.mark.skipif(not _STANDARD_INVOICE.exists(), reason="specs/ not present in this checkout")
def test_br_co_09_known_limitation_fires_on_standard_invoice() -> None:
    """Documents the known, permanent BR-CO-09 false positive for AE TRNs.

    UAE Tax Registration Numbers carry no ISO 3166-1 alpha-2 prefix, so this
    EU-oriented rule is expected to fire on every genuine AE invoice —
    confirmed directly against the government-supplied example fixture. See
    EN16931_BASE_KNOWN_LIMITATIONS_WARNING in tools/validation.py.
    """
    validator = en16931_base_validator()
    result = validator.validate(_STANDARD_INVOICE.read_bytes())
    assert any(m.rule_id == "BR-CO-09" for m in result.errors)
