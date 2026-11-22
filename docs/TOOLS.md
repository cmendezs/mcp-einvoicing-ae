# Tool reference — `mcp_einvoicing_ae`

This file is generated from the MCP server's tool registry by `scripts/gen_tool_reference.py`. Do not edit it by hand; run the script instead.

**Tools:** 18

## `check_document_type_id_in_codelist`

Check whether a (scheme, value) pair is a recognized Peppol document type identifier.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).
Searches all entries regardless of state, so a historical (deprecated
or removed) document type is still reported as found.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `scheme` | string | yes |  |  |
| `value` | string | yes |  |  |

## `check_participant_id_scheme_in_codelist`

Check whether a 4-digit ISO 6523 ICD code (e.g. "0208") is a recognized Peppol scheme.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `icd` | string | yes |  |  |

## `check_process_id_in_codelist`

Check whether a (scheme, value) pair is a recognized Peppol process identifier.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `scheme` | string | yes |  |  |
| `value` | string | yes |  |  |

## `generate_invoice_ae`

Generate a PINT AE UBL 2.1 e-invoice XML document from structured data.

Applies the correct CustomizationID (BT-24) and ProfileID (BT-23) for
the selected variant. All unconditionally-mandatory PINT AE elements
are emitted: ``cbc:UUID``, ``cbc:ProfileExecutionID``, per-line
``cac:ItemPriceExtension``, and ``PartyLegalEntity/CompanyID``
(``AEParty.trade_license_number``, when set).

Returns a dict with:
- ``xml``: the generated UBL 2.1 XML string
- ``customization_id``: the CustomizationID applied (BT-24)
- ``profile_id``: the ProfileID applied (BT-23)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `invoice_data` | object | yes |  | Invoice fields matching the AEInvoice schema |
| `variant` | string | no | `'billing'` | PINT AE profile variant: 'billing' (default) or 'selfbilling' |

## `generate_tdd_ae`

Generate a Peppol AE Tax Data Document (``pxs:TaxData``) XML from structured data.

The TDD is the 5th-corner report sent to the tax authority (via the
reporting service provider, C5) for each issued or received PINT AE
invoice. It carries its own namespace (``urn:peppol:schema:taxdata:1.0``),
a summary of the reported invoice, and the full source invoice embedded
in ``pxs:SourceDocument``. This tool builds the document only: sending it
is a Peppol access-point function (the TDD travels over the Peppol network
in an SBDH whose Sender/Receiver match ``ReportingParty``/``ReceivingParty``).

Rules enforced before emitting (TDD Schematron ibr-tdd-*): exactly one
reported transaction, reported-document identifiers and amounts present,
a source document present, a timezone on ``issue_time``, a mandatory
reporters representative, and receiver scheme ``0242``.

Returns a dict with:
- ``xml``: the generated ``pxs:TaxData`` XML string
- ``customization_id``: the CustomizationID applied
- ``profile_id``: the ProfileID applied

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `tdd_data` | object | yes |  | Tax Data Document fields matching the AETaxDataDocument schema |

## `get_peppol_codelist_version`

Report the OpenPeppol eDEC code list release version(s) currently configured locally.

_No parameters._

## `list_document_type_ids`

List Peppol document type identifiers from the OpenPeppol eDEC code list.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `active_only` | boolean | no | `True` | When True (default), omit deprecated/removed entries. |

## `list_participant_id_schemes`

List Peppol participant identifier (ICD) schemes from the OpenPeppol eDEC code list.

Requires EINVOICING_PEPPOL_CODELIST_DIR to point at a local copy of
the eDEC "Participant Identifier Schemes" GeneriCode export (not
bundled with this package, no confirmed redistribution rights, see
`mcp_einvoicing_core.peppol.codelists` module docstring).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `active_only` | boolean | no | `True` | When True (default), omit deprecated/removed entries. |

## `list_process_ids`

List Peppol process identifiers from the OpenPeppol eDEC code list.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `active_only` | boolean | no | `True` | When True (default), omit deprecated/removed entries. |

## `list_spis_use_case_ids`

List Peppol SPIS use case identifiers from the OpenPeppol eDEC code list.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `active_only` | boolean | no | `True` | When True (default), omit deprecated/removed entries. |

## `parse_invoice_ae`

Parse a PINT AE UBL 2.1 XML invoice into a structured dict.

Accepts a PINT AE billing or self-billing UBL 2.1 document (Invoice or
CreditNote root), extracts the EN 16931 core field set plus the AE
extensions (document_uuid, profile_execution_id, trade_license_number),
and re-validates the merged result as an AEInvoice — so TRN format and
tax-rate/category consistency are re-checked on parsed content, not just
on freshly constructed invoices.

Returns ``{"success": true, "invoice": {...}}`` on success, or
``{"success": false, "error": "..."}`` on parse or validation failure.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `xml_content` | string | yes |  | Raw PINT AE UBL 2.1 XML invoice content |

## `peppol_directory_search`

Search the Peppol Directory for registered participants.

Public, unauthenticated search (no relation to SMP lookup). At least
one of q/participant/name/country/doctype must be supplied.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `q` | string | null | no | `None` | General purpose query term, matched across all fields. |
| `participant` | string | null | no | `None` | Exact match on a scheme-qualified participant ID (e.g. "iso6523-actorid-upis::0208:0123456789"). |
| `name` | string | null | no | `None` | Partial match on business entity name (min. 3 characters). |
| `country` | string | null | no | `None` | Exact match on ISO 3166-2 country code. |
| `doctype` | string | null | no | `None` | Exact match on a full document type identifier URN. |
| `result_page_index` | integer | no | `0` | 0-based result page index. |
| `result_page_count` | integer | no | `20` | Results per page. |
| `environment` | string | no | `'production'` | "production" or "test". |

## `peppol_get_service_endpoint`

Fetch the AS4 endpoint for a Peppol participant's document type.

Resolves the SMP hostname via DNS, then fetches service metadata for
*document_type_id*. If the SMP returns a redirect, the result's
`redirect_url` is set and `endpoint_url` is None; callers must not
follow more than one redirect hop (SMP 1.4.0 §3.2).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `identifier` | string | yes |  | Peppol participant ID or adaptable national identifier. |
| `document_type_id` | string | no | `'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1'` | Peppol document type identifier URN (default: BIS Billing 3.0 invoice). |
| `environment` | string | no | `'production'` | "production" or "test". |

## `peppol_lookup_participant`

Check whether a business is registered on the Peppol network.

Performs a DNS-over-HTTPS U-NAPTR lookup followed by an SMP
service-group request to determine registration status and the list
of supported document type identifiers.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `identifier` | string | yes |  | Peppol participant ID ("<scheme>:<value>") or a bare national identifier this server knows how to adapt (e.g. a VAT number, if a national identifier adapter is configured). |
| `environment` | string | no | `'production'` | "production" or "test". |

## `peppol_send`

Send a UBL/CII invoice to a Peppol participant via AS4.

Looks up the recipient's AS4 endpoint (SMP), builds the ebMS3/AS4
envelope, and transmits it using the supplied signing credentials.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `invoice_xml_base64` | string | yes |  | Base64-encoded UBL or CII invoice XML. |
| `recipient_identifier` | string | yes |  | Peppol participant ID or adaptable national identifier of the receiver. |
| `sender_id` | string | yes |  | Peppol AP identifier of the sender. |
| `certificate_path` | string | yes |  | Path to the PEM-encoded signing certificate. |
| `private_key_path` | string | yes |  | Path to the PEM-encoded private key. |
| `private_key_password` | string | no | `''` | Optional password for the private key. |
| `document_type_id` | string | no | `'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1'` | Peppol document type identifier URN (default: BIS Billing 3.0 invoice). |
| `environment` | string | no | `'test'` | "production" or "test". |

## `resolve_peppol_dns`

Resolve the SMP hostname for a Peppol participant via DNS only.

Performs the raw U-NAPTR (SML) lookup without fetching the SMP
service group, useful for diagnosing whether a participant is
registered in the SML independently of SMP reachability.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `identifier` | string | yes |  | Peppol participant ID or adaptable national identifier. |
| `environment` | string | no | `'production'` | "production" or "test". |

## `validate_invoice_ae`

Validate a PINT AE UBL 2.1 invoice against the CEN EN16931 base Schematron.

Checks the CEN EN16931 base rules (structural + arithmetic/totals,
~50 BR-* rules) via core's bundled, licensing-clean Schematron. Does
NOT check the PINT-AE jurisdiction overlay (ibr-*-ae rules) — the
result's metadata.scope is "en16931-base-only", and
EN16931_BASE_ONLY_SCOPE_WARNING is always included. BR-CO-09 is
expected to fire on every genuine AE invoice (see
EN16931_BASE_KNOWN_LIMITATIONS_WARNING, always included) since UAE
TRNs carry no ISO country prefix. This is not a full PINT AE
conformance check; a document that passes may still be rejected by a
real Peppol Access Point (no confirmed OpenPeppol redistribution
rights for the overlay rules).
Returns a structured result with per-rule error and warning messages.
The ``variant`` parameter is accepted for interface stability with
v0.1.0 but does not change which rules run — the CEN base rules are
identical for both billing and self-billing profiles.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `xml` | string | yes |  | Raw PINT AE UBL 2.1 XML invoice content |
| `variant` | string | no | `'billing'` | PINT AE profile variant: 'billing' (default) or 'selfbilling' |

## `validate_tdd_ae`

Validate a Peppol AE Tax Data Document (TDD).

Always returns an explicit "unavailable" result — see module
docstring and _TDD_VALIDATION_UNAVAILABLE for why no TDD validation
is currently available.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `xml` | string | yes |  | Raw Peppol AE Tax Data Document (TDD) XML content |
