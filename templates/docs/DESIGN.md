# DESIGN.md — [Project Name]

> Profile: docs

---

## 0. Contract Metadata

- **Locale**: `ja-JP`
- **Profile**: `docs`
- **Review status**: `draft`

---

## 1. Documentation Intent

- Technical explanation is the primary use case
- Prose, code, table, callout, and navigation must be distinguishable
- Readers must be able to skim and dive

---

## 2. Typography Defaults

| Role | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|--------|-------------|----------------|------|
| H1 | 30px | 700 | 1.35 | 0 | page title |
| H2 | 24px | 700 | 1.4 | 0 | section title |
| H3 | 20px | 600 | 1.45 | 0 | subsection |
| Body | 16px | 400 | 1.7 | normal | explanation |
| Caption | 13px | 400 | 1.6 | normal | note/support |
| Code | 14px | 400 | 1.7 | 0 | code/text contrast |

### Rules
- Paragraph rhythm must support sustained reading
- Code blocks must not inherit paragraph spacing blindly
- Tables must not use article defaults
- Mixed Japanese and English technical terms must remain legible

---

## 3. Layout Defaults

- Reading width should support code and prose balance
- Long lines in code must have a clear handling policy
- TOC, callouts, and examples must remain visually distinct

---

## 4. Validation Targets

- Must pass prose reading review
- Must pass code block review
- Must pass table review
- Must pass mixed-script technical heading review
