"""Tests for AE profile-registry registration (core ProfileRegistry reuse)."""

from mcp_einvoicing_core.profile_registry import profile_registry

import mcp_einvoicing_ae.standards.pint_ae as pint_ae  # noqa: F401  (registers on import)


def test_billing_registered_in_core_profile_registry() -> None:
    assert profile_registry.is_registered("AE", "BILLING", "UBL")
    assert (
        profile_registry.get_guideline_id("AE", "BILLING", "UBL")
        == "urn:peppol:pint:billing-1@ae-1"
    )


def test_selfbilling_registered_in_core_profile_registry() -> None:
    assert profile_registry.is_registered("AE", "SELFBILLING", "UBL")
    assert (
        profile_registry.get_guideline_id("AE", "SELFBILLING", "UBL")
        == "urn:peppol:pint:selfbilling-1@ae-1"
    )
