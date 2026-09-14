# Japanese UI Contract Review

Use this skill when an AI agent is asked to create, revise, or review a Japanese web interface governed by `DESIGN.md`.

## Goal

Keep UI generation inside the selected Japanese UI contract, then return observed failures to the contract instead of patching screenshots ad hoc.

## Inputs

Required:
- project `DESIGN.md`
- target UI code or rendered preview

Recommended:
- closest profile under `templates/`
- relevant CSS recipes under `recipes/`
- relevant fixture under `fixtures/`

## Workflow

1. Read `DESIGN.md` before proposing visual changes.
2. Run static validation:
   ```bash
   python validators/contract.py validate DESIGN.md
   ```
3. Identify the active profile and validation targets.
4. Create or modify the UI without weakening explicit contract rules.
5. Test the output against the closest fixtures. At minimum, check any fixture named by the contract's validation targets.
6. Review the rendered result using `validators/scorecard.md` and classify findings as PASS / WARN / FAIL.
7. Attribute each WARN or FAIL to exactly one primary bucket:
   - missing contract rule
   - weak profile default
   - missing fixture
   - validator gap
   - implementation bug
8. Fix the owning layer. Do not hide a contract problem with a one-off local style override unless the override is explicitly justified.
9. Re-run validation and report evidence.

## Output

Return a compact review record containing:

```md
## Contract review
- Profile:
- Static validation: PASS / WARN / FAIL
- Visual validation: PASS / WARN / FAIL
- Fixtures checked:

## Findings
- Finding:
- Attribution:
- Evidence:
- Change made:

## Residual risk
- Remaining manual checks:
```

## Guardrails

- Do not globally introduce `word-break: break-all`.
- Do not optimize Japanese body typography from Latin-first defaults without checking long Japanese text.
- Keep paragraph, table, and form density separate.
- Treat screenshots as evidence, not as the contract itself.
- Do not silently weaken a validation target to make a result pass.
- When evidence is insufficient, leave the result as WARN and state the missing check.

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
