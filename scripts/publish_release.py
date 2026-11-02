"""Publish v0.3.0 only from a verified main commit; never move an existing tag.

Runs in GitHub Actions with gh and GH_TOKEN. Default mode only verifies/downloads.
No credentials or production service access are needed by the unit tests.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import zipfile

VERSION = '0.3.0'
TAG = 'v' + VERSION
REPO = 'hirokaji/jp-ui-contracts'
WORKFLOW = '.github/workflows/contract-validation.yml'
JOBS = {'validate-contracts', 'rendered-validation'}
ARTIFACT = 'rendered-validation-evidence'
MAX_ZIP = 100 * 1024 * 1024
MAX_EXPANDED = 250 * 1024 * 1024


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def validate_run(run, jobs, artifact, sha, repo=REPO):
    require(re.fullmatch(r'[0-9a-f]{40}', sha), 'Full commit SHA required')
    require(run.get('repository', {}).get('full_name') == repo, 'Wrong run repository')
    require(run.get('head_repository', {}).get('full_name') == repo, 'Fork run rejected')
    require(run.get('head_sha') == sha and run.get('head_branch') == 'main', 'Run must match candidate on main')
    require(run.get('event') in {'push', 'workflow_dispatch'}, 'PR/scheduled run is not a release gate')
    require(run.get('path') == WORKFLOW, 'Wrong validation workflow')
    require(run.get('status') == 'completed' and run.get('conclusion') == 'success', 'Validation is not successful')
    require(len(jobs) == len(JOBS) and {j.get('name') for j in jobs} == JOBS, 'Required jobs missing or duplicated')
    require(all(j.get('conclusion') == 'success' and j.get('status') == 'completed' and j.get('head_sha') == sha for j in jobs), 'A required job did not pass on candidate')
    require(artifact.get('name') == ARTIFACT and artifact.get('expired') is False, 'Evidence missing or expired')
    require(0 < artifact.get('size_in_bytes', 0) <= MAX_ZIP, 'Invalid Evidence size')
    require(isinstance(artifact.get('digest'), str) and re.fullmatch(r'sha256:[0-9a-f]{64}', artifact['digest']), 'Evidence digest missing')
    arun = artifact.get('workflow_run', {})
    require(arun.get('id') == run.get('id') and arun.get('head_sha') == sha, 'Evidence belongs to another run/commit')


def inspect_evidence(data, expected_digest):
    require(0 < len(data) <= MAX_ZIP and digest(data) == expected_digest, 'Evidence checksum mismatch')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        require(len(infos) <= 10000 and sum(i.file_size for i in infos) <= MAX_EXPANDED, 'Evidence expansion exceeds limit')
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)), 'Duplicate archive paths')
        require(all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n for n in names), 'Unsafe archive path')
        require(archive.testzip() is None, 'Corrupt Evidence ZIP')
        require('playwright-report/index.html' in names, 'HTML report absent')
        require(any(n.startswith('test-results/') and n.endswith('.png') for n in names), 'Screenshots absent')
        paths = [n for n in names if n.endswith('/walkthrough/measurements.json')]
        require(len(paths) == 1, 'Walkthrough measurements absent/ambiguous')
        m = json.loads(archive.read(paths[0]))
        for state, expected in [('before', 'FAIL'), ('after', 'PASS')]:
            result = m[state]
            require(result['status'] == expected, 'Walkthrough outcome changed')
            metrics = result['metrics']
            require(all(type(metrics.get(key)) is int and metrics[key] > 0
                        for key in ('clientWidth', 'scrollWidth')), 'Invalid walkthrough widths')
            require(type(result['viewport']['width']) is int and result['viewport']['width'] == 412
                    and metrics['clientWidth'] == 412, 'Unexpected walkthrough viewport')
            # Match validators/overflow.mjs: font-dependent widths are observations,
            # not a pixel baseline; one pixel of excess is within tolerance.
            excess = metrics['scrollWidth'] - metrics['clientWidth']
            require((excess > 1) == (expected == 'FAIL'), 'Walkthrough overflow changed')
            checks = [c for c in result['checks'] if c.get('id') == 'document-horizontal-overflow']
            require(len(checks) == 1 and checks[0].get('status') == expected
                    and type(checks[0].get('excessPx')) is int and type(checks[0].get('tolerancePx')) is int
                    and checks[0].get('excessPx') == excess and checks[0].get('tolerancePx') == 1,
                    'Inconsistent walkthrough overflow check')
            require(result['browser']['name'] == 'chromium', 'Unexpected browser')
        return {'before': m['before']['metrics'], 'after': m['after']['metrics'], 'browser': m['after']['browser']}


def validate_tag(ref, sha):
    if ref is not None:
        require(ref.get('object', {}).get('type') == 'commit' and ref['object']['sha'] == sha, 'Existing tag differs; never overwrite it')


def gh_api(endpoint, data=None, binary=False, optional=False):
    args = ['gh', 'api', '--hostname', 'github.com', endpoint, '-H', 'X-GitHub-Api-Version: 2022-11-28']
    if data is not None:
        args += ['--method', 'POST', '--input', '-']
    result = subprocess.run(args, input=None if data is None else json.dumps(data).encode(), capture_output=True, check=False)
    if result.returncode:
        # Only a real HTTP 404 is absence; permissions/network errors must fail closed.
        if optional and b'(HTTP 404)' in result.stderr:
            return None
        raise RuntimeError(result.stderr.decode(errors='replace'))
    return result.stdout if binary else json.loads(result.stdout)


def patch_release(endpoint, body):
    result = subprocess.run(['gh', 'api', '--hostname', 'github.com', endpoint, '--method', 'PATCH', '--input', '-'], input=json.dumps(body).encode(), capture_output=True, check=True)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sha', required=True)
    parser.add_argument('--run-id', required=True, type=int)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    require(re.fullmatch(r'[0-9a-f]{40}', args.sha) and args.run_id > 0, 'Invalid SHA or run ID')
    require(os.environ.get('GITHUB_REPOSITORY') == REPO, 'Unexpected repository')
    require(os.environ.get('GITHUB_EVENT_NAME') == 'workflow_dispatch' and os.environ.get('GITHUB_REF') == 'refs/heads/main', 'Manual execution on main required')
    require(os.environ.get('GITHUB_SHA') == args.sha, 'Dispatch commit must equal candidate')
    require(subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == args.sha, 'Checkout differs from candidate')
    manifest = json.loads(Path('RELEASE_MANIFEST.json').read_text())
    require(Path('VERSION').read_text().strip() == VERSION == manifest['version'] == json.loads(Path('package.json').read_text())['version'], 'Version mismatch')
    require(manifest['publication']['status'] == 'candidate' and manifest['publication']['tag'] == TAG, 'Manifest must describe this candidate')
    base = f'repos/{REPO}'
    require(gh_api(base + '/branches/main')['commit']['sha'] == args.sha, 'main has moved; verify the new candidate')
    run = gh_api(f'{base}/actions/runs/{args.run_id}')
    jobs = gh_api(f'{base}/actions/runs/{args.run_id}/jobs?per_page=100')
    require(jobs['total_count'] == len(jobs['jobs']), 'Incomplete jobs response')
    artifacts = gh_api(f'{base}/actions/runs/{args.run_id}/artifacts?per_page=100')
    require(artifacts['total_count'] == len(artifacts['artifacts']), 'Incomplete artifacts response')
    matches = [a for a in artifacts['artifacts'] if a['name'] == ARTIFACT]
    require(len(matches) == 1, 'Expected exactly one Evidence artifact')
    artifact = matches[0]
    validate_run(run, jobs['jobs'], artifact, args.sha)
    data = gh_api(f"{base}/actions/artifacts/{artifact['id']}/zip", binary=True)
    observed = inspect_evidence(data, artifact['digest'])
    tag_ref = gh_api(f'{base}/git/ref/tags/{TAG}', optional=True)
    validate_tag(tag_ref, args.sha)
    release = gh_api(f'{base}/releases/tags/{TAG}', optional=True)
    if release is not None:
        require(release['draft'] is True and release['target_commitish'] == args.sha, 'Existing release is not this unpublished candidate; leave it unchanged')
    verification = {'version': VERSION, 'tag': TAG, 'commit': args.sha, 'repository': REPO,
                    'workflow_run': args.run_id, 'workflow_url': run['html_url'], 'run_attempt': run['run_attempt'],
                    'artifact_id': artifact['id'], 'artifact_digest': artifact['digest'], 'artifact_expires_at': artifact['expires_at'],
                    'jobs': {j['name']: j['conclusion'] for j in jobs['jobs']}, 'walkthrough': observed,
                    'note': 'Chromium structural gates; not full DESIGN.md conformance, native IME or other-browser certification.'}
    print(json.dumps(verification, indent=2, ensure_ascii=False))
    if not args.publish:
        print('Verification only: no tag, release or asset was written.')
        return
    # Recheck main/run immediately before the first write to limit stale-candidate publication.
    require(gh_api(base + '/branches/main')['commit']['sha'] == args.sha, 'main moved during verification')
    current = gh_api(f'{base}/actions/runs/{args.run_id}')
    require(current['status'] == 'completed' and current['conclusion'] == 'success' and current['run_attempt'] == run['run_attempt'], 'Validation run changed during verification')
    if tag_ref is None:
        gh_api(f'{base}/git/refs', {'ref': f'refs/tags/{TAG}', 'sha': args.sha})
    validate_tag(gh_api(f'{base}/git/ref/tags/{TAG}'), args.sha)
    notes = Path(f'docs/releases/{TAG}.md').read_text()
    # Repository-relative links in a source document need tag-bound URLs in a release body.
    notes = re.sub(r'\]\(\.\./([^)]*)\)', lambda m: f'](https://github.com/{REPO}/blob/{TAG}/docs/{m[1]})', notes)
    body = notes + '\n\n## Verified release commit\n\n' + f"Commit: `{args.sha}`\n\nCI: {run['html_url']}\n\nEvidence artifact: `{artifact['id']}`\n\nSHA-256: `{artifact['digest']}`\n\nThe original Evidence ZIP and release-verification.json are attached to this release.\n"
    if release is None:
        release = gh_api(f'{base}/releases', {'tag_name': TAG, 'target_commitish': args.sha, 'name': TAG + ' — local UI checks and onboarding', 'body': body, 'draft': True, 'prerelease': False})
    else:
        release = patch_release(f"{base}/releases/{release['id']}", {'body': body})
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        files = {f'{ARTIFACT}.zip': data, 'release-verification.json': (json.dumps(verification, ensure_ascii=False, indent=2) + '\n').encode()}
        for name, content in files.items():
            path = root / name
            path.write_bytes(content)
            assets = gh_api(f"{base}/releases/{release['id']}/assets?per_page=100")
            existing = [a for a in assets if a['name'] == name]
            if existing:
                require(len(existing) == 1 and existing[0].get('digest') == digest(content), 'Existing draft asset differs; stop without replacing it')
            else:
                subprocess.run(['gh', 'release', 'upload', TAG, str(path), '--repo', REPO], check=True)
        assets = gh_api(f"{base}/releases/{release['id']}/assets?per_page=100")
        for name, content in files.items():
            found = [a for a in assets if a['name'] == name and a['state'] == 'uploaded' and a['size'] == len(content) and a.get('digest') == digest(content)]
            require(len(found) == 1, 'Release asset verification failed; release remains draft')
    validate_tag(gh_api(f'{base}/git/ref/tags/{TAG}'), args.sha)
    require(gh_api(base + '/branches/main')['commit']['sha'] == args.sha, 'main moved before publication; release remains draft')
    published = patch_release(f"{base}/releases/{release['id']}", {'draft': False, 'prerelease': False, 'make_latest': 'true'})
    require(published['draft'] is False and published['tag_name'] == TAG, 'Publication response mismatch')
    print('Published: ' + published['html_url'])


if __name__ == '__main__':
    main()
