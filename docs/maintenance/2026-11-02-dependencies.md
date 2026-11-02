# Dependency verification — 2026-11-02

Owner: validation runtime and CI dependencies. No contract, fixture, validator rule, published v0.2.0 record or release workflow was changed by PRs #16 and #17.

## Decision and order

1. [#17](https://github.com/hirokaji/jp-ui-contracts/pull/17): setup-python v5 → v7. Its Node24 requirement is supported by the observed GitHub-hosted runner 2.338.2 (upstream minimum 2.327.1). The workflow uses only `python-version: 3.12`, not the removed `pip-install` input. Python 3.12.15 installed successfully. The prior setup-python Node20 warning is absent from the reviewed new logs.
2. Merge that main into [#16](https://github.com/hirokaji/jp-ui-contracts/pull/16) before rechecking Playwright 1.64.0 → 1.64.1. The changes have no direct dependency, but this order isolates the Actions runtime change and then tests the combined tree.
3. Merge #16 only after the combined PR run and downloaded Evidence pass review; verify main again.

Upstream references: [setup-python v7](https://github.com/actions/setup-python/tree/v7), [its action inputs/runtime](https://github.com/actions/setup-python/blob/v7/action.yml), and [Playwright 1.64.1 release notes](https://github.com/microsoft/playwright/releases/tag/v1.64.1). The Playwright patch addresses Electron window handling and Chromium routed cross-origin redirects. The repository's existing redirect/error and rendering checks were retained.

## Verified runs

| State | Commit | Successful run | Evidence artifact |
|---|---|---|---|
| #17 on prior main | `532f6f21a53b927f26ad87b0005ba73555756e72` | [41384942245](https://github.com/hirokaji/jp-ui-contracts/actions/runs/41384942245) | 13114278414 |
| main after #17 | `c8d50ade0ef5e0bda4850d30143ffe4d2fa0206b` | [41411673975](https://github.com/hirokaji/jp-ui-contracts/actions/runs/41411673975) | 13125962382 |
| combined #16 with #17 | `ebc219366aee772ab8c2e6bd8326b2989d36bc0d` | [41411717656](https://github.com/hirokaji/jp-ui-contracts/actions/runs/41411717656) | 13125414011 |
| main after both merges | `ebe6dda809ff501c353256d9890160b1751dfe6d` | [41412164007](https://github.com/hirokaji/jp-ui-contracts/actions/runs/41412164007) | 13126710480 |

Final dependency-main run: strict contracts succeeded (five expected template-placeholder warnings), 11 Python tests passed, CLI argument test passed, and 27 rendered tests passed with one intentional desktop skip. No setup-python Node20 warning appeared in either final job log.

Downloaded and verified final Evidence SHA-256:

`f89a6cbd08812c3fb7132cd815d6c82e19259e3497a7d563a1757662c8247691`

Combined PR Evidence SHA-256:

`d9a5d5a61089edef2b359e15d7e7d8900adf0f94cd7580d99e886c5c636336a6`

Both ZIP integrity checks passed; screenshots, walkthrough JSON and the HTML report were present. Compared with the reviewed original #16 artifact 13114097747, the combined PR's 32 fixture/walkthrough PNG entries were byte-identical. Final main matched 30/32 entries; the two differing entries are copies of the same desktop form screenshot, with 13 pixels differing by at most one RGB channel level. Visual inspection found no layout/content change. This comparison is review evidence, not a new pixel-perfect acceptance gate.

The walkthrough remains FAIL at scrollWidth 549/clientWidth 412 before repair and PASS at 412/412 afterward. Chromium reported 156.0.8078.4. README before/after images remain unchanged.

## Scope and follow-up

These runs verify repository fixtures and a synthetic walkthrough, not a user's production application or native IME operation. CI artifacts retain the existing 14-day expiry; this record preserves identifiers/digests, not the ZIP bytes indefinitely.

[The proposed v0.3 release gate](../v0.3-release-gate.md) and [release-note draft](../releases/v0.3.0-draft.md) prepare the new feature release. VERSION, root RELEASE_MANIFEST.json and published v0.2.0 remain unchanged until a separate publication change. A subsequent documentation commit needs its own main CI and Evidence; the run above attests only to the dependency merge commit.
