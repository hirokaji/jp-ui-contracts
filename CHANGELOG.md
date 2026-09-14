# Changelog

All notable changes to `jp-ui-contracts` are documented here.

## [Unreleased] — v0.2 contract + rendered validation loop

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
- fixture completeness gate for required P0/P1 fixtures
- executable P0 fixture pages and review criteria for:
  - long Japanese paragraphs
  - mixed-script headings
  - long URL / machine token overflow
  - Japanese forms / IME / error states
- executable P1 fixture pages and review criteria for:
  - dense tables
  - mobile wrapping stress
- Playwright 1.63.0 rendered validation harness
  - desktop Chromium project
  - mobile Chromium project using the iPhone 15 device profile
  - document-level horizontal overflow gate across P0/P1 fixtures
  - dense-table local overflow containment check
  - form label / helper / error / control inspection
  - mobile 44px minimum action-height check
- rendered Evidence capture
  - full-page screenshots
  - JSON render metrics
  - retained failure traces
  - Playwright HTML report
  - GitHub Actions artifact retention for 14 days
- explicit [`docs/v0.2-release-gate.md`](docs/v0.2-release-gate.md)

### Changed

- repositioned the repository from a template collection toward a Japanese UI contract + validation loop
- clarified that `DESIGN.md` remains the human-edited source and JSON is generated, not maintained independently
- replaced the stale README roadmap with implemented status and release-gate conditions
- made failure attribution explicit: missing rule / weak profile default / fixture gap / validator gap / implementation bug
- extended the core loop from static contract checks to rendered browser Evidence

### Not included yet

- pixel-perfect screenshot baseline comparison
- Firefox / WebKit release gating
- automated visual-diff approval workflow
- `docs-prose-code` P2 fixture implementation
- package / CLI distribution beyond direct Python invocation
- hosted gallery / GitHub Pages
- v0.2 release tag

## [0.1.0] — 2026-04-19

Initial public preview.

Included:
- `DESIGN.md` templates for base / media / saas / docs / dashboard
- CSS recipes for Japanese text, mixed-script headings, forms, and overflow handling
- validation rules and review checklist
- Issue Forms for broken output reports and profile gap requests
- early fixture definitions and profile selector documents
