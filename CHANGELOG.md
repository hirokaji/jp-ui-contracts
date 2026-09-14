# Changelog

All notable changes to `jp-ui-contracts` are documented here.

## [Unreleased] — v0.2 contract validation loop

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
- executable P0 fixture pages and review criteria for:
  - long Japanese paragraphs
  - mixed-script headings
  - long URL / machine token overflow
  - Japanese forms / IME / error states

### Changed

- repositioned the repository from a template collection toward a Japanese UI contract + validation loop
- clarified that `DESIGN.md` remains the human-edited source and JSON is generated, not maintained independently
- replaced the stale README roadmap with implemented status and next work
- made failure attribution explicit: missing rule / weak profile default / fixture gap / validator gap / implementation bug

### Not included yet

- automated browser screenshot comparison
- `dense-tables` fixture implementation
- `mobile-wrap-stress` fixture implementation
- `docs-prose-code` fixture implementation
- package / CLI distribution beyond direct Python invocation
- v0.2 release tag

## [0.1.0] — 2026-04-19

Initial public preview.

Included:
- `DESIGN.md` templates for base / media / saas / docs / dashboard
- CSS recipes for Japanese text, mixed-script headings, forms, and overflow handling
- validation rules and review checklist
- Issue Forms for broken output reports and profile gap requests
- early fixture definitions and profile selector documents
