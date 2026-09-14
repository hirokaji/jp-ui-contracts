import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "validators" / "contract.py"
spec = importlib.util.spec_from_file_location("contract", MODULE_PATH)
contract = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(contract)


class ContractValidatorTests(unittest.TestCase):
    def write_design(self, text: str) -> Path:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        path = Path(tempdir.name) / "DESIGN.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_parses_metadata_and_targets(self):
        path = self.write_design(
            """# DESIGN.md — Demo

## 0. Contract Metadata
- **Locale**: `ja-JP`
- **Profile**: `media`
- **Review status**: `verified`
- **Primary writing mode**: `horizontal-tb`

---

## 4. Validation Targets
- Must pass long paragraph review
- Must pass mobile article review
- Must pass mixed-script title review
"""
        )
        parsed = contract.parse_contract(path)
        self.assertEqual(parsed["locale"], "ja-JP")
        self.assertEqual(parsed["profile"], "media")
        self.assertEqual(parsed["reviewStatus"], "verified")
        self.assertEqual(parsed["writingMode"], "horizontal-tb")
        self.assertEqual(len(parsed["validationTargets"]), 3)

    def test_valid_contract_passes_strict_mode(self):
        path = self.write_design(
            """# DESIGN.md — Demo

## 0. Contract Metadata
- **Locale**: `ja-JP`
- **Profile**: `saas`
- **Review status**: `draft`

---

## 4. Validation Targets
- Must pass form review
- Must pass table review
- Must pass mobile review
"""
        )
        errors, warnings, _ = contract.validate_contract(path, strict=True)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_rejects_global_break_all_in_css_example(self):
        path = self.write_design(
            """# DESIGN.md — Demo

## 0. Contract Metadata
- **Locale**: `ja-JP`
- **Profile**: `base`
- **Review status**: `draft`

---

```css
html:lang(ja) { word-break: break-all; }
```

## 4. Validation Targets
- One
- Two
- Three
"""
        )
        errors, _, _ = contract.validate_contract(path, strict=True)
        self.assertTrue(any("break-all" in item for item in errors))

    def test_strict_mode_requires_three_targets(self):
        path = self.write_design(
            """# DESIGN.md — Demo

## 0. Contract Metadata
- **Locale**: `ja-JP`
- **Profile**: `docs`
- **Review status**: `draft`

---

## 4. Validation Targets
- Must pass docs review
"""
        )
        errors, _, _ = contract.validate_contract(path, strict=True)
        self.assertTrue(any("three validation targets" in item for item in errors))

    def test_template_placeholder_is_warning_not_failure(self):
        path = self.write_design(
            """# DESIGN.md — [Project Name]

## 0. Contract Metadata
- **Locale**: `ja-JP`
- **Profile**: `dashboard`
- **Review status**: `draft`

---

## 4. Validation Targets
- One
- Two
- Three
"""
        )
        errors, warnings, _ = contract.validate_contract(path, strict=True)
        self.assertEqual(errors, [])
        self.assertTrue(any("Project Name" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
