## What to improve next

`jp-ui-contracts` is not just a template collection.
The next step is to make the contract more testable, more comparable, and easier to improve from real-world failures.

In the short term, this repository will evolve in four directions:

1. **Stronger contract structure**  
   Make `DESIGN.md` easier to lint and compare by clarifying required fields, validation targets, and profile-specific overlays.

2. **Validation-first workflow**  
   Treat generated UI as reviewable output. The goal is not one-shot perfection, but a stable loop of contract → generation → review → contract update.

3. **Reusable fixtures**  
   Build a shared set of failure-prone Japanese UI cases such as long paragraphs, mixed-script headings, long URLs, tables, forms, and mobile wrapping.

4. **Community feedback intake**  
   Convert stars and reactions into actionable issue reports and profile gap requests.

---

## Validation model

This repository uses a two-layer validation model.

### 1. Static validation
Check whether the contract itself is sufficiently specified.

Examples:
- Is the locale explicit?
- Is the profile selected?
- Is Japanese font fallback declared?
- Is `word-break: break-all` avoided as a global default?
- Are validation targets written down?

### 2. Visual validation
Check whether the generated UI still respects the contract once rendered.

Examples:
- Long Japanese paragraphs remain readable
- Mixed Japanese-English headings do not break awkwardly
- Long URLs do not destroy paragraph rhythm
- Tables and forms do not inherit article spacing blindly
- Mobile width remains stable

---

## Validator scorecard

We score validation results using three levels.

- **PASS**: acceptable for current profile
- **WARN**: usable, but contract or implementation should be tightened
- **FAIL**: violates contract or breaks readability / usability

See [`validators/scorecard.md`](validators/scorecard.md) for the detailed review sheet.

---

## Fixtures

The repository will grow around reusable fixtures rather than brand imitation.

Initial fixture families:
- long paragraphs
- mixed-script headings
- long URL overflow
- forms with helper and error text
- dense tables
- mobile wrapping
- docs-style prose + code coexistence

See [`fixtures/fixture-matrix.md`](fixtures/fixture-matrix.md).

---

## Feedback channels

To keep improvements grounded in real use cases, issue intake is split into two tracks.

- **Broken output report**  
  For cases where the current contract produced unstable or poor Japanese UI.

- **Profile gap request**  
  For cases where an existing profile is too weak or a new profile / overlay is needed.

Issue forms live in `.github/ISSUE_TEMPLATE/`.

---

## Recommended next commit order

1. Add Issue Forms and config
2. Add validator scorecard
3. Add fixture matrix
4. Add `profile-selector.md`
5. Add real fixture samples
6. Start collecting broken outputs from users
