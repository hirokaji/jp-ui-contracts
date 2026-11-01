import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseOptions } from '../validators/overflow.mjs';

test('requires an explicit local URL and rejects malformed arguments', () => {
  for (const args of [[], ['--url', 'file:///tmp/a.html'], ['--url', 'https://example.com'],
    ['--url', 'http://user:pass@localhost/'], ['--url', 'http://localhost', '--width', '412px'],
    ['--url', 'http://localhost', '--width', '0'], ['--url', 'http://localhost', '--timeout', '0'],
    ['--url', 'http://localhost', '--ready-selector', ''], ['--typo']]) {
    assert.throws(() => parseOptions(args));
  }
  for (const host of ['localhost', '127.0.0.1', '[::1]']) {
    assert.equal(parseOptions(['--url', `http://${host}:8000/`]).width, 412);
  }
});
