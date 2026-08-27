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
| PINT AE (billing) | 1.0.4 (2026-06-02, "Status: Final") | https://docs.peppol.eu/poac/ae/ | 2026-08-26 (docs); URL added 2026-08-27 |
| PINT AE self-billing | Same release train as PINT AE billing (see `pint-ae-self-billing/common/docs/pint-ae-self-billing-release-notes.pdf` for its own version history) | https://docs.peppol.eu/poac/ae/ | 2026-08-26 (docs); URL added 2026-08-27 |
| Peppol AE TDD (tax data document, 5th-corner reporting) | 1.0.3 (2026-05-25, "Status: Final") | https://docs.peppol.eu/poac/ae/ | 2026-08-26 (docs); URL added 2026-08-27 |
| UAE Electronic Invoicing Guidelines | V1.1, 01 June 2026 | https://u.ae/en/information-and-services/business/important-digital-services/digital-invoicing | 2026-08-26 (docs); URL added 2026-08-27 |
| UAE Electronic Invoice — mandatory fields | V1.0, 23 Feb 2026 | https://u.ae/en/information-and-services/business/important-digital-services/digital-invoicing | 2026-08-26 (docs); URL added 2026-08-27 |
| Considerations for selecting an ASP | V1.0, 23 Feb 2024 | https://u.ae/en/information-and-services/business/important-digital-services/digital-invoicing | 2026-08-26 (docs); URL added 2026-08-27 |
| UAE FTA e-Invoicing compliance page (statutory rules, EmaraTax onboarding, Pre-Approved ASP list) | n/a | https://tax.gov.ae/en/taxes/Vat/uae.einvoicing.aspx | 2026-08-27 |
| Federal Decree-Law No. 46 of 2021 (Electronic Transactions and Trust Services) | n/a | [NEED: legislation/gazette portal URL — not hosted on the MOF e-invoicing initiative page, and absent from the u.ae digital-invoicing page's own legal-reference list] | 2026-08-26 |
| VAT Decree-Law No. 8 of 2017 | n/a (unofficial translation) | https://u.ae/en/information-and-services/business/important-digital-services/digital-invoicing | 2026-08-26 (doc); URL added 2026-08-27 |
| Ministerial Decision No. 243 of 2025 (Electronic Invoicing System) | n/a | https://mof.gov.ae/en/about-us/initiatives/einvoicing/ | 2026-08-26 (doc); URL added 2026-08-27 |
| Ministerial Decision No. 244 of 2025 (Implementation of the Electronic Invoicing System) | n/a | https://mof.gov.ae/en/about-us/initiatives/einvoicing/ | 2026-08-26 (doc); URL added 2026-08-27 |
| Ministerial Decision — Eligibility and Accreditation procedure for Service Providers (No. 64 of 2025) | n/a | https://mof.gov.ae/en/about-us/initiatives/einvoicing/ | 2026-08-26 (doc); URL added 2026-08-27 |
| Ministerial Resolution No. 56 of 2026 (amending Resolution No. 64 of 2025) | n/a | https://mof.gov.ae/en/about-us/initiatives/einvoicing/ | 2026-08-26 (doc); URL added 2026-08-27 |
| Ministerial Resolution No. 66 of 2026 (amending Resolution No. 244 of 2025) | n/a | https://mof.gov.ae/en/about-us/initiatives/einvoicing/ | 2026-08-26 (doc); URL added 2026-08-27 |
| Cabinet Decision No. 106 of 2025 (Violations and Penalties, e-Invoicing) | n/a | https://mof.gov.ae/en/about-us/initiatives/einvoicing/ | 2026-08-26 (doc); URL added 2026-08-27 |

**2026-08-27 update (round 2):** the user identified
`https://mof.gov.ae/en/about-us/initiatives/einvoicing/` as the Ministry of Finance page hosting
the Legislative Documents section, and pasted that page's own document cards (title text plus
file size, e.g. "Ministerial Resolution No. (66) of 2026 ... (85 KB, PDF)") confirming it lists
six of the eight legal instruments: Ministerial Decisions 243 and 244 of 2025, the SP
eligibility/accreditation decision, Ministerial Resolutions 56 and 66 of 2026, and Cabinet
Decision 106 of 2025. Recorded as a citation for facts already established from the local PDFs;
the page itself was not fetched or browsed. Federal Decree-Law No. 46 of 2021 and VAT Decree-Law
No. 8 of 2017 did not appear among the six cards shown and still need their own
legislation/gazette-portal URL — they are general UAE legislation, not e-invoicing-initiative
documents, so a different MOF/legislation-portal page likely hosts them.

**2026-08-27 update (round 3):** the user pasted the "Electronic Invoicing System" section of
`https://u.ae/en/information-and-services/business/important-digital-services/digital-invoicing`
(the same page already cited for the three FTA guidance PDFs). That section links VAT Decree-Law
No. 8 of 2017 directly (labeled "PDF, 1 MB", consistent with the file already held at
`specs/legal/VAT-Decree-Law-No-8-of-2017.pdf`) — resolving its Authority URL above — and also
links Ministerial Decision No. 243 of 2025 (already resolved via the MOF page; this is a second,
consistent citation, not a conflict). It also names a document not previously in this list:
**Federal Decree-Law No. 14 of 2023 (Concerning the Modern Technology-based Trade)**. This is a
distinct instrument from Federal Decree-Law No. 46 of 2021 already tracked above — see the new
"Pending specs" row below. As before, the page itself was not fetched or browsed; only the
titles and labels the user pasted were used.

## Pending specs

| Document | Status | Notes |
|---|---|---|
| OASIS UBL 2.1 base XSD (Invoice / CreditNote) | `[NEED:]` | PINT AE's examples reference these via `schemaLocation` but the base OASIS schemas were not included in any of the three supplied ZIPs. Needed for local wire-schema validation. |
| Independent OpenPeppol jurisdiction-registry confirmation | `[NEED:]` | The UAE Peppol Authority's own "Status: Final" release notes and the FTA's "published on its website" statement are strong evidence PINT AE is published. The likely registry URL is now known (https://docs.peppol.eu/poac/ae/, supplied 2026-08-27), but its content has not been read or fetched by this assistant — per project convention, normative sources are read from user-supplied local files or user-pasted text only, never fetched. Not blocking (see gate note above). Closes out if the user visits the page and reports what it says, or pastes its content. |
| TDD transport mechanism | `[NEED:]` | None of the supplied TDD documents state whether the 5th-corner reporting document travels over the same AS4/Peppol channel as the PINT AE invoice or a separate channel. |
| Federal Decree-Law No. 14 of 2023 (Concerning the Modern Technology-based Trade) | `[NEED:]` | Named on the u.ae digital-invoicing page (2026-08-27) alongside VAT Decree-Law No. 8 of 2017 and Ministerial Decision No. 243 of 2025 as a legal basis for e-invoicing. No PDF has been supplied yet, and its relevance relative to the already-tracked Federal Decree-Law No. 46 of 2021 (Electronic Transactions and Trust Services) has not been assessed — they may be complementary, not alternatives. Do not assume either supersedes the other without reading both texts. |

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
