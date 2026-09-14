# Maintenance loop

`jp-ui-contracts` should remain useful even when the maintainer is not actively adding features.

The maintenance model therefore separates **automatic drift detection** from **human promotion decisions**.

## Automatic maintenance

### Weekly validation

`contract-validation` runs every Monday at 03:17 UTC in addition to pull-request and main-branch runs.

The scheduled run executes:

- strict `DESIGN.md` contract validation
- Python validator / fixture-completeness tests
- desktop Chromium rendered validation
- Pixel 7 Chromium rendered validation
- Evidence artifact upload

A scheduled failure means the repository changed underneath the contract even if no repository file changed. Examples include runner, browser, dependency, or platform drift.

### Dependency proposals

Dependabot checks weekly for:

- npm / Playwright updates
- GitHub Actions updates

Dependency PRs are proposals, not automatic promotions. CI must remain green before merge.

## Human maintenance

A human review is needed when one of the following occurs:

- scheduled validation fails
- a Dependabot PR changes browser behavior or a major version
- a broken-output issue is reproducible
- a profile-gap request repeats an existing pain point
- the public README describes behavior that no longer matches the implementation
- a release has accumulated enough accepted changes to justify a new tag

## Broken-output promotion path

```text
broken output
  ↓
minimal reproduction
  ↓
fixture candidate
  ↓
failure attribution
  ↓
contract | profile | validator | implementation change
  ↓
rendered regression gate
  ↓
Evidence
  ↓
merge / release
```

Do not add a permanent rule from one screenshot alone. Promote a failure when it is reproducible and the owning layer can be identified.

## Monthly review checklist

A monthly review can remain short when CI is green.

- review open broken-output and profile-gap issues
- review pending dependency PRs
- confirm the latest release still matches README Status
- check whether a repeated local workaround should become a fixture or contract rule
- check whether CI Evidence retention is sufficient for current review latency

If there is no new evidence, do not change defaults merely to create activity.

## Release hygiene

Before a release:

1. satisfy `docs/v0.2-release-gate.md` or the current release gate
2. confirm main CI is green on the release candidate commit
3. confirm Evidence artifact exists
4. update CHANGELOG from Unreleased to the release version/date
5. ensure README Status matches the published release
6. create the tag / GitHub Release
7. only then announce the release externally

## Maintenance principle

The repository should improve from observed failures, not from maintenance theater. Automation detects drift; humans decide whether evidence deserves a new contract rule.
