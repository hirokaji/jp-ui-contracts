// Opt-in Playwright helper. DESIGN.md remains the only hand-edited contract.
// This does not certify arbitrary CSS clipping, accessibility, or visual taste.
export function parseMeasuredElements(markdown) {
  const sections = markdown.split(/^## Measured Elements\s*$/m);
  if (sections.length !== 2) throw new Error('Exactly one Measured Elements section is required');
  const section = sections[1].split(/^## /m)[0];
  const rows = section.split('\n').filter(line => line.trim().startsWith('|'));
  const cells = row => row.trim().slice(1, -1).split('|').map(x => x.trim());
  if (JSON.stringify(cells(rows[0] || '||')) !== JSON.stringify(['Selector', 'Min font px', 'Min line-height', 'Overflow'])) {
    throw new Error('Unsupported measured-elements table header');
  }
  if (!/^\|[\s:|-]+\|$/.test(rows[1] || '')) throw new Error('Table separator is required');
  const seen = new Set();
  const targets = rows.slice(2).map(row => {
    if (!row.endsWith('|')) throw new Error('Table row must end with |');
    const fields = cells(row);
    const [selector, font, line, overflow] = fields;
    if (fields.length !== 4 || !selector || seen.has(selector)
      || !/^\d+(\.\d+)?$/.test(font) || !/^\d+(\.\d+)?$/.test(line)
      || !Number.isFinite(Number(font)) || !Number.isFinite(Number(line)) || Number(font) <= 0 || Number(line) <= 0 || !['fit', 'scroll-x'].includes(overflow)) {
      throw new Error('Invalid or duplicate measured element');
    }
    seen.add(selector);
    return { selector, minFontPx: Number(font), minLineHeight: Number(line), overflow };
  });
  if (!targets.length) throw new Error('No measured elements');
  return targets;
}

export async function inspectMeasuredElements(page, targets) {
  if (!Array.isArray(targets) || !targets.length) throw new Error('No measured elements');
  if (targets.some(target => typeof target.selector !== 'string' || !target.selector.trim()
    || !Number.isFinite(target.minFontPx) || target.minFontPx <= 0
    || !Number.isFinite(target.minLineHeight) || target.minLineHeight <= 0
    || !['fit', 'scroll-x'].includes(target.overflow))) throw new Error('Invalid measured element');
  // Invalid CSS selectors throw; callers must report inspection error, never PASS.
  return page.evaluate(targets => targets.map(target => {
    const elements = document.querySelectorAll(target.selector);
    if (elements.length !== 1) return { ...target, status: 'FAIL', reason: 'Expected exactly one element', count: elements.length };
    const element = elements[0];
    const css = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    const fontPx = Number.parseFloat(css.fontSize);
    const lineHeightPx = Number.parseFloat(css.lineHeight);
    const visible = element.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true }) && rect.width > 0 && rect.height > 0;
    const horizontalExcess = element.scrollWidth - element.clientWidth;
    const verticalExcess = element.scrollHeight - element.clientHeight;
    const fits = horizontalExcess <= 1 && verticalExcess <= 1;
    const scrolls = ['auto', 'scroll'].includes(css.overflowX) && verticalExcess <= 1;
    const status = visible && Number.isFinite(lineHeightPx)
      && fontPx >= target.minFontPx && lineHeightPx / fontPx + 0.001 >= target.minLineHeight
      && (target.overflow === 'fit' ? fits : scrolls) ? 'PASS' : 'FAIL';
    return { ...target, status, visible, fontPx, lineHeightPx, horizontalExcess, verticalExcess, overflowX: css.overflowX };
  }), targets);
}
