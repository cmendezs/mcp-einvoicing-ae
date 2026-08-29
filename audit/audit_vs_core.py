"""Pre-publish audit: verify mcp-einvoicing-ae coherence against mcp-einvoicing-core.

Run standalone (from the workspace root):
    uv run python mcp-einvoicing-ae/audit/audit_vs_core.py
    uv run python mcp-einvoicing-ae/audit/audit_vs_core.py --output mcp-einvoicing-ae/audit/report.json
    uv run python mcp-einvoicing-ae/audit/audit_vs_core.py --fail-on blocking

Exit codes:
    0  All checks passed
    1  Warnings only (non-blocking)
    2  Blocking failures found

Phase D status (2026-08-27)
---------------------------
The invoice-tree pathway is resolved (``_IS_EN16931_FAMILY = True``,
``AEInvoice``), so CHECK 1 (core interface coverage) now runs for real instead
of being deferred. Models (``AEInvoice``, ``AEParty``, ``AETaxDataDocument``),
the Schematron/XSD validators, and the profile-registry registration exist;
tools (MCP-exposed generate/validate/parse functions) do not yet — CHECK 0's
server-module checks still gate on that.

CHECK 4 (version compatibility) and CHECK 5 (spec sources) are meaningful now and
run unconditionally.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from mcp_einvoicing_core.audit import (
    SEVERITY_BLOCKING,
    SEVERITY_OK,
    SEVERITY_WARNING,
    AuditReport,
    CheckFinding,
    CheckResult,
    _try_import,
    make_report,
    parse_audit_args,
    render_summary_table,
    run_check_core_coverage,
    run_check_version_compatibility,
)

_PACKAGE = "mcp-einvoicing-ae"
_MODULE = "mcp_einvoicing_ae"
_ROOT = Path(__file__).resolve().parent.parent
_PYPROJECT = _ROOT / "pyproject.toml"
_SOURCES = _ROOT / "specs" / "README.md"

# ---------------------------------------------------------------------------
# CHECK 1 configuration — country-specific constants
# ---------------------------------------------------------------------------

# Invoice-tree pathway, resolved 2026-08-27 (Phase D) per
# context-library/countries/ae.md "Invoice-tree pathway": PINT AE's
# CustomizationID/ProfileID (urn:peppol:pint:billing-1@ae-1 /
# urn:peppol:bis:billing) are a UBL 2.1 CIUS of EN 16931-1:2017 — the
# EN16931Invoice pathway per CLAUDE.md's "any PINT-* format uses EN16931Invoice"
# rule. This is set together with the AEInvoice model class itself, per
# CLAUDE.md: "do not change it without a corresponding model refactor."
_IS_EN16931_FAMILY: bool | None = True
_PRIMARY_INVOICE_CLASS: tuple[str, str] | None = ("mcp_einvoicing_ae.models.invoice", "AEInvoice")

_MODULES: list[str] = [
    f"{_MODULE}.server",
    f"{_MODULE}.models.invoice",
    f"{_MODULE}.models.party",
    f"{_MODULE}.models.tdd",
    f"{_MODULE}.standards.pint_ae",
    f"{_MODULE}.validators.schematron",
    # AE-AG-1: these four were missing from the scan list, which made CHECK 1
    # report ~90 core symbols as "unused" that are genuinely imported and
    # used here — just in modules the audit never looked at.
    f"{_MODULE}.tools.generation",
    f"{_MODULE}.tools.parsing",
    f"{_MODULE}.tools.validation",
    f"{_MODULE}.wire_formats",
]

_INTENTIONAL_OVERRIDES: dict[str, set[str]] = {
    "mcp_einvoicing_core.base_server": {
        # OVERRIDE-REASON: stdlib/typing re-exports; AE imports these from stdlib directly where needed
        "ABC",
        "Any",
        "Callable",
        "Generic",
        "TypeVar",
        "abstractmethod",
        # OVERRIDE-REASON: third-party re-export; pydantic BaseModel/Field imported from pydantic directly in AE models
        "BaseModel",
        "Field",
        # OVERRIDE-REASON: AE has no document parser class; parse_invoice_ae is a standalone function
        "BaseDocumentParser",
        # OVERRIDE-REASON: Peppol AE TDD (5th-corner reporting) is push-based; no session-based lifecycle API required yet (AE-LC-1)
        "BaseLifecycleManager",
        # OVERRIDE-REASON: party validation (TRN format) runs inline via a pydantic field_validator on AEParty, not the ABC party validator pattern
        "BasePartyValidator",
        # OVERRIDE-REASON: AE uses EInvoicingMCPServer; raw FastMCP handle not needed in package code
        "FastMCP",
        # OVERRIDE-REASON: AEInvoice/AEParty extend EN16931Invoice/EN16931Party (canonical invoice tree), not InvoiceDocument/InvoiceParty
        "InvoiceDocument",
        "InvoiceParty",
        # OVERRIDE-REASON: AE has no submission tool yet; the TDD reporting leg (AE-LC-1) is parked pending the transport-channel spec
        "SubmitResult",
        # OVERRIDE-REASON: AEParty's TRN check raises pydantic ValidationError inline via field_validator, not via TaxIdValidationResult
        "TaxIdValidationResult",
        # OVERRIDE-REASON: assert_not_read_only is an internal server guard not needed in AE tool handlers
        "assert_not_read_only",
        # OVERRIDE-REASON: scrub not applied at AE's tool boundary yet (tracked as future work, same posture as BE-SH-1)
        "scrub",
    },
    "mcp_einvoicing_core.digital_signature": {
        # OVERRIDE-REASON: stdlib re-exports; AE imports these from stdlib directly
        "ABC",
        "abstractmethod",
        "dataclass",
        "datetime",
        "field",
        # OVERRIDE-REASON: Peppol AE TDD relies on AS4 transport-level signing (5th-corner); no document-level XAdES/CAdES signing implemented
        "BaseDocumentSigner",
        "CAdESSigner",
        "CAdESSignerConfig",
        "XAdESEPESSigner",
        "XAdESSignerConfig",
        "XMLDSigSigner",
        "XMLDSigSignerConfig",
        # OVERRIDE-REASON: AE has no mTLS/JWS client-certificate auth path (no external HTTP client integration yet); load_certificate_der not needed
        "load_certificate_der",
    },
    "mcp_einvoicing_core.download_rules": {
        # OVERRIDE-REASON: AE spec artefacts (Schematron, XSDs) are supplied manually into specs/; the artefact-download framework is not used
        "DownloadSpec",
        "Path",
        "dataclass",
        "download_artefacts",
        "entry_points",
        "field",
        "main",
    },
    "mcp_einvoicing_core.en16931": {
        # OVERRIDE-REASON: stdlib/third-party re-exports; AE imports these from pydantic/stdlib directly
        "BaseModel",
        "Decimal",
        "Field",
        "date",
        "field_validator",
        "model_validator",
        # OVERRIDE-REASON: inherited field types on EN16931Invoice/EN16931Party (address, allowances, payment means, tax lines) are not imported by name in AE's own modules — AE only subclasses the parent models
        "EN16931Address",
        "EN16931AllowanceCharge",
        "EN16931PaymentMeans",
        "EN16931Tax",
    },
    "mcp_einvoicing_core.exceptions": {
        # OVERRIDE-REASON: AE tools have no authenticated external HTTP client path (specs/validation are local); not raised
        "AuthenticationError",
        "PlatformError",
        # OVERRIDE-REASON: AE raises specific exception subclasses (DocumentGenerationError) directly; the EInvoicingError base is not re-raised at the tool layer
        "EInvoicingError",
        # OVERRIDE-REASON: TRN validation raises pydantic ValidationError inline via field_validator on AEParty; PartyValidationError not raised
        "PartyValidationError",
        # OVERRIDE-REASON: AE surfaces core's DocumentValidationResult/ValidationResult from the Schematron validator, not this exception type, at the tool layer
        "SchematronValidationError",
        # OVERRIDE-REASON: PINT AE validation uses Schematron, not XSD, for business rules; XSD schema validation is a separate, currently-unavailable path (AE-LC-1)
        "XSDValidationError",
        # OVERRIDE-REASON: AE tools catch exceptions generically (`except Exception`) and re-raise as DocumentGenerationError; ValidationError is not re-raised as this specific type
        "ValidationError",
    },
    "mcp_einvoicing_core.http_client": {
        # OVERRIDE-REASON: AE has no external HTTP client integration yet (no government lookup API, unlike BE's BCE/KBO tool) — http_client's OAuth2/mTLS/retry machinery is entirely unused
        "Any",
        "AuthMode",
        "AuthenticationError",
        "BaseEInvoicingClient",
        "BaseEInvoicingConfig",
        "BaseModel",
        "BaseSettings",
        "Field",
        "JWSConfig",
        "OAuthConfig",
        "OAuthValues",
        "Path",
        "PlatformError",
        "StrEnum",
        "TokenCache",
        "compute_retry_delay",
        "field_validator",
        "parsedate_to_datetime",
        "urlparse",
    },
    "mcp_einvoicing_core.models": {
        # OVERRIDE-REASON: stdlib/third-party re-exports; AE imports these from pydantic/stdlib directly
        "BaseModel",
        "Decimal",
        "Field",
        "field_validator",
        "model_validator",
        # OVERRIDE-REASON: AEInvoice/AEParty/AEInvoiceLine extend the EN16931Invoice family (canonical invoice tree); the non-EN16931 InvoiceDocument pathway's base classes are not used
        "InvoiceDocument",
        "InvoiceLineItem",
        "InvoiceParty",
        "PartyAddress",
        "PaymentTerms",
        "VATSummary",
        # OVERRIDE-REASON: TRN validation raises inline via field_validator; TaxIdValidationResult not returned by AE
        "TaxIdValidationResult",
    },
    "mcp_einvoicing_core.pdf": {
        # OVERRIDE-REASON: PINT AE does not require PDF/A-3 hybrid embedding (Peppol UBL XML transport only); PDFEmbedder not applicable
        "PDFEmbedder",
    },
    "mcp_einvoicing_core.peppol": {
        # OVERRIDE-REASON: stdlib/typing re-exports; AE imports these from stdlib directly
        "Callable",
        "StrEnum",
        "dataclass",
        "field",
        # OVERRIDE-REASON: AE-LC-2 resolved via core's peppol.tools plugin (register_peppol_tools, mounted in server.py); the lower-level SMP client classes are not imported directly, mirroring BE's own pattern
        "PeppolEnvironment",
        "PeppolLookupResult",
        "PeppolParticipantId",
        "PeppolSMPClient",
        "PeppolServiceInfo",
        # OVERRIDE-REASON: re-exported by peppol; AE has no authenticated external HTTP path (see http_client override)
        "PlatformError",
        # OVERRIDE-REASON: resolve_naptr (core v1.19.0) is a standalone DNS diagnostic surfaced via the peppol.tools plugin's own tool set, not called directly by AE package code
        "resolve_naptr",
    },
    "mcp_einvoicing_core.profile_registry": {
        # OVERRIDE-REASON: AE uses its own CUSTOMIZATION_IDS/PROFILE_IDS dicts in standards/pint_ae.py; only the shared profile_registry singleton instance is imported, not these classes/helper
        "ProfileEntry",
        "ProfileRegistry",
        "dataclass",
        "set_profile_registry",
    },
    "mcp_einvoicing_core.qr": {
        # OVERRIDE-REASON: PINT AE does not require QR code generation
        "generate_qr_png_base64",
    },
    "mcp_einvoicing_core.schematron": {
        # OVERRIDE-REASON: stdlib re-exports; AE imports these from stdlib directly
        "ABC",
        "Path",
        "abstractmethod",
        "dataclass",
        "field",
        # OVERRIDE-REASON: AE validation is Schematron-based; JSON/XSD structured validators not used (XSD path tracked separately as AE-LC-1)
        "BaseJSONValidator",
        "BaseXSDValidator",
        "XSDValidator",
        # OVERRIDE-REASON: AE's validators/schematron.py gets a pre-built validator from en16931_base_schematron_validator(); the concrete engine classes and factory are not imported by name
        "SaxonSchematronValidator",
        "SchematronValidator",
        "load_schematron_validator",
        # OVERRIDE-REASON: AE returns core's DocumentValidationResult at the tool boundary, not these lower-level Schematron detail types
        "ValidationMessage",
        "ValidationResult",
        # OVERRIDE-REASON: diagnostic helper for compiled XSLT; not called by AE's validation tools
        "get_xslt_version",
        # OVERRIDE-REASON: not called directly; used internally by core's schematron/wire_formats modules
        "safe_parser",
    },
    "mcp_einvoicing_core.xml_utils": {
        # OVERRIDE-REASON: stdlib/typing re-exports; not used directly in AE package code
        "Any",
        "Decimal",
        # OVERRIDE-REASON: used internally by core's EN16931UBLSerializer/AEUBLSerializer; not called directly by AE
        "filter_empty_values",
        "format_amount",
        "format_quantity",
        "safe_parser",
        "xml_element",
        "xml_escape",
        "xml_optional",
        # OVERRIDE-REASON: AE tools return plain error-string dicts; the structured format_error helper is not used
        "format_error",
        # OVERRIDE-REASON: mark_untrusted / mark_untrusted_fields prompt-injection helpers not yet applied at AE's tool boundary (tracked as future work, same posture as BE)
        "mark_untrusted",
        "mark_untrusted_fields",
        # OVERRIDE-REASON: AE tools accept raw XML strings/bytes directly; resolve_xml_input indirection not used
        "resolve_xml_input",
        # OVERRIDE-REASON: date validation handled by Pydantic's date field type on AEInvoice
        "validate_date_iso",
        # OVERRIDE-REASON: PINT AE payment_means (BG-16) IBAN, when present, is not yet independently re-validated by AE beyond core's own model
        "validate_iban",
    },
}


def _finding(tag: str, severity: str, symbol: str, message: str) -> CheckFinding:
    return CheckFinding(
        check_id="CHECK_0",
        tag=tag,
        severity=severity,
        symbol=symbol,
        message=message,
    )


def run_check_0() -> CheckResult:
    """CHECK 0 — scaffold gates that block implementation and publication."""
    result = CheckResult(check_id="CHECK_0", name="Scaffold gates")

    if _IS_EN16931_FAMILY is None:
        result.findings.append(
            _finding(
                "[NEED]",
                SEVERITY_BLOCKING,
                "_IS_EN16931_FAMILY",
                (
                    "Invoice-tree pathway is unresolved. Set it from the conformance "
                    "statement recorded in context-library/countries/ae.md, never from memory. "
                    "No model code may be written while this is None."
                ),
            )
        )
    elif _PRIMARY_INVOICE_CLASS is None:
        result.findings.append(
            _finding(
                "[MISSING]",
                SEVERITY_BLOCKING,
                "_PRIMARY_INVOICE_CLASS",
                "Pathway is declared but no primary invoice class is registered for the tree check.",
            )
        )
    else:
        result.findings.append(
            _finding("[OK]", SEVERITY_OK, "_IS_EN16931_FAMILY", "Invoice-tree pathway declared.")
        )

    server_mod, err = _try_import(f"{_MODULE}.server")
    if server_mod is None:
        result.findings.append(
            _finding(
                "[MISSING]",
                SEVERITY_BLOCKING,
                f"{_MODULE}.server",
                f"Could not import the server module: {err}",
            )
        )
    else:
        for attr in ("mcp", "main"):
            present = hasattr(server_mod, attr)
            result.findings.append(
                _finding(
                    "[OK]" if present else "[MISSING]",
                    SEVERITY_OK if present else SEVERITY_BLOCKING,
                    f"server.{attr}",
                    f"server.{attr} is {'present' if present else 'absent'}.",
                )
            )

    return result


def run_check_5() -> CheckResult:
    """CHECK 5 — normative spec sources are recorded with an authority URL."""
    result = CheckResult(check_id="CHECK_5", name="Spec sources")

    if not _SOURCES.exists():
        result.findings.append(
            CheckFinding(
                check_id="CHECK_5",
                tag="[MISSING]",
                severity=SEVERITY_BLOCKING,
                symbol="specs/README.md",
                message="specs/README.md is absent. One authority URL per standard is required.",
            )
        )
        return result

    text = _SOURCES.read_text(encoding="utf-8")
    unresolved = text.count("[NEED:")
    if unresolved:
        result.findings.append(
            CheckFinding(
                check_id="CHECK_5",
                tag="[NEED]",
                severity=SEVERITY_BLOCKING,
                symbol="specs/README.md",
                message=(
                    f"{unresolved} unresolved [NEED:] marker(s) remain. Every standard needs an "
                    "authority URL and a retrieval date before this package can publish."
                ),
            )
        )
    else:
        result.findings.append(
            CheckFinding(
                check_id="CHECK_5",
                tag="[OK]",
                severity=SEVERITY_OK,
                symbol="specs/README.md",
                message="All spec sources carry an authority URL and a retrieval date.",
            )
        )

    return result


def _deferred(check_id: str, name: str, reason: str) -> CheckResult:
    result = CheckResult(check_id=check_id, name=name)
    result.findings.append(
        CheckFinding(
            check_id=check_id,
            tag="[DEFERRED]",
            severity=SEVERITY_WARNING,
            symbol=_PACKAGE,
            message=reason,
        )
    )
    return result


def run_audit() -> AuditReport:
    """Execute all checks and return the aggregated AuditReport. No side effects."""
    report = make_report(_PACKAGE, _PYPROJECT)

    check_0 = run_check_0()
    report.checks.append(check_0)

    scaffold_stage = _IS_EN16931_FAMILY is None
    if scaffold_stage:
        report.checks.append(
            _deferred(
                "CHECK_1",
                "Core interface coverage",
                (
                    "Deferred while the invoice-tree pathway is unresolved (CHECK 0). "
                    "Running coverage against a package with no models reports every core "
                    "symbol as missing and hides the real gate."
                ),
            )
        )
    else:
        report.checks.append(
            run_check_core_coverage(
                package_name=_PACKAGE,
                package_modules=_MODULES,
                intentional_overrides=_INTENTIONAL_OVERRIDES,
                is_en16931_family=_IS_EN16931_FAMILY,
                primary_invoice_class=_PRIMARY_INVOICE_CLASS,
            )
        )

    report.checks.append(
        run_check_version_compatibility(
            package_name=_PACKAGE,
            pyproject_path=_PYPROJECT,
        )
    )
    report.checks.append(run_check_5())

    return report


def main(argv: list[str] | None = None) -> int:
    args = parse_audit_args(f"Pre-publish audit: {_PACKAGE} vs mcp-einvoicing-core", argv)
    report = run_audit()

    output_path = Path(args.output) if args.output else _ROOT / "audit" / "report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")

    if not args.quiet:
        print(render_summary_table(report))
        print(f"\nJSON report written to: {output_path}")

    if args.fail_on == "never":
        return 0
    if args.fail_on == "warnings":
        return min(report.exit_code, 2)
    return 2 if report.total_blocking > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
