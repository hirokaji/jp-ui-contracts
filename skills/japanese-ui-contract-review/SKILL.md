# Japanese UI Contract Review

Use this skill when an AI agent is asked to create, revise, or review a Japanese web interface governed by `DESIGN.md`.

## Goal

Keep UI generation inside the selected Japanese UI contract, then return observed failures to the owning contract layer instead of patching screenshots ad hoc.

## Inputs

Required:
- project `DESIGN.md`
- target UI code or rendered preview

Recommended:
- closest profile under `templates/`
- relevant CSS recipes under `recipes/`
- relevant fixture under `fixtures/`
- CI or local rendered-validation Evidence when available

## Workflow

1. Read `DESIGN.md` before proposing visual changes.
2. Run static validation:
   ```bash
   python validators/contract.py validate DESIGN.md
   ```
3. Identify the active profile and validation targets.
4. Create or modify the UI without weakening explicit contract rules.
5. Test the output against the closest fixtures. At minimum, check any fixture named by the contract's validation targets.
6. When this repository's browser harness is available, run rendered validation:
   ```bash
   npm install
   npx playwright install chromium
   npm run test:rendered
   ```
7. Review the rendered result using `validators/scorecard.md` and classify findings as PASS / WARN / FAIL.
8. Attribute each WARN or FAIL to exactly one primary bucket:
   - missing contract rule
   - weak profile default
   - missing fixture
   - validator gap
   - implementation bug
9. Fix the owning layer. Do not hide a contract problem with a one-off local style override unless the override is explicitly justified.
10. Re-run static and rendered validation as applicable.
11. Report Evidence and residual manual checks.

## Evidence priority

Prefer Evidence that another reviewer can inspect or reproduce:

1. failing or passing browser gate with exact fixture and viewport
2. geometry or overflow measurement
3. DOM / accessibility assertion
4. screenshot of the rendered fixture
5. human visual observation with explicit PASS / WARN / FAIL rationale

A screenshot alone is not sufficient when the relevant condition can be measured directly.

## Output

Return a compact review record containing:

```md
## Contract review
- Profile:
- Static validation: PASS / WARN / FAIL
- Rendered validation: PASS / WARN / FAIL / NOT RUN
- Visual review: PASS / WARN / FAIL
- Fixtures checked:
- Viewports checked:

## Findings
- Finding:
- Attribution:
- Evidence:
- Change made:

## Residual risk
- Remaining manual checks:
- Unsupported browsers / surfaces:
```

## Guardrails

- Do not globally introduce `word-break: break-all`.
- Do not optimize Japanese body typography from Latin-first defaults without checking long Japanese text.
- Keep paragraph, table, and form density separate.
- Treat screenshots as Evidence, not as the contract itself.
- Prefer measurable browser checks over visual assertion when the property is measurable.
- Do not silently weaken a validation target to make a result pass.
- When Evidence is insufficient, leave the result as WARN and state the missing check.
- Do not treat Chromium-only success as proof of Firefox or WebKit compatibility.

## Useful commands

Validate a contract:

```bash
python validators/contract.py validate DESIGN.md
```

Export a machine-readable projection for another agent or CI step:

```bash
python validators/contract.py export DESIGN.md -o design-contract.json
```

Strict repository check:

```bash
python validators/contract.py validate --strict templates/*/DESIGN.md
```

Run the browser gates:

```bash
npm run test:rendered
```

See `docs/v0.2-release-gate.md` for the release-level acceptance conditions.
