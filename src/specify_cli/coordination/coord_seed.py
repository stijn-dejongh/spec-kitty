"""Coordination write-location core: establish, seed, refuse (mission coord-artifact-single-home-01M3V4BE, WP03).

The single answer to "where does a COORD write go" for a coordination-routed
Mission (``establish_coord_write_location``), and the one-time carry-over from
the repository-root checkout to the coordination surface (``seed_coord_surface``).
See ``contracts/write-location-accessor.md`` and ``contracts/seed.md``.

Cold-import discipline: every ``specify_cli`` submodule this module needs
(``specify_cli.status.locking``, ``specify_cli.missions._read_path_resolver``,
``specify_cli.coordination.surface_resolver`` / ``workspace`` /
``commit_router``, ``specify_cli.git.protection_policy``) is imported inside
the function that needs it, never at module level, so a future cold-import
caller of this module never drags the whole status/coordination stack in
just to read a type.
"""

from __future__ import annotations

import logging
import os
import subprocess
import uuid
from dataclasses import dataclass, replace
from pathlib import Path
from typing import TYPE_CHECKING, Literal, NoReturn

from mission_runtime import (
    ActionContextError,
    Establishment,
    MissionArtifactKind,
    OwnedCheckout,
    OwnedRefusalCode,
    SeedReport,
    TopologySurface,
    WriteLocation,
    is_primary_artifact_kind,
    kind_for_mission_file,
    placement_seam,
)
from specify_cli.core.constants import KITTY_SPECS_DIR
from specify_cli.coordination.event_prefix import (
    PrefixVerdict,
    classify_prefix,
    event_ids_of,
    merged_log_bytes,
    non_blank_lines_of,
)

if TYPE_CHECKING:
    from specify_cli.coordination.commit_router import CommitRouterResult
    from specify_cli.missions._read_path_resolver import CoordState

__all__ = [
    "COORD_SEED_TRAILER",
    "CoordSeedForkRefused",
    "SeedRequest",
    "establish_coord_write_location",
    "seed_coord_surface",
]

logger = logging.getLogger(__name__)

#: The ONE commit-trailer key every seed commit (and the create-time commit,
#: WP06 T031) carries, keyed by ``mission_id`` -- the D4 post-fix discriminator.
COORD_SEED_TRAILER = "Spec-Kitty-Coordination-Seed"

_COORD_SEED_FORK_REFUSED_CODE = "COORD_SEED_FORK_REFUSED"
_STATUS_LOG_FILENAME = "status.events.jsonl"
_DECISION_LOG_FILENAME = "decisions.events.jsonl"
_LOG_FILENAMES: tuple[str, ...] = (_STATUS_LOG_FILENAME, _DECISION_LOG_FILENAME)
_STATUS_COMMITTED = "committed"


class CoordSeedForkRefused(ActionContextError):
    """A coordination log stream has forked from its root-checkout counterpart (D3).

    Raised **before** anything is written (I-SEED-4): neither surface is
    touched. ``.code`` is ``"COORD_SEED_FORK_REFUSED"`` (``ActionContextError``
    stores ``.code``, never ``.error_code`` -- binding correction).
    """

    error_code = _COORD_SEED_FORK_REFUSED_CODE

    def __init__(
        self,
        *,
        root_path: Path,
        coord_path: str,
        coord_ref: str,
        first_divergence_root: str | None,
        first_divergence_coord: str | None,
        reconcile_steps: tuple[str, ...],
    ) -> None:
        message = (
            f"coordination seed refused: {root_path} and {coord_ref}:{coord_path} "
            "have diverged (first divergence: "
            f"root event_id={first_divergence_root!r}, "
            f"coordination event_id={first_divergence_coord!r}). " + "; ".join(reconcile_steps) + "."
        )
        super().__init__(self.error_code, message)
        self.root_path = root_path
        self.coord_path = coord_path
        self.coord_ref = coord_ref
        self.first_divergence_root = first_divergence_root
        self.first_divergence_coord = first_divergence_coord
        self.reconcile_steps = reconcile_steps


@dataclass(frozen=True, kw_only=True)
class SeedRequest:
    """Everything :func:`seed_coord_surface` needs for one seed attempt (data-model.md §3)."""

    repo_root: Path
    mission_slug: str
    mission_dir_name: str
    mid8: str
    mission_id: str
    coordination_branch: str
    coord_worktree: Path
    root_mission_dir: Path
    #: ``True`` when this is the post-fix restore-then-seed leg (the branch
    #: already carried the seed trailer and COORD-kind paths were just
    #: restored from its tip) -- merges root-only leftovers IN PLACE rather
    #: than building a fresh temp dir for an atomic rename (the target dir
    #: already exists after the restore).
    post_fix: bool = False
    owned: OwnedCheckout | None = None


@dataclass(frozen=True)
class _StreamMerge:
    relpath: str
    merged_text: str | None
    carried: bool


@dataclass(frozen=True)
class _MergeResult:
    stream_merges: tuple[_StreamMerge, ...]
    non_log_files: tuple[tuple[str, bytes], ...]
    carried: tuple[str, ...]
    warnings: tuple[str, ...]
    fork: CoordSeedForkRefused | None


def _lock_root(request: SeedRequest) -> Path:
    return request.owned.owned_root if request.owned is not None else request.repo_root


def _kind_of_relpath(relpath: str) -> MissionArtifactKind | None:
    return kind_for_mission_file(f"{KITTY_SPECS_DIR}/_mission_/{relpath}")


def _is_coord_relpath(relpath: str) -> bool:
    kind = _kind_of_relpath(relpath)
    return kind is not None and not is_primary_artifact_kind(kind)


def _walk_root_coord_relpaths(root_mission_dir: Path) -> tuple[str, ...]:
    if not root_mission_dir.exists():
        return ()
    relpaths = []
    for candidate in sorted(root_mission_dir.rglob("*")):
        if not candidate.is_file():
            continue
        relpath = candidate.relative_to(root_mission_dir).as_posix()
        if _is_coord_relpath(relpath):
            relpaths.append(relpath)
    return tuple(relpaths)


def _coord_tip_relpaths(repo_root: Path, coordination_branch: str, mission_dir_name: str) -> tuple[str, ...]:
    prefix = f"{KITTY_SPECS_DIR}/{mission_dir_name}/"
    result = subprocess.run(
        ["git", "-C", str(repo_root), "ls-tree", "-r", "--name-only", coordination_branch, "--", prefix],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ()
    relpaths = []
    for line in result.stdout.splitlines():
        if not line.startswith(prefix):
            continue
        relpath = line[len(prefix) :]
        if _is_coord_relpath(relpath):
            relpaths.append(relpath)
    return tuple(relpaths)


def _read_text_newline_preserving(path: Path) -> str:
    """Read *path* as text without universal-newline translation (byte-faithful).

    ``Path.read_text(newline=...)`` is Python 3.13+ only; this is the
    3.11/3.12-portable equivalent via the file object's own ``newline``
    support.
    """
    with path.open(encoding="utf-8", newline="") as handle:
        return handle.read()


def _coord_side_text(
    repo_root: Path,
    coord_worktree: Path,
    coordination_branch: str,
    mission_dir_name: str,
    relpath: str,
) -> str | None:
    """Return the coordination-side content for *relpath*: disk first, else the branch tip blob (D3)."""
    disk_path = coord_worktree / KITTY_SPECS_DIR / mission_dir_name / relpath
    if disk_path.exists():
        return _read_text_newline_preserving(disk_path)
    result = subprocess.run(
        ["git", "-C", str(repo_root), "show", f"{coordination_branch}:{KITTY_SPECS_DIR}/{mission_dir_name}/{relpath}"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def _reconcile_steps() -> tuple[str, ...]:
    return (
        "inspect with `spec-kitty doctor decisions`",
        "keep the coordination log",
        "re-open any root-only decisions with `spec-kitty agent decision open ...`",
        "then remove the root copy",
    )


def _merge_stream(request: SeedRequest, filename: str) -> _StreamMerge | CoordSeedForkRefused | None:
    root_path = request.root_mission_dir / filename
    root_text = _read_text_newline_preserving(root_path) if root_path.exists() else ""
    coord_text = _coord_side_text(request.repo_root, request.coord_worktree, request.coordination_branch, request.mission_dir_name, filename) or ""
    root_lines = non_blank_lines_of(root_text.splitlines(keepends=True))
    coord_lines = non_blank_lines_of(coord_text.splitlines(keepends=True))
    root_ids = event_ids_of(root_lines)
    coord_ids = event_ids_of(coord_lines)
    verdict: PrefixVerdict = classify_prefix(root_ids, coord_ids)
    if verdict.kind == "fork":
        coord_ref_path = f"{KITTY_SPECS_DIR}/{request.mission_dir_name}/{filename}"
        return CoordSeedForkRefused(
            root_path=root_path,
            coord_path=coord_ref_path,
            coord_ref=request.coordination_branch,
            first_divergence_root=verdict.first_divergence[0],
            first_divergence_coord=verdict.first_divergence[1],
            reconcile_steps=_reconcile_steps(),
        )
    if verdict.kind == "nothing" and not coord_lines:
        return None
    merged = merged_log_bytes(root_lines, coord_lines, verdict).decode("utf-8")
    return _StreamMerge(relpath=filename, merged_text=merged, carried=verdict.kind == "carry_tail")


def _merge_non_log_files(request: SeedRequest) -> tuple[tuple[tuple[str, bytes], ...], tuple[str, ...], tuple[str, ...]]:
    root_relpaths = {p for p in _walk_root_coord_relpaths(request.root_mission_dir) if p not in _LOG_FILENAMES}
    coord_relpaths = {p for p in _coord_tip_relpaths(request.repo_root, request.coordination_branch, request.mission_dir_name) if p not in _LOG_FILENAMES}
    non_log_files: list[tuple[str, bytes]] = []
    carried: list[str] = []
    warnings: list[str] = []
    for relpath in sorted(root_relpaths | coord_relpaths):
        coord_text = _coord_side_text(request.repo_root, request.coord_worktree, request.coordination_branch, request.mission_dir_name, relpath)
        root_path = request.root_mission_dir / relpath
        if coord_text is not None:
            if root_path.exists() and _read_text_newline_preserving(root_path) != coord_text:
                warnings.append(f"{relpath}: root and coordination copies differ; keeping the coordination copy")
            continue
        if root_path.exists():
            non_log_files.append((relpath, root_path.read_bytes()))
            carried.append(relpath)
    return tuple(non_log_files), tuple(carried), tuple(warnings)


def _merge_coord_content(request: SeedRequest) -> _MergeResult:
    stream_merges: list[_StreamMerge] = []
    carried: list[str] = []
    for filename in _LOG_FILENAMES:
        merge = _merge_stream(request, filename)
        if isinstance(merge, CoordSeedForkRefused):
            return _MergeResult(stream_merges=(), non_log_files=(), carried=(), warnings=(), fork=merge)
        if merge is None:
            continue
        stream_merges.append(merge)
        if merge.carried:
            carried.append(merge.relpath)
    non_log_files, non_log_carried, warnings = _merge_non_log_files(request)
    carried.extend(non_log_carried)
    return _MergeResult(
        stream_merges=tuple(stream_merges),
        non_log_files=non_log_files,
        carried=tuple(carried),
        warnings=warnings,
        fork=None,
    )


def _write_merge_files(target_dir: Path, merge: _MergeResult) -> None:
    for stream in merge.stream_merges:
        if stream.merged_text is None:
            continue
        path = target_dir / stream.relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(stream.merged_text)
    for relpath, content in merge.non_log_files:
        path = target_dir / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def _cleanup_stale_seed_temp_dirs(request: SeedRequest) -> None:
    specs_dir = request.coord_worktree / KITTY_SPECS_DIR
    if not specs_dir.exists():
        return
    stale_prefix = f".{request.mission_dir_name}.seed-"
    for candidate in specs_dir.iterdir():
        if candidate.is_dir() and candidate.name.startswith(stale_prefix):
            _remove_tree(candidate)


def _remove_tree(path: Path) -> None:
    import shutil

    shutil.rmtree(path, ignore_errors=True)


def _write_merge_via_temp_rename(request: SeedRequest, merge: _MergeResult) -> Path:
    # Explicit ``Path`` annotations: ``KITTY_SPECS_DIR`` is typed ``Any`` under
    # the project's ``follow_imports = "skip"`` mypy config, which would
    # otherwise poison the ``/`` chain below with ``Any``.
    specs_dir: Path = request.coord_worktree / KITTY_SPECS_DIR
    specs_dir.mkdir(parents=True, exist_ok=True)
    final_dir: Path = specs_dir / request.mission_dir_name
    temp_dir: Path = specs_dir / f".{request.mission_dir_name}.seed-{os.getpid()}-{uuid.uuid4().hex[:12]}"
    temp_dir.mkdir(parents=True)
    _write_merge_files(temp_dir, merge)
    os.rename(temp_dir, final_dir)
    return final_dir


def _write_merge_in_place(request: SeedRequest, merge: _MergeResult) -> Path:
    final_dir: Path = request.coord_worktree / KITTY_SPECS_DIR / request.mission_dir_name
    final_dir.mkdir(parents=True, exist_ok=True)
    _write_merge_files(final_dir, merge)
    return final_dir


def _to_repo_relpath(repo_root: Path, path: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def _git_path_status(repo_root: Path, repo_relpath: str) -> Literal["dirty", "untracked", "clean"]:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--porcelain=v1", "--", repo_relpath],
        capture_output=True,
        text=True,
        check=False,
    )
    output = result.stdout.strip("\n")
    if not output:
        return "clean"
    if output.startswith("??"):
        return "untracked"
    return "dirty"


def _restore_root_files(request: SeedRequest, carried: tuple[str, ...]) -> tuple[str, ...]:
    restored: list[str] = []
    for relpath in carried:
        root_path = request.root_mission_dir / relpath
        if not root_path.exists():
            continue
        repo_relpath = _to_repo_relpath(request.repo_root, root_path)
        status = _git_path_status(request.repo_root, repo_relpath)
        if status == "untracked":
            root_path.unlink()
            restored.append(repo_relpath)
        elif status == "dirty":
            subprocess.run(["git", "-C", str(request.repo_root), "checkout", "--", repo_relpath], check=True, capture_output=True)
            restored.append(repo_relpath)
        # "clean": pre-fix history stays untouched (C-004).
    return tuple(restored)


def _commit_seed(request: SeedRequest, commit_paths: tuple[Path, ...]) -> CommitRouterResult:
    from specify_cli.coordination.commit_router import commit_for_mission
    from specify_cli.git.protection_policy import ProtectionPolicy

    policy = (
        ProtectionPolicy.resolve_for_owned(request.owned, request.mission_slug)
        if request.owned is not None
        else ProtectionPolicy.resolve_for_mission(request.repo_root, request.mission_slug)
    )
    message = f"chore({request.mission_slug}): seed coordination surface\n\n{COORD_SEED_TRAILER}: {request.mission_id}"
    return commit_for_mission(
        request.repo_root,
        request.mission_slug,
        files=commit_paths,
        message=message,
        policy=policy,
        kind=MissionArtifactKind.STATUS_STATE,
        owned=request.owned,
    )


_STATUS_UNCHANGED = "unchanged"


def _commit_and_restore(request: SeedRequest, merge: _MergeResult, final_dir: Path) -> SeedReport:
    """Commit every COORD-kind file now on disk (I-SEED-7), then restore the root checkout (I-SEED-8).

    Committing everything on disk -- not merely ``merge.carried`` -- matters
    for a RETRY of a previously-refused seed commit (I-SEED-10): the dir
    already holds the fully-merged, fork-checked content from the attempt
    that built it; this attempt's own ``merge.carried`` may be empty (root is
    already a prefix of what is on disk), yet the untracked files still need
    their first commit.
    """
    warnings = list(merge.warnings)
    coord_commit: str | None = None
    commit_relpaths = _coord_kind_relpaths_on_disk(final_dir)
    if commit_relpaths:
        commit_paths = tuple(final_dir / relpath for relpath in commit_relpaths)
        result = _commit_seed(request, commit_paths)
        if result.status == _STATUS_COMMITTED:
            coord_commit = result.commit_hash
        elif result.status != _STATUS_UNCHANGED:
            reason = f", reason={result.reason!r}" if result.reason else ""
            warnings.append(
                f"seed commit not applied (status={result.status!r}{reason}); the mission "
                "dir is present but uncommitted. The next coordination write retries the commit."
            )
    restored_root = _restore_root_files(request, merge.carried)
    if merge.carried or warnings:
        logger.warning(
            "coordination seed for mission %s: carried=%s restored_root=%s coord_commit=%s warnings=%s",
            request.mission_slug,
            merge.carried,
            restored_root,
            coord_commit,
            warnings,
        )
    return SeedReport(
        carried=merge.carried,
        restored_root=restored_root,
        coord_commit=coord_commit,
        warnings=tuple(warnings),
    )


def _trailer_present(repo_root: Path, coordination_branch: str, mission_id: str) -> bool:
    if not mission_id:
        return False
    result = subprocess.run(
        ["git", "-C", str(repo_root), "log", f"--format=%(trailers:key={COORD_SEED_TRAILER},valueonly)", coordination_branch],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return False
    return mission_id in {line.strip() for line in result.stdout.splitlines() if line.strip()}


def _seed_pending(request: SeedRequest) -> bool:
    """I-SEED-10: pending iff the Mission dir is wholly untracked AND has no trailer/committed blob."""
    repo_relpath = f"{KITTY_SPECS_DIR}/{request.mission_dir_name}/"
    result = subprocess.run(
        ["git", "-C", str(request.coord_worktree), "status", "--porcelain", "--", repo_relpath],
        capture_output=True,
        text=True,
        check=False,
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if lines != [f"?? {repo_relpath}"]:
        return False
    if _trailer_present(request.repo_root, request.coordination_branch, request.mission_id):
        return False
    return not _coord_tip_relpaths(request.repo_root, request.coordination_branch, request.mission_dir_name)


def _coord_kind_relpaths_on_disk(final_dir: Path) -> tuple[str, ...]:
    if not final_dir.exists():
        return ()
    relpaths = []
    for candidate in sorted(final_dir.rglob("*")):
        if not candidate.is_file():
            continue
        relpath = candidate.relative_to(final_dir).as_posix()
        if _is_coord_relpath(relpath):
            relpaths.append(relpath)
    return tuple(relpaths)


def _run_merge_and_commit(request: SeedRequest, *, in_place: bool) -> SeedReport:
    """Merge (with a full fork re-check, I-SEED-4), write, commit, restore.

    Used by both the fresh pre-fix/post-fix paths and the MATERIALIZED
    pending-seed retry (I-SEED-10): the fork check always re-runs against the
    CURRENT root content, regardless of whatever happens to already sit on
    disk, so a retry never blindly trusts stale or adversarial disk content.
    """
    merge = _merge_coord_content(request)
    if merge.fork is not None:
        raise merge.fork
    final_dir = _write_merge_in_place(request, merge) if in_place else _write_merge_via_temp_rename(request, merge)
    return _commit_and_restore(request, merge, final_dir)


def _seed_coord_surface_locked(request: SeedRequest) -> SeedReport:
    from specify_cli.missions._read_path_resolver import CoordState, probe_coord_state

    state = probe_coord_state(request.repo_root, request.mission_slug, request.mid8, coordination_branch=request.coordination_branch)
    if state is CoordState.MATERIALIZED:
        if not _seed_pending(request):
            return SeedReport()
        return _run_merge_and_commit(request, in_place=True)

    _cleanup_stale_seed_temp_dirs(request)
    return _run_merge_and_commit(request, in_place=request.post_fix)


def seed_coord_surface(request: SeedRequest) -> SeedReport:
    """Carry root-checkout COORD records onto the coordination surface exactly once.

    See ``contracts/seed.md``. Runs under the mission status lock (I-SEED-1);
    re-entrant, so a caller already holding it (``BookkeepingTransaction``) is
    not deadlocked.
    """
    from specify_cli.status.locking import (
        BOUNDED_STATUS_LOCK_TIMEOUT_SECONDS,
        feature_status_lock,
    )

    with feature_status_lock(_lock_root(request), request.mission_dir_name, timeout=BOUNDED_STATUS_LOCK_TIMEOUT_SECONDS):
        return _seed_coord_surface_locked(request)


# ---------------------------------------------------------------------------
# establish_coord_write_location
# ---------------------------------------------------------------------------


def _primary_write_location(repo_root: Path, mission_slug: str, kind: MissionArtifactKind, owned: OwnedCheckout | None) -> WriteLocation:
    path = placement_seam(repo_root, mission_slug, owned=owned).read_dir(kind)
    checkout_root = owned.owned_root if owned is not None else repo_root
    return WriteLocation(
        path=path,
        checkout_root=checkout_root,
        surface=TopologySurface.PRIMARY,
        coord_state_before=None,
        establishment=Establishment.NONE,
    )


def _resolve_coord_worktree_root(repo_root: Path, mission_slug: str, mid8: str, owned: OwnedCheckout | None) -> Path:
    from specify_cli.coordination.workspace import CoordinationWorkspace

    root = owned.repository_root if owned is not None else repo_root
    worktree: Path = CoordinationWorkspace.worktree_path(root, mission_slug, mid8)
    return worktree


def _establish_owned_coord_workspace(owned: OwnedCheckout, mission_slug: str, mid8: str) -> None:
    from runtime.next.runtime_bridge import _resolve_owned_coordination_workspace
    from specify_cli.coordination.workspace import CoordinationWorkspace

    _resolve_owned_coordination_workspace(CoordinationWorkspace, owned.repository_root, mission_slug, mid8)


def _materialize_for_write(
    repo_root: Path,
    mission_slug: str,
    mid8: str,
    coordination_branch: str,
    owned: OwnedCheckout | None,
) -> CoordState:
    from specify_cli.missions._read_path_resolver import probe_coord_state

    if owned is not None:
        try:
            _establish_owned_coord_workspace(owned, mission_slug, mid8)
        except Exception as exc:  # noqa: BLE001 -- translated into the owned refusal code (C-001: no new error type)
            raise ActionContextError(
                OwnedRefusalCode.OWNED_COORDINATION_WORKSPACE_UNAVAILABLE.value,
                f"owned coordination workspace unavailable for mission {mission_slug!r}: {exc}",
            ) from exc
    else:
        from specify_cli.coordination.surface_resolver import materialize_coord_surface_for_write

        materialize_coord_surface_for_write(repo_root, mission_slug)
    return probe_coord_state(repo_root, mission_slug, mid8, coordination_branch=coordination_branch)


def _raise_coord_branch_deleted(
    repo_root: Path,
    mission_slug: str,
    mid8: str,
    coordination_branch: str,
    primary_candidate: Path,
) -> NoReturn:
    from specify_cli.coordination.surface_resolver import CoordinationBranchDeleted

    raise CoordinationBranchDeleted.for_mission(
        repo_root=repo_root,
        mission_slug=mission_slug,
        mid8=mid8,
        coordination_branch=coordination_branch,
        primary_candidate=primary_candidate,
    )


def _restore_coord_kind_paths_from_tip(
    repo_root: Path,
    coordination_branch: str,
    mission_dir_name: str,
    coord_worktree: Path,
) -> tuple[str, ...]:
    relpaths = _coord_tip_relpaths(repo_root, coordination_branch, mission_dir_name)
    if not relpaths:
        return ()
    pathspecs = [f"{KITTY_SPECS_DIR}/{mission_dir_name}/{relpath}" for relpath in relpaths]
    subprocess.run(
        ["git", "-C", str(coord_worktree), "checkout", coordination_branch, "--", *pathspecs],
        check=True,
        capture_output=True,
    )
    return tuple(sorted(relpaths))


@dataclass(frozen=True, kw_only=True)
class _EstablishContext:
    repo_root: Path
    mission_slug: str
    mission_dir_name: str
    mid8: str
    mission_id: str
    coordination_branch: str
    coord_worktree: Path
    root_mission_dir: Path
    owned: OwnedCheckout | None


def _to_seed_request(ctx: _EstablishContext, *, post_fix: bool) -> SeedRequest:
    return SeedRequest(
        repo_root=ctx.repo_root,
        mission_slug=ctx.mission_slug,
        mission_dir_name=ctx.mission_dir_name,
        mid8=ctx.mid8,
        mission_id=ctx.mission_id,
        coordination_branch=ctx.coordination_branch,
        coord_worktree=ctx.coord_worktree,
        root_mission_dir=ctx.root_mission_dir,
        post_fix=post_fix,
        owned=ctx.owned,
    )


def _handle_materialized(ctx: _EstablishContext, coord_state_before: CoordState) -> WriteLocation:
    report = seed_coord_surface(_to_seed_request(ctx, post_fix=False))
    seed = report if (report.carried or report.coord_commit or report.warnings) else None
    coord_dir = ctx.coord_worktree / KITTY_SPECS_DIR / ctx.mission_dir_name
    return WriteLocation(
        path=coord_dir,
        checkout_root=ctx.coord_worktree,
        surface=TopologySurface.COORD,
        coord_state_before=coord_state_before,
        establishment=Establishment.NONE,
        seed=seed,
    )


def _handle_empty_pre_fix(ctx: _EstablishContext, coord_state_before: CoordState) -> WriteLocation:
    report = seed_coord_surface(_to_seed_request(ctx, post_fix=False))
    coord_dir = ctx.coord_worktree / KITTY_SPECS_DIR / ctx.mission_dir_name
    return WriteLocation(
        path=coord_dir,
        checkout_root=ctx.coord_worktree,
        surface=TopologySurface.COORD,
        coord_state_before=coord_state_before,
        establishment=Establishment.SEEDED,
        seed=report,
    )


def _handle_empty_post_fix(ctx: _EstablishContext, coord_state_before: CoordState) -> WriteLocation:
    logger.warning(
        "coordination Mission dir missing from worktree for mission %s (branch %s); restoring from branch tip.",
        ctx.mission_slug,
        ctx.coordination_branch,
    )
    restored = _restore_coord_kind_paths_from_tip(ctx.repo_root, ctx.coordination_branch, ctx.mission_dir_name, ctx.coord_worktree)
    report = seed_coord_surface(_to_seed_request(ctx, post_fix=True))
    merged_report = replace(report, restored_from_branch=restored)
    coord_dir = ctx.coord_worktree / KITTY_SPECS_DIR / ctx.mission_dir_name
    return WriteLocation(
        path=coord_dir,
        checkout_root=ctx.coord_worktree,
        surface=TopologySurface.COORD,
        coord_state_before=coord_state_before,
        establishment=Establishment.RESTORED_FROM_BRANCH,
        seed=merged_report,
    )


def _handle_unmaterialized(repo_root: Path, mission_slug: str, ctx: _EstablishContext) -> WriteLocation:
    from specify_cli.missions._read_path_resolver import CoordState

    new_state = _materialize_for_write(repo_root, mission_slug, ctx.mid8, ctx.coordination_branch, ctx.owned)
    materialized_ctx = replace(ctx, coord_worktree=_resolve_coord_worktree_root(repo_root, mission_slug, ctx.mid8, ctx.owned))
    if new_state is CoordState.MATERIALIZED:
        return _handle_materialized(materialized_ctx, CoordState.UNMATERIALIZED)
    if new_state is CoordState.EMPTY:
        trailer_present = _trailer_present(repo_root, ctx.coordination_branch, ctx.mission_id)
        if not trailer_present:
            return _handle_empty_pre_fix(materialized_ctx, CoordState.UNMATERIALIZED)
        return _handle_empty_post_fix(materialized_ctx, CoordState.UNMATERIALIZED)
    # Materialization is documented to leave only MATERIALIZED/EMPTY on
    # success (surface_resolver.materialize_coord_surface_for_write); any
    # other outcome means it already raised.
    raise AssertionError(f"unexpected coord state after materialization: {new_state!r}")


def establish_coord_write_location(
    repo_root: Path,
    mission_slug: str,
    kind: MissionArtifactKind,
    *,
    owned: OwnedCheckout | None = None,
) -> WriteLocation:
    """Resolve, materialize, seed or refuse the write location for a COORD write.

    See ``contracts/write-location-accessor.md``. Absorbs the coordination
    write gate (research D22): the old refusal for an ``UNMATERIALIZED``
    local-head coordination branch that already carries committed content is
    replaced by materializing and letting the state machine below decide.
    """
    if is_primary_artifact_kind(kind):
        return _primary_write_location(repo_root, mission_slug, kind, owned)

    from specify_cli.coordination.surface_resolver import resolve_declared_mid8
    from specify_cli.missions._read_path_resolver import (
        CoordState,
        coord_feature_dir,
        probe_coord_state,
        read_primary_meta,
    )

    meta, _declares_coordination = read_primary_meta(repo_root, mission_slug)
    raw_branch = meta.get("coordination_branch")
    coordination_branch = str(raw_branch) if raw_branch else None
    if coordination_branch is None:
        return _primary_write_location(repo_root, mission_slug, kind, owned)

    mid8 = resolve_declared_mid8(meta, mission_slug)
    mission_id = str(meta.get("mission_id") or "")
    mission_dir_name = coord_feature_dir(repo_root, mission_slug, mid8).name
    root_mission_dir = placement_seam(repo_root, mission_slug, owned=owned).read_dir(MissionArtifactKind.PRIMARY_METADATA)

    state = probe_coord_state(repo_root, mission_slug, mid8, coordination_branch=coordination_branch)
    coord_worktree = _resolve_coord_worktree_root(repo_root, mission_slug, mid8, owned)
    ctx = _EstablishContext(
        repo_root=repo_root,
        mission_slug=mission_slug,
        mission_dir_name=mission_dir_name,
        mid8=mid8,
        mission_id=mission_id,
        coordination_branch=coordination_branch,
        coord_worktree=coord_worktree,
        root_mission_dir=root_mission_dir,
        owned=owned,
    )

    if state is CoordState.DELETED:
        _raise_coord_branch_deleted(repo_root, mission_slug, mid8, coordination_branch, root_mission_dir)
    if state is CoordState.UNMATERIALIZED:
        return _handle_unmaterialized(repo_root, mission_slug, ctx)
    if state is CoordState.MATERIALIZED:
        return _handle_materialized(ctx, CoordState.MATERIALIZED)
    # state is EMPTY.
    if not _trailer_present(repo_root, coordination_branch, mission_id):
        return _handle_empty_pre_fix(ctx, CoordState.EMPTY)
    return _handle_empty_post_fix(ctx, CoordState.EMPTY)
