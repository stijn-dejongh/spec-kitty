"""WP14 (coord-artifact-single-home-01M3V4BE): planning-command consumers render per-surface outcomes.

Covers T074 (setup-plan masking), T075 (setup-plan's two discarded-result
sites) and T078 (consumer tests + C-008 controls + JSON additivity) for the
``mission_setup_plan.py`` surface (contracts/commit-outcome.md).

``_commit_to_branch`` never naturally splits a single planning-artifact file
across the PRIMARY/COORDINATION partitions (``spec.md``/``plan.md``/
``tasks.md`` are always PRIMARY-kind), so a genuinely mixed-surface batch is
reproduced here by monkeypatching ``commit_for_mission`` at its owning module
(``specify_cli.coordination.commit_router``) to return a crafted
:class:`CommitRouterResult` carrying two surfaces -- a committed PRIMARY
surface alongside a COORDINATION surface refused with ``STATUS_LOCK_HELD``.
This is the same "test via a stubbed CommitRouterResult, labelled as a unit
test" escape hatch the WP prompt names for the report-transaction consumer
(T076 edge cases), applied here for the identical reason.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

import specify_cli.coordination.commit_router as commit_router_module
from specify_cli.cli.commands.agent.mission_setup_plan import (
    CommitToBranchResult,
    _build_setup_plan_result,
    _commit_to_branch,
    _warn_on_incomplete_surfaces,
)
from specify_cli.coordination.commit_outcome import PathFate, SurfaceOutcome, commit_outcome_payload
from specify_cli.coordination.commit_router import CommitRouterResult

pytestmark = [pytest.mark.integration, pytest.mark.git_repo]

_COORD_BRANCH = "kitty/mission-demo-01TESTPLAN"
_TARGET_BRANCH = "topic"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def _init_repo(repo: Path) -> None:
    _git(repo, "init", "-q", "-b", _TARGET_BRANCH)
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Test")
    (repo / "plan.md").write_text("# Plan\n", encoding="utf-8")
    _git(repo, "add", "plan.md")
    _git(repo, "-c", "commit.gpgsign=false", "commit", "-qm", "seed")


def _mixed_surfaces_result(*, primary_ref: str) -> CommitRouterResult:
    """A split batch: PRIMARY committed cleanly, COORDINATION refused by a contended status lock."""
    primary = SurfaceOutcome(
        surface="primary",
        branch=primary_ref,
        status="committed",
        commit_hash="abc1234567890",
        committed=("kitty-specs/demo/plan.md",),
    )
    coordination = SurfaceOutcome(
        surface="coordination",
        branch=_COORD_BRANCH,
        status="error",
        commit_hash=None,
        refused=(PathFate(path="kitty-specs/demo/status.events.jsonl", reason="STATUS_LOCK_HELD"),),
        diagnostic="status lock held by another writer",
    )
    return CommitRouterResult(
        status="committed",
        placement_ref=primary_ref,
        commit_hash="abc1234567890",
        surfaces=(primary, coordination),
    )


# ---------------------------------------------------------------------------
# T075 -- _commit_to_branch carries the router's full surfaces tuple through.
# ---------------------------------------------------------------------------


def test_commit_to_branch_carries_router_surfaces_through(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _init_repo(tmp_path)
    plan_file = tmp_path / "plan.md"
    mixed = _mixed_surfaces_result(primary_ref=_TARGET_BRANCH)
    monkeypatch.setattr(commit_router_module, "commit_for_mission", lambda **_kwargs: mixed)

    result = _commit_to_branch(plan_file, "demo", "plan", tmp_path, _TARGET_BRANCH, json_output=True)

    assert result.status == "committed"
    assert result.surfaces == mixed.surfaces
    # Load-bearing (T074): the non-caller COORDINATION surface's STATUS_LOCK_HELD
    # refusal reaches the JSON payload even though the top-level/caller status
    # is "committed" -- the exact masking this WP cures (#5513, #5501).
    payload = commit_outcome_payload(result)
    surface_names = {entry["surface"] for entry in payload["surfaces"]}
    assert surface_names == {"primary", "coordination"}
    coordination_payload = next(entry for entry in payload["surfaces"] if entry["surface"] == "coordination")
    assert coordination_payload["refused"][0]["reason"] == "STATUS_LOCK_HELD"


# ---------------------------------------------------------------------------
# T075 -- the two discarded-result sites now warn via _warn_on_incomplete_surfaces.
# ---------------------------------------------------------------------------


def test_warn_on_incomplete_surfaces_silent_on_an_all_success_batch(capsys: pytest.CaptureFixture[str]) -> None:
    """D8 rule: an all-committed/unchanged batch prints nothing (C-008 control)."""
    all_ok = CommitRouterResult(
        status="committed",
        placement_ref=_TARGET_BRANCH,
        commit_hash="abc",
        surfaces=(SurfaceOutcome(surface="primary", branch=_TARGET_BRANCH, status="committed", commit_hash="abc", committed=("a",)),),
    )

    _warn_on_incomplete_surfaces(all_ok, json_output=False)

    assert capsys.readouterr().out == ""


def test_warn_on_incomplete_surfaces_silent_in_json_mode(capsys: pytest.CaptureFixture[str]) -> None:
    mixed = _mixed_surfaces_result(primary_ref=_TARGET_BRANCH)

    _warn_on_incomplete_surfaces(mixed, json_output=True)

    assert capsys.readouterr().out == ""


def test_warn_on_incomplete_surfaces_renders_the_refused_surface(capsys: pytest.CaptureFixture[str]) -> None:
    mixed = _mixed_surfaces_result(primary_ref=_TARGET_BRANCH)

    _warn_on_incomplete_surfaces(mixed, json_output=False)

    out = capsys.readouterr().out
    assert "coordination" in out
    assert "STATUS_LOCK_HELD" in out


# ---------------------------------------------------------------------------
# T074/T078 -- setup-plan's JSON envelope gains `surfaces` additively.
# ---------------------------------------------------------------------------


def _base_build_kwargs(tmp_path: Path, *, plan_commit_result: CommitToBranchResult | None) -> dict[str, Any]:
    return {
        "plan_file": tmp_path / "plan.md",
        "spec_file": tmp_path / "spec.md",
        "feature_dir": tmp_path / "kitty-specs" / "demo",
        "mission_slug": "demo",
        "plan_is_substantive": True,
        "plan_blocked_reason": None,
        "plan_commit_result": plan_commit_result,
        "gap_analysis_path": None,
        "generators_detected": [],
        "target_branch": _TARGET_BRANCH,
        "current_branch": _TARGET_BRANCH,
    }


def test_setup_plan_reports_skipped_surface_in_json(tmp_path: Path) -> None:
    """T074 (setup-plan half): a refused coordination surface reaches the JSON envelope.

    RED at the WP base: ``plan_commit_result`` was turned into ``commit_hash``/
    ``commit_status``/``commit_diagnostic`` alone -- the four legacy fields
    (contract rule 4) -- so a non-caller surface's refusal never reached the
    JSON payload at all.
    """
    mixed = _mixed_surfaces_result(primary_ref=_TARGET_BRANCH)
    commit_result = CommitToBranchResult(status="committed", placement_ref=_TARGET_BRANCH, commit_hash="abc1234567890", surfaces=mixed.surfaces)

    outcome = _build_setup_plan_result(**_base_build_kwargs(tmp_path, plan_commit_result=commit_result))

    assert "surfaces" in outcome.payload
    surfaces = outcome.payload["surfaces"]
    assert isinstance(surfaces, list)
    surface_names = {entry["surface"] for entry in surfaces}
    assert surface_names == {"primary", "coordination"}
    coordination_payload = next(entry for entry in surfaces if entry["surface"] == "coordination")
    assert coordination_payload["refused"][0]["reason"] == "STATUS_LOCK_HELD"


def test_setup_plan_json_is_additive_when_every_surface_committed(tmp_path: Path) -> None:
    """C-008 control: a non-coordination Mission's existing JSON keys are unchanged (plus the additive key)."""
    single = CommitRouterResult(
        status="committed",
        placement_ref=_TARGET_BRANCH,
        commit_hash="abc1234567890",
        surfaces=(SurfaceOutcome(surface="primary", branch=_TARGET_BRANCH, status="committed", commit_hash="abc1234567890", committed=("plan.md",)),),
    )
    commit_result = CommitToBranchResult(status="committed", placement_ref=_TARGET_BRANCH, commit_hash="abc1234567890", surfaces=single.surfaces)

    before = _build_setup_plan_result(**_base_build_kwargs(tmp_path, plan_commit_result=None))
    after = _build_setup_plan_result(**_base_build_kwargs(tmp_path, plan_commit_result=commit_result))

    # Every pre-existing key the no-commit-result payload carries is present,
    # byte-identical, in the single-surface payload too (JSON additivity).
    shared_keys = set(before.payload) & set(after.payload)
    for key in shared_keys:
        if key in ("commit_created", "commit_hash", "commit_status"):
            continue  # these three are populated BY plan_commit_result itself (unchanged shape)
        assert before.payload[key] == after.payload[key], key
    assert "surfaces" in after.payload


def test_setup_plan_json_omits_surfaces_when_commit_result_carries_none(tmp_path: Path) -> None:
    """A legacy/empty-``surfaces`` ``CommitToBranchResult`` adds no ``surfaces`` key (additive, never a crash)."""
    commit_result = CommitToBranchResult(status="unchanged", placement_ref=_TARGET_BRANCH)

    outcome = _build_setup_plan_result(**_base_build_kwargs(tmp_path, plan_commit_result=commit_result))

    assert "surfaces" not in outcome.payload
