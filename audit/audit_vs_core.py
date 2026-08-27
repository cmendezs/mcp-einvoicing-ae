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
]

_INTENTIONAL_OVERRIDES: dict[str, set[str]] = {}


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
