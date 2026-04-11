# DESIGN.md — [Project Name]

> Profile: dashboard

---

## 0. Contract Metadata

- **Locale**: `ja-JP`
- **Profile**: `dashboard`
- **Review status**: `draft`

---

## 1. Dashboard Intent

- High-density information scan is the primary use case
- Metrics, labels, filters, tables, and cards must remain separable
- Readability must hold under repeated operational use

---

## 2. Typography Defaults

| Role | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|--------|-------------|----------------|------|
| H1 | 24px | 700 | 1.3 | 0 | page title |
| H2 | 18px | 600 | 1.35 | 0 | card title |
| Body | 14px | 400 | 1.5 | 0 | default text |
| Caption | 12px | 400 | 1.4 | 0 | support text |
| Metric | 24px | 700 | 1.2 | 0 | number emphasis |
| Label | 12px | 500 | 1.35 | 0 | compact metadata |

### Rules
- Paragraph rhythm is secondary to scanability
- Table density must remain readable
- Numeric alignment and label wrapping must be reviewed together
- Filters and controls must keep enough tap area

---

## 3. Layout Defaults

- Prefer modular cards
- Preserve clear information grouping
- Avoid decorative whitespace that hides relationships
- Compress width before compressing text rhythm too far

---

## 4. Validation Targets

- Must pass card scan review
- Must pass metric readability review
- Must pass dense table review
- Must pass mobile overflow review
