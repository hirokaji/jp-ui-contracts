# DESIGN.md — [Project Name]

> Japanese UI design contract for AI agents and human reviewers.

---

## 0. Contract Metadata

- **Locale**: `ja-JP`
- **Profile**: `base`
- **Primary writing mode**: `horizontal-tb`
- **Target surfaces**: `web`
- **Review status**: `draft`
- **Last reviewed at**: `YYYY-MM-DD`
- **Reviewer**: `[name/team]`

---

## 1. Product Intent

- **What this product is**:
- **Primary audience**:
- **Primary usage context**:
- **Design stance**:
- **Must feel like**:
- **Must not feel like**:

---

## 2. Visual Theme & Brand Signals

- **Keywords**:
- **Visual temperature**: `calm | neutral | warm | sharp`
- **Density**: `airy | balanced | compact`
- **Tone**:
- **Motion stance**: `minimal | moderate | expressive`

---

## 3. Color System

### Brand colors
- **Primary**: `#000000`
- **Primary hover**:
- **Accent**:

### Semantic colors
- **Success**:
- **Warning**:
- **Danger**:
- **Info**:

### Neutral colors
- **Text primary**:
- **Text secondary**:
- **Text muted**:
- **Border**:
- **Background**:
- **Surface**:
- **Surface elevated**:

### Color usage rules
- Do not rely on color alone for meaning
- Keep primary actions visually distinct
- Avoid low-contrast muted text on tinted surfaces

---

## 4. Typography System

### 4.1 Japanese fonts
- **Sans**:
- **Serif**:
- **Mono**:

### 4.2 Latin fonts
- **Sans**:
- **Serif**:
- **Mono**:

### 4.3 Fallback policy
```css
font-family: "Preferred Japanese Font", "Preferred Latin Font", sans-serif;
```

- Japanese fallback must be explicit
- Font stack must be stable on macOS and Windows
- Avoid leaving Japanese rendering to browser defaults

### 4.4 Type scale

| Role | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|--------|-------------|----------------|------|
| Display |  |  |  |  |  |
| H1 |  |  |  |  |  |
| H2 |  |  |  |  |  |
| H3 |  |  |  |  |  |
| Body L |  |  |  |  |  |
| Body M |  |  |  |  |  |
| Body S |  |  |  |  |  |
| Caption |  |  |  |  |  |
| Label |  |  |  |  |  |
| Mono |  |  |  |  |  |

### 4.5 Japanese paragraph rules
- Default Japanese body line-height should usually stay within `1.5–2.0`
- Default Japanese body letter-spacing should usually remain `normal` or conservative
- Do not apply aggressive tracking to body text by default
- Heading and label spacing may differ from body spacing

### 4.6 Mixed-script rules
- Review Japanese + Latin text together
- Avoid visual collision in headings containing English product names
- Do not optimize Latin words in a way that harms Japanese paragraph rhythm
- Numeric strings, code, and IDs may require separate handling

### 4.7 OpenType and rendering
```css
font-kerning: auto;
font-feature-settings: normal;
```

- `palt` may be used for headings or navigation after visual review
- Avoid global `palt` on body text unless reading comfort is verified
- Use proportional settings only where they improve actual reading

### 4.8 Writing direction
- Default writing direction is horizontal
- Vertical writing is: `not used`

---

## 5. Line Breaking & Overflow

### Default rules
```css
html:lang(ja) {
  line-break: strict;
  word-break: normal;
  overflow-wrap: anywhere;
}
```

### Additional rules
- Do not use global `word-break: break-all`
- Use stronger breaking only for logs, hashes, URLs, and machine-like strings
- Review headings at narrow widths
- Review long English words inside Japanese UI
- Prevent URL overflow without breaking paragraph readability

### Optional enhancement
```css
h1:lang(ja),
h2:lang(ja),
h3:lang(ja) {
  word-break: auto-phrase;
}
```

### Experimental enhancement
```css
html:lang(ja) {
  text-autospace: normal;
}
```

- Treat `text-autospace` as progressive enhancement
- Do not make it a hard dependency

---

## 6. Layout Principles

- **Container width**:
- **Reading width**:
- **Grid system**:
- **Spacing scale**:
- **Section spacing rule**:
- **Whitespace policy**:

### Layout rules
- Reading width must prioritize comfort for Japanese paragraphs
- Dense UI should compress containers before compressing line-height
- Visual grouping should rely on spacing before borders when possible

---

## 7. Component Guidelines

### Buttons
- Primary button must be obvious
- Label length in Japanese must be tested
- Avoid overly short button heights in compact layouts

### Inputs
- Placeholder is not a label replacement
- Japanese IME input states must remain legible
- Error and help text must stay readable at smaller sizes

### Cards
- Keep title, body, meta, and actions visually separated
- Do not collapse vertical rhythm to fit more content unless profile requires it

### Tables
- Table density must be tuned separately from paragraph density
- Numeric alignment and label wrapping must be reviewed
- Avoid applying article-style line-height to high-density tables

### Navigation
- Mixed Japanese and English labels must be reviewed
- Active state must be visible without relying on color alone

### Modals / Drawers
- Long Japanese text must not create cramped vertical rhythm
- Confirm and cancel actions must remain distinct

---

## 8. Depth, Border, and Surface

### Surface levels
| Level | Usage | Border | Shadow |
|------|------|--------|--------|
| 0 | Page background | none | none |
| 1 | Base surface | optional | subtle |
| 2 | Raised card | optional | subtle |
| 3 | Modal / overlay | optional | moderate |

### Rules
- Prefer subtle depth
- Avoid decorative shadows that reduce seriousness
- Use border and elevation consistently

---

## 9. Responsive Behavior

- **Breakpoints**:
- **Mobile reading width**:
- **Tablet layout stance**:
- **Desktop layout stance**:

### Responsive rules
- Recheck paragraph rhythm on mobile
- Recheck heading wrapping on mobile
- Table fallback strategy must be explicit
- Form spacing must be verified on small screens
- Dense desktop UI must not be copied directly onto mobile

---

## 10. Motion & Interaction

- **Animation stance**:
- **Transition speed**:
- **Reduced motion policy**:

### Rules
- Motion should support hierarchy, not decorate it
- Avoid large shifts that disturb reading
- Loading states must stay legible in Japanese

---

## 11. Do's and Don'ts

### Do
- Preserve Japanese reading comfort
- Keep mixed-script text visually balanced
- Review actual line breaks at real widths
- Separate paragraph rules from table rules
- Prefer stable defaults over clever tricks

### Don't
- Do not globalize `word-break: break-all`
- Do not copy Latin-first typography blindly
- Do not increase body letter-spacing without clear reason
- Do not use body line-height that feels compressed for long Japanese text
- Do not accept screenshots alone as final validation

---

## 12. Agent Prompt Guide

Use calm, readable Japanese typography.

Honor the locale and profile before inventing stylistic variations.

Preserve readability first when there is tension between novelty and comfort.

When uncertain:
- keep body text conservative
- keep headings clear
- avoid aggressive spacing
- avoid fragile wrapping rules

Do not imitate Western editorial spacing in Japanese body text without review.

---

## 13. Validation Targets

- Must pass long paragraph review
- Must pass mixed-script heading review
- Must pass long URL overflow review
- Must pass form density review
- Must pass mobile layout review
- Must pass color contrast review
