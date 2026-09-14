# AGENTS.md

This file defines repository-level guidance for coding agents working on `jp-ui-contracts`.

## Mission

Maintain a **Japanese UI contract + validation kit**, not a catalog of brand imitations.

The core loop is:

```text
DESIGN.md → generation → static validation → rendered validation → Evidence → failure attribution → contract update
```

## Source hierarchy

When changing behavior, read in this order:

1. the target `DESIGN.md`
2. `docs/v0.2-release-gate.md`
3. the relevant fixture README and `index.html`
4. `validators/contract.py` and validator docs
5. `fixtures/fixture-matrix.md`
6. `CONTRIBUTING.md`

`DESIGN.md` is the human-edited contract source. Do not introduce a second hand-maintained JSON contract. Machine-readable JSON is a projection.

## Required checks

Before proposing or completing a code change, run the checks relevant to the files changed.

Static repository checks:

```bash
python validators/contract.py validate --strict \
  templates/base/DESIGN.md \
  templates/media/DESIGN.md \
  templates/saas/DESIGN.md \
  templates/docs/DESIGN.md \
  templates/dashboard/DESIGN.md \
  examples/sample-media/DESIGN.md \
  examples/sample-saas/DESIGN.md
python -m unittest discover -s tests -p "test_*.py" -v
```

Rendered checks:

```bash
npm install
npx playwright install chromium
npm run test:rendered
```

Do not claim rendered validation passed unless it was actually executed or CI Evidence confirms it.

## Change routing

When a failure is found, assign one primary owner before editing:

- missing contract rule → `DESIGN.md` / template
- weak repeated default → profile template
- missing reproducible scenario → fixture
- measurable condition not enforced → validator / browser test
- contract is correct but UI violates it → implementation
- unclear or unsupported evidence → keep as WARN; do not invent a permanent rule

Prefer changing the owning layer over adding a local workaround.

## Hard guardrails

- do not globalize `word-break: break-all`
- do not apply strong body `letter-spacing` without evidence
- do not use one density rule for prose, tables, forms, and code
- do not silently weaken a test or validation target to make CI green
- do not turn screenshots into canonical contract values
- do not add copied brand DESIGN.md files as the main growth strategy
- do not claim Firefox or WebKit compatibility from Chromium-only Evidence

## Fixture changes

A required fixture must have:

- `README.md`
- `index.html`
- `lang="ja"`
- a stable `data-fixture` identity
- PASS / WARN / FAIL criteria
- no `TBD` criteria

If a new fixture represents a durable failure mode, add it to the fixture matrix and decide explicitly whether it belongs in the release gate.

## Pull requests

A PR should explain:

- the observed or anticipated failure
- the owning layer
- the change made
- the validation performed
- residual risk

Prefer small, attributable PRs. Dependency-only changes should not be mixed with contract redesign unless required by the update.

## Definition of done

A change is done when:

1. the owning layer is identified,
2. the implementation is updated,
3. applicable static and rendered gates pass,
4. Evidence exists for browser-level behavior when relevant,
5. README / CHANGELOG / release-gate documentation are not left stale.
