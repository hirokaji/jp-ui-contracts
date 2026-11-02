import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile

from scripts.publish_release import ARTIFACT, REPO, WORKFLOW, digest, inspect_evidence, validate_run, validate_tag, gh_api

SHA = 'a' * 40


def provenance():
    run = {'id': 1, 'repository': {'full_name': REPO}, 'head_repository': {'full_name': REPO}, 'head_sha': SHA,
           'head_branch': 'main', 'event': 'push', 'path': WORKFLOW, 'status': 'completed', 'conclusion': 'success'}
    jobs = [{'name': name, 'status': 'completed', 'conclusion': 'success', 'head_sha': SHA}
            for name in ['validate-contracts', 'rendered-validation']]
    artifact = {'name': ARTIFACT, 'expired': False, 'size_in_bytes': 100, 'digest': 'sha256:' + 'a' * 64,
                'workflow_run': {'id': 1, 'head_sha': SHA}}
    return run, jobs, artifact


def evidence(entries=None, measurements=None):
    measurements = measurements if measurements is not None else {key: {'status': status, 'metrics': {'clientWidth': 412, 'scrollWidth': width}, 'browser': {'name': 'chromium'},
                         'viewport': {'width': 412, 'height': 839},
                         'checks': [{'id': 'document-horizontal-overflow', 'status': status,
                                     'excessPx': width - 412, 'tolerancePx': 1}]}
                    for key, status, width in [('before', 'FAIL', 549), ('after', 'PASS', 412)]}
    items = {'playwright-report/index.html': '<html>report</html>', 'test-results/screenshot.png': b'fixture-placeholder',
             'test-results/example/walkthrough/measurements.json': json.dumps(measurements)}
    if entries is not None:
        items = entries
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w') as archive:
        for name, content in items.items():
            archive.writestr(name, content)
    return output.getvalue()


class PublicationGateTests(unittest.TestCase):
    def test_accepts_exact_successful_main_provenance(self):
        validate_run(*provenance(), SHA)

    def test_rejects_wrong_run_context(self):
        for key, value in [('head_sha', 'b' * 40), ('head_branch', 'topic'), ('event', 'pull_request'),
                           ('event', 'schedule'), ('path', 'other.yml'), ('status', 'in_progress'), ('conclusion', 'failure'),
                           ('repository', {'full_name': 'someone/fork'}), ('head_repository', {'full_name': 'someone/fork'})]:
            with self.subTest(key=key, value=value):
                run, jobs, artifact = provenance()
                run[key] = value
                with self.assertRaises(ValueError):
                    validate_run(run, jobs, artifact, SHA)

    def test_rejects_missing_skipped_duplicate_and_wrong_sha_jobs(self):
        run, jobs, artifact = provenance()
        variants = [jobs[:1], jobs + jobs[:1], [jobs[0], jobs[0]],
                    [jobs[0], dict(jobs[1], conclusion='skipped')], [jobs[0], dict(jobs[1], head_sha='b' * 40)]]
        for variant in variants:
            with self.subTest(variant=variant), self.assertRaises(ValueError):
                validate_run(run, variant, artifact, SHA)

    def test_rejects_invalid_artifact_provenance(self):
        for key, value in [('name', 'other'), ('expired', True), ('size_in_bytes', 0), ('size_in_bytes', 101 * 1024 * 1024),
                           ('digest', None), ('digest', 'abc'), ('workflow_run', {'id': 2, 'head_sha': SHA}),
                           ('workflow_run', {'id': 1, 'head_sha': 'b' * 40})]:
            run, jobs, artifact = provenance()
            artifact[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_run(run, jobs, artifact, SHA)

    def test_rejects_malformed_sha(self):
        for sha in ['main', 'a' * 7, 'a' * 40 + '\n']:
            with self.subTest(sha=sha), self.assertRaises(ValueError):
                validate_run(*provenance(), sha)

    def test_tag_is_never_moved(self):
        validate_tag(None, SHA)
        validate_tag({'object': {'type': 'commit', 'sha': SHA}}, SHA)
        for value in [{'object': {'type': 'commit', 'sha': 'b' * 40}}, {'object': {'type': 'tag', 'sha': SHA}}]:
            with self.assertRaises(ValueError):
                validate_tag(value, SHA)

    def test_accepts_measured_evidence_and_rejects_bad_digest(self):
        data = evidence()
        self.assertEqual(inspect_evidence(data, digest(data))['after']['scrollWidth'], 412)
        with self.assertRaises(ValueError):
            inspect_evidence(data, 'sha256:' + '0' * 64)

    def walkthrough(self):
        with zipfile.ZipFile(io.BytesIO(evidence())) as archive:
            return json.loads(archive.read('test-results/example/walkthrough/measurements.json'))

    def test_accepts_variable_before_width_and_preserves_observations(self):
        for width in [414, 548, 549, 550, 600]:
            for after_width in [412, 413]:
                with self.subTest(before=width, after=after_width):
                    m = self.walkthrough()
                    for state, measured in [('before', width), ('after', after_width)]:
                        m[state]['metrics']['scrollWidth'] = measured
                        m[state]['checks'][0]['excessPx'] = measured - 412
                    data = evidence(measurements=m)
                    observed = inspect_evidence(data, digest(data))
                    self.assertEqual(observed['before'], m['before']['metrics'])
                    self.assertEqual(observed['after'], m['after']['metrics'])

    def test_rejects_wrong_overflow_behavior(self):
        for state, width in [('before', 412), ('before', 413), ('after', 414), ('after', 549)]:
            with self.subTest(state=state, width=width):
                m = self.walkthrough()
                m[state]['metrics']['scrollWidth'] = width
                m[state]['checks'][0]['excessPx'] = width - 412
                data = evidence(measurements=m)
                with self.assertRaises(ValueError):
                    inspect_evidence(data, digest(data))

    def test_rejects_inconsistent_walkthrough_evidence(self):
        variants = [('viewport', 'width', 1440), ('metrics', 'clientWidth', 411),
                    ('browser', 'name', 'firefox'), ('check', 'status', 'ERROR'),
                    ('check', 'excessPx', 999), ('check', 'tolerancePx', 2),
                    ('check', 'id', 'other'), ('viewport', 'width', 412.0),
                    ('check', 'tolerancePx', True), ('check', 'tolerancePx', 1.0),
                    ('check', 'excessPx', False), ('check', 'excessPx', 0.0),
                    ('check', 'excessPx', 137.0)]
        for state in ['before', 'after']:
            for section, key, value in variants:
                with self.subTest(state=state, section=section, key=key):
                    m = self.walkthrough()
                    target = m[state]['checks'][0] if section == 'check' else m[state][section]
                    target[key] = value
                    data = evidence(measurements=m)
                    with self.assertRaises(ValueError):
                        inspect_evidence(data, digest(data))
            original_checks = self.walkthrough()[state]['checks']
            for checks in [[], original_checks * 2]:
                m = self.walkthrough()
                m[state]['checks'] = checks
                data = evidence(measurements=m)
                with self.assertRaises(ValueError):
                    inspect_evidence(data, digest(data))

    def test_rejects_non_integer_or_nonpositive_widths(self):
        for state in ['before', 'after']:
            for key in ['clientWidth', 'scrollWidth']:
                for value in [True, False, None, '549', 549.0, -1, 0, float('nan'), float('inf')]:
                    with self.subTest(state=state, key=key, value=value):
                        m = self.walkthrough()
                        m[state]['metrics'][key] = value
                        data = evidence(measurements=m)
                        with self.assertRaises(ValueError):
                            inspect_evidence(data, digest(data))

    def test_rejects_missing_and_unsafe_archive_content(self):
        for entries in [{}, {'../outside': 'bad'}, {'/absolute': 'bad'}, {'x\\y': 'bad'}, {'playwright-report/index.html': 'only report'}]:
            data = evidence(entries)
            with self.subTest(entries=entries), self.assertRaises(ValueError):
                inspect_evidence(data, digest(data))

    def test_rejects_wrong_walkthrough_result(self):
        data = evidence()
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = {n: archive.read(n) for n in archive.namelist()}
        name = 'test-results/example/walkthrough/measurements.json'
        m = json.loads(entries[name]);m['before']['status'] = 'PASS';entries[name] = json.dumps(m)
        data = evidence(entries)
        with self.assertRaises(ValueError):
            inspect_evidence(data, digest(data))

    def test_api_absence_is_only_404_not_authorization_or_network_failure(self):
        class Result:
            returncode = 1
            stdout = b''
            stderr = b'gh: Not Found (HTTP 404)'
        with patch('scripts.publish_release.subprocess.run', return_value=Result()):
            self.assertIsNone(gh_api('repos/example/repo', optional=True))
        for error in [b'gh: Forbidden (HTTP 403)', b'gh: Bad credentials (HTTP 401)', b'network timed out']:
            result = Result();result.stderr = error
            with patch('scripts.publish_release.subprocess.run', return_value=result), self.assertRaises(RuntimeError):
                gh_api('repos/example/repo', optional=True)

    def test_publication_is_manual_and_old_sync_has_no_write_permission(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / '.github/workflows/publish-release.yml').read_text()
        self.assertIn('workflow_dispatch:', workflow)
        self.assertNotIn('workflow_run:', workflow)
        self.assertNotIn('\n  push:', workflow)
        self.assertIn('default: false', workflow)
        self.assertIn("github.ref == 'refs/heads/main'", workflow)
        retired = (root / '.github/workflows/post-release-v0.2.0.yml').read_text()
        self.assertNotIn('contents: write', retired)
        self.assertNotIn('git push', retired)


if __name__ == '__main__':
    unittest.main()
