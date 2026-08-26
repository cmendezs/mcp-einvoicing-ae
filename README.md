# mcp-einvoicing-ae 🇦🇪

[English](README.md) | [العربية](README.ar.md)

<!-- mcp-name: io.github.cmendezs/mcp-einvoicing-ae -->

[![PyPI version](https://badge.fury.io/py/mcp-einvoicing-ae.svg)](https://badge.fury.io/py/mcp-einvoicing-ae)
[![Python](https://img.shields.io/pypi/pyversions/mcp-einvoicing-ae.svg)](https://pypi.org/project/mcp-einvoicing-ae/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

> **Specs supplied, package not yet published.** The PINT AE / TDD publication-status gate
> resolved on 2026-08-26 once normative specifications and FTA guidelines were supplied. No
> model, validator, or tool code exists yet, and no release has been tagged.
> See [Current status](#current-status) for what is still blocking implementation.

---

## Introduction

`mcp-einvoicing-ae` is an [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server
that will expose tools for United Arab Emirates electronic invoicing. It is part of the
`mcp-einvoicing-*` family of country-specific servers, all built on
[`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core), which provides the
shared validation engine, EN 16931 abstractions, and Peppol network utilities.

---

## Current status

Normative specifications and FTA guidelines were supplied on 2026-08-26, resolving the
publication-status gate and the invoice-tree pathway. Model, validator, and tool code do not
exist yet — a core-gap check in the shared `mcp-einvoicing-core` library is required first.

| Area | Status |
|---|---|
| Repository, CI, governance docs | Done |
| Package skeleton (`src/` layout, server entry point) | Done |
| PINT AE publication status | **Confirmed** (2026-08-26) |
| Normative specifications under `specs/` | **Supplied** (2026-08-26) |
| Invoice-tree pathway | **Confirmed** — `EN16931Invoice` |
| Supported standards and profile URNs | **Known** — see below |
| Core-gap check (`mcp-einvoicing-core`) | Pending |
| Invoice model and validators | Blocked (pending core-gap check) |
| MCP tools | Blocked |
| First release (`v0.1.0`) | Blocked |

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
Model code, validators, and tools await a core-gap check (`TaxIdentifier.validate_ae_trn()`,
PINT AE profile-registry constants, and the TDD transport mechanism are the known gaps). Full
detail: [`specs/README.md`](specs/README.md).

---

## Installation

### Requirements

- Python ≥ 3.11
- [`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core) (installed
  automatically as a dependency)

### Using `uvx` (recommended, once published)

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

None yet. The server starts and registers zero tools at this stage.

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
