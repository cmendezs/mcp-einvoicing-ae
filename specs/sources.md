# Sources

> **BLOCKING — this file is not yet populated.** Audit gate CHECK 5 requires one authority URL
> per standard listed in `pyproject.toml`. Until the rows below are filled from documents placed
> in this directory, `mcp-einvoicing-ae` cannot pass its audit gate and cannot be published.
>
> Normative sources are never web-fetched for this package. Download each document yourself,
> drop it in `specs/`, and record the URL plus retrieval date here.
> Compliance values derived from these documents belong in
> [`context-library/countries/ae.md`](../../context-library/countries/ae.md), not in code.

> **Additional gate specific to the UAE.** PINT AE was absent from the published OpenPeppol
> jurisdiction PINT list at the last local verification (2026-06-29, recorded in
> `context-library/countries/be.md:81`, which lists EU, Singapore, AUNZ, Japan, and Malaysia).
> The first document below must therefore establish **publication status**, not only content.
> If only a draft or a data dictionary exists, this package stays a skeleton with no model code.

## Watch list

| Standard | Version | Authority URL | Retrieved |
|---|---|---|---|
| UAE PINT AE specification / Data Dictionary | [NEED:] | [NEED:] | [NEED:] |
| 5-corner ASP model / accreditation documentation | [NEED:] | [NEED:] | [NEED:] |
| PINT AE Schematron (if published) | [NEED:] | [NEED:] | [NEED:] |
| UBL 2.1 Invoice + CreditNote XSD | 2.1 | [NEED:] | [NEED:] |
| FTA authority page (VAT rate, TRN format, mandate timeline) | n/a | [NEED:] | [NEED:] |

## What each document unblocks

| Document | Unblocks |
|---|---|
| PINT AE specification | Publication status, invoice-tree pathway (`_IS_EN16931_FAMILY`), `CustomizationID` / `ProfileID` URNs, and whether a JSON binding is normative alongside XML |
| 5-corner ASP model docs | Transport design, ASP role, and whether the tax-authority reporting leg is a core gap |
| PINT AE Schematron | Validator implementation and the country audit prompt rule IDs |
| UBL 2.1 XSD | Wire-schema validation and namespace declarations |
| FTA authority page | VAT standard rate, TRN format and length, mandate effective dates |
