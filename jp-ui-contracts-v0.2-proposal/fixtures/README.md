# fixtures

Fixtures are reusable failure-prone UI cases for Japanese interfaces.

They exist to answer a practical question:

**Can this contract survive the kinds of screens that usually break Japanese readability?**

Fixtures are more important than brand imitation.
Each fixture should represent a repeated review pain point.

---

## Fixture design rules

A good fixture is:

- small enough to reproduce quickly
- realistic enough to matter
- tied to a known failure mode
- reusable across multiple profiles
- easy to review with screenshots

---

## Recommended directory shape

```text
fixtures/
├─ long-paragraphs/
│  ├─ README.md
│  ├─ input.md
│  ├─ expected.md
│  └─ preview.html
├─ mixed-script-headings/
├─ long-url-overflow/
├─ forms-ime-errors/
├─ dense-tables/
├─ mobile-wrap-stress/
└─ docs-prose-code/
```

Each family should explain:
- what failure it targets
- which profiles it affects
- what a PASS output looks like
- what a FAIL output looks like

---

## First fixture families

1. long-paragraphs
2. mixed-script-headings
3. long-url-overflow
4. forms-ime-errors
5. dense-tables
6. mobile-wrap-stress
7. docs-prose-code
