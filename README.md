# jp-ui-contracts

> Japanese UI contract & validation kit for AI agents.  
> Write the design intent in `DESIGN.md`, generate the UI, validate the result, and return failures to the contract.

`jp-ui-contracts` は、日本語UIをAIエージェントやコード生成ツールへ任せるための **design contract + validation kit** です。

公開サイトを大量に収集する見本帳ではありません。日本語本文、和欧混植、改行、フォーム密度、表、モバイル幅のような壊れやすい条件を、**契約 → 生成 → 検証 → Evidence → 契約修正**のループとして扱います。

## Status

- Latest release: `v0.1.0 — public preview`
- `v0.2`: release-gate implementation in progress
- `DESIGN.md` remains the human-edited source
- machine-readable JSON is generated from `DESIGN.md`; it is not maintained separately
- P0 + P1 fixtures are renderable and CI-gated
- browser-level validation uses desktop and mobile Chromium projects

See [`docs/v0.2-release-gate.md`](docs/v0.2-release-gate.md) for the exact release conditions.

## What this repository provides

- `DESIGN.md` templates for Japanese UI
- context profiles: `base`, `media`, `saas`, `docs`, `dashboard`
- Japanese typography and overflow CSS recipes
- reusable failure fixtures
- PASS / WARN / FAIL review criteria
- executable zero-dependency contract validator
- JSON projection for CI and agents
- an agent skill for contract-driven UI review
- browser-level rendered validation with Playwright
- screenshot and render-metric Evidence from CI
- GitHub Actions validation on pull requests
- Issue Forms for broken outputs and profile gaps

## What this repository does not try to be

- a catalog of copied brand designs
- a ranking of Japanese websites
- one universal typography rule for every Japanese interface
- a promise that a prompt alone guarantees UI quality

---

## Core loop

```text
DESIGN.md
   ↓
AI / code generation
   ↓
rendered UI
   ↓
fixture + static validator + browser gate + human review
   ↓
PASS / WARN / FAIL
   ↓
Evidence: screenshot / geometry / trace / report
   ↓
missing rule | weak default | fixture gap | validator gap | implementation bug
   ↓
return the change to the owning layer
```

The important unit is not a pretty screenshot. It is a failure that can be reproduced, attributed, evidenced, and prevented from returning.

---

## Profiles

| Profile | Best for | Main concern |
|---|---|---|
| `base` | minimal shared contract | locale / typography / validation |
| `media` | articles, blogs, owned media | long-form reading rhythm |
| `saas` | admin, settings, B2B tools | labels / forms / stable density |
| `docs` | technical docs, help, knowledge | prose + code + tables |
| `dashboard` | KPI, monitoring, analytics | scanning / tables / metrics |

---

## Quick start

### 1. Choose a template

Copy one of:

```text
templates/base/DESIGN.md
templates/media/DESIGN.md
templates/saas/DESIGN.md
templates/docs/DESIGN.md
templates/dashboard/DESIGN.md
```

Fill in the project-specific design intent, typography, component rules, prohibited patterns, and validation targets.

### 2. Validate the contract

No Python package install is required.

```bash
python validators/contract.py validate DESIGN.md
```

For repository-level checks:

```bash
python validators/contract.py validate --strict templates/*/DESIGN.md
```

### 3. Export a machine-readable projection

```bash
python validators/contract.py export DESIGN.md -o design-contract.json
```

`DESIGN.md` is still the editable source. The JSON is a projection for CI, agents, and other tools.

### 4. Generate or revise the UI

Give the active `DESIGN.md` to the coding agent before visual implementation. Add only the CSS recipes required by the project.

### 5. Run the rendered fixtures

Install the pinned Playwright test dependency and Chromium once:

```bash
npm install
npx playwright install chromium
```

Then run:

```bash
npm run test:rendered
```

The rendered suite exercises every P0/P1 fixture on desktop and mobile Chromium configurations. It checks document-level overflow plus fixture-specific geometry and accessibility-oriented conditions.

### 6. Review PASS / WARN / FAIL

Current implemented fixtures:

- [`fixtures/long-paragraphs/`](fixtures/long-paragraphs/) — sustained Japanese reading
- [`fixtures/mixed-script-headings/`](fixtures/mixed-script-headings/) — Japanese + English headings
- [`fixtures/long-url-overflow/`](fixtures/long-url-overflow/) — URLs and long machine tokens
- [`fixtures/forms-ime-errors/`](fixtures/forms-ime-errors/) — Japanese labels, IME, help, error, actions
- [`fixtures/dense-tables/`](fixtures/dense-tables/) — dense Japanese tables and local overflow containment
- [`fixtures/mobile-wrap-stress/`](fixtures/mobile-wrap-stress/) — narrow viewport wrapping and minimum action size

Use each fixture README and [`validators/scorecard.md`](validators/scorecard.md) to classify the result as PASS / WARN / FAIL.

### 7. Return failures to the owning layer

Every WARN / FAIL should be attributed to one primary bucket:

- missing contract rule
- weak profile default
- missing fixture
- validator gap
- implementation bug

Do not accumulate one-off CSS patches when the real problem belongs in the contract or profile.

---

## Agent skill

[`skills/japanese-ui-contract-review/SKILL.md`](skills/japanese-ui-contract-review/SKILL.md) defines a reusable workflow for AI agents:

1. read the contract
2. statically validate it
3. identify profile and validation targets
4. generate or revise the UI
5. exercise the relevant fixtures
6. run rendered checks when available
7. score PASS / WARN / FAIL
8. attribute the failure
9. fix the owning layer
10. re-run validation and report Evidence

The skill is deliberately tool-neutral. It can be adapted to coding agents that can read repository files, execute commands, and inspect rendered UI.

---

## Validation model

### 1. Static contract validation

The executable validator checks machine-readable contract basics and hard rules that are safe to automate.

Current checks include:

- Locale is present
- Profile is one of the supported profiles
- Review status is valid
- Validation targets exist
- strict mode requires at least three validation targets
- fenced CSS examples do not introduce `word-break: break-all`

The parser also exports selected Contract Metadata to JSON using [`schema/design-contract.schema.json`](schema/design-contract.schema.json).

### 2. Fixture completeness validation

`tests/test_fixture_manifest.py` prevents P0/P1 fixtures from silently regressing to placeholders.

It requires:

- a renderable `index.html`
- Japanese page language
- stable fixture identity
- completed PASS / WARN / FAIL criteria
- no remaining `TBD` in required P0/P1 fixture criteria

### 3. Rendered browser validation

Playwright renders the fixture set in:

- desktop Chromium at 1440px width
- a mobile Chromium project using the iPhone 15 device profile

Common hard gate:

- no document-level horizontal overflow

Fixture-specific gates currently include:

- dense tables keep wide overflow inside the table wrapper
- forms expose labels, helper text, errors, and controls correctly
- mobile-marked actions preserve at least 44px target height

Every common rendered test captures a full-page screenshot and JSON render metrics. Failed browser runs retain Playwright trace Evidence.

Rendered validation does not yet mean pixel-perfect visual regression. It verifies structural rendering properties and leaves aesthetic judgment to the scorecard and human review.

---

## Fixtures

The fixture strategy intentionally focuses on **failure modes**, not brands.

### P0 — implemented and CI-gated

- `long-paragraphs`
- `mixed-script-headings`
- `long-url-overflow`
- `forms-ime-errors`

### P1 — implemented and CI-gated

- `dense-tables`
- `mobile-wrap-stress`

### P2 — later

- `docs-prose-code`

See [`fixtures/fixture-matrix.md`](fixtures/fixture-matrix.md).

---

## Repository structure

```text
jp-ui-contracts/
├─ README.md
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ package.json
├─ playwright.config.mjs
├─ docs/
├─ templates/
├─ recipes/
├─ validators/
│  ├─ contract.py
│  ├─ lint-rules.md
│  └─ scorecard.md
├─ schema/
├─ fixtures/
├─ skills/
├─ examples/
├─ tests/
│  └─ rendered/
└─ .github/workflows/
```

---

## CI

Pull requests run two independent validation jobs.

### Contract validation

```bash
python validators/contract.py validate --strict ...
python -m unittest discover -s tests -p "test_*.py" -v
```

### Rendered validation

```bash
npm install
npx playwright install --with-deps chromium
npm run test:rendered
```

The rendered job uploads a `rendered-validation-evidence` artifact containing `test-results/` and the Playwright HTML report. CI Evidence is currently retained for 14 days.

---

## Feedback loop

Two Issue Forms are available:

- **Broken output report** — a current contract produced a reproducible Japanese UI failure
- **Profile gap request** — an existing profile cannot express a repeated real-world requirement

A useful broken-output report should be promotable into a fixture or validator case. That is how the repository improves from real failures instead of adding rules speculatively.

---

## v0.2 release direction

The target of v0.2 is to close this loop:

```text
contract → generation → static validation → rendered validation → evidence → contract update
```

The release decision is governed by [`docs/v0.2-release-gate.md`](docs/v0.2-release-gate.md).

Current post-gate extensions include:

1. implement the P2 `docs-prose-code` fixture
2. decide whether cross-browser Firefox / WebKit checks should become a later hard gate
3. evaluate pixel-baseline comparison separately from structural rendered checks
4. improve profile-specific semantic validation
5. add a hosted visual surface only if it helps review rather than turning the project into a catalog

See [`CHANGELOG.md`](CHANGELOG.md) for implemented changes.

---

## License

MIT

## Start here

Copy `templates/base/DESIGN.md` or the closest profile, define the validation targets, then run:

```bash
python validators/contract.py validate DESIGN.md
```

The target is not a perfect first generation. The target is a UI contract that can explain a failure, preserve Evidence, and prevent the same failure from returning.
