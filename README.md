# mcp-einvoicing-ae 🇦🇪

[English](README.md) | [العربية](README.ar.md)

<!-- mcp-name: io.github.cmendezs/mcp-einvoicing-ae -->

[![PyPI version](https://badge.fury.io/py/mcp-einvoicing-ae.svg)](https://badge.fury.io/py/mcp-einvoicing-ae)
[![Python](https://img.shields.io/pypi/pyversions/mcp-einvoicing-ae.svg)](https://pypi.org/project/mcp-einvoicing-ae/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

> **v0.2.0 published 2026-08-28.** `AEInvoice`, `AEParty`, `AETaxDataDocument`, and the
> `generate`/`validate`/`parse` MCP tools are live on PyPI and the MCP registry.
> `validate_invoice_ae` now checks core's shared CEN EN16931 base Schematron rather than the
> self-compiled OpenPeppol-derived stylesheets v0.1.0 bundled without confirmed redistribution
> rights; `validate_tdd_ae` currently reports "unavailable" — see
> [Supported standards](#supported-standards) and [Tools](#tools) below.

---

## Introduction

`mcp-einvoicing-ae` is an [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server
that exposes tools for United Arab Emirates electronic invoicing. It is part of the
`mcp-einvoicing-*` family of country-specific servers, all built on
[`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core), which provides the
shared validation engine, EN 16931 abstractions, and Peppol network utilities.

---

## Current status

Normative specifications and FTA guidelines were supplied on 2026-08-26, resolving the
publication-status gate and the invoice-tree pathway. The core-gap check (2026-08-27) added
`TaxIdentifier.validate_ae_trn()` to `mcp-einvoicing-core` v1.22.0 and confirmed the profile-URN
and TDD-transport questions were not core gaps at all. Model, validator, and MCP tool code all
landed the same day, and `v0.1.0` published the same week.

| Area | Status |
|---|---|
| Repository, CI, governance docs | Done |
| Package skeleton (`src/` layout, server entry point) | Done |
| PINT AE publication status | **Confirmed** (2026-08-26) |
| Normative specifications under `specs/` | **Supplied** (2026-08-26) |
| Invoice-tree pathway | **Confirmed** — `EN16931Invoice` |
| Supported standards and profile URNs | **Known** — see below |
| Core-gap check (`mcp-einvoicing-core`) | **Done** — `TaxIdentifier.validate_ae_trn()`, core v1.22.0 |
| `AEInvoice` / `AEParty` (billing + self-billing) | **Implemented** (2026-08-27) |
| `AETaxDataDocument` (Peppol AE TDD model) | **Implemented** — no validation available (see below) |
| Invoice validation (`validate_invoice_ae`) | **CEN EN16931 base only** (v0.2.0, 2026-08-28) — the PINT AE jurisdiction overlay and TDD Schematron/XSD v0.1.0 bundled had no confirmed redistribution rights and were removed; see [Supported standards](#supported-standards) |
| `profile_registry` registration (PINT AE URNs) | **Done** |
| MCP tools (generate / validate / parse) | **Implemented** (2026-08-27) — see [Tools](#tools) |
| First release (`v0.1.0`) | **Published** (2026-08-27) — PyPI and MCP registry |
| Licensing fix release (`v0.2.0`) | **Published** (2026-08-28) — see [`CHANGELOG.md`](CHANGELOG.md) |

### The publication gate — resolved 2026-08-26

At the prior verification of the OpenPeppol jurisdiction PINT documentation index (2026-06-29),
the published jurisdiction profiles were the EU, Singapore, Australia and New Zealand, Japan,
and Malaysia; the UAE was absent. Documents supplied on 2026-08-26 resolve this: the UAE Peppol
Authority's own release notes record PINT AE (billing) at **"Status: Final"**, version 1.0.4,
released 2026-06-02, and the Peppol AE Tax Data Document (TDD — the 5th-corner reporting
document) at **"Status: Final"**, version 1.0.3, released 2026-05-25. The FTA's own June 2026
guideline states directly that the PINT-AE billing specifications *"are published on its
website."*

One caveat remains open: this is the specialization publisher's own release-status label, not an
independently observed OpenPeppol governance-registry page — strong evidence, not full
certainty. Full detail and citations: [`specs/README.md`](specs/README.md) and the monorepo's
[`context-library/countries/ae.md`](https://github.com/cmendezs/mcp-einvoicing/blob/main/context-library/countries/ae.md).

---

## Supported standards

- **PINT AE (billing)** — UBL 2.1, `CustomizationID: urn:peppol:pint:billing-1@ae-1`,
  `ProfileID: urn:peppol:bis:billing`. Version 1.0.4 (2026-06-02).
- **PINT AE (self-billing)** — `CustomizationID: urn:peppol:pint:selfbilling-1@ae-1`,
  `ProfileID: urn:peppol:bis:selfbilling`.
- **Peppol AE TDD** (Tax Data Document) — the 5th-corner reporting document sent to the FTA; its
  own XML namespace (`urn:peppol:schema:taxdata:1.0`), not a UBL invoice. Version 1.0.3
  (2026-05-25).

The UAE programme is a decentralized Peppol **5-corner** model routed through Accredited Service
Providers, adding a tax-authority reporting leg (the TDD above) beyond the 4-corner exchange used
elsewhere in this family. The invoice-tree pathway is confirmed `EN16931Invoice` (PINT AE is a
UBL 2.1 CIUS of EN 16931-1:2017) — no JSON binding was found in the supplied specifications.

`AEInvoice` reuses `mcp_einvoicing_core.wire_formats.EN16931UBLSerializer`/`EN16931UBLParser`
directly rather than a bespoke serializer, since `profile`/`business_process` hold the real
Peppol URNs. `AEParty.vat_id` carries the 15-digit TRN, format-validated via
`TaxIdentifier.validate_ae_trn()` (core v1.22.0); the Peppol participant ID (TIN) is auto-derived
as its first 10 digits. `AETaxDataDocument` models the TDD's mandatory fields but is not a UBL
invoice and is not built on `AEInvoice`. MCP tools reuse this stack directly — see
[Tools](#tools) for what's covered and what isn't. The TDD transport channel (same AS4 channel as
the invoice, or a separate one) remains an open documentation question, not a code gap. Full
detail: [`specs/README.md`](specs/README.md).

**Validation scope, as of v0.2.0:** `validate_invoice_ae` checks the CEN EN16931 base Schematron
only (structural + arithmetic/totals rules, shared with `mcp-einvoicing-be`/`mcp-ksef-pl`) — not
the PINT AE jurisdiction overlay (`ibr-*-ae` rules). `BR-CO-09` (VAT identifier must carry an ISO
3166-1 alpha-2 prefix) is expected to fire on every genuine AE invoice, since UAE TRNs carry no
country prefix; this is disclosed in every result, not a defect in your data. `validate_tdd_ae`
currently has no validation available at all. v0.1.0 bundled five self-compiled files derived
from OpenPeppol's PINT AE and TDD Schematron/XSD sources with no confirmed redistribution
rights — removed in v0.2.0. See [`CHANGELOG.md`](CHANGELOG.md) and this monorepo's
[`context-library/decisions/peppol-schematron-artifact.md`](https://github.com/cmendezs/mcp-einvoicing/blob/main/context-library/decisions/peppol-schematron-artifact.md).

---

## Installation

### Requirements

- Python ≥ 3.11
- [`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core) (installed
  automatically as a dependency)

### Using `uvx` (recommended)

```bash
uvx mcp-einvoicing-ae
```

### Using `uv`

```bash
uv add mcp-einvoicing-ae
```

### From source

```bash
git clone https://github.com/cmendezs/mcp-einvoicing-ae.git
cd mcp-einvoicing-ae
uv sync --all-extras
```

---

## Configuration

Add the server to your MCP client configuration:

```json
{
  "mcpServers": {
    "einvoicing-ae": {
      "command": "uvx",
      "args": ["mcp-einvoicing-ae"]
    }
  }
}
```

### Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `LOG_LEVEL` | No | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, or `ERROR` |

Country-specific variables (transport endpoints, credentials, environment switches) are added
once the specification documents them. See [`.env.example`](.env.example).

---

## Tools

| Tool | Description |
|---|---|
| `generate_invoice_ae` | Generate a PINT AE UBL 2.1 invoice XML (billing or self-billing) from structured data. Only the EN 16931 core field set is emitted — `AEParty.trade_license_number` has no mapping in core's generic UBL serializer yet and is dropped from the output. |
| `validate_invoice_ae` | Validate a PINT AE UBL 2.1 invoice against core's shared CEN EN16931 base Schematron (structural + arithmetic/totals rules only — not the PINT AE jurisdiction overlay). Requires the `xslt2` extra. |
| `validate_tdd_ae` | Always returns an explicit "unavailable" result — no licensed validation artifact is currently available for the Peppol AE Tax Data Document (TDD). |
| `parse_invoice_ae` | Parse a PINT AE UBL 2.1 invoice XML into a structured dict (EN 16931 core field set only — AE-specific extensions such as `trade_license_number` are not extracted). |

`generate_invoice_ae`/`validate_invoice_ae`/`parse_invoice_ae` require `mcp-einvoicing-ae[xslt2]`
(bundles `saxonche`) for the base Schematron validator to load; without it, `validate_invoice_ae`
returns an explicit "unavailable" result rather than a silent pass.

The tool reference in [`docs/TOOLS.md`](docs/TOOLS.md) is generated from the running server:

```bash
uv run python scripts/gen_tool_reference.py
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, the test and lint commands, and
the pull request checklist. Security issues follow the private disclosure process in
[SECURITY.md](SECURITY.md).

---

## Other e-invoicing MCP servers

| Country | Server |
|---------|--------|
| 🌍 Global | [mcp-einvoicing-core](https://github.com/cmendezs/mcp-einvoicing-core) |
| 🇧🇪 Belgium | [mcp-einvoicing-be](https://github.com/cmendezs/mcp-einvoicing-be) |
| 🇧🇷 Brazil | [mcp-nfe-br](https://github.com/cmendezs/mcp-nfe-br) |
| 🇫🇷 France | [mcp-facture-electronique-fr](https://github.com/cmendezs/mcp-facture-electronique-fr) |
| 🇩🇪 Germany | [mcp-einvoicing-de](https://github.com/cmendezs/mcp-einvoicing-de) |
| 🇮🇹 Italy | [mcp-fattura-elettronica-it](https://github.com/cmendezs/mcp-fattura-elettronica-it) |
| 🇵🇱 Poland | [mcp-ksef-pl](https://github.com/cmendezs/mcp-ksef-pl) |
| 🇸🇬 Singapore | [mcp-invoicenow-sg](https://github.com/cmendezs/mcp-invoicenow-sg) |
| 🇪🇸 Spain | [mcp-facturacion-electronica-es](https://github.com/cmendezs/mcp-facturacion-electronica-es) |
| 🇦🇪 United Arab Emirates | [mcp-einvoicing-ae](https://github.com/cmendezs/mcp-einvoicing-ae) |

---

## License

This project is licensed under the **Apache 2.0** license — see [LICENSE](LICENSE) for details.
