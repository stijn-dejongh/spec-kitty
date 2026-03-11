"""Tests for constitution context bootstrap rendering."""

from pathlib import Path

from specify_cli.constitution.context import build_constitution_context


def _write_constitution_bundle(root: Path) -> None:
    constitution_dir = root / ".kittify" / "constitution"
    constitution_dir.mkdir(parents=True)
    (constitution_dir / "constitution.md").write_text(
        """# Project Constitution

## Policy Summary

- Intent: deterministic delivery
- Testing: pytest + coverage

## Project Directives

1. Keep tests strict
""",
        encoding="utf-8",
    )
    (constitution_dir / "references.yaml").write_text(
        """schema_version: "1.0.0"
references:
  - id: "USER:PROJECT_PROFILE"
    kind: user_profile
    title: User Project Profile
    local_path: library/user-project-profile.md
""",
        encoding="utf-8",
    )


def test_context_bootstrap_then_compact(tmp_path: Path) -> None:
    _write_constitution_bundle(tmp_path)

    first = build_constitution_context(tmp_path, action="specify", mark_loaded=True)
    second = build_constitution_context(tmp_path, action="specify", mark_loaded=True)

    assert first.mode == "bootstrap"
    assert first.first_load is True
    assert "Policy Summary" in first.text
    assert first.references_count == 1

    assert second.mode == "compact"
    assert second.first_load is False
    assert "Governance:" in second.text or "Governance: unresolved" in second.text


def test_context_missing_constitution_reports_missing(tmp_path: Path) -> None:
    result = build_constitution_context(tmp_path, action="plan", mark_loaded=True)

    assert result.mode == "missing"
    assert "Constitution file not found" in result.text


def test_non_bootstrap_action_uses_compact_context(tmp_path: Path) -> None:
    _write_constitution_bundle(tmp_path)

    result = build_constitution_context(tmp_path, action="tasks", mark_loaded=True)

    assert result.mode == "compact"
    assert result.first_load is False


def test_context_depth_defaults_to_2_on_first_load(tmp_path: Path) -> None:
    _write_constitution_bundle(tmp_path)

    result = build_constitution_context(tmp_path, action="implement", mark_loaded=False)

    assert result.first_load is True
    assert result.depth == 2


def test_context_depth_defaults_to_1_on_later_load(tmp_path: Path) -> None:
    _write_constitution_bundle(tmp_path)

    # First load marks the state
    build_constitution_context(tmp_path, action="implement", mark_loaded=True)
    # Second load should get depth=1
    result = build_constitution_context(tmp_path, action="implement", mark_loaded=False)

    assert result.first_load is False
    assert result.depth == 1


def test_context_explicit_depth_wins(tmp_path: Path) -> None:
    _write_constitution_bundle(tmp_path)

    # Even on first load, explicit depth=1 overrides the default depth=2
    result = build_constitution_context(tmp_path, action="implement", mark_loaded=False, depth=1)

    assert result.depth == 1
    assert result.mode == "compact"


def test_context_missing_constitution_degrades_gracefully(tmp_path: Path) -> None:
    # No constitution bundle at all
    result = build_constitution_context(tmp_path, action="implement", mark_loaded=False)

    assert result.mode == "missing"
    assert "Constitution file not found" in result.text
    assert result.depth == 2  # first_load so depth defaults to 2


def test_context_result_has_depth_field(tmp_path: Path) -> None:
    _write_constitution_bundle(tmp_path)

    result = build_constitution_context(tmp_path, action="specify", mark_loaded=False)

    # The field must exist on the frozen dataclass
    assert hasattr(result, "depth")
    assert isinstance(result.depth, int)


def test_context_local_support_action_scope_filtering(tmp_path: Path) -> None:
    constitution_dir = tmp_path / ".kittify" / "constitution"
    constitution_dir.mkdir(parents=True)
    (constitution_dir / "constitution.md").write_text(
        "## Policy Summary\n- test policy\n", encoding="utf-8"
    )
    # Write references with mixed local_support scoping
    (constitution_dir / "references.yaml").write_text(
        """schema_version: "1.0.0"
references:
  - id: "GLOBAL_REF"
    kind: user_profile
    title: Global Reference
    local_path: library/global.md
  - id: "LOCAL_IMPLEMENT"
    kind: local_support
    title: Implement Guide
    local_path: library/implement-guide.md
    summary: "A guide (action: implement) for implementation"
  - id: "LOCAL_SPECIFY"
    kind: local_support
    title: Specify Guide
    local_path: library/specify-guide.md
    summary: "A guide (action: specify) for specification"
  - id: "LOCAL_GLOBAL"
    kind: local_support
    title: Global Support
    local_path: library/global-support.md
    summary: "A guide with no action scope"
""",
        encoding="utf-8",
    )

    result = build_constitution_context(tmp_path, action="implement", mark_loaded=False)

    # GLOBAL_REF (non-local_support) always included
    assert "GLOBAL_REF" in result.text
    # LOCAL_IMPLEMENT matches action=implement → included
    assert "LOCAL_IMPLEMENT" in result.text
    # LOCAL_SPECIFY does not match action=implement → excluded
    assert "LOCAL_SPECIFY" not in result.text
    # LOCAL_GLOBAL has no action scope → included
    assert "LOCAL_GLOBAL" in result.text


def test_context_corrupt_constitution_degrades_gracefully(tmp_path: Path) -> None:
    constitution_dir = tmp_path / ".kittify" / "constitution"
    constitution_dir.mkdir(parents=True)
    # Write a non-corrupt constitution (the file exists)
    (constitution_dir / "constitution.md").write_text(
        "## Policy Summary\n- a policy\n", encoding="utf-8"
    )
    # Write corrupt references.yaml
    (constitution_dir / "references.yaml").write_text(
        "this is: [not: valid: yaml: {{}}", encoding="utf-8"
    )

    # Should not raise; references just fallback to empty
    result = build_constitution_context(tmp_path, action="implement", mark_loaded=False)

    assert result.mode in {"bootstrap", "compact", "missing"}
    assert result.references_count == 0
