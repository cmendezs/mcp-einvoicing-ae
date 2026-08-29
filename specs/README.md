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
- `shared/ubl-2.1/common/` — the public OASIS UBL 2.1 base schemas (`UBL-CommonBasicComponents`,
  `UBL-CommonAggregateComponents`, `UBL-CommonExtensionComponents`, `UBL-UnqualifiedDataTypes`/
  `QualifiedDataTypes`, `CCTS_CCT_SchemaModule`, `CoreComponentParameters`, and the signature/XAdES
  schemas they transitively `xsd:import`). Copied verbatim (2026-08-29) from
  `mcp-invoicenow-sg/specs/shared/ubl-2.1/common/`, which vendors the identical public OASIS
  `os-UBL-2.1/xsdrt/common/` release that `peppol-tdd-1.0.0.xsd`'s own `schemaLocation` attributes
  point at (verified: same namespace URIs, same OASIS release path). Not a fresh fetch — these
  are the exact bytes SG already vendored and uses to compile its own UBL 2.1 documents; AE's
  `.xsd` files still declare their `schemaLocation` as the absolute `docs.oasis-open.org` URL
  (unchanged), so a local XSD compiler needs to resolve those imports against this directory (by
  filename, via a custom resolver, or a working-directory copy) rather than fetching over the
  network. See "Pending specs" below — no AE code currently compiles or consumes these files.

**2026-08-27 (Phase D):** five compiled `.xslt` stylesheets and the TDD XSD were copied from here
into `src/mcp_einvoicing_ae/rules/` for wheel bundling, mirroring `mcp-einvoicing-de`'s `rules/`
pattern (`specs/` itself is dev-reference-only, never published — see
`context-library/decisions/specs-directory-convention.md`). Only one copy per profile is bundled:
`pint-ae/trn-invoice/schematron/PINT-jurisdiction-aligned-rules.xslt` and
`pint-ae/trn-creditnote/schematron/PINT-jurisdiction-aligned-rules.xslt` are byte-identical
(confirmed 2026-08-27), as are the two profiles' own `trn-invoice`/`trn-creditnote` UBL-validation
stylesheets and the billing/self-billing jurisdiction-aligned rules — see
`src/mcp_einvoicing_ae/validators/schematron.py`'s module docstring for the full breakdown.

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
| Federal Decree-Law No. 46 of 2021 (Electronic Transactions and Trust Services) | n/a (unofficial translation) | https://uaelegislation.gov.ae/en/legislations/2585 ; also https://u.ae/en/about-the-uae/digital-uae/regulatory-framework/electronic-transactions-and-trust-services-law | 2026-08-26 (doc); URL added 2026-08-27 |
| Federal Decree-Law No. 14 of 2023 (Concerning the Modern Technology-Based Trade) | n/a (unofficial translation) | https://uaelegislation.gov.ae/en/legislations/2150 | 2026-08-27 |
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
distinct instrument from Federal Decree-Law No. 46 of 2021 already tracked above.

**2026-08-27 update (round 4):** the user supplied the Federal Decree-Law No. 14 of 2023 PDF
(now at `specs/legal/Federal-Decree-by-Law-No-14-of-2023-Concerning-the-Modern-Technology-Based-Trade.pdf`)
and its authority URL, `https://uaelegislation.gov.ae/en/legislations/2150` — the UAE's official
legislation portal. Reading the local PDF confirms the connection to e-invoicing: Article (5)(8)
obligates a "digital trader" to provide "a detailed non-paper invoice through Modern Technology
regarding the purchase of goods and services." This is a **B2C/consumer-facing** obligation on
digital traders generally, distinct in scope from the FTA's B2B/B2G PINT AE regime — it is not
itself a PINT AE format requirement, and no assumption is made here about whether or how it
constrains the invoice model. The user also supplied two files for Federal Decree-Law No. 46 of
2021: one is byte-identical (MD5 `c6ab428c...`) to the copy already held in `specs/legal/`; the
other (`Federal Decree Law No 46 OF 2021 On Electronic Transactions and Trust Services EN.pdf`,
29pp/525KB vs. the held 45pp/224KB) is a different rendition of the same unofficial-translation
text — confirmed by reading both cover pages, which carry identical title and near-identical
enacting recitals in a different layout. Not added as a second file since it carries no
additional normative content over the copy already held; see "Excluded sources" below. The two
authority URLs supplied for Federal Decree-Law No. 46 of 2021
(`https://uaelegislation.gov.ae/en/legislations/2585` and
`https://u.ae/en/about-the-uae/digital-uae/regulatory-framework/electronic-transactions-and-trust-services-law`)
resolve its previously open Authority URL cell. As with prior updates, none of these URLs was
fetched or browsed by this assistant.

## Pending specs

None of the three items below block the v0.1.0 publish — this release ships document models,
Schematron-based validation, and generate/validate/parse MCP tools; none of it depends on the
missing pieces described here. Each is tracked with full detail in
`context-library/countries/ae.md` ("Known gaps and open items") and
`context-library/roadmap-2026.md`, and will be revisited when it becomes load-bearing for a
future release.

| Document | Status | Notes |
|---|---|---|
| OASIS UBL 2.1 base XSD (Invoice / CreditNote) | `[VENDORED — 2026-08-29, not yet consumed by code]` | PINT AE's examples and `tdd/common/peppol-tdd-1.0.0.xsd` reference these via `schemaLocation`, and the base OASIS schemas were not included in any of the three originally supplied ZIPs. Now copied into `shared/ubl-2.1/common/` from `mcp-invoicenow-sg`'s identical vendored copy (see "Directory layout" above), so a future XSD-level wire validator has the files available. No AE code currently implements XSD-level TDD or invoice validation — Schematron-level validation (both PINT AE invoices and the TDD) does not depend on this schema and is unaffected either way. Implementing the TDD leg itself (serialize + XSD validate + transport) remains parked behind the still-open transport-channel question below (AE-LC-1). |
| Independent OpenPeppol jurisdiction-registry confirmation | `[NOT BLOCKING]` | The UAE Peppol Authority's own "Status: Final" release notes and the FTA's "published on its website" statement are strong, dated, regulator-sourced evidence that PINT AE is published — sufficient corroboration for this release. The likely registry URL is known (https://docs.peppol.eu/poac/ae/, supplied 2026-08-27), but its content has not been read or fetched by this assistant, per project convention (normative sources come from user-supplied local files or user-pasted text only, never a fetch). Upgrades from "strong evidence" to "independently confirmed" if the user visits the page and reports or pastes its content. |
| TDD transport mechanism | `[DEFERRED — out of scope for this release]` | None of the supplied TDD documents state whether the 5th-corner reporting document travels over the same AS4/Peppol channel as the PINT AE invoice or a separate channel. `mcp_einvoicing_ae/models/tdd.py` deliberately implements no transport binding, and no transport code ships in this version — this becomes relevant only once a transport implementation is added, and Phase C (2026-08-27) already confirmed it is a documentation question, not a core-library gap (`PeppolTransmitter`/`BaseEInvoicingClient` already accept either answer generically). |

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
| `Federal Decree Law No 46 OF 2021 On Electronic Transactions and Trust Services EN.pdf` (from `Downloads/`, 2026-08-27) | A different-source rendition of the same unofficial-translation text already held at `specs/legal/Federal-Decree-by-Law-No-46-of-2021-on-Electronic-Transactions-and-Trust-Services.pdf` (confirmed by reading both cover pages and enacting recitals — same law, same title, different layout/pagination, 29pp/525KB vs. the held 45pp/224KB). Not byte-identical, but carries no additional normative content over the copy already held, so a second copy is not kept. |
