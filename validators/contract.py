#!/usr/bin/env python3
"""Zero-dependency parser, validator, and JSON exporter for jp-ui-contracts DESIGN.md.

DESIGN.md remains the human-edited source. This tool projects the structured
parts needed by CI and agents instead of requiring a second hand-maintained
contract file.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

SCHEMA_VERSION = "0.2.0"
ALLOWED_PROFILES = {"base", "media", "saas", "docs", "dashboard"}
ALLOWED_REVIEW_STATUS = {"draft", "verified", "production"}

META_RE = re.compile(r"^- \*\*(?P<key>[^*]+)\*\*:\s*(?P<value>.*)$")
HEADING_RE = re.compile(r"^##\s+(?:\d+\.\s*)?(?P<title>.+?)\s*$")
FENCED_CSS_RE = re.compile(r"```css\s*\n(?P<body>.*?)```", re.DOTALL | re.IGNORECASE)


def _clean(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        value = value[1:-1]
    return value.strip()


def _camel(label: str) -> str:
    words = re.split(r"[\s_-]+", label.strip().lower())
    return words[0] + "".join(word.capitalize() for word in words[1:])


def parse_contract(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    metadata: dict[str, str] = {}
    validation_targets: list[str] = []
    in_metadata = False
    in_validation = False

    for raw in text.splitlines():
        line = raw.rstrip()
        heading = HEADING_RE.match(line)
        if heading:
            title = heading.group("title").strip().lower()
            in_metadata = title == "contract metadata"
            in_validation = title == "validation targets"
            continue

        if in_metadata:
            match = META_RE.match(line)
            if match:
                metadata[_camel(match.group("key"))] = _clean(match.group("value"))
            elif line.startswith("---"):
                in_metadata = False

        if in_validation and line.startswith("- "):
            validation_targets.append(line[2:].strip())
        elif in_validation and line.startswith("---"):
            in_validation = False

    contract = {
        "$schema": "schema/design-contract.schema.json",
        "schemaVersion": SCHEMA_VERSION,
        "source": path.as_posix(),
        "locale": metadata.get("locale", ""),
        "profile": metadata.get("profile", ""),
        "reviewStatus": metadata.get("reviewStatus", ""),
        "validationTargets": validation_targets,
    }

    optional_map = {
        "primaryWritingMode": "writingMode",
        "targetSurfaces": "targetSurfaces",
        "lastReviewedAt": "lastReviewedAt",
        "reviewer": "reviewer",
    }
    for source_key, output_key in optional_map.items():
        value = metadata.get(source_key)
        if value:
            contract[output_key] = value

    return contract


def validate_contract(path: Path, strict: bool = False) -> tuple[list[str], list[str], dict]:
    text = path.read_text(encoding="utf-8")
    contract = parse_contract(path)
    errors: list[str] = []
    warnings: list[str] = []

    if not contract["locale"]:
        errors.append("Contract Metadata must define Locale")
    elif contract["locale"] != "ja-JP":
        warnings.append(f"Locale is {contract['locale']!r}; this kit is optimized for ja-JP")

    if contract["profile"] not in ALLOWED_PROFILES:
        errors.append(
            "Profile must be one of: " + ", ".join(sorted(ALLOWED_PROFILES))
        )

    if contract["reviewStatus"] not in ALLOWED_REVIEW_STATUS:
        errors.append(
            "Review status must be one of: " + ", ".join(sorted(ALLOWED_REVIEW_STATUS))
        )

    targets = contract["validationTargets"]
    if not targets:
        errors.append("A Validation Targets section with at least one bullet is required")
    elif strict and len(targets) < 3:
        errors.append("Strict mode requires at least three validation targets")

    css_blocks = "\n".join(match.group("body") for match in FENCED_CSS_RE.finditer(text))
    if re.search(r"word-break\s*:\s*break-all\s*;", css_blocks, re.IGNORECASE):
        errors.append("CSS examples must not set word-break: break-all")

    if "[Project Name]" in text:
        warnings.append("Template placeholder [Project Name] is still present")

    return errors, warnings, contract


def cmd_validate(paths: Iterable[str], strict: bool) -> int:
    failed = False
    for raw in paths:
        path = Path(raw)
        try:
            errors, warnings, contract = validate_contract(path, strict=strict)
        except (OSError, UnicodeError) as exc:
            print(f"FAIL {path}: {exc}", file=sys.stderr)
            failed = True
            continue

        state = "FAIL" if errors else ("WARN" if warnings else "PASS")
        print(f"{state} {path} [{contract['profile'] or 'unknown'}]")
        for item in errors:
            print(f"  ERROR: {item}")
        for item in warnings:
            print(f"  WARN: {item}")
        failed = failed or bool(errors)
    return 1 if failed else 0


def cmd_export(path: str, output: str | None) -> int:
    source = Path(path)
    errors, warnings, contract = validate_contract(source, strict=False)
    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        return 1
    if warnings:
        contract["warnings"] = warnings
    payload = json.dumps(contract, ensure_ascii=False, indent=2) + "\n"
    if output:
        Path(output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate or export jp-ui-contracts DESIGN.md")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate one or more DESIGN.md files")
    validate.add_argument("paths", nargs="+")
    validate.add_argument("--strict", action="store_true")

    export = sub.add_parser("export", help="project one DESIGN.md to machine-readable JSON")
    export.add_argument("path")
    export.add_argument("-o", "--output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "validate":
        return cmd_validate(args.paths, strict=args.strict)
    if args.command == "export":
        return cmd_export(args.path, args.output)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
