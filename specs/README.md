# mcp-einvoicing-ae — Specification assets

This directory holds the normative source material for the UAE's e-invoicing standard(s) —
official PDFs, XSD/XSLT schemas, WSDL/Swagger files, and other primary documents. Values
derived from these documents belong in
[`context-library/countries/ae.md`](../../context-library/countries/ae.md), not in code and
not duplicated as a new file in this directory.

Normative sources are never web-fetched for this package (per project convention). Download
each document yourself and drop it in this directory. What gets committed versus excluded
follows [`context-library/decisions/specs-directory-convention.md`](../../context-library/decisions/specs-directory-convention.md).

> **Gate specific to the UAE — resolved 2026-08-26.** The last local verification (2026-06-29)
> found PINT AE absent from the published OpenPeppol jurisdiction PINT list
> (`context-library/countries/be.md:81`). The documents below resolve that gate:
> - PINT AE (billing): **"Status: Final"**, v1.0.4, released 2026-06-02
>   (`pint-ae/common/docs/pint-ae-billing-release-notes.pdf`).
> - PINT AE TDD (the 5th-corner tax-authority reporting document): **"Status: Final"**, v1.0.3,
>   released 2026-05-25 (`tdd/common/docs/tdd-release-notes.pdf`).
> - The FTA's own guideline (dated 01 June 2026) states directly: *"These requirements are set
>   out in detail within Peppol's PINT-AE billing specifications, which are **published** on
>   its website."* (`guidelines/UAE-Electronic-Invoicing-Guidelines_V-1.1-01June2026.pdf`).
>
> **Caveat, not fully closed:** the "Final"/"Published" labels above are the UAE Peppol
> Authority's own release-status terminology for its specialization documents, not an
> independently observed OpenPeppol jurisdiction-registry page. Treat this as strong evidence
> the gate is resolved, not certainty that it matches OpenPeppol's own governance-lifecycle
> vocabulary term-for-term.

## Directory layout

One subdirectory per standard/system, since more than one has accumulated:

- `legal/` — primary UAE legislation and regulatory decisions (Federal Decree-Law, VAT
  Decree-Law, Ministerial Decisions/Resolutions, Cabinet Decision on penalties).
- `guidelines/` — FTA operational guidance: the main Electronic Invoicing Guidelines, the
  mandatory-fields specification, and Accredited Service Provider selection considerations.
- `pint-ae/` — PINT AE billing specification (UBL 2.1 Invoice + CreditNote): schematron, XSLT,
  codelists, ~26 example documents, and the BIS/release-notes/compliance docs under
  `common/docs/`.
- `pint-ae-self-billing/` — the PINT AE self-billing variant, same structure as `pint-ae/`.
- `tdd/` — the Peppol AE Tax Data Document (the 5th-corner reporting document sent to the FTA):
  XSD (`common/peppol-tdd-1.0.0.xsd`), schematron, codelists, examples, and `common/docs/`.

## Sources and versions

| Standard | Version | Authority URL | Retrieved |
|---|---|---|---|
| PINT AE (billing) | 1.0.4 (2026-06-02, "Status: Final") | [NEED: OpenPeppol PINT AE documentation portal URL — not stated inside the supplied documents themselves] | 2026-08-26 |
| PINT AE self-billing | Same release train as PINT AE billing (see `pint-ae-self-billing/common/docs/pint-ae-self-billing-release-notes.pdf` for its own version history) | [NEED: as above] | 2026-08-26 |
| Peppol AE TDD (tax data document, 5th-corner reporting) | 1.0.3 (2026-05-25, "Status: Final") | [NEED: as above] | 2026-08-26 |
| UAE Electronic Invoicing Guidelines | V1.1, 01 June 2026 | [NEED: FTA / u.ae publication page URL] | 2026-08-26 |
| UAE Electronic Invoice — mandatory fields | V1.0, 23 Feb 2026 | [NEED: as above] | 2026-08-26 |
| Considerations for selecting an ASP | V1.0, 23 Feb 2024 | [NEED: as above] | 2026-08-26 |
| Federal Decree-Law No. 46 of 2021 (Electronic Transactions and Trust Services) | n/a | [NEED: UAE Ministry of Justice / official gazette URL] | 2026-08-26 |
| VAT Decree-Law No. 8 of 2017 | n/a (unofficial translation) | [NEED: FTA official gazette URL] | 2026-08-26 |
| Ministerial Decision No. 243 of 2025 (Electronic Invoicing System) | n/a | [NEED:] | 2026-08-26 |
| Ministerial Decision No. 244 of 2025 (Implementation of the Electronic Invoicing System) | n/a | [NEED:] | 2026-08-26 |
| Ministerial Decision — Eligibility and Accreditation procedure for Service Providers (No. 64 of 2025) | n/a | [NEED:] | 2026-08-26 |
| Ministerial Resolution No. 56 of 2026 (amending Resolution No. 64 of 2025) | n/a | [NEED:] | 2026-08-26 |
| Ministerial Resolution No. 66 of 2026 (amending Resolution No. 244 of 2025) | n/a | [NEED:] | 2026-08-26 |
| Cabinet Decision No. 106 of 2025 (Violations and Penalties, e-Invoicing) | n/a | [NEED:] | 2026-08-26 |

The `[NEED:]` markers in the "Authority URL" column reflect that these documents were supplied
as local files without an accompanying source URL captured at download time — not that the
standard/version itself is unconfirmed. Fill in the URL if/when the user provides it; do not
guess or web-fetch it (per project convention).

## Pending specs

| Document | Status | Notes |
|---|---|---|
| OASIS UBL 2.1 base XSD (Invoice / CreditNote) | `[NEED:]` | PINT AE's examples reference these via `schemaLocation` but the base OASIS schemas were not included in any of the three supplied ZIPs. Needed for local wire-schema validation. |
| Independent OpenPeppol jurisdiction-registry confirmation | `[NEED:]` | The UAE Peppol Authority's own "Status: Final" release notes and the FTA's "published on its website" statement are strong evidence PINT AE is published, but no OpenPeppol governance/registry page was among the supplied documents. Not blocking (see gate note above), but worth closing out if a session is ever permitted to check it. |
| TDD transport mechanism | `[NEED:]` | None of the supplied TDD documents state whether the 5th-corner reporting document travels over the same AS4/Peppol channel as the PINT AE invoice or a separate channel. |

## Non-file sources

Nothing pasted in chat needed retention this round — all facts below came from the documents
themselves, cited by file and page/section in `context-library/countries/ae.md`. If future facts
arrive by chat-paste rather than as a document, record the URL and retrieval date in the table
above, add a note here that no local file is retained for that row, and fold the actual content
into `context-library/countries/ae.md` rather than inventing a markdown file here to hold it.

## Excluded sources

Per `context-library/decisions/specs-directory-convention.md`, the following were deliberately
**not** copied into this directory:

| File (in the original `Downloads/AE` drop) | Reason |
|---|---|
| `UAE-Electronic-Invoicing-Guidelines_V-1.0-23Feb2026.pdf` | Byte-identical duplicate (same MD5) of `guidelines/UAE-Electronic-Invoicing-Guidelines_V-1.1-01June2026.pdf`, despite the different filename/version label — the file's own internal content is V1.1. |
| `UAE-eInvoicing-Programme-09Feb2026.pdf` | PowerPoint-derived FTA programme/roadmap overview deck (20 slides, ~9.8MB) — explanatory/promotional material aimed at businesses, not a technical or legal specification. Carries no field, rate, rule, or namespace the code needs to cite. |
| `UAE-eInvoicing-Programme-30June2026.pdf` | Same as above, later revision (21 slides, ~3.4MB) — also excluded for the same reason. |
