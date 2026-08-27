# Release Process for mcp-einvoicing-ae

This document describes how to release a new version of `mcp-einvoicing-ae` to PyPI and the official MCP registry.

## One-Time Setup Requirements

**PyPI Trusted Publishing:**
PyPI publishing is fully automated via OIDC (no token stored). The Trusted Publisher is configured on PyPI under `cmendezs/mcp-einvoicing-ae`, workflow `publish.yml`, environment `pypi`. No `.env` or secret needed.

**MCP Publisher CLI:**
Binary installed at `~/.local/bin/mcp-publisher` (already in `PATH`). To update:
```bash
curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_darwin_arm64.tar.gz" \
  | tar xzf - -C ~/.local/bin/
```

**MCP Registry Authentication:**
Authenticate once with GitHub (device flow):
```bash
mcp-publisher login github
```

## Release Steps

**Step 1 — Version bump:** update `version` in `pyproject.toml` and `server.json` (top-level and `packages[].version`).

**Step 2 — Commit, tag and push:**
```bash
git add pyproject.toml server.json
git commit -m "release: v0.1.0 — {summary}"
git push origin main
git tag v0.1.0
git push origin v0.1.0
```
GitHub Actions publishes to PyPI automatically on tag push.

**Step 3 — MCP registry:**
```bash
mcp-publisher publish
```

## Changelog

Release notes live in [`CHANGELOG.md`](CHANGELOG.md) (Keep a Changelog + SemVer).
Update the `[Unreleased]` section there as part of each change; on release, move
those entries under the new version heading.

---

## Release history

**`v0.1.0`** — published 2026-08-27 (first release). The three gates that previously blocked
this release are now closed:

1. PINT AE publication status confirmed 2026-08-26 — see `context-library/countries/ae.md`
   "PINT AE publication gate".
2. `specs/README.md`'s `[NEED:]` rows were resolved editorially: the base OASIS UBL 2.1 XSD and
   the TDD transport channel are tracked as deferred, non-blocking open items (neither affects
   what ships in v0.1.0); the OpenPeppol jurisdiction-registry page is documented as strong,
   not yet independently confirmed, evidence. `audit/audit_vs_core.py --fail-on blocking`
   passes.
3. `AEInvoice`/`AEParty`/`AETaxDataDocument` models, four bundled Schematron validators, and the
   `generate_invoice_ae`/`validate_invoice_ae`/`validate_tdd_ae`/`parse_invoice_ae` MCP tools
   are implemented and registered.

The PyPI pending publisher was registered before the `v0.1.0` tag push, so OIDC authenticated
correctly on the first release.

---

## Notes

- The MCP registry does **not** sync automatically with PyPI or GitHub — step 3 is required for every release.
- The `server.json` description field must be **≤ 100 characters**.
- PyPI rejects re-uploads of the same version — always bump before tagging.
- Publishing without a passing audit gate is prohibited. `publish.yml` enforces this, and the
  monorepo `/audit-gate` skill is the local equivalent.
