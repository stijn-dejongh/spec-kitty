#!/usr/bin/env python3
"""Acceptance workflow utilities for Spec Kitty missions."""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, UTC
from pathlib import Path
from collections.abc import Iterable, Mapping, Sequence

from .tasks_support import (
    LANES,
    TaskCliError,
    WorkPackage,
    get_lane_from_frontmatter,
    git_status_lines,
    is_legacy_format,
    run_git,
    split_frontmatter,
)
from specify_cli.status.store import EVENTS_FILENAME, StoreError
from specify_cli.status.lane_reader import CanonicalStatusNotFoundError
from specify_cli.mission_metadata import load_meta, record_acceptance, write_meta
from specify_cli.mission import MissionError, get_mission_for_mission_dir
from specify_cli.validators.paths import PathValidationError, validate_mission_paths
from specify_cli.core.paths import (
    get_mission_dir,
    require_explicit_mission as _require_explicit_mission,
)
from specify_cli.core.tool_config import get_auto_commit_default

logger = logging.getLogger(__name__)

AcceptanceMode = str  # Expected values: "pr", "local", "checklist"


class AcceptanceError(TaskCliError):
    """Raised when acceptance cannot complete due to outstanding issues."""


class ArtifactEncodingError(AcceptanceError):
    """Raised when a project artifact cannot be decoded as UTF-8."""

    def __init__(self, path: Path, error: UnicodeDecodeError):
        byte = error.object[error.start : error.start + 1]
        byte_display = f"0x{byte[0]:02x}" if byte else "unknown"
        message = (
            f"Invalid UTF-8 encoding in {path}: byte {byte_display} at offset {error.start}. "
            "Run with --normalize-encoding to fix automatically."
        )
        super().__init__(message)
        self.path = path
        self.error = error


@dataclass
class WorkPackageState:
    work_package_id: str
    lane: str
    title: str
    path: str
    has_lane_entry: bool
    latest_lane: str | None
    metadata: dict[str, str | None] = field(default_factory=dict)


@dataclass
class AcceptanceSummary:
    mission_slug: str
    repo_root: Path
    mission_dir: Path
    tasks_dir: Path
    branch: str | None
    worktree_root: Path
    primary_repo_root: Path
    lanes: dict[str, list[str]]
    work_packages: list[WorkPackageState]
    metadata_issues: list[str]
    activity_issues: list[str]
    unchecked_tasks: list[str]
    needs_clarification: list[str]
    missing_artifacts: list[str]
    optional_missing: list[str]
    git_dirty: list[str]
    path_violations: list[str]
    warnings: list[str]

    @property
    def mission(self) -> str:
        """Compatibility alias for legacy callers that still expect feature naming."""
        return self.mission_slug

    @property
    def feature(self) -> str:
        """Compatibility alias for legacy callers that still expect feature naming."""
        return self.mission_slug

    @property
    def all_done(self) -> bool:
        """True when all WPs are approved or done (no WPs still in progress or review)."""
        return not (
            self.lanes.get("planned")
            or self.lanes.get("claimed")
            or self.lanes.get("doing")
            or self.lanes.get("in_progress")
            or self.lanes.get("for_review")
        )

    @property
    def ok(self) -> bool:
        return (
            self.all_done
            and not self.metadata_issues
            and not self.activity_issues
            and not self.unchecked_tasks
            and not self.needs_clarification
            and not self.missing_artifacts
            and not self.git_dirty
            and not self.path_violations
        )

    def outstanding(self) -> dict[str, list[str]]:
        buckets = {
            "not_done": [
                *self.lanes.get("planned", []),
                *self.lanes.get("claimed", []),
                *self.lanes.get("doing", []),
                *self.lanes.get("in_progress", []),
                *self.lanes.get("for_review", []),
            ],
            "metadata": self.metadata_issues,
            "activity": self.activity_issues,
            "unchecked_tasks": self.unchecked_tasks,
            "needs_clarification": self.needs_clarification,
            "missing_artifacts": self.missing_artifacts,
            "git_dirty": self.git_dirty,
            "path_violations": self.path_violations,
        }
        return {key: value for key, value in buckets.items() if value}

    def to_dict(self) -> dict[str, object]:
        return {
            "mission_slug": self.mission_slug,
            "branch": self.branch,
            "repo_root": str(self.repo_root),
            "mission_dir": str(self.mission_dir),
            "tasks_dir": str(self.tasks_dir),
            "worktree_root": str(self.worktree_root),
            "primary_repo_root": str(self.primary_repo_root),
            "lanes": self.lanes,
            "work_packages": [
                {
                    "id": wp.work_package_id,
                    "lane": wp.lane,
                    "title": wp.title,
                    "path": wp.path,
                    "latest_lane": wp.latest_lane,
                    "has_lane_entry": wp.has_lane_entry,
                    "metadata": wp.metadata,
                }
                for wp in self.work_packages
            ],
            "metadata_issues": self.metadata_issues,
            "activity_issues": self.activity_issues,
            "unchecked_tasks": self.unchecked_tasks,
            "needs_clarification": self.needs_clarification,
            "missing_artifacts": self.missing_artifacts,
            "optional_missing": self.optional_missing,
            "git_dirty": self.git_dirty,
            "path_violations": self.path_violations,
            "warnings": self.warnings,
            "all_done": self.all_done,
            "ok": self.ok,
        }


@dataclass
class AcceptanceResult:
    summary: AcceptanceSummary
    mode: AcceptanceMode
    accepted_at: str
    accepted_by: str
    parent_commit: str | None
    accept_commit: str | None
    commit_created: bool
    instructions: list[str]
    cleanup_instructions: list[str]
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "accepted_at": self.accepted_at,
            "accepted_by": self.accepted_by,
            "mode": self.mode,
            "parent_commit": self.parent_commit,
            "accept_commit": self.accept_commit,
            "commit_created": self.commit_created,
            "instructions": self.instructions,
            "cleanup_instructions": self.cleanup_instructions,
            "notes": self.notes,
            "summary": self.summary.to_dict(),
        }


def _iter_work_packages(repo_root: Path, mission_slug: str) -> Iterable[WorkPackage]:
    """Iterate over work packages, supporting both legacy and new formats.

    Legacy format: WP files in tasks/{lane}/ subdirectories
    New format: WP files in flat tasks/ directory with lane in frontmatter
    """
    mission_path = get_mission_dir(repo_root, mission_slug, main_repo=False)
    tasks_dir = mission_path / "tasks"
    if not tasks_dir.exists():
        raise AcceptanceError(f"Mission '{mission_slug}' has no tasks directory at {tasks_dir}.")

    use_legacy = is_legacy_format(mission_path)

    if use_legacy:
        # Legacy format: iterate over lane subdirectories
        for lane_dir in sorted(tasks_dir.iterdir()):
            if not lane_dir.is_dir():
                continue
            lane = lane_dir.name
            if lane not in LANES:
                continue
            for path in sorted(lane_dir.rglob("*.md")):
                text = _read_text_strict(path)
                front, body, padding = split_frontmatter(text)
                relative = path.relative_to(lane_dir)
                yield WorkPackage(
                    mission_slug=mission_slug,
                    path=path,
                    current_lane=lane,
                    relative_subpath=relative,
                    frontmatter=front,
                    body=body,
                    padding=padding,
                )
    else:
        # New format: flat tasks/ directory, lane from frontmatter
        for path in sorted(tasks_dir.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            text = _read_text_strict(path)
            front, body, padding = split_frontmatter(text)
            try:
                lane = get_lane_from_frontmatter(path, warn_on_missing=False)
            except CanonicalStatusNotFoundError:
                lane = "planned"
            relative = path.relative_to(tasks_dir)
            yield WorkPackage(
                mission_slug=mission_slug,
                path=path,
                current_lane=lane,
                relative_subpath=relative,
                frontmatter=front,
                body=body,
                padding=padding,
            )


def detect_mission_slug(
    repo_root: Path,
    *,
    explicit_mission: str | None = None,
    env: Mapping[str, str] | None = None,  # noqa: ARG001 -- kept for signature compat
    cwd: Path | None = None,  # noqa: ARG001 -- kept for signature compat
    announce_fallback: bool = True,  # noqa: ARG001 -- kept for signature compat
) -> str:
    """Require an explicit mission slug; no auto-detection.

    Args:
        repo_root: Repository root path (unused — kept for signature compatibility)
        explicit_mission: Mission slug to use (required).
        env: Unused; kept for backward-compatible call sites.
        cwd: Unused; kept for backward-compatible call sites.
        announce_fallback: Unused; kept for backward-compatible call sites.

    Returns:
        Mission slug (e.g., "020-my-mission")

    Raises:
        AcceptanceError: If no explicit mission slug is provided.
    """
    try:
        return _require_explicit_mission(explicit_mission, command_hint="--mission <slug>")
    except ValueError as e:
        raise AcceptanceError(str(e)) from e


def detect_feature_slug(
    repo_root: Path,
    *,
    explicit_feature: str | None = None,
    env: Mapping[str, str] | None = None,
    cwd: Path | None = None,
    announce_fallback: bool = True,
) -> str:
    """Compatibility alias for legacy callers renamed to mission terminology."""
    return detect_mission_slug(
        repo_root,
        explicit_mission=explicit_feature,
        env=env,
        cwd=cwd,
        announce_fallback=announce_fallback,
    )


def _read_text_strict(path: Path) -> str:
    """Read a file as UTF-8, raising ArtifactEncodingError on decode failure."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ArtifactEncodingError(path, exc) from exc


def _read_file(path: Path) -> str:
    return _read_text_strict(path) if path.exists() else ""


def _find_unchecked_tasks(tasks_file: Path) -> list[str]:
    if not tasks_file.exists():
        return ["tasks.md missing"]

    unchecked: list[str] = []
    for line in _read_text_strict(tasks_file).splitlines():
        if re.match(r"^\s*-\s*\[ \]", line):
            unchecked.append(line.strip())
    return unchecked


def _check_needs_clarification(files: Sequence[Path]) -> list[str]:
    results: list[str] = []
    for file_path in files:
        if file_path.exists():
            text = _read_text_strict(file_path)
            if "[NEEDS CLARIFICATION" in text:
                results.append(str(file_path))
    return results


def _missing_artifacts(mission_dir: Path) -> tuple[list[str], list[str]]:
    required = [mission_dir / "spec.md", mission_dir / "plan.md", mission_dir / "tasks.md"]
    optional = [
        mission_dir / "quickstart.md",
        mission_dir / "data-model.md",
        mission_dir / "research.md",
        mission_dir / "contracts",
    ]
    missing_required = [str(p.relative_to(mission_dir)) for p in required if not p.exists()]
    missing_optional = [str(p.relative_to(mission_dir)) for p in optional if not p.exists()]
    return missing_required, missing_optional


def normalize_mission_encoding(repo_root: Path, mission_slug: str) -> list[Path]:
    """Normalize file encoding from Windows-1252 to UTF-8 with ASCII character mapping.

    Converts Windows-1252 encoded files to UTF-8, replacing Unicode smart quotes
    and special characters with ASCII equivalents for maximum compatibility.
    """
    # Map Unicode characters to ASCII equivalents
    NORMALIZE_MAP = {
        "\u2018": "'",  # Left single quotation mark -> apostrophe
        "\u2019": "'",  # Right single quotation mark -> apostrophe
        "\u201a": "'",  # Single low-9 quotation mark -> apostrophe
        "\u201c": '"',  # Left double quotation mark -> straight quote
        "\u201d": '"',  # Right double quotation mark -> straight quote
        "\u201e": '"',  # Double low-9 quotation mark -> straight quote
        "\u2014": "--",  # Em dash -> double hyphen
        "\u2013": "-",  # En dash -> hyphen
        "\u2026": "...",  # Horizontal ellipsis -> three dots
        "\u00a0": " ",  # Non-breaking space -> regular space
        "\u2022": "*",  # Bullet -> asterisk
        "\u00b7": "*",  # Middle dot -> asterisk
    }

    mission_dir = get_mission_dir(repo_root, mission_slug, main_repo=False)
    if not mission_dir.exists():
        return []

    candidates: list[Path] = []
    primary_files = [
        mission_dir / "spec.md",
        mission_dir / "plan.md",
        mission_dir / "quickstart.md",
        mission_dir / "tasks.md",
        mission_dir / "research.md",
        mission_dir / "data-model.md",
    ]
    candidates.extend(p for p in primary_files if p.exists())

    for subdir in [mission_dir / "tasks", mission_dir / "research", mission_dir / "checklists"]:
        if subdir.exists():
            candidates.extend(path for path in subdir.rglob("*.md"))

    rewritten: list[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        if path in seen or not path.exists():
            continue
        seen.add(path)
        data = path.read_bytes()
        try:
            data.decode("utf-8")
            continue
        except UnicodeDecodeError:
            pass

        text: str | None = None
        for encoding in ("cp1252", "latin-1"):
            try:
                text = data.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        if text is None:
            text = data.decode("utf-8", errors="replace")

        # Strip UTF-8 BOM if present in the text
        text = text.lstrip("\ufeff")

        # Normalize Unicode characters to ASCII equivalents
        for unicode_char, ascii_replacement in NORMALIZE_MAP.items():
            text = text.replace(unicode_char, ascii_replacement)

        path.write_text(text, encoding="utf-8")
        rewritten.append(path)

    return rewritten


def normalize_feature_encoding(repo_root: Path, mission_slug: str) -> list[Path]:
    """Compatibility alias for legacy callers renamed to mission terminology."""
    return normalize_mission_encoding(repo_root, mission_slug)


def collect_mission_summary(
    repo_root: Path,
    mission_slug: str,
    *,
    strict_metadata: bool = True,
) -> AcceptanceSummary:
    mission_dir = get_mission_dir(repo_root, mission_slug, main_repo=False)
    tasks_dir = mission_dir / "tasks"
    if not mission_dir.exists():
        raise AcceptanceError(f"Mission directory not found: {mission_dir}")

    branch: str | None = None
    try:
        branch_value = run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root, check=True).stdout.strip()
        if branch_value and branch_value != "HEAD":
            branch = branch_value
    except TaskCliError:
        branch = None

    try:
        worktree_root = Path(
            run_git(["rev-parse", "--show-toplevel"], cwd=repo_root, check=True).stdout.strip()
        ).resolve()
    except TaskCliError:
        worktree_root = repo_root

    try:
        git_common_dir = Path(
            run_git(["rev-parse", "--git-common-dir"], cwd=repo_root, check=True).stdout.strip()
        ).resolve()
        primary_repo_root = git_common_dir.parent
    except TaskCliError:
        primary_repo_root = repo_root

    # Capture git cleanliness before any status inspection. Query paths must
    # not rewrite derived files like status.json.
    try:
        git_dirty = git_status_lines(repo_root)
    except TaskCliError:
        git_dirty = []

    lanes: dict[str, list[str]] = {lane: [] for lane in LANES}
    work_packages: list[WorkPackageState] = []
    metadata_issues: list[str] = []
    activity_issues: list[str] = []

    is_legacy_format(mission_dir)

    # ── Canonical state validation via reducer-only snapshot ──────────────
    events_path = mission_dir / EVENTS_FILENAME
    use_legacy_lane_fallback = not events_path.exists()
    if not events_path.exists():
        activity_issues.append(f"No canonical state found for mission '{mission_slug}': missing {EVENTS_FILENAME}.")
        snapshot_wps: dict[str, dict[str, str | None]] = {}
    else:
        try:
            from specify_cli.status.reducer import reduce
            from specify_cli.status.store import read_events

            snapshot = reduce(read_events(mission_dir))
        except StoreError as exc:
            raise AcceptanceError(f"Status event log is corrupted for mission '{mission_slug}': {exc}") from exc
        snapshot_wps = snapshot.work_packages
        if not snapshot_wps:
            activity_issues.append(f"No canonical state found for mission '{mission_slug}' in {EVENTS_FILENAME}.")
            use_legacy_lane_fallback = True

    # Collect WP IDs from task files
    expected_wp_ids: list[str] = []
    for wp in _iter_work_packages(repo_root, mission_slug):
        wp_id = wp.work_package_id or wp.path.stem
        title = (wp.title or "").strip('"')
        expected_wp_ids.append(wp_id)

        # Check canonical state for this WP
        wp_snapshot = snapshot_wps.get(wp_id)
        canonical_lane = wp_snapshot.get("lane") if wp_snapshot else None
        has_lane_entry = canonical_lane is not None
        latest_lane = canonical_lane

        if use_legacy_lane_fallback:
            bucket_lane = wp.current_lane or "planned"
            latest_lane = bucket_lane
            has_lane_entry = True
        else:
            # Use canonical lane for bucketing when the event log exists.
            bucket_lane = canonical_lane if canonical_lane is not None else "planned"
        if bucket_lane in lanes:
            lanes[bucket_lane].append(wp_id)
        else:
            lanes["planned"].append(wp_id)

        metadata: dict[str, str | None] = {
            "lane": canonical_lane,
            "agent": wp.agent.to_compact() if wp.agent else None,
            "assignee": wp.assignee,
            "shell_pid": wp.shell_pid,
        }

        if strict_metadata:
            if not wp.agent:
                metadata_issues.append(f"{wp_id}: missing agent in frontmatter")
            lane_for_validation = bucket_lane
            if lane_for_validation in {"doing", "in_progress", "for_review"} and not wp.assignee:
                metadata_issues.append(f"{wp_id}: missing assignee in frontmatter")
            if not wp.shell_pid:
                metadata_issues.append(f"{wp_id}: missing shell_pid in frontmatter")

        work_packages.append(
            WorkPackageState(
                work_package_id=wp_id,
                lane=bucket_lane,
                title=title,
                path=str(wp.path.relative_to(repo_root)),
                has_lane_entry=has_lane_entry,
                latest_lane=latest_lane,
                metadata=metadata,
            )
        )

    # Validate canonical state for all WPs (only if event log exists and has events)
    # WPs must be in 'approved' or 'done' — acceptance transitions approved → done.
    if events_path.exists() and snapshot_wps and not use_legacy_lane_fallback:
        for wp_id in expected_wp_ids:
            wp_snapshot = snapshot_wps.get(wp_id)
            if wp_snapshot is None:
                activity_issues.append(f"{wp_id}: no canonical state found in status.events.jsonl")
            elif wp_snapshot.get("lane") not in {"approved", "done"}:
                activity_issues.append(
                    f"{wp_id}: canonical lane is '{wp_snapshot.get('lane')}', "
                    f"expected 'approved' or 'done'"
                )

    unchecked_tasks = _find_unchecked_tasks(mission_dir / "tasks.md")
    needs_clarification = _check_needs_clarification(
        [
            mission_dir / "spec.md",
            mission_dir / "plan.md",
            mission_dir / "quickstart.md",
            mission_dir / "tasks.md",
            mission_dir / "research.md",
            mission_dir / "data-model.md",
        ]
    )
    missing_required, missing_optional = _missing_artifacts(mission_dir)

    path_violations: list[str] = []
    try:
        mission = get_mission_for_mission_dir(mission_dir)
    except MissionError:
        mission = None

    if mission and mission.config.paths:
        try:
            validate_mission_paths(mission, repo_root, strict=True)
        except PathValidationError as exc:
            message = exc.result.format_errors() or str(exc)
            path_violations.append(message)

    warnings: list[str] = []
    if missing_optional:
        warnings.append("Optional artifacts missing: " + ", ".join(missing_optional))
    if path_violations:
        warnings.append("Path conventions not satisfied.")

    # Lane-based acceptance gates
    try:
        from specify_cli.lanes.persistence import read_lanes_json
        lanes_manifest = read_lanes_json(feature_dir)
    except Exception:
        lanes_manifest = None

    if lanes_manifest is not None:
        # Gate: must be on mission branch
        if branch and branch != lanes_manifest.mission_branch:
            activity_issues.append(
                f"Acceptance must run on mission branch {lanes_manifest.mission_branch}, "
                f"not {branch}"
            )

        # Gate: acceptance matrix must exist when lanes.json exists
        from specify_cli.acceptance_matrix import (
            enforce_negative_invariants,
            read_acceptance_matrix,
            validate_matrix_evidence,
            write_acceptance_matrix,
        )
        acc_matrix = read_acceptance_matrix(feature_dir)
        if acc_matrix is None:
            activity_issues.append(
                "Acceptance matrix (acceptance-matrix.json) is required for "
                "lane-based features but was not found"
            )
        else:
            # Run negative invariant enforcement (not just read stored verdict)
            if acc_matrix.negative_invariants:
                acc_matrix.negative_invariants = enforce_negative_invariants(
                    repo_root, acc_matrix.negative_invariants,
                )
                write_acceptance_matrix(feature_dir, acc_matrix)

            # Validate evidence completeness
            evidence_errors = validate_matrix_evidence(acc_matrix)
            for err in evidence_errors:
                activity_issues.append(f"Evidence: {err}")

            # Block on fail or pending
            verdict = acc_matrix.overall_verdict
            if verdict == "fail":
                activity_issues.append(
                    "Acceptance matrix verdict is 'fail' — "
                    "negative invariants or criteria not satisfied"
                )
            elif verdict == "pending":
                activity_issues.append(
                    "Acceptance matrix verdict is 'pending' — "
                    "criteria or invariants have not been verified"
                )

    return AcceptanceSummary(
        mission_slug=mission_slug,
        repo_root=repo_root,
        mission_dir=mission_dir,
        tasks_dir=tasks_dir,
        branch=branch,
        worktree_root=worktree_root,
        primary_repo_root=primary_repo_root,
        lanes=lanes,
        work_packages=work_packages,
        metadata_issues=metadata_issues,
        activity_issues=activity_issues,
        unchecked_tasks=unchecked_tasks if unchecked_tasks != ["tasks.md missing"] else [],
        needs_clarification=needs_clarification,
        missing_artifacts=missing_required,
        optional_missing=missing_optional,
        git_dirty=git_dirty,
        path_violations=path_violations,
        warnings=warnings,
    )


def collect_feature_summary(
    repo_root: Path,
    mission_slug: str,
    *,
    strict_metadata: bool = True,
) -> AcceptanceSummary:
    """Compatibility alias for legacy callers renamed to mission terminology."""
    return collect_mission_summary(
        repo_root,
        mission_slug,
        strict_metadata=strict_metadata,
    )


def choose_mode(preference: str | None, repo_root: Path) -> AcceptanceMode:
    if preference in {"pr", "local", "checklist"}:
        return preference
    try:
        remotes = run_git(["remote"], cwd=repo_root, check=False).stdout.strip().splitlines()
        if remotes:
            return "pr"
    except TaskCliError:
        pass
    return "local"


def perform_acceptance(
    summary: AcceptanceSummary,
    *,
    mode: AcceptanceMode,
    actor: str | None,
    tests: Sequence[str] | None = None,
    auto_commit: bool | None = None,
) -> AcceptanceResult:
    # Resolve auto_commit: explicit value wins, then project config, then default True
    if auto_commit is None:
        auto_commit = get_auto_commit_default(summary.repo_root)

    if mode != "checklist" and not summary.ok:
        raise AcceptanceError("Acceptance checks failed; run verify to see outstanding issues.")

    actor_name = (actor or os.getenv("USER") or os.getenv("USERNAME") or "system").strip()
    timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    parent_commit: str | None = None
    accept_commit: str | None = None

    if auto_commit and mode != "checklist":
        try:
            parent_commit = run_git(["rev-parse", "HEAD"], cwd=summary.repo_root, check=False).stdout.strip() or None
        except TaskCliError:
            parent_commit = None

        record_acceptance(
            summary.mission_dir,
            accepted_by=actor_name,
            mode=mode,
            from_commit=parent_commit,
            accept_commit=None,
        )

        meta_path = summary.mission_dir / "meta.json"
        run_git(
            ["add", str(meta_path.relative_to(summary.repo_root))],
            cwd=summary.repo_root,
            check=True,
        )

        status = run_git(["diff", "--cached", "--name-only"], cwd=summary.repo_root, check=True)
        staged_files = [line.strip() for line in status.stdout.splitlines() if line.strip()]
        commit_created = False
        if staged_files:
            commit_msg = f"Accept {summary.mission_slug}"
            run_git(["commit", "-m", commit_msg], cwd=summary.repo_root, check=True)
            commit_created = True
            try:
                accept_commit = run_git(["rev-parse", "HEAD"], cwd=summary.repo_root, check=True).stdout.strip()
            except TaskCliError:
                accept_commit = None
            # Persist commit SHA to meta.json
            if accept_commit:
                _meta = load_meta(summary.mission_dir)
                if _meta is not None:
                    _meta["accept_commit"] = accept_commit
                    _history = _meta.get("acceptance_history", [])
                    if _history:
                        _history[-1]["accept_commit"] = accept_commit
                    write_meta(summary.mission_dir, _meta)
        else:
            commit_created = False
    else:
        commit_created = False

    instructions: list[str] = []
    cleanup_instructions: list[str] = []

    branch = summary.branch or summary.mission_slug

    # Determine whether `branch` is the integration/target branch itself.
    # If so, merge and branch-deletion guidance is nonsensical and dangerous
    # (e.g. "git merge main" or "git branch -d main" when already on main).
    _WELL_KNOWN_INTEGRATION_BRANCHES = frozenset(
        {
            "main",
            "master",
            "develop",
            "development",
            "2.x",
            "3.x",
        }
    )
    _meta = load_meta(summary.mission_dir)
    _target_branch = (_meta or {}).get("target_branch")
    _is_integration_branch = branch == _target_branch or (
        _target_branch is None and branch in _WELL_KNOWN_INTEGRATION_BRANCHES
    )

    if mode == "pr":
        if _is_integration_branch:
            instructions.append(
                f"Acceptance recorded on integration branch `{branch}`. Push and open a pull request if needed."
            )
        else:
            instructions.extend(
                [
                    f"Review the acceptance commit on branch `{branch}`.",
                    f"Push your branch: `git push origin {branch}`",
                    "Open a pull request referencing spec/plan/tasks artifacts.",
                    "Include acceptance summary and test evidence in the PR description.",
                ]
            )
    elif mode == "local":
        if _is_integration_branch:
            instructions.append(f"Acceptance recorded directly on `{branch}`. No merge needed.")
        else:
            instructions.extend(
                [
                    "Switch to your integration branch (e.g., `git checkout main`).",
                    "Synchronize it (e.g., `git pull --ff-only`).",
                    f"Merge the mission branch: `git merge {branch}`",
                ]
            )
    else:  # checklist
        instructions.append("All checks passed. Proceed with your manual acceptance workflow.")

    if summary.worktree_root != summary.primary_repo_root:
        cleanup_instructions.append(
            f"After merging, remove the worktree: `git worktree remove {summary.worktree_root}`"
        )
    if not _is_integration_branch:
        cleanup_instructions.append(f"Delete the mission branch when done: `git branch -d {branch}`")

    notes: list[str] = []
    if accept_commit:
        notes.append(f"Acceptance commit: {accept_commit}")
    if parent_commit:
        notes.append(f"Accepted from parent commit: {parent_commit}")
    if tests:
        notes.append("Validation commands:")
        notes.extend(f"  - {cmd}" for cmd in tests)

    return AcceptanceResult(
        summary=summary,
        mode=mode,
        accepted_at=timestamp,
        accepted_by=actor_name,
        parent_commit=parent_commit,
        accept_commit=accept_commit,
        commit_created=commit_created,
        instructions=instructions,
        cleanup_instructions=cleanup_instructions,
        notes=notes,
    )


__all__ = [
    "AcceptanceError",
    "AcceptanceMode",
    "AcceptanceResult",
    "AcceptanceSummary",
    "ArtifactEncodingError",
    "WorkPackageState",
    "choose_mode",
    "collect_feature_summary",
    "collect_mission_summary",
    "detect_feature_slug",
    "detect_mission_slug",
    "normalize_feature_encoding",
    "normalize_mission_encoding",
    "perform_acceptance",
]
