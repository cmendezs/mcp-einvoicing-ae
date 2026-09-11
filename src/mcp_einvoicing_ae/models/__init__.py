"""UAE e-invoicing Pydantic models.

See the package's own compliance reference and format reference for
field-level citations.
"""

from mcp_einvoicing_core import DocumentValidationResult

from mcp_einvoicing_ae.models.invoice import (
    AE_STANDARD_VAT_RATE,
    AEInvoice,
    AEInvoiceLine,
    AEProfileVariant,
    AEVatCategory,
)
from mcp_einvoicing_ae.models.party import AEParty
from mcp_einvoicing_ae.models.tdd import (
    AETaxDataDocument,
    TDDParty,
    TDDReportedDocument,
    TDDReportedTransaction,
)

ValidationResult = DocumentValidationResult

__all__ = [
    "AE_STANDARD_VAT_RATE",
    "AEInvoice",
    "AEInvoiceLine",
    "AEParty",
    "AEProfileVariant",
    "AETaxDataDocument",
    "AEVatCategory",
    "DocumentValidationResult",
    "TDDParty",
    "TDDReportedDocument",
    "TDDReportedTransaction",
    "ValidationResult",
]
