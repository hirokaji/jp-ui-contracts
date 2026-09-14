import { test, expect } from '@playwright/test';

const fixtures = [
  'long-paragraphs',
  'mixed-script-headings',
  'long-url-overflow',
  'forms-ime-errors',
  'dense-tables',
  'mobile-wrap-stress',
];

async function captureEvidence(page, testInfo, fixture) {
  const metrics = await page.evaluate(() => {
    const root = document.documentElement;
    const body = document.body;
    return {
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight,
        devicePixelRatio: window.devicePixelRatio,
      },
      document: {
        clientWidth: root.clientWidth,
        scrollWidth: root.scrollWidth,
        bodyScrollWidth: body.scrollWidth,
      },
      title: document.title,
      lang: root.lang,
    };
  });

  const screenshotPath = testInfo.outputPath(`${fixture}.png`);
  await page.screenshot({ path: screenshotPath, fullPage: true });
  await testInfo.attach('rendered-screenshot', {
    path: screenshotPath,
    contentType: 'image/png',
  });
  await testInfo.attach('render-evidence', {
    body: Buffer.from(JSON.stringify({ fixture, ...metrics }, null, 2)),
    contentType: 'application/json',
  });

  return metrics;
}

for (const fixture of fixtures) {
  test(`${fixture}: renders without document-level horizontal overflow`, async ({ page }, testInfo) => {
    await page.goto(`/fixtures/${fixture}/index.html`);
    await expect(page.locator('html')).toHaveAttribute('lang', 'ja');
    await expect(page.locator(`[data-fixture="${fixture}"]`)).toBeVisible();

    const metrics = await captureEvidence(page, testInfo, fixture);
    expect(metrics.document.scrollWidth).toBeLessThanOrEqual(metrics.document.clientWidth + 1);
  });
}

test('dense-tables: table overflow is contained locally', async ({ page }, testInfo) => {
  await page.goto('/fixtures/dense-tables/index.html');
  const scroller = page.locator('[data-table-scroll]');
  const table = scroller.locator('table');

  await expect(scroller).toBeVisible();
  await expect(table).toBeVisible();

  const geometry = await scroller.evaluate((element) => ({
    clientWidth: element.clientWidth,
    scrollWidth: element.scrollWidth,
    overflowX: getComputedStyle(element).overflowX,
  }));
  expect(['auto', 'scroll']).toContain(geometry.overflowX);

  await testInfo.attach('table-geometry', {
    body: Buffer.from(JSON.stringify(geometry, null, 2)),
    contentType: 'application/json',
  });
});

test('forms-ime-errors: labels, helper text, errors and controls remain inspectable', async ({ page }) => {
  await page.goto('/fixtures/forms-ime-errors/index.html');

  await expect(page.getByLabel('会社・組織名')).toBeVisible();
  await expect(page.getByLabel('問い合わせ内容')).toBeVisible();
  await expect(page.locator('[data-helper]')).toBeVisible();
  await expect(page.locator('[data-error]')).toBeVisible();

  const controls = page.locator('input, textarea, button');
  await expect(controls.first()).toBeVisible();
  expect(await controls.count()).toBeGreaterThanOrEqual(4);
});

test('mobile-wrap-stress: mobile targets keep a minimum 44px action height', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'mobile-chromium', 'mobile-specific gate');
  await page.goto('/fixtures/mobile-wrap-stress/index.html');

  const targets = page.locator('[data-min-tap]');
  const count = await targets.count();
  expect(count).toBeGreaterThan(0);

  for (let index = 0; index < count; index += 1) {
    const box = await targets.nth(index).boundingBox();
    expect(box, `target ${index} should have a bounding box`).not.toBeNull();
    expect(box.height, `target ${index} height`).toBeGreaterThanOrEqual(44);
  }
});
