"""MCP server entry point — registers UAE (PINT AE / Peppol AE TDD) tools."""

from typing import Any

from mcp_einvoicing_core import EInvoicingMCPServer
from mcp_einvoicing_core.peppol.tools import register_peppol_tools

from mcp_einvoicing_ae.standards.pint_ae import PEPPOL_PARTICIPANT_SCHEME
from mcp_einvoicing_ae.tools.generation import AEDocumentGenerator
from mcp_einvoicing_ae.tools.parsing import parse_invoice_ae
from mcp_einvoicing_ae.tools.validation import AEDocumentValidator

_generator = AEDocumentGenerator()
_validator = AEDocumentValidator()


def _ae_id_adapter(identifier: str) -> str:
    """Normalize a bare UAE TRN to a Peppol participant ID.

    Scheme 0235 is the TIN (Tax Identification Number) — the first 10 digits
    of the 15-digit TRN, per specs/guidelines/UAE-Electronic-Invoicing-
    Guidelines_V-1.1-01June2026.pdf p.3/p.7 (also cited in
    AEParty._derive_peppol_participant_id). Already scheme-qualified
    identifiers (containing ':') pass through unchanged.
    """
    if ":" in identifier:
        return identifier
    return f"{PEPPOL_PARTICIPANT_SCHEME}:{identifier[:10]}"


def _register_ae_tools(mcp: Any) -> None:
    """Register all UAE e-invoicing tools onto the shared FastMCP instance."""
    mcp.tool()(_generator.generate_invoice_ae)
    mcp.tool()(_validator.validate_invoice_ae)
    mcp.tool()(_validator.validate_tdd_ae)
    mcp.tool()(parse_invoice_ae)


mcp = EInvoicingMCPServer(
    "mcp-einvoicing-ae",
    instructions=(
        "Tools for United Arab Emirates electronic invoicing: PINT AE "
        "(billing + self-billing) UBL 2.1 invoice generation, validation, "
        "and parsing, Peppol AE Tax Data Document (TDD) validation, and "
        "Peppol participant lookup (5-corner transport). "
        "Schematron validation requires the optional 'xslt2' extra "
        "(saxonche) — see README. TDD schema (XSD) validation is currently "
        "unavailable; validate_tdd_ae runs Schematron only and flags this "
        "explicitly in its result."
    ),
)
mcp.register_plugin(_register_ae_tools, "ae")
mcp.register_plugin(lambda m: register_peppol_tools(m, id_adapter=_ae_id_adapter), "peppol")


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
