import { chromium } from '@playwright/test';
import { mkdir, mkdtemp, writeFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

export const scope = 'Document-level horizontal overflow at one viewport in Chromium';
export const notChecked = [
  'DESIGN.md conformance, typography and reading comfort',
  'Clipped or hidden content, local component overflow and accessibility compliance',
  'Native IME operation, other states, viewports and browsers',
];

function boundedInteger(value, name, min, max) {
  if (!/^\d+$/.test(value) || Number(value) < min || Number(value) > max) {
    throw new Error(`${name} must be an integer between ${min} and ${max}`);
  }
  return Number(value);
}

export function parseOptions(args) {
  const { values } = parseArgs({ args, options: {
    url: { type: 'string' }, width: { type: 'string', default: '412' },
    height: { type: 'string', default: '839' },
    timeout: { type: 'string', default: '15000' },
    'ready-selector': { type: 'string' },
    output: { type: 'string', default: 'ui-evidence' },
    help: { type: 'boolean', short: 'h' },
  } });
  if (values.help) return { help: true };
  if (!values.url) throw new Error('--url is required');
  const url = new URL(values.url);
  if (!['http:', 'https:'].includes(url.protocol) ||
      !['localhost', '127.0.0.1', '[::1]'].includes(url.hostname) ||
      url.username || url.password) {
    throw new Error('--url must be a local HTTP(S) URL without embedded credentials (localhost, 127.0.0.1 or [::1])');
  }
  if (values['ready-selector'] !== undefined && !values['ready-selector'].trim()) {
    throw new Error('--ready-selector must not be empty');
  }
  return {
    url: url.href,
    width: boundedInteger(values.width, '--width', 240, 4096),
    height: boundedInteger(values.height, '--height', 240, 4096),
    timeout: boundedInteger(values.timeout, '--timeout', 100, 120000),
    readySelector: values['ready-selector'] ?? 'body', output: values.output,
  };
}

// This measures a page. It does not parse or certify a DESIGN.md contract.
export async function checkOverflow(options) {
  const root = resolve(options.output);
  await mkdir(root, { recursive: true });
  const directory = await mkdtemp(join(root, 'run-'));
  const report = {
    schemaVersion: 1, status: 'ERROR', scope, notChecked,
    startedAt: new Date().toISOString(), targetUrl: options.url,
    viewport: { width: options.width, height: options.height },
    readiness: { selector: options.readySelector, fonts: 'loaded', timeoutMs: options.timeout },
    checks: [],
  };
  let browser;
  try {
    browser = await chromium.launch();
    report.browser = { name: 'chromium', version: browser.version() };
    const page = await browser.newPage({ viewport: report.viewport, locale: 'ja-JP' });
    const response = await page.goto(options.url, { waitUntil: 'load', timeout: options.timeout });
    report.finalUrl = page.url();
    report.httpStatus = response?.status() ?? null;
    if (!response || !response.ok()) throw new Error(`Navigation did not return HTTP 2xx (${report.httpStatus})`);
    if (new URL(page.url()).origin !== new URL(options.url).origin) {
      throw new Error('Navigation left the requested origin; the requested UI was not verified');
    }
    await page.locator(options.readySelector).first().waitFor({ state: 'visible', timeout: options.timeout });
    await page.waitForFunction(() => document.fonts.status === 'loaded', null, { timeout: options.timeout });
    const metrics = await page.evaluate(() => ({
      title: document.title, lang: document.documentElement.lang,
      clientWidth: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
      bodyScrollWidth: document.body?.scrollWidth ?? null,
    }));
    report.metrics = metrics;
    if (metrics.clientWidth <= 0) throw new Error('Document has no measurable viewport width');
    const excessPx = metrics.scrollWidth - metrics.clientWidth;
    const status = excessPx <= 1 ? 'PASS' : 'FAIL';
    report.checks.push({ id: 'document-horizontal-overflow', status, excessPx, tolerancePx: 1 });
    await page.screenshot({ path: join(directory, 'viewport.png'), fullPage: false, timeout: options.timeout });
    report.screenshot = 'viewport.png';
    report.status = status;
  } catch (error) {
    report.status = 'ERROR';
    report.error = error.message;
  } finally {
    if (browser) {
      try { await browser.close(); } catch (error) {
        report.status = 'ERROR'; report.error = `Browser cleanup failed: ${error.message}`;
      }
    }
    report.finishedAt = new Date().toISOString();
    await writeFile(join(directory, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  }
  return { report, directory, exitCode: { PASS: 0, FAIL: 1, ERROR: 2 }[report.status] };
}

async function main() {
  try {
    const options = parseOptions(process.argv.slice(2));
    if (options.help) {
      console.log('Usage: npm run check:ui -- --url http://127.0.0.1:3000/ [--width 412] [--height 839] [--ready-selector "[data-ui-ready]"] [--timeout 15000] [--output ui-evidence]');
      console.log('Checks document horizontal overflow only. Exit codes: 0 PASS, 1 FAIL, 2 ERROR. No contract certification.');
      return;
    }
    const { report, directory, exitCode } = await checkOverflow(options);
    console.log(`${report.status} document-horizontal-overflow`);
    if (report.metrics) console.log(`clientWidth=${report.metrics.clientWidth} scrollWidth=${report.metrics.scrollWidth}`);
    if (report.error) console.error(report.error);
    console.log(`Evidence: ${directory}`);
    console.log('Not checked: ' + notChecked.join('; '));
    process.exitCode = exitCode;
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exitCode = 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) await main();
