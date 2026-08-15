---
work_package_id: WP07
title: AGENTS.md stale-line fix + guard
dependencies: []
requirement_refs:
- FR-003
- NFR-002
- NFR-005
merge_target_branch: kitty/mission-workflow-self-doc
subtasks:
- T015
- T016
owned_files:
- AGENTS.md
authoritative_surface: AGENTS.md
create_intent:
- tests/architectural/test_workspace_resolution_doc.py
execution_mode: code_change
---

## Objective
Delete the phantom `lanes.json`-absent `-WP##` fallback at `AGENTS.md:307`; pin the fix with a guard. Standalone fast lane (repo-root, no rollup regen).

## Subtasks
- **T015** Correct `AGENTS.md` line ~307: the stale ``- `lanes.json` absent → legacy: `.worktrees/<feature>-WP##``` is FALSE — `resolve_workspace_for_wp` (`src/specify_cli/workspace/context.py:738`) → `require_lanes_json` raises `MissingLanesError` (`lanes/persistence.py`) with no fallback. State the real contract: flat/`SINGLE_BRANCH`/`LANES` still require `lanes.json`. (`CLAUDE.md` is a symlink → `AGENTS.md`; one edit fixes both.)
- **T016** New `tests/architectural/test_workspace_resolution_doc.py`: assert the stale phrase (`.worktrees/<feature>-WP##` OR `absent → legacy`) is ABSENT from `AGENTS.md`, AND the corrected statement (e.g. `lanes.json` + `MissingLanesError` / "require lanes.json") is PRESENT. Do NOT ban the bare `WP##` token — it appears legitimately at :305/:315 (`spec-kitty implement WP##`). `pytestmark` matching sibling arch tests.

## Rules
Verify the resolver against code (C-005). Run the new guard + terminology. `.venv/bin/python`, never bare `uv run`.

## Done
Stale claim gone; guard green; bare `WP##` usages preserved.
