"""MCP server entry point — registers UAE (PINT AE / Peppol AE TDD) tools."""

from typing import Any

from mcp_einvoicing_core import EInvoicingMCPServer

from mcp_einvoicing_ae.tools.generation import AEDocumentGenerator
from mcp_einvoicing_ae.tools.parsing import parse_invoice_ae
from mcp_einvoicing_ae.tools.validation import AEDocumentValidator

_generator = AEDocumentGenerator()
_validator = AEDocumentValidator()


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
        "and parsing, plus Peppol AE Tax Data Document (TDD) validation. "
        "Schematron validation requires the optional 'xslt2' extra "
        "(saxonche) — see README. TDD schema (XSD) validation is currently "
        "unavailable; validate_tdd_ae runs Schematron only and flags this "
        "explicitly in its result."
    ),
)
mcp.register_plugin(_register_ae_tools, "ae")


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
