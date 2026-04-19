# validator scorecard

This scorecard is the bridge between `DESIGN.md` and rendered UI review.

The goal is not aesthetic scoring.
The goal is to decide whether a generated output is **contract-aligned, reviewable, and reusable**.

---

## Rating scale

### PASS
The output is acceptable for the selected profile.
Minor polish may remain, but the contract and implementation are directionally sound.

### WARN
The output is usable, but the contract is underspecified or the implementation needs tightening.
A future failure is likely unless the rule is clarified.

### FAIL
The output violates the contract, breaks readability or usability, or reveals that the contract is missing a required rule.

---

## Scorecard dimensions

| Dimension | PASS | WARN | FAIL |
|---|---|---|---|
| Locale clarity | Locale and profile are explicit | Locale or profile is implied but not explicit | Locale or profile is missing |
| Font fallback | Japanese fallback is explicit and reasonable | Fallback exists but platform behavior is uncertain | Japanese fallback is absent or unstable |
| Long paragraph readability | Long Japanese paragraphs are comfortable to read | Slightly dense or slightly loose but usable | Cramped, tiring, or visibly unstable |
| Heading wrapping | Headings wrap naturally at target widths | Some headings are borderline awkward | Headings wrap in clearly broken positions |
| Mixed-script stability | Japanese-English mixed text feels coherent | Some mixed text looks uneven | Mixed text visibly breaks rhythm or hierarchy |
| URL / long token overflow | Long tokens wrap without harming layout | Overflow handling works but hurts rhythm in places | Tokens overflow or force layout breakage |
| Table density | Tables remain scannable and readable | Density is borderline for repeated use | Tables are too tight, too loose, or visually unstable |
| Form readability | Labels, help text, errors, and controls stay readable | Form is usable but visually strained | Form copy becomes cramped or ambiguous |
| Mobile stability | Mobile layout remains readable and operable | Some areas need refinement | Mobile layout breaks readability or operability |
| Contract traceability | Problems can be mapped back to a contract rule | Some issues are only loosely traceable | Failures cannot be traced back to any contract rule |

---

## Review workflow

### Step 1. Static check
Review the contract before reviewing the screen.

Check:
- Locale is explicit
- Profile is explicit
- Typography rules are present
- Line-break / overflow strategy is stated
- Validation targets are written
- Global anti-patterns are not present

### Step 2. Visual check
Review the rendered output against actual UI fragments.

Check:
- Long paragraph
- Mixed-script heading
- Long URL or long token
- Table
- Form
- Mobile width

### Step 3. Contract return
Every WARN or FAIL should be returned to one of these buckets:

- Missing rule
- Weak profile default
- Missing fixture
- Validator gap
- Implementation bug

---

## Review summary template

```md
## Summary
PASS / WARN / FAIL

## Profile
media / saas / docs / dashboard / base

## Static check
- Locale:
- Profile:
- Typography:
- Line-break / overflow:
- Validation targets:

## Visual check
- Long paragraph:
- Mixed-script heading:
- Long token overflow:
- Table:
- Form:
- Mobile:

## Contract return
- Missing rule:
- Weak default:
- Missing fixture:
- Validator gap:
- Implementation bug:

## Next action
```
