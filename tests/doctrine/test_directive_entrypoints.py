"""Directive entrypoint integrity and lazy-fetch policy tests."""

from __future__ import annotations

from pathlib import Path
import re

from ruamel.yaml import YAML


REPO_ROOT = Path(__file__).resolve().parents[2]
DOCTRINE_ROOT = REPO_ROOT / "src" / "doctrine"
DIRECTIVES_DIR = DOCTRINE_ROOT / "directives"
TACTICS_DIR = DOCTRINE_ROOT / "tactics"
PARADIGMS_DIR = DOCTRINE_ROOT / "paradigms"
STYLEGUIDES_DIR = DOCTRINE_ROOT / "styleguides"
TOOLGUIDES_DIR = DOCTRINE_ROOT / "toolguides"
DIRECTIVE_FILENAME_PATTERN = re.compile(r"^(?P<code>\d{3})-[a-z0-9-]+\.directive\.yaml$")


def _load_yaml(path: Path) -> dict:
    yaml = YAML(typ="safe")
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.load(handle) or {}
    assert isinstance(payload, dict), f"Expected mapping in {path}"
    return payload


def _collect_ids(directory: Path, key: str, pattern: str) -> set[str]:
    values: set[str] = set()
    for artifact_file in directory.rglob(pattern):
        payload = _load_yaml(artifact_file)
        value = str(payload.get(key, "")).strip()
        if value:
            values.add(value)
    return values


def _load_numbered_directive_files() -> list[tuple[int, Path]]:
    numbered: list[tuple[int, Path]] = []
    for directive_file in sorted(DIRECTIVES_DIR.glob("*.directive.yaml")):
        match = DIRECTIVE_FILENAME_PATTERN.fullmatch(directive_file.name)
        if match is None:
            continue
        numbered.append((int(match.group("code")), directive_file))
    return numbered


def test_directive_filenames_follow_numbered_convention() -> None:
    """All directives must use NNN-kebab-name.directive.yaml naming."""
    invalid_names = [
        directive_file.name
        for directive_file in sorted(DIRECTIVES_DIR.glob("*.directive.yaml"))
        if DIRECTIVE_FILENAME_PATTERN.fullmatch(directive_file.name) is None
    ]
    assert invalid_names == [], (
        "Directive files must follow NNN-kebab-name.directive.yaml naming:\n"
        + "\n".join(f"  - {name}" for name in invalid_names)
    )


def test_directive_codes_are_unique_and_contiguous() -> None:
    """Directive numeric IDs must be unique and contiguous from 001."""
    numbered = _load_numbered_directive_files()
    codes = [code for code, _ in numbered]
    assert codes, "No numbered directives found in src/doctrine/directives"
    assert len(codes) == len(set(codes)), f"Duplicate directive codes found: {codes}"

    expected = list(range(1, len(codes) + 1))
    assert codes == expected, (
        "Directive codes must be contiguous and ordered from 001:\n"
        f"  expected={expected}\n  actual={codes}"
    )


def test_directive_ids_are_unique() -> None:
    """Directive id values must be globally unique across directive files."""
    seen: dict[str, str] = {}
    duplicates: list[str] = []

    for _, directive_file in _load_numbered_directive_files():
        directive_id = str(_load_yaml(directive_file).get("id", "")).strip()
        if not directive_id:
            continue
        if directive_id in seen:
            duplicates.append(
                f"{directive_id} ({seen[directive_id]} and {directive_file.name})"
            )
        else:
            seen[directive_id] = directive_file.name

    assert duplicates == [], "Duplicate directive ids found:\n" + "\n".join(
        f"  - {entry}" for entry in duplicates
    )


def test_directive_entrypoint_refs_resolve_to_local_artifacts() -> None:
    """Each directive entrypoint reference must map to an existing local artifact id."""
    tactic_ids = _collect_ids(TACTICS_DIR, "id", "*.tactic.yaml")
    paradigm_ids = _collect_ids(PARADIGMS_DIR, "id", "*.paradigm.yaml")
    styleguide_ids = _collect_ids(STYLEGUIDES_DIR, "id", "*.styleguide.yaml")
    toolguide_ids = _collect_ids(TOOLGUIDES_DIR, "id", "*.toolguide.yaml")

    unresolved: list[str] = []

    for directive_file in sorted(DIRECTIVES_DIR.glob("*.directive.yaml")):
        directive = _load_yaml(directive_file)
        tactic_refs = directive.get("tactic_refs", [])
        paradigm_refs = directive.get("paradigm_refs", [])
        styleguide_refs = directive.get("styleguide_refs", [])
        toolguide_refs = directive.get("toolguide_refs", [])

        # Minimum entrypoint quality gate: at least one reference source per directive.
        assert any([tactic_refs, paradigm_refs, styleguide_refs, toolguide_refs]), (
            f"{directive_file.name} has no entrypoint references"
        )

        for tactic_ref in tactic_refs:
            if tactic_ref not in tactic_ids:
                unresolved.append(f"{directive_file.name}: tactic_refs -> {tactic_ref}")
        for paradigm_ref in paradigm_refs:
            if paradigm_ref not in paradigm_ids:
                unresolved.append(f"{directive_file.name}: paradigm_refs -> {paradigm_ref}")
        for styleguide_ref in styleguide_refs:
            if styleguide_ref not in styleguide_ids:
                unresolved.append(f"{directive_file.name}: styleguide_refs -> {styleguide_ref}")
        for toolguide_ref in toolguide_refs:
            if toolguide_ref not in toolguide_ids:
                unresolved.append(f"{directive_file.name}: toolguide_refs -> {toolguide_ref}")

    assert unresolved == [], "Unresolved directive entrypoints:\n" + "\n".join(
        f"  - {item}" for item in unresolved
    )


def test_directives_use_lazy_fetch_policy() -> None:
    """Directive fetch policy enforces lazy-fetch token discipline defaults."""
    for directive_file in sorted(DIRECTIVES_DIR.glob("*.directive.yaml")):
        directive = _load_yaml(directive_file)
        fetch_policy = directive["fetch_policy"]
        assert fetch_policy["strategy"] == "lazy_fetch", (
            f"{directive_file.name} must use lazy_fetch strategy"
        )
        assert fetch_policy["token_discipline"] == "on_demand", (
            f"{directive_file.name} must use on_demand token discipline"
        )
        assert fetch_policy["fetch_order"][0] == "paradigms", (
            f"{directive_file.name} must start fetch_order with paradigms"
        )
