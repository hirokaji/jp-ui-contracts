# DESIGN.md — Chronicle Notes

> Profile: media

---

## 0. Contract Metadata

- **Locale**: `ja-JP`
- **Profile**: `media`
- **Primary writing mode**: `horizontal-tb`
- **Target surfaces**: `web`
- **Review status**: `verified`
- **Last reviewed at**: `2026-04-07`
- **Reviewer**: `editorial-team`

---

## 1. Reading Experience

- Long-form reading is the primary use case
- Calm, modern, slightly editorial
- Visual noise must stay low
- Japanese paragraphs should feel breathable, not loose

---

## 2. Typography

### Japanese fonts
- **Sans**: `"Noto Sans JP", "Hiragino Sans", "Yu Gothic UI", Meiryo, sans-serif`
- **Serif**: `"Noto Serif JP", "Hiragino Mincho ProN", "Yu Mincho", serif`
- **Mono**: `"BIZ UDGothic", "SFMono-Regular", Consolas, monospace`

### Latin fonts
- **Sans**: `"Inter", "Helvetica Neue", Arial, sans-serif`
- **Serif**: `"Source Serif 4", Georgia, serif`
- **Mono**: `"JetBrains Mono", "SFMono-Regular", Consolas, monospace`

### Type scale

| Role | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|--------|-------------|----------------|------|
| H1 | 34px | 700 | 1.4 | 0.02em | primary article title |
| H2 | 28px | 700 | 1.5 | 0.02em | section title |
| H3 | 22px | 700 | 1.55 | 0.01em | subsection |
| Body | 18px | 400 | 1.9 | normal | reading-first |
| Caption | 14px | 400 | 1.7 | normal | support |

---

## 3. Line Break

```css
html:lang(ja) {
  line-break: strict;
  word-break: normal;
  overflow-wrap: anywhere;
}
```

- Never globalize `word-break: break-all`
- Mixed-script headings must be reviewed at mobile width
- Long URLs must wrap without damaging paragraph rhythm

---

## 4. Layout

- Reading width: `42em`
- Single-column article body
- Large top spacing before sections
- Images should punctuate rhythm, not fragment it

---

## 5. Validation Targets

- Must pass long paragraph review
- Must pass mobile article review
- Must pass mixed-script title review
- Must pass long URL review
