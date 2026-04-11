# DESIGN.md — Ops Console

> Profile: saas

---

## 0. Contract Metadata

- **Locale**: `ja-JP`
- **Profile**: `saas`
- **Primary writing mode**: `horizontal-tb`
- **Target surfaces**: `web`
- **Review status**: `verified`
- **Last reviewed at**: `2026-04-07`
- **Reviewer**: `product-design-team`

---

## 1. Product Use

- Internal business dashboard
- Frequent daily use
- Dense information with stable scanability
- Long Japanese labels should remain legible

---

## 2. Typography

### Japanese fonts
- **Sans**: `"Noto Sans JP", "Hiragino Sans", "Yu Gothic UI", Meiryo, sans-serif`
- **Mono**: `"BIZ UDGothic", "SFMono-Regular", Consolas, monospace`

### Latin fonts
- **Sans**: `"Inter", "Helvetica Neue", Arial, sans-serif`
- **Mono**: `"JetBrains Mono", "SFMono-Regular", Consolas, monospace`

### Type scale

| Role | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|--------|-------------|----------------|------|
| H1 | 28px | 700 | 1.35 | 0 | page title |
| H2 | 20px | 700 | 1.4 | 0 | section title |
| H3 | 16px | 600 | 1.45 | 0 | group label |
| Body | 14px | 400 | 1.55 | 0 | default UI text |
| Caption | 12px | 400 | 1.45 | 0 | helper text |
| Label | 13px | 500 | 1.4 | 0 | field labels |

---

## 3. Form and Table Policy

- Forms must not inherit article-style spacing
- Mixed Japanese-English navigation must be reviewed
- Long labels may wrap, but buttons must stay readable
- Numeric tables require separate density tuning

---

## 4. Validation Targets

- Must pass form density review
- Must pass table scan review
- Must pass mobile overflow review
- Must pass mixed navigation review
