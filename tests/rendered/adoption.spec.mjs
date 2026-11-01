import { test, expect } from '@playwright/test';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { readFile, readdir, copyFile, mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { createServer } from 'node:http';

const execute = promisify(execFile);
const base = 'http://127.0.0.1:4173/examples/overflow-walkthrough';
let server, origin;

test.beforeAll(async () => {
  server = createServer((req, res) => {
    if (req.url === '/missing') { res.writeHead(404); res.end('Not found'); return; }
    if (req.url === '/redirect') { res.writeHead(302, { Location: `${base}/after.html` }); res.end(); return; }
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.end('<html lang="ja"><body style="margin:0"><div style="width:100%;overflow:hidden"><div style="width:2000px">切り落とされる内容</div></div></body></html>');
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  origin = `http://127.0.0.1:${server.address().port}`;
});
test.afterAll(async () => { if (server) await new Promise(resolve => server.close(resolve)); });

async function cli(testInfo, url, extra = []) {
  const output = testInfo.outputPath('ui-evidence');
  let code = 0, stdout, stderr;
  try {
    ({ stdout, stderr } = await execute(process.execPath,
      ['validators/overflow.mjs', '--url', url, '--output', output, ...extra], { timeout: 25000 }));
  } catch (error) {
    if (typeof error.code !== 'number') throw error;
    code = error.code; stdout = error.stdout; stderr = error.stderr;
  }
  const runs = (await readdir(output)).sort();
  const reports = await Promise.all(runs.map(async name => ({
    directory: join(output, name), report: JSON.parse(await readFile(join(output, name, 'report.json'), 'utf8')),
  })));
  return { code, stdout, stderr, reports };
}

test('walkthrough detects the failure, verifies the repair and captures README evidence', async ({}, testInfo) => {
  const before = await cli(testInfo, `${base}/before.html`);
  expect(before.code).toBe(1);
  const broken = before.reports[0];
  expect(broken.report.status).toBe('FAIL');
  expect(broken.report.checks[0].excessPx).toBeGreaterThan(1);
  const after = await cli(testInfo, `${base}/after.html`, ['--ready-selector', '[data-ui-ready]']);
  expect(after.code).toBe(0);
  expect(after.reports).toHaveLength(2); // Evidence is not overwritten between executions.
  const fixed = after.reports.find(x => x.report.targetUrl.endsWith('/after.html'));
  expect(fixed.report.status).toBe('PASS');
  expect(fixed.report.metrics.clientWidth).toBe(412);
  const target = testInfo.outputPath('walkthrough');
  await mkdir(target);
  await copyFile(join(broken.directory, 'viewport.png'), join(target, 'before.png'));
  await copyFile(join(fixed.directory, 'viewport.png'), join(target, 'after.png'));
  await writeFile(join(target, 'measurements.json'), JSON.stringify({
    generatedBy: 'tests/rendered/adoption.spec.mjs',
    note: 'Synthetic demonstration, not a reported production incident. Resized desktop Chromium; not Pixel 7 emulation.',
    before: broken.report, after: fixed.report,
  }, null, 2) + '\n');
  for (const name of ['before.png', 'after.png']) {
    await testInfo.attach(name, { path: join(target, name), contentType: 'image/png' });
  }
});

test('repair also passes at desktop width', async ({}, testInfo) => {
  const result = await cli(testInfo, `${base}/after.html`, ['--width', '1440', '--height', '1000']);
  expect(result.code).toBe(0);
  expect(result.reports[0].report.viewport.width).toBe(1440);
});

test('HTTP errors produce ERROR evidence and exit 2', async ({}, testInfo) => {
  const result = await cli(testInfo, `${origin}/missing`);
  expect(result.code).toBe(2);
  expect(result.reports[0].report.status).toBe('ERROR');
  expect(result.reports[0].report.httpStatus).toBe(404);
  expect(result.reports[0].report.checks).toHaveLength(0);
});

test('missing readiness selector does not pass', async ({}, testInfo) => {
  const result = await cli(testInfo, `${base}/after.html`, ['--ready-selector', '#not-ready', '--timeout', '2000']);
  expect(result.code).toBe(2);
  expect(result.reports[0].report.status).toBe('ERROR');
});

test('connection failure and cross-origin redirect do not pass', async ({}, testInfo) => {
  const redirect = await cli(testInfo, `${origin}/redirect`);
  expect(redirect.code).toBe(2);
  expect(redirect.reports[0].report.error).toContain('left the requested origin');
  const closed = createServer();
  await new Promise(resolve => closed.listen(0, '127.0.0.1', resolve));
  const port = closed.address().port;
  await new Promise(resolve => closed.close(resolve));
  const result = await cli(testInfo, `http://127.0.0.1:${port}/`, ['--timeout', '2000']);
  expect(result.code).toBe(2);
  expect(result.reports.every(x => x.report.status === 'ERROR')).toBe(true);
});

test('clipped content documents a PASS that is not overall UI approval', async ({}, testInfo) => {
  const result = await cli(testInfo, `${origin}/clipped`);
  expect(result.code).toBe(0);
  expect(result.reports[0].report.notChecked.join(' ')).toContain('Clipped or hidden content');
});
