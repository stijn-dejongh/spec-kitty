---
work_package_id: WP03
title: 'Wave 2: charter_preflight package + CLI (FR-006, FR-007, FR-008)'
dependencies:
- WP02
requirement_refs:
- FR-006
- FR-007
- FR-008
- NFR-001
planning_base_branch: main
merge_target_branch: main
branch_strategy: Planning artifacts for this mission were generated on main. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into main unless the human explicitly redirects the landing branch.
subtasks:
- T015
- T016
- T017
- T018
- T019
- T020
- T021
agent: claude
history:
- by: claude
  at: '2026-05-23T13:30:00+00:00'
  action: generated
agent_profile: implementer-ivan
authoritative_surface: src/specify_cli/charter_preflight/
execution_mode: code_change
mission_id: 01KSAF14K8FZ56MHYT45EGWHHC
mission_slug: charter-ux-and-org-pack-vocabulary-01KSAF14
owned_files:
- src/specify_cli/charter_preflight/**
- tests/specify_cli/charter_preflight/**
priority: P0
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Invoke `/ad-hoc-profile-load` with argument `implementer-ivan` before reading further.

## Objective

Create a new `charter_preflight` package that introduces a `spec-kitty charter preflight` command and a callable `run_charter_preflight(...)` hook. The command consumes the WP02 freshness payload and, depending on the `--auto-refresh` flag and worktree cleanliness, either (a) reports the state, (b) runs the safe refresh sequence, or (c) blocks with an exact remediation command. Performance budget: <300 ms warm / <1.0 s cold (NFR-001).

## Branch strategy

- Planning base branch: `main`
- Merge target branch: `main`
- Execution worktree: allocated by `finalize-tasks`.

## Context

- `kitty-specs/.../spec.md` — FR-006, FR-007, FR-008
- `kitty-specs/.../contracts/charter-preflight-json.md` — full JSON shape + caller contract
- `kitty-specs/.../data-model.md` — §4 (`CharterPreflightResult` dataclass)
- WP02 owns `src/specify_cli/charter_freshness/` — this WP imports from it.
- Reference pattern: `src/specify_cli/core/git_preflight.py` (existing `run_git_preflight` is the architectural template).

## Subtask details

### T015 — DIR-012 assign #1100 to HiC

```bash
unset GITHUB_TOKEN
gh issue edit 1100 --add-assignee @stijn-dejongh --repo Priivacy-ai/spec-kitty
```

### T016 — `result.py` dataclasses

**Files**: NEW `src/specify_cli/charter_preflight/__init__.py`, `src/specify_cli/charter_preflight/result.py`

Per data-model §4:
```python
from dataclasses import dataclass, field, asdict
from typing import Literal

CheckState = Literal["fresh", "stale", "missing", "built_in_only", "invalid", "skipped"]

@dataclass(frozen=True)
class CharterPreflightCheck:
    name: str
    state: CheckState
    detail: str
    remediation: str | None

@dataclass(frozen=True)
class CharterPreflightResult:
    passed: bool
    checks: list[CharterPreflightCheck] = field(default_factory=list)
    auto_refresh_applied: bool = False
    auto_refresh_actions: list[str] = field(default_factory=list)
    blocked_reason: str | None = None

    def to_json(self) -> str: ...
    def to_dict(self) -> dict: ...
```

Export both classes plus `run_charter_preflight` from `__init__.py`.

### T017 — `runner.py` — `run_charter_preflight`

**Files**: NEW `src/specify_cli/charter_preflight/runner.py`

```python
def run_charter_preflight(
    repo_root: Path,
    *,
    auto_refresh: bool = False,
    strict: bool = False,
) -> CharterPreflightResult:
    """Compute freshness, optionally refresh, return result."""
```

Algorithm:
1. Call `compute_freshness(repo_root)` (from WP02).
2. Translate each `FreshnessSubState` into a `CharterPreflightCheck`.
3. Compute `passed = all check.state in {"fresh","skipped","built_in_only"}`.
4. If `passed` → return.
5. If `auto_refresh=True`:
   - Check uncommitted artifacts (T018). If dirty → return with `auto_refresh_applied=False`, `blocked_reason="uncommitted generated artifacts; commit or stash and retry"`.
   - Otherwise → invoke refresh sequence (T019).
6. If `auto_refresh=False` → return with `blocked_reason` derived from the first failing check's remediation.

### T018 — Uncommitted-artifact detection

**Files**: `src/specify_cli/charter_preflight/runner.py`

Per `contracts/charter-preflight-json.md` Detection mechanism section, use a single subprocess invocation:
```python
result = subprocess.run(
    ["git", "status", "--porcelain", "--", ".kittify/charter/", ".kittify/doctrine/"],
    cwd=repo_root,
    capture_output=True,
    text=True,
    timeout=5.0,
)
```

Failure modes:
- `FileNotFoundError` (git missing) → return `blocked_reason="git CLI not available; cannot determine worktree cleanliness"`.
- `result.returncode != 0` → return `blocked_reason=f"git status failed (exit {result.returncode}): {result.stderr.splitlines()[0]}"`.
- `result.stdout` non-empty → dirty; name each affected file in the relevant check's `detail`.

Detection MUST complete within 100 ms on a clean tree.

### T019 — Auto-refresh sequence

**Files**: `src/specify_cli/charter_preflight/runner.py`

Sequence (only when worktree is clean and `auto_refresh=True`):
1. `spec-kitty charter sync` (skip if `charter_source.state == "fresh"` and `synced_bundle.state == "fresh"`).
2. `spec-kitty charter synthesize` (skip if `synthesized_drg.state == "fresh"`).
3. `spec-kitty charter bundle validate` (always).

Invoke each via `subprocess.run` with `cwd=repo_root`, `timeout=30.0`. Capture the exact command in `auto_refresh_actions`. If any command exits non-zero, stop and set `blocked_reason` to the failing command's first stderr line.

### T020 — CLI surface

**Files**: NEW `src/specify_cli/charter_preflight/cli.py`, edit `src/specify_cli/cli/commands/charter.py`

Add a new typer command:
```python
@app.command("preflight")
def charter_preflight(
    json_output: bool = typer.Option(False, "--json"),
    auto_refresh: bool = typer.Option(False, "--auto-refresh"),
    strict: bool = typer.Option(False, "--strict"),
) -> None:
    """Verify charter-derived state before a governed session begins."""
    ...
```

Per `contracts/charter-preflight-json.md` exit-codes table:
- 0 = `passed=true` OR (`passed=false` AND not `--strict`)
- 1 = `passed=false` AND `--strict`
- 2 = hard error

Wire the typer command into `cli/commands/charter.py` (preserve the existing module conventions — register under the `charter_app`).

### T021 — Tests

**Files**: NEW `tests/specify_cli/charter_preflight/test_runner.py`, `test_cli.py`, `test_performance.py`

Cases:
1. Fresh repo, all checks pass → `passed=True`.
2. Missing synthesized DRG → `passed=False`, `blocked_reason` mentions synthesize.
3. Dirty worktree with `--auto-refresh` → no-op, `blocked_reason` cites uncommitted files.
4. Clean worktree with `--auto-refresh` → `auto_refresh_applied=True`, refresh commands executed in order.
5. `--strict` + non-fresh → exit 1.
6. CLI emits valid JSON with `--json`.
7. **NFR-001**: `test_performance.py` asserts `run_charter_preflight(repo_root)` on a fresh-cached repo completes in <300 ms (use `pytest-benchmark` or a simple `time.monotonic()` assertion).

Use `tmp_path` fixtures + a small helper that materialises a fake repo with charter/synthesis state.

## Definition of Done

- [ ] Issue #1100 assigned to HiC.
- [ ] `charter_preflight` package exists with three modules (`result`, `runner`, `cli`).
- [ ] `spec-kitty charter preflight --json` returns the JSON shape from the contract.
- [ ] `--auto-refresh` honours the worktree-cleanliness safety rule.
- [ ] Exit codes match the contract table.
- [ ] NFR-001 perf test passes.
- [ ] `mypy --strict` and `ruff check` pass.

## Risks

- **Subprocess timeout on slow CI**: 30 s per refresh step may not be enough on very slow runners. Mitigation: make the timeout configurable via env (`SPEC_KITTY_PREFLIGHT_TIMEOUT_SECS`, default 30).
- **Cyclic invocation**: if a user binds `charter sync` to also run preflight, we get a loop. Mitigation: the refresh sequence MUST call sync/synthesize via the underlying Python functions (not the CLI subprocess) where convenient, OR pass an env flag that prevents recursive preflight.
- **Windows subprocess**: `git status --porcelain` works the same; verify with the Windows CI matrix.

## Reviewer guidance

1. Verify the runner never panics on filesystem errors — every failure produces a `CharterPreflightResult` with a sensible `blocked_reason`.
2. Verify the NFR-001 perf test runs in CI (don't skip).
3. Confirm `--strict` exit code is honoured by callers (WP04 will test this further).
