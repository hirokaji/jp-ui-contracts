# fixture matrix

This matrix defines the first fixture set for `jp-ui-contracts`.

| Fixture family | Primary failure mode | Affected profiles | Why it matters |
|---|---|---|---|
| `long-paragraphs` | Japanese body text becomes cramped or rhythmless | media, docs | Long reading is where poor line-height and poor wrapping become obvious |
| `mixed-script-headings` | Japanese-English headings break awkwardly | media, docs, saas | Mixed text is often the first place where “looks fine” starts to fail |
| `long-url-overflow` | URLs or long English tokens break cards or paragraphs | media, docs, saas | Overflow fixes often damage readability if done globally |
| `forms-ime-errors` | Labels, helper text, errors, and IME input become unstable | saas, dashboard | Form density is often too tight when contracts only think about paragraphs |
| `dense-tables` | Table scanability collapses | saas, dashboard, docs | Tables should not inherit article-like spacing blindly |
| `mobile-wrap-stress` | Narrow widths force bad line breaks | all | Mobile is where hidden fragility becomes visible |
| `docs-prose-code` | Prose, code, and callouts fight each other | docs | Technical documentation needs a different balance than pure article UI |

---

## Priority order

### P0
- `long-paragraphs`
- `mixed-script-headings`
- `long-url-overflow`
- `forms-ime-errors`

### P1
- `dense-tables`
- `mobile-wrap-stress`

### P2
- `docs-prose-code`

---

## Suggested first contents

### `long-paragraphs`
Include:
- 2 to 3 long Japanese paragraphs
- one paragraph with inline English product name
- one quote block
- one caption

### `mixed-script-headings`
Include:
- Japanese heading with English product name
- Japanese heading with long acronym
- Japanese heading with slash-separated English token

### `long-url-overflow`
Include:
- long URL inside article body
- long URL inside card body
- long English token in a heading or tag line

### `forms-ime-errors`
Include:
- long Japanese field label
- helper text
- error text
- textarea with long note
- button row with long labels

### `dense-tables`
Include:
- mixed numeric and Japanese labels
- narrow columns
- long row title
- status chip

### `mobile-wrap-stress`
Include:
- mobile-width article card
- mobile-width modal
- mobile-width form
- mobile-width dashboard card

### `docs-prose-code`
Include:
- prose paragraph
- code block
- callout
- table
- heading with mixed Japanese and English terms
