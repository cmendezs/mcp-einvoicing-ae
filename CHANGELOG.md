# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.3.0] - 2026-08-29

Resolves the BLOCKING and now-actionable findings from the first AE compliance audit
(`audit/2026-08-audit-ae.md`, tracked in `context-library/audit-history.md`).

### Fixed
- **AE-SC-1 (BLOCKING): generated PINT AE invoices are now structurally conformant.**
  `generate_invoice_ae` previously reused core's unmodified `EN16931UBLSerializer`, which could
  not emit the unconditionally-mandatory `cbc:UUID` (BTAE-07), `cbc:ProfileExecutionID`
  (BTAE-02), or per-line `cac:ItemPriceExtension` (BTAE-10/BTAE-08) — every generated invoice was
  non-conformant, masked by v0.2.0's EN16931-base-only validation. Fixed via
  `mcp-einvoicing-core` v1.25.0 (`document_uuid` field + `cac:ItemPriceExtension` opt-in
  serializer flag) plus a new `AEUBLSerializer` (`mcp_einvoicing_ae/wire_formats.py`) that adds
  `cbc:ProfileExecutionID` and the `trade_license_number` `PartyLegalEntity/CompanyID`
  (`schemeAgencyID="TL"`). `AEInvoice.profile_execution_id` is now a required field
  (`^[01]{8}$`), and `document_uuid` (inherited from core) is enforced via a model validator.
- **AE-SC-3: `trade_license_number` now round-trips.** Previously accepted and validated on
  `AEParty` but silently dropped by generation and never re-extracted on parse. Generation now
  emits it (via `AEUBLSerializer`); `parse_invoice_ae` re-extracts it (plus `document_uuid` and
  `profile_execution_id`) from the raw XML and re-validates the result as `AEInvoice`.

### Added
- **AE-TC-1: the 5.00% standard VAT rate is now enforced.** `AEInvoiceLine` gained a model
  validator requiring `tax_rate == AE_STANDARD_VAT_RATE` for category `S`, and `tax_rate == 0`
  for `AE`/`E`/`O`/`Z` (the zero-rate constraint is definitionally safe per EN 16931
  `BR-{Z,E,AE,O}-05`, independent of any AE-specific citation).
- **AE-LC-2: Peppol participant lookup registered.** `server.py` now mounts core's
  `register_peppol_tools` plugin with an AE-specific TIN-based id adapter (scheme `0235`, first
  10 digits of the TRN).
- **AE-LC-1 (partial): OASIS UBL 2.1 base schemas vendored.** Copied from
  `mcp-invoicenow-sg`'s identical vendored copy into `specs/shared/ubl-2.1/common/`, unblocking a
  future XSD-level TDD validator. No XSD validation is implemented yet — the full TDD leg
  (serialize + validate + transport) stays parked behind the transport-channel question.

### Changed
- **AE-AG-1: audit gate cleaned up.** `audit/audit_vs_core.py`'s module-scan list was missing
  `tools/generation.py`, `tools/parsing.py`, `tools/validation.py`, and the new `wire_formats.py`
  — CHECK 1 was reporting ~90 core symbols as "unused" that were genuinely imported, just in
  unscanned files. Fixed the scan list and populated `_INTENTIONAL_OVERRIDES` for the remaining
  genuinely-unused symbols. CHECK 1 now runs 0 blocking / 0 warnings (down from 142).
- Core dependency pin bumped `>=1.23.0,<2.0.0` → `>=1.25.0,<2.0.0` (requires the new
  `document_uuid`/`ItemPriceExtension` core capabilities).

## [0.2.0] - 2026-08-28

### Fixed
- **Removed unlicensed bundled OpenPeppol-derived Schematron/XSD artifacts.**
  v0.1.0 shipped five self-compiled files with no confirmed redistribution
  rights: `pint-ubl-billing.xslt`, `pint-ubl-selfbilling.xslt`,
  `pint-jurisdiction-ae.xslt`, `peppol-ae-tdd.xslt`, and
  `peppol-tdd-1.0.0.xsd`. v0.1.0's docstrings argued the licensing blocker
  in `context-library/decisions/peppol-schematron-artifact.md` was "moot"
  here because the source files were supplied directly by the user rather
  than fetched from the web — that reasoning was wrong: being user-supplied
  only avoids Claude autonomously retrieving copyrighted material, it does
  not confer redistribution rights to bundle the content into a published
  wheel. Same gap already identified and fixed for `mcp-invoicenow-sg`
  v0.2.0, and already blocked-and-labeled honestly for `mcp-einvoicing-be`/
  `mcp-ksef-pl`'s Peppol overlay.

### Changed
- **`validate_invoice_ae` now runs core's shared, licensing-clean CEN
  EN16931 base Schematron** (`en16931_base_schematron_validator()` — the
  same artifact `mcp-einvoicing-be` v0.8.0 / `mcp-ksef-pl` v0.6.0 consume)
  in place of the two removed PINT AE stylesheets. Unlike
  `mcp-invoicenow-sg` (blocked by an unsourced GST-category crosswalk), AE
  has no equivalent blocker — `AEInvoice`'s tax category codes are already
  UNCL5305-derived (`Aligned-TaxCategoryCodes.gc`) and its `TaxScheme/ID` is
  already the literal `"VAT"` (core's unmodified `EN16931UBLSerializer`).
  Every result now carries `EN16931_BASE_ONLY_SCOPE_WARNING` (PINT-AE
  jurisdiction rules are not checked) and
  `EN16931_BASE_KNOWN_LIMITATIONS_WARNING` (`BR-CO-09` is expected to fire
  on every genuine AE invoice — UAE TRNs carry no ISO 3166-1 alpha-2
  prefix, confirmed against the government-supplied example fixture).
- **`validate_tdd_ae` now always returns an explicit `engine="unavailable"`
  result.** No licensing-clean substitute exists for the removed
  `peppol_ae_tdd` Schematron and `peppol-tdd-1.0.0.xsd` — the Peppol AE TDD
  is a distinct document type from an EN16931 UBL invoice, and core
  provides no TDD validation capability at all.
- **Known coverage loss, documented not silent**: the PINT-AE jurisdiction
  overlay (`ibr-*-ae` rules) and all TDD validation are no longer checked.
  See `EN16931_BASE_ONLY_SCOPE_WARNING` and `_TDD_VALIDATION_UNAVAILABLE` in
  `tools/validation.py`.

## [0.1.0] - 2026-08-27

### Added
- Initial package scaffold: `src/` layout, governance documents, CI and publish
  workflows, audit directory, and a stdio MCP server entry point with no tools
  registered yet.
- Normative specifications supplied under `specs/`; PINT AE publication-status
  gate resolved (2026-08-26). See `specs/README.md` and
  `context-library/countries/ae.md` in the root repo.
- `AEInvoice`/`AEParty`/`AEInvoiceLine` models (billing + self-billing via a
  `variant` constructor input), reusing `mcp_einvoicing_core.wire_formats`'s
  `EN16931UBLSerializer`/`EN16931UBLParser` directly. `AETaxDataDocument` model
  for the Peppol AE TDD (5th-corner reporting document, not a UBL invoice).
  PINT AE billing/self-billing profile URNs registered via
  `mcp_einvoicing_core.profile_registry`. Four bundled Schematron validators
  (PINT AE billing/self-billing UBL + jurisdiction rules, Peppol AE TDD),
  requiring the `xslt2` optional extra (`saxonche`). `_IS_EN16931_FAMILY`
  flipped to `True` in `audit/audit_vs_core.py`. (2026-08-27)
- Core dependency bumped to `mcp-einvoicing-core>=1.22.0,<2.0.0` for
  `TaxIdentifier.validate_ae_trn()`, then to `>=1.23.0,<2.0.0` at release time to match the
  latest published core version.
- MCP tools registered on the server: `generate_invoice_ae`, `validate_invoice_ae`,
  `validate_tdd_ae`, `parse_invoice_ae`. Generation and parsing reuse
  `mcp_einvoicing_core.wire_formats.EN16931UBLSerializer`/`EN16931UBLParser` directly
  (`AEInvoice`/`AEParty` add no bespoke serializer); validation dispatches to the four bundled
  Schematron stylesheets. Known limitation: `AEParty.trade_license_number` has no mapping in
  core's generic UBL serializer/parser and does not round-trip through `generate_invoice_ae`/
  `parse_invoice_ae`. `validate_tdd_ae` runs Schematron only and flags the missing XSD check
  explicitly in every result. (2026-08-27)

### Blocked
- Schema-level (XSD) validation of the Peppol AE TDD document —
  `peppol-tdd-1.0.0.xsd` imports the base OASIS `UnqualifiedDataTypes-2`
  schema, which has not been supplied. Schematron-level TDD validation is
  unaffected.
- The TDD reporting-leg transport channel (same AS4 channel as the invoice, or
  a separate one, e.g. a direct EmaraTax REST push) — undocumented in any
  supplied source; not a core gap either way, but blocks a transport
  implementation until resolved.

[0.2.0]: https://github.com/cmendezs/mcp-einvoicing-ae/releases/tag/v0.2.0
[0.1.0]: https://github.com/cmendezs/mcp-einvoicing-ae/releases/tag/v0.1.0
