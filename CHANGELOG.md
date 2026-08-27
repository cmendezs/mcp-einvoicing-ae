# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

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

[0.1.0]: https://github.com/cmendezs/mcp-einvoicing-ae/releases/tag/v0.1.0
