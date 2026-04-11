# DESIGN.md — [Project Name]

> Profile: media

---

## 0. Contract Metadata

- **Locale**: `ja-JP`
- **Profile**: `media`
- **Review status**: `draft`

---

## 1. Reading Experience

- Long-form reading is the primary use case
- Vertical rhythm must feel spacious
- Visual noise must stay low
- Headings should guide pace, not overpower paragraphs

---

## 2. Typography Defaults

| Role | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|--------|-------------|----------------|------|
| H1 | 32px | 700 | 1.4 | 0.02em | calm emphasis |
| H2 | 26px | 700 | 1.5 | 0.02em | section anchor |
| H3 | 22px | 700 | 1.55 | 0.01em | subsection anchor |
| Body | 18px | 400 | 1.85 | normal | reading-first |
| Caption | 14px | 400 | 1.7 | normal | supportive text |

### Rules
- Body line-height should usually remain within `1.75–2.0`
- Body letter-spacing should usually remain `normal`
- Paragraph spacing must be generous enough to avoid wall-of-text feeling
- Pull quotes and lead text may slightly diverge, but body must remain stable

---

## 3. Layout Defaults

- Reading width: `38–44em`
- Prefer single-column reading for article body
- Side metadata must not disrupt paragraph rhythm
- Images should reset pace, not fragment flow

---

## 4. Validation Targets

- Must pass long article reading review
- Must pass mobile article review
- Must pass mixed-script title review
- Must pass caption readability review
