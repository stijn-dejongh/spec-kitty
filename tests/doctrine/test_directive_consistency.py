"""Consistency checks between shipped profile directive references and directives."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonschema
from ruamel.yaml import YAML


REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILES_DIR = REPO_ROOT / "src" / "doctrine" / "agent_profiles" / "shipped"
DIRECTIVES_DIR = REPO_ROOT / "src" / "doctrine" / "directives" / "shipped"
DIRECTIVE_SCHEMA = REPO_ROOT / "src" / "doctrine" / "schemas" / "directive.schema.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    yaml = YAML(typ="safe")
    with path.open("r", encoding="utf-8") as fh:
        return yaml.load(fh) or {}


def _profile_directive_refs() -> dict[str, str]:
    refs: dict[str, str] = {}
    yaml = YAML(typ="safe")

    for profile_path in sorted(PROFILES_DIR.glob("*.agent.yaml")):
        with profile_path.open("r", encoding="utf-8") as fh:
            profile = yaml.load(fh) or {}

        for ref in profile.get("directive-references", []):
            code = str(ref.get("code", "")).strip()
            title = str(ref.get("name", "")).strip()
            if not code:
                continue
            refs[code] = title

    return refs


def test_all_referenced_directives_have_matching_files_and_titles() -> None:
    refs = _profile_directive_refs()
    assert refs, "No directive references found in shipped profiles"

    for code, expected_title in refs.items():
        matches = list(DIRECTIVES_DIR.glob(f"{code}-*.directive.yaml"))
        assert matches, f"Missing directive file for code {code}"

        directive = _load_yaml(matches[0])
        actual_title = str(directive.get("title", "")).strip()
        assert actual_title == expected_title, (
            f"Directive title mismatch for code {code}: "
            f"expected '{expected_title}', got '{actual_title}'"
        )


def test_directive_files_validate_against_schema() -> None:
    schema = _load_yaml(DIRECTIVE_SCHEMA)
    validator = jsonschema.Draft202012Validator(schema)

    directive_files = sorted(DIRECTIVES_DIR.glob("*.directive.yaml"))
    assert directive_files, "No directive files found"

    for path in directive_files:
        data = _load_yaml(path)
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        assert not errors, f"Schema validation failed for {path.name}: {[e.message for e in errors]}"
