# fixture matrix

This matrix defines the required failure-oriented fixture set for `jp-ui-contracts` v0.2.

| Fixture family | Priority | Status | Primary failure mode | Affected profiles |
|---|---|---|---|---|
| `long-paragraphs` | P0 | implemented + CI-gated | Japanese body text becomes cramped or rhythmless | media, docs |
| `mixed-script-headings` | P0 | implemented + CI-gated | Japanese-English headings break awkwardly | media, docs, saas |
| `long-url-overflow` | P0 | implemented + CI-gated | URLs or long English tokens break cards or paragraphs | media, docs, saas |
| `forms-ime-errors` | P0 | implemented + CI-gated | Labels, helper text, errors, and IME-oriented form density become unstable | saas, dashboard |
| `dense-tables` | P1 | implemented + CI-gated | Table scanability collapses or overflow escapes its surface | saas, dashboard, docs |
| `mobile-wrap-stress` | P1 | implemented + CI-gated | Narrow widths force bad line breaks or undersized actions | all |
| `docs-prose-code` | P2 | implemented + CI-gated | Prose, code, callouts, and tables inherit the wrong density or overflow responsibility | docs, base |

---

## P0 — repeated foundational failures

### `long-paragraphs`
Covers:
- sustained Japanese prose
- inline English product names
- quote / supporting text rhythm
- mobile reading width

### `mixed-script-headings`
Covers:
- Japanese heading + English product name
- long acronyms and English tokens
- narrow-width heading wrap behavior

### `long-url-overflow`
Covers:
- long URLs in reading surfaces
- long machine-like tokens
- containment without global `word-break: break-all`

### `forms-ime-errors`
Covers:
- long Japanese labels
- helper text
- error text
- textarea / input controls
- repeated action buttons

---

## P1 — operational density and narrow-width failures

### `dense-tables`
Covers:
- mixed numeric and Japanese labels
- long row titles
- status chips
- local horizontal overflow containment

### `mobile-wrap-stress`
Covers:
- long mixed-script heading
- long machine identifier
- form input
- modal / card actions
- minimum 44px marked action height

---

## P2 — technical-document composition failure

### `docs-prose-code`
Covers:
- sustained Japanese technical prose
- inline code inside Japanese sentences
- long code block with exact machine identifiers
- callout density
- table density
- independent code / table overflow containment

---

## Promotion rule

A new fixture should not be added because a UI pattern is popular. Add or split a fixture when a failure is:

1. observed in a real generated output or repeated review,
2. reproducible with a compact page,
3. attributable to a contract/profile/validator/implementation boundary,
4. valuable enough to prevent recurrence through CI or a documented human gate.

The fixture set is therefore a **failure corpus**, not a brand catalog.
