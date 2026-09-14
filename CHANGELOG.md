# Changelog

All notable changes to `jp-ui-contracts` are documented here.

## [Unreleased]

No queued changes after the v0.2.0 release.

## [0.2.0] — 2026-09-14

Published as [`v0.2.0 — executable contract validation`](https://github.com/hirokaji/jp-ui-contracts/releases/tag/v0.2.0).

Release tag target: `ba4f44c65b18c27ba784d9171a80859f798c5c89`.

### Added

- zero-dependency `validators/contract.py`
  - parses Contract Metadata from `DESIGN.md`
  - validates locale, profile, review status, and validation targets
  - rejects `word-break: break-all` inside fenced CSS examples
  - supports stricter repository checks
  - exports a machine-readable JSON projection
- v0.2 `design-contract.schema.json` for generated projections
- `skills/japanese-ui-contract-review/SKILL.md`
- GitHub Actions contract validation workflow
- unit tests for parser and validator behavior
- release metadata consistency tests for `VERSION`, `package.json`, and `RELEASE_MANIFEST.json`
- fixture completeness gate for required P0/P1/P2 fixtures
- executable P0 fixture pages and review criteria for:
  - long Japanese paragraphs
  - mixed-script headings
  - long URL / machine token overflow
  - Japanese forms / IME / error states
- executable P1 fixture pages and review criteria for:
  - dense tables
  - mobile wrapping stress
- executable P2 fixture page and review criteria for:
  - Japanese technical prose + inline code + code blocks + callouts + tables
- Playwright 1.63.0 rendered validation harness
  - desktop Chromium project
  - mobile Chromium project using the Pixel 7 device profile
  - explicit Chromium browser binding for both projects
  - document-level horizontal overflow gate across all required fixtures
  - dense-table local overflow containment check
  - form label / helper / error / control inspection
  - mobile 44px minimum action-height check
  - docs code/table local overflow containment and callout inspection
- rendered Evidence capture
  - full-page screenshots
  - JSON render metrics
  - retained failure traces
  - Playwright HTML report
  - GitHub Actions artifact retention for 14 days
- explicit [`docs/v0.2-release-gate.md`](docs/v0.2-release-gate.md)
- [`docs/releases/v0.2.0.md`](docs/releases/v0.2.0.md) release notes
- `RELEASE_MANIFEST.json` and root `VERSION`
- weekly scheduled validation and manual `workflow_dispatch`
- Dependabot version-update proposals for npm / Playwright and GitHub Actions
- [`docs/maintenance.md`](docs/maintenance.md) low-touch maintenance loop
- root [`AGENTS.md`](AGENTS.md) repository contract for coding agents
- evidence-oriented pull request template

### Changed

- repositioned the repository from a template collection toward a Japanese UI contract + validation loop
- clarified that `DESIGN.md` remains the human-edited source and JSON is generated, not maintained independently
- replaced the stale README roadmap with implemented status and release-gate conditions
- made failure attribution explicit: missing rule / weak profile default / fixture gap / validator gap / implementation bug
- extended the core loop from static contract checks to rendered browser Evidence
- corrected the mobile project from an iPhone descriptor that implicitly selected WebKit to a Chromium-bound Pixel 7 profile, keeping the declared browser gate aligned with installed CI dependencies
- promoted `docs-prose-code` from a future P2 placeholder into the v0.2 required fixture set
- shifted maintenance from ad hoc human memory toward scheduled drift detection plus reviewable dependency PRs
- expanded CI path coverage so release metadata and documentation changes also execute the release gates

### Compatibility

- Existing `DESIGN.md` files remain the editable contract source.
- Machine-readable JSON is generated and does not become a second file that users must maintain.
- Adoption of the Python validator and rendered browser harness can be incremental.

### Known non-goals

- pixel-perfect screenshot baseline comparison
- Firefox / WebKit release gating
- automated visual-diff approval workflow
- package / CLI distribution beyond direct Python invocation
- hosted gallery / GitHub Pages

### Rollback

The previous public release is `v0.1.0`.

## [0.1.0] — 2026-04-19

Initial public preview.

Included:
- `DESIGN.md` templates for base / media / saas / docs / dashboard
- CSS recipes for Japanese text, mixed-script headings, forms, and overflow handling
- validation rules and review checklist
- Issue Forms for broken output reports and profile gap requests
- early fixture definitions and profile selector documents
