# mcp-einvoicing-ae 🇦🇪

[English](README.md) | [العربية](README.ar.md)

<!-- mcp-name: io.github.cmendezs/mcp-einvoicing-ae -->

[![PyPI version](https://badge.fury.io/py/mcp-einvoicing-ae.svg)](https://badge.fury.io/py/mcp-einvoicing-ae)
[![Python](https://img.shields.io/pypi/pyversions/mcp-einvoicing-ae.svg)](https://pypi.org/project/mcp-einvoicing-ae/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

> **Scaffold stage — not yet published.** This repository contains the package skeleton only.
> No tools, models, or validators are implemented yet, and no release has been tagged.
> See [Current status](#current-status) for what is blocking implementation.

---

## Introduction

`mcp-einvoicing-ae` is an [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server
that will expose tools for United Arab Emirates electronic invoicing. It is part of the
`mcp-einvoicing-*` family of country-specific servers, all built on
[`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core), which provides the
shared validation engine, EN 16931 abstractions, and Peppol network utilities.

---

## Current status

The package is a scaffold, and it stays a scaffold for longer than its sibling packages by
design. Beyond the usual missing-specification gate, the UAE profile itself is not confirmed
as published.

| Area | Status |
|---|---|
| Repository, CI, governance docs | Done |
| Package skeleton (`src/` layout, server entry point) | Done |
| PINT AE publication status | **Unconfirmed** |
| Normative specifications under `specs/` | **Missing** |
| Supported standards and profile URNs | Blocked |
| Invoice model and validators | Blocked |
| MCP tools | Blocked |
| First release (`v0.1.0`) | Blocked |

### The publication gate

At the last verification of the OpenPeppol jurisdiction PINT documentation index (2026-06-29),
the published jurisdiction profiles were the EU, Singapore, Australia and New Zealand, Japan,
and Malaysia. The UAE was absent from that list. Public descriptions of a "PINT AE" profile
exist, but a description is not a normative specification and cannot establish a conformance
statement or a `CustomizationID`.

Implementation therefore waits on a document that establishes **publication status**, not only
content. If only a draft or a data dictionary exists, this package remains a documented
skeleton. See [`specs/sources.md`](specs/sources.md) for the document list.

---

## Supported standards

`[NEED: confirm from a published PINT AE specification]`

The UAE programme is described as a decentralized Peppol **5-corner** model routed through
Accredited Service Providers, which adds a tax-authority reporting leg beyond the 4-corner
exchange used elsewhere in this family. The wire syntax, profile URNs, EN 16931 conformance
relationship, and whether a JSON binding is normative alongside XML are all unresolved. This
section is filled in from the specification, not from memory.

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
