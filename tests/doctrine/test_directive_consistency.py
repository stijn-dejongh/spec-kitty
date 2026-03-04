"""Consistency checks between shipped profile directive references and directives."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonschema
from ruamel.yaml import YAML


REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILES_DIR = REPO_ROOT / "src" / "doctrine" / "agent_profiles" / "shipped"
DIRECTIVES_DIR = REPO_ROOT / "src" / "doctrine" / "directives" / "shipped"
TACTICS_DIR = REPO_ROOT / "src" / "doctrine" / "tactics" / "shipped"
PARADIGMS_DIR = REPO_ROOT / "src" / "doctrine" / "paradigms" / "shipped"
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


def _shipped_tactic_ids() -> set[str]:
    tactic_ids: set[str] = set()
    for path in sorted(TACTICS_DIR.glob("*.tactic.yaml")):
        data = _load_yaml(path)
        tactic_id = str(data.get("id", "")).strip()
        if tactic_id:
            tactic_ids.add(tactic_id)
    return tactic_ids


def test_all_directive_tactic_refs_resolve_to_shipped_tactics() -> None:
    tactic_ids = _shipped_tactic_ids()
    assert tactic_ids, "No shipped tactics found"

    directive_files = sorted(DIRECTIVES_DIR.glob("*.directive.yaml"))
    assert directive_files, "No directive files found"

    unresolved: list[str] = []
    for path in directive_files:
        data = _load_yaml(path)
        refs = data.get("tactic_refs", []) or []
        if not isinstance(refs, list):
            unresolved.append(f"{path.name}: tactic_refs is not a list")
            continue

        for ref in refs:
            ref_str = str(ref).strip()
            if ref_str and ref_str not in tactic_ids:
                unresolved.append(f"{path.name}: unresolved tactic_ref '{ref_str}'")

    assert not unresolved, "Unresolved tactic references:\n" + "\n".join(unresolved)


# ---------------------------------------------------------------------------
# Tactic cross-reference graph: loop detection
# ---------------------------------------------------------------------------

def _build_tactic_ref_graph() -> dict[str, list[str]]:
    """Return adjacency list: tactic_id -> [referenced tactic_ids]."""
    graph: dict[str, list[str]] = {}
    for path in sorted(TACTICS_DIR.glob("*.tactic.yaml")):
        data = _load_yaml(path)
        tactic_id = str(data.get("id", "")).strip()
        if not tactic_id:
            continue
        neighbours: list[str] = []
        # Root-level references
        for ref in data.get("references", []) or []:
            if ref.get("type") == "tactic":
                neighbours.append(str(ref["id"]).strip())
        # Step-level references
        for step in data.get("steps", []) or []:
            for ref in step.get("references", []) or []:
                if ref.get("type") == "tactic":
                    neighbours.append(str(ref["id"]).strip())
        graph[tactic_id] = neighbours
    return graph


def _detect_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    """DFS cycle detection; returns list of cycles (each cycle as ordered node list)."""
    visited: set[str] = set()
    path: list[str] = []
    path_set: set[str] = set()
    cycles: list[list[str]] = []

    def dfs(node: str) -> None:
        if node in path_set:
            start = path.index(node)
            cycles.append(path[start:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        path_set.add(node)
        for neighbour in graph.get(node, []):
            dfs(neighbour)
        path.pop()
        path_set.discard(node)

    for node in graph:
        dfs(node)
    return cycles


def test_tactic_reference_graph_has_no_cycles() -> None:
    """Tactic cross-references must form a DAG; cycles would cause infinite resolution loops."""
    graph = _build_tactic_ref_graph()
    assert graph, "No tactics found to build reference graph"
    cycles = _detect_cycles(graph)
    assert not cycles, (
        "Cyclic tactic references detected (would cause infinite resolution loops):\n"
        + "\n".join(" -> ".join(cycle) for cycle in cycles)
    )


def test_tactic_references_resolve_to_known_tactics() -> None:
    """All tactic-type cross-references inside tactic files must point to a shipped tactic."""
    tactic_ids = _shipped_tactic_ids()
    unresolved: list[str] = []
    for path in sorted(TACTICS_DIR.glob("*.tactic.yaml")):
        data = _load_yaml(path)
        tactic_id = str(data.get("id", "")).strip()
        for ref in data.get("references", []) or []:
            if ref.get("type") == "tactic":
                ref_id = str(ref.get("id", "")).strip()
                if ref_id and ref_id not in tactic_ids:
                    unresolved.append(f"{tactic_id}: root reference '{ref_id}' not found")
        for step in data.get("steps", []) or []:
            for ref in step.get("references", []) or []:
                if ref.get("type") == "tactic":
                    ref_id = str(ref.get("id", "")).strip()
                    if ref_id and ref_id not in tactic_ids:
                        step_title = step.get("title", "?")
                        unresolved.append(
                            f"{tactic_id} step '{step_title}': reference '{ref_id}' not found"
                        )
    assert not unresolved, "Unresolved tactic-to-tactic references:\n" + "\n".join(unresolved)


# ---------------------------------------------------------------------------
# opposed_by resolution checks
# ---------------------------------------------------------------------------

def _shipped_directive_ids() -> set[str]:
    ids: set[str] = set()
    for path in sorted(DIRECTIVES_DIR.glob("*.directive.yaml")):
        data = _load_yaml(path)
        d_id = str(data.get("id", "")).strip()
        if d_id:
            ids.add(d_id)
    return ids


def _shipped_paradigm_ids() -> set[str]:
    ids: set[str] = set()
    for path in sorted(PARADIGMS_DIR.glob("*.paradigm.yaml")):
        data = _load_yaml(path)
        p_id = str(data.get("id", "")).strip()
        if p_id:
            ids.add(p_id)
    return ids


def test_directive_opposed_by_refs_resolve() -> None:
    """All opposed_by entries in directives must point to known artifacts."""
    directive_ids = _shipped_directive_ids()
    tactic_ids = _shipped_tactic_ids()
    paradigm_ids = _shipped_paradigm_ids()
    id_map = {"directive": directive_ids, "tactic": tactic_ids, "paradigm": paradigm_ids}

    unresolved: list[str] = []
    for path in sorted(DIRECTIVES_DIR.glob("*.directive.yaml")):
        data = _load_yaml(path)
        source_id = str(data.get("id", "")).strip()
        for entry in data.get("opposed_by", []) or []:
            ref_type = str(entry.get("type", "")).strip()
            ref_id = str(entry.get("id", "")).strip()
            if ref_type not in id_map:
                unresolved.append(f"{source_id}: unknown opposed_by type '{ref_type}'")
                continue
            if ref_id and ref_id not in id_map[ref_type]:
                unresolved.append(
                    f"{source_id}: opposed_by {ref_type} '{ref_id}' not found"
                )
    assert not unresolved, "Unresolved directive opposed_by references:\n" + "\n".join(unresolved)


def test_tactic_opposed_by_refs_resolve() -> None:
    """All opposed_by entries in tactics must point to known artifacts."""
    directive_ids = _shipped_directive_ids()
    tactic_ids = _shipped_tactic_ids()
    paradigm_ids = _shipped_paradigm_ids()
    id_map = {"directive": directive_ids, "tactic": tactic_ids, "paradigm": paradigm_ids}

    unresolved: list[str] = []
    for path in sorted(TACTICS_DIR.glob("*.tactic.yaml")):
        data = _load_yaml(path)
        source_id = str(data.get("id", "")).strip()
        for entry in data.get("opposed_by", []) or []:
            ref_type = str(entry.get("type", "")).strip()
            ref_id = str(entry.get("id", "")).strip()
            if ref_type not in id_map:
                unresolved.append(f"{source_id}: unknown opposed_by type '{ref_type}'")
                continue
            if ref_id and ref_id not in id_map[ref_type]:
                unresolved.append(
                    f"{source_id}: opposed_by {ref_type} '{ref_id}' not found"
                )
    assert not unresolved, "Unresolved tactic opposed_by references:\n" + "\n".join(unresolved)


def test_paradigm_tactic_refs_resolve_to_shipped_tactics() -> None:
    """All tactic_refs on paradigms must resolve to shipped tactics."""
    tactic_ids = _shipped_tactic_ids()
    unresolved: list[str] = []
    for path in sorted(PARADIGMS_DIR.glob("*.paradigm.yaml")):
        data = _load_yaml(path)
        paradigm_id = str(data.get("id", "")).strip()
        for ref in data.get("tactic_refs", []) or []:
            ref_str = str(ref).strip()
            if ref_str and ref_str not in tactic_ids:
                unresolved.append(f"{paradigm_id}: unresolved tactic_ref '{ref_str}'")
    assert not unresolved, "Unresolved paradigm tactic_refs:\n" + "\n".join(unresolved)
