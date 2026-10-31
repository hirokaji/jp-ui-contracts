import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "0.2.0"
EXPECTED_FIXTURES = {
    "long-paragraphs",
    "mixed-script-headings",
    "long-url-overflow",
    "forms-ime-errors",
    "dense-tables",
    "mobile-wrap-stress",
    "docs-prose-code",
}


class ReleaseMetadataTests(unittest.TestCase):
    def setUp(self):
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.manifest = json.loads((ROOT / "RELEASE_MANIFEST.json").read_text(encoding="utf-8"))

    def test_version_is_consistent(self):
        self.assertEqual(self.version, EXPECTED_VERSION)
        self.assertEqual(self.package["version"], EXPECTED_VERSION)
        self.assertEqual(self.manifest["version"], EXPECTED_VERSION)

    def test_manifest_names_previous_release_and_rollback(self):
        self.assertEqual(self.manifest["previous_release"], "v0.1.0")
        self.assertEqual(self.manifest["rollback"]["target"], "v0.1.0")

    def test_manifest_fixture_set_matches_release_gate(self):
        configured = set()
        for names in self.manifest["required_fixtures"].values():
            configured.update(names)
        self.assertEqual(configured, EXPECTED_FIXTURES)
        for name in configured:
            self.assertTrue((ROOT / "fixtures" / name / "index.html").is_file())
            self.assertTrue((ROOT / "fixtures" / name / "README.md").is_file())

    def test_release_notes_and_gate_exist(self):
        self.assertTrue((ROOT / "docs" / "releases" / "v0.2.0.md").is_file())
        self.assertTrue((ROOT / "docs" / "v0.2-release-gate.md").is_file())

    def test_manifest_requires_final_post_rc_gate(self):
        rule = self.manifest["release_gate"]["release_candidate_rule"]
        self.assertIn("final main commit", rule)
        self.assertIn("passes the same required gates", rule)


if __name__ == "__main__":
    unittest.main()
