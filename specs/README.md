# mcp-einvoicing-ae — Specification assets

This directory holds the normative source material for the UAE's e-invoicing standard(s) —
official PDFs, XSD/XSLT schemas, WSDL/Swagger files, and other primary documents. Values
derived from these documents belong in
[`context-library/countries/ae.md`](../../context-library/countries/ae.md), not in code and
not duplicated as a new file in this directory.

Normative sources are never web-fetched for this package (per project convention). Download
each document yourself and drop it in this directory.

> **Additional gate specific to the UAE.** PINT AE was absent from the published OpenPeppol
> jurisdiction PINT list at the last local verification (2026-06-29, recorded in
> `context-library/countries/be.md:81`, which lists EU, Singapore, AUNZ, Japan, and Malaysia).
> The first document below must therefore establish **publication status**, not only content.
> If only a draft or a data dictionary exists, this package stays a skeleton with no model code.

## Directory layout

No files have been supplied yet. Once documents arrive, use one subdirectory per
standard/system if more than one accumulates (e.g. `pint-ae/`, `ubl/`); a single-standard set
can stay flat, matching how single-standard packages like IT keep files at the top level.

## Sources and versions

| Standard | Version | Authority URL | Retrieved |
|---|---|---|---|
| UAE PINT AE specification / Data Dictionary | [NEED:] | [NEED:] | [NEED:] |
| 5-corner ASP model / accreditation documentation | [NEED:] | [NEED:] | [NEED:] |
| PINT AE Schematron (if published) | [NEED:] | [NEED:] | [NEED:] |
| UBL 2.1 Invoice + CreditNote XSD | 2.1 | [NEED:] | [NEED:] |
| FTA authority page (VAT rate, TRN format, mandate timeline) | n/a | [NEED:] | [NEED:] |

## Pending specs

| Document | Status | Notes |
|---|---|---|
| PINT AE specification | `[NEED:]` | Unblocks publication status, invoice-tree pathway (`_IS_EN16931_FAMILY`), `CustomizationID` / `ProfileID` URNs, and whether a JSON binding is normative alongside XML |
| 5-corner ASP model docs | `[NEED:]` | Unblocks transport design, ASP role, and whether the tax-authority reporting leg is a core gap |
| PINT AE Schematron | `[NEED:]` | Unblocks validator implementation and the country audit prompt rule IDs |
| UBL 2.1 XSD | `[NEED:]` | Unblocks wire-schema validation and namespace declarations |
| FTA authority page | `[NEED:]` | Unblocks VAT standard rate, TRN format and length, mandate effective dates |

## Non-file sources

Nothing has been supplied for this package yet — no chat-pasted content or dropped-in files.
If the user supplies facts by pasting text in chat rather than dropping a document under this
directory, record the URL and retrieval date in the table above, add a note here that no local
file is retained for that row, and fold the actual content into
[`context-library/countries/ae.md`](../../context-library/countries/ae.md) rather than
inventing a markdown file here to hold it.
