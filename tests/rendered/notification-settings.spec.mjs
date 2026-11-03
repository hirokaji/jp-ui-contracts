import { test, expect } from '@playwright/test';
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { parseMeasuredElements, inspectMeasuredElements } from '../../validators/measured-elements.mjs';

const directory = 'examples/notification-settings';
const contract = await readFile(`${directory}/DESIGN.md`, 'utf8');
const targets = parseMeasuredElements(contract);
const files = ['DESIGN.md', 'before.html', 'after.html', 'settings.js', 'styles.css'];
const sourceHashes = Object.fromEntries(await Promise.all(files.map(async file => [file,
  createHash('sha256').update(await readFile(`${directory}/${file}`)).digest('hex')])));

async function open(page, variant, state) {
  await page.goto(`/${directory}/${variant}.html?state=${state}`);
  await expect(page.locator('[data-ui-ready]')).toBeVisible();
  await page.evaluate(() => document.fonts.ready);
}
async function evidence(page, testInfo, name, checks) {
  const path = testInfo.outputPath(`${name}.png`);
  await page.screenshot({ path, fullPage: true });
  await testInfo.attach(name, { path, contentType: 'image/png' });
  await testInfo.attach(`${name}-measurements`, { contentType: 'application/json', body: Buffer.from(JSON.stringify({
    sourceHashes, url: page.url(), viewport: page.viewportSize(), browser: page.context().browser().version(),
    measuredAt: new Date().toISOString(), checks,
    notChecked: ['native IME', 'screen reader', '200% browser zoom', 'user task time', 'ancestor clipping/overlap', 'visual taste'],
  }, null, 2)) });
}

for (const state of ['normal', 'long', 'empty', 'error']) {
  test(`settings ${state}: same content, explicit geometry and Evidence`, async ({ page }, testInfo) => {
    await open(page, 'before', state);
    const beforeText = await page.locator('main').innerText();
    const beforeName = await page.locator('#display-name').inputValue();
    const before = await inspectMeasuredElements(page, targets);
    const root = await page.evaluate(() => ({ client: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth }));
    expect(root.scroll).toBeLessThanOrEqual(root.client + 1);
    if (state === 'long') expect(before.find(x => x.selector === '#delivery-label').status).toBe('FAIL');
    await evidence(page, testInfo, `before-${state}`, before);
    await open(page, 'after', state);
    expect(await page.locator('main').innerText()).toBe(beforeText);
    expect(await page.locator('#display-name').inputValue()).toBe(beforeName);
    const after = await inspectMeasuredElements(page, targets);
    expect(after.every(x => x.status === 'PASS'), JSON.stringify(after)).toBe(true);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1)).toBe(true);
    if (state === 'error') {
      await expect(page.getByRole('alert')).toBeVisible();
      await expect(page.locator('#display-name')).toBeFocused();
    } else await expect(page.getByRole('alert')).toBeHidden();
    await evidence(page, testInfo, `after-${state}`, after);
  });
}

test('settings: keyboard, error recovery and reset preserve behavior', async ({ page }) => {
  for (const variant of ['before', 'after']) {
    await open(page, variant, 'empty');
    await page.keyboard.press('Tab');
    await expect(page.locator('#display-name')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.locator('#delivery')).toBeFocused();
    await page.keyboard.press('Space');
    await expect(page.locator('#delivery')).not.toBeChecked();
    await page.keyboard.press('Tab');
    await expect(page.locator('#save')).toBeFocused();
    const focus = await page.locator('#save').evaluate(el => ({ style: getComputedStyle(el).outlineStyle, width: getComputedStyle(el).outlineWidth }));
    expect(focus.style).not.toBe('none');
    expect(Number.parseFloat(focus.width)).toBeGreaterThanOrEqual(2);
    await page.keyboard.press('Enter');
    await expect(page.getByRole('alert')).toBeVisible();
    await expect(page.locator('#display-name')).toBeFocused();
    await page.keyboard.insertText('海外サービス品質保証');
    await page.keyboard.press('Enter');
    await expect(page.getByRole('status')).toContainText('このページ内に設定を保存しました');
    await expect(page.getByRole('alert')).toBeHidden();
    await page.locator('#reset').focus();
    await page.keyboard.press('Enter');
    await expect(page.locator('#display-name')).toHaveValue('');
    await expect(page.locator('#delivery')).toBeChecked();
    await expect(page.getByRole('status')).toBeEmpty();
    await expect(page.getByRole('alert')).toBeHidden();
  }
});

test('settings: 320px long label retains measured content', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 320, height: 839 });
  await open(page, 'after', 'long');
  const checks = await inspectMeasuredElements(page, targets);
  expect(checks.every(x => x.status === 'PASS'), JSON.stringify(checks)).toBe(true);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1)).toBe(true);
  await evidence(page, testInfo, 'after-320', checks);
});

test('measured elements: reject clipping, tiny text, hidden/missing/ambiguous targets; allow declared scrolling', async ({ page }) => {
  await page.setContent(`<div id="target" style="font-size:16px;line-height:1.6;width:100px;overflow:hidden;white-space:nowrap">長い日本語ラベルが欠ける反例を再現する</div>`);
  const target = [{ selector: '#target', minFontPx: 16, minLineHeight: 1.5, overflow: 'fit' }];
  expect((await inspectMeasuredElements(page, target))[0].status).toBe('FAIL');
  await page.locator('#target').evaluate(el => el.style.overflowX = 'auto');
  expect((await inspectMeasuredElements(page, [{ ...target[0], overflow: 'scroll-x' }]))[0].status).toBe('PASS');
  await page.locator('#target').evaluate(el => { el.style.whiteSpace = 'normal'; el.style.fontSize = '10px'; });
  expect((await inspectMeasuredElements(page, target))[0].status).toBe('FAIL');
  await page.locator('#target').evaluate(el => { el.style.fontSize = '16px'; el.style.lineHeight = '1'; });
  expect((await inspectMeasuredElements(page, target))[0].status).toBe('FAIL');
  await page.locator('#target').evaluate(el => { el.style.lineHeight = '1.6'; el.hidden = true; });
  expect((await inspectMeasuredElements(page, target))[0].status).toBe('FAIL');
  expect((await inspectMeasuredElements(page, [{ ...target[0], selector: '#missing' }]))[0].status).toBe('FAIL');
  await page.setContent('<p>one</p><p>two</p>');
  expect((await inspectMeasuredElements(page, [{ ...target[0], selector: 'p' }]))[0].status).toBe('FAIL');
  await expect(inspectMeasuredElements(page, [{ ...target[0], selector: '[' }])).rejects.toThrow();
});

test('measured contract: malformed, empty and duplicate tables cannot pass silently', () => {
  expect(targets).toHaveLength(4);
  for (const bad of ['', contract.replace('| Selector | Min font px |', '| Selector | Font |'), contract.replace('| 16 |', '| NaN |'),
    contract.replace('| #reset |', '| #save |'), contract.replace(/\| #.*\n/g, '')]) {
    expect(() => parseMeasuredElements(bad)).toThrow();
  }
});
