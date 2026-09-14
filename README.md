# jp-ui-contracts

> Japanese UI contract & validation kit for AI agents.  
> Write the design intent in `DESIGN.md`, generate the UI, validate the result, and return failures to the contract.

`jp-ui-contracts` は、日本語UIをAIエージェントやコード生成ツールへ任せるための **design contract + validation kit** です。

公開サイトを大量に収集する見本帳ではありません。日本語本文、和欧混植、改行、フォーム密度、表、モバイル幅のような壊れやすい条件を、**契約 → 生成 → 検証 → 契約修正**のループとして扱います。

## Status

- Latest release: `v0.1.0 — public preview`
- `v0.2`: contract validation loop in development
- `DESIGN.md` remains the human-edited source
- machine-readable JSON is generated from `DESIGN.md`; it is not maintained separately

## What this repository provides

- `DESIGN.md` templates for Japanese UI
- context profiles: `base`, `media`, `saas`, `docs`, `dashboard`
- Japanese typography and overflow CSS recipes
- reusable failure fixtures
- PASS / WARN / FAIL review scorecard
- executable zero-dependency contract validator
- JSON projection for CI and agents
- an agent skill for contract-driven UI review
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
fixture + validator + human review
   ↓
PASS / WARN / FAIL
   ↓
missing rule | weak default | fixture gap | validator gap | implementation bug
   ↓
return the change to the owning layer
```

The important unit is not a screenshot. It is a failure that can be reproduced, attributed, and prevented from returning.

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

### 5. Run fixtures and review

Start with the fixture that matches the risk:

- [`fixtures/long-paragraphs/`](fixtures/long-paragraphs/) — sustained Japanese reading
- [`fixtures/mixed-script-headings/`](fixtures/mixed-script-headings/) — Japanese + English headings
- [`fixtures/long-url-overflow/`](fixtures/long-url-overflow/) — URLs and long machine tokens
- [`fixtures/forms-ime-errors/`](fixtures/forms-ime-errors/) — Japanese labels, IME, help, error, actions

Use [`validators/scorecard.md`](validators/scorecard.md) to classify the result as PASS / WARN / FAIL.

### 6. Return failures to the contract

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
6. score PASS / WARN / FAIL
7. attribute the failure
8. fix the owning layer
9. re-run validation and report evidence

The skill is deliberately tool-neutral. It can be adapted to coding agents that can read repository files, execute commands, and inspect rendered UI.

---

## Validation model

### Static validation

The executable validator checks machine-readable contract basics and hard rules that are safe to automate.

Current checks include:

- Locale is present
- Profile is one of the supported profiles
- Review status is valid
- Validation targets exist
- strict mode requires at least three validation targets
- fenced CSS examples do not introduce `word-break: break-all`

The parser also exports selected Contract Metadata to JSON using [`schema/design-contract.schema.json`](schema/design-contract.schema.json).

### Visual validation

Not every UI property should be reduced to static lint. Rendered output still needs review against realistic stress cases.

Examples:

- long Japanese paragraphs remain readable
- Japanese-English headings wrap naturally
- long URLs do not destroy layout or paragraph rhythm
- form labels, helper text, errors, and IME states remain usable
- mobile width does not reveal hidden overflow

The repository treats visual review as evidence that feeds contract improvement, not as a replacement for the contract.

---

## Fixtures

The fixture strategy intentionally focuses on **failure modes**, not brands.

### P0 — implemented

- `long-paragraphs`
- `mixed-script-headings`
- `long-url-overflow`
- `forms-ime-errors`

### P1 — next

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
└─ .github/workflows/
```

---

## CI

Pull requests that change contracts, the validator, schema, or tests run:

```bash
python validators/contract.py validate --strict ...
python -m unittest discover -s tests -p "test_*.py" -v
```

This is the first step toward treating Japanese UI rules as regression-testable contracts rather than prose that is read once and forgotten.

---

## Feedback loop

Two Issue Forms are available:

- **Broken output report** — a current contract produced a reproducible Japanese UI failure
- **Profile gap request** — an existing profile cannot express a repeated real-world requirement

A useful broken-output report should be promotable into a fixture or validator case. That is how the repository improves from real failures instead of adding rules speculatively.

---

## v0.2 direction

The goal of v0.2 is not to increase the number of collected designs. It is to close this loop:

```text
contract → generation → validation → evidence → contract update
```

Near-term work:

1. stabilize the executable validator and JSON projection
2. complete P0 fixture coverage
3. add P1 fixtures for dense tables and mobile wrapping
4. connect rendered regression evidence to pull requests
5. improve profile-specific validation without creating a second source of truth

See [`CHANGELOG.md`](CHANGELOG.md) for implemented changes.

---

## License

MIT

## Start here

Copy `templates/base/DESIGN.md` or the closest profile, define the validation targets, then run:

```bash
python validators/contract.py validate DESIGN.md
```

The target is not a perfect first generation. The target is a UI contract that can explain a failure and prevent the same failure from returning.
