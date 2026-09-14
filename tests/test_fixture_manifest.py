import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIXTURES = (
    "long-paragraphs",
    "mixed-script-headings",
    "long-url-overflow",
    "forms-ime-errors",
    "dense-tables",
    "mobile-wrap-stress",
    "docs-prose-code",
)


class FixtureManifestTests(unittest.TestCase):
    def test_required_fixtures_have_renderable_pages_and_finished_criteria(self):
        for name in REQUIRED_FIXTURES:
            with self.subTest(fixture=name):
                fixture_dir = ROOT / "fixtures" / name
                readme = fixture_dir / "README.md"
                page = fixture_dir / "index.html"

                self.assertTrue(readme.is_file(), f"missing {readme}")
                self.assertTrue(page.is_file(), f"missing {page}")

                criteria = readme.read_text(encoding="utf-8")
                self.assertNotIn("TBD", criteria, f"unfinished criteria in {readme}")
                self.assertIn("## PASS criteria", criteria)
                self.assertIn("## WARN criteria", criteria)
                self.assertIn("## FAIL criteria", criteria)

                html = page.read_text(encoding="utf-8")
                self.assertIn('lang="ja"', html)
                self.assertIn(f'data-fixture="{name}"', html)


if __name__ == "__main__":
    unittest.main()
