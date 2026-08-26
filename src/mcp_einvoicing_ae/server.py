"""MCP server entry point for mcp-einvoicing-ae.

Scaffold stage: no tools are registered yet.

[NEED: tool registration]
No normative specification has been supplied under specs/, and PINT AE was
absent from the published OpenPeppol jurisdiction PINT list at the last local
verification (2026-06-29). See the publication gate in
context-library/countries/ae.md. This package stays a skeleton until that
status is established from a supplied document.
"""

from mcp_einvoicing_core import EInvoicingMCPServer

mcp = EInvoicingMCPServer(
    "mcp-einvoicing-ae",
    instructions=(
        "Tools for United Arab Emirates electronic invoicing. "
        "This server is a scaffold: no tools are registered yet. Tool "
        "implementation is blocked until a published PINT AE specification is "
        "supplied under specs/ and the compliance values are recorded in "
        "context-library/countries/ae.md."
    ),
)


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
