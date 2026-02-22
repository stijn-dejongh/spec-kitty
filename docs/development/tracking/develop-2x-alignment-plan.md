# Develop -> 2.x Branch Alignment Plan

**Date:** 2026-02-22
**Status:** Complete
**Branch:** `2.x` (target), `develop_reference` (archived source)

---

## Context

The `develop` branch diverged from `2.x` with 30 commits (23 unique after deduplication).
The `2.x` branch advanced 165 commits ahead of the merge base. To prevent further divergence,
we aligned develop onto 2.x by renaming the old develop to `develop_reference` and creating a
new `develop` from the current `2.x` HEAD, then selectively cherry-picking valuable changes.

**Merge base:** `2cf1ccd446aaa7ce67db27d1facadaec322185d3`

---

## Step 1: Branch Housekeeping

- [x] Rename local `develop` to `develop_reference`
- [x] Rename remote `origin/develop` to `origin/develop_reference`
- [x] Create new local `develop` from `2.x` HEAD
- [x] Push new `develop` to origin

---

## Step 2: Cherry-Pick / Extract Commits

### Feature Implementations

| Order | Hash | Message | Group | Status | Notes |
|---|---|---|---|---|---|
| 1 | `45d774ed` | feat(agent-profile): feature 047 model + terminology | A4 | [x] | Clean cherry-pick |
| 2 | `3dc89963` | feat(doctrine): selective extraction from A6+A7 | A6+A7 | [x] | 73 files extracted (specs 048-053, doctrine structure, design templates, tracking docs). Skipped telemetry, conflicting glossary/constitution changes |

### CI/Quality Infrastructure

| Order | Hash | Message | Group | Status | Notes |
|---|---|---|---|---|---|
| 3 | `18b65e9e` | ci(quality): staged test execution + commitlint fix | C1 | [x] | Resolved CI workflow conflicts (kept 2.x security scans, added doctrine test paths) |
| 4 | `b10c244a` | chore(quality): tiered domain coverage | C3 | [x] | Resolved pyproject.toml, CI, glossary conflicts |
| 5 | - | ci(quality): unit-tests if: always() | C4 | [x] | Skipped (already applied in C1 resolution) |
| 6 | - | fix(ci): skip sonarcloud on test failure | C5 | [x] | Skipped (already applied in C1 resolution) |
| 7 | - | ci(workflow): decouple tests from lint | C6 | [x] | Skipped (already applied in C1 resolution) |
| 8 | `5787a5a5` | fix(ci): test failures + deprecation warnings | C7 | [x] | Kept 2.x test files, accepted non-test changes |

### Tests & Documentation

| Order | Hash | Message | Group | Status | Notes |
|---|---|---|---|---|---|
| 9 | `91367041` | test(doctrine): behavioral tests for missions | E1 | [x] | Resolved add/add conflicts |
| 10 | `2ae01121` | docs(test): architectural context (part 1) | E2 | [x] | Clean cherry-pick |
| 11 | `440b613c` | docs(test): architectural context (part 2) | E3 | [x] | Resolved queue.py formatting conflict (kept nosec annotations) |
| 12 | - | doc(style): prefer absolute paths | E4 | [x] | Skipped (empty after glossary conflict resolution) |

### Cleanup

| Order | Hash | Message | Group | Status | Notes |
|---|---|---|---|---|---|
| 13 | `a8ca6be4` | chore: clean up stale agent-strategy remnants | F1 | [x] | Resolved init.py formatting conflicts |

### Step 3: Architecture Docs

- [x] Extract journey docs (A1b) from `d82a9db8` -> `d0c93f02`
- [x] Include journey 004 (curation governance) from A6

### Step 4: Fresh Formatting

- [x] `ruff format` -> `87969f06` (467 files reformatted)
- [x] `markdownlint --fix` -> `93ef1966` (337 files reformatted)
- [ ] mypy strict typing pass (deferred - requires code changes, not just formatting)

---

## Final Result

**12 commits** on new `develop` ahead of `2.x`:

```text
93ef1966 style: apply markdownlint auto-fix to documentation
87969f06 style: apply ruff format (Black-compatible) to entire codebase
a8ca6be4 chore(rebase): clean up stale agent-strategy remnants and lint errors
440b613c docs(test): enhance test documentation with architectural context
2ae01121 docs(test): enhance test documentation with architectural context
91367041 test(doctrine): add behavioral tests for missions package
5787a5a5 fix(ci): resolve test failures and deprecation warnings
b10c244a chore(quality): implement tiered domain coverage enforcement
18b65e9e ci(quality): split test execution into staged groups and fix commitlint
d0c93f02 docs(architecture): add journey docs and curation governance journey
3dc89963 feat(doctrine): selective extraction of governance specs, doctrine structure, and design templates
45d774ed feat(agent-profile): add feature 047 model and terminology alignment
```

**891 files changed**, +29,362 / -9,524 (vs 2.x)

---

## Skipped (with rationale)

| Commit/Group | Reason |
|---|---|
| A1a (glossary contexts) | Already on 2.x via `e5e9bd6c` |
| A1c (specs 041-046) | Conflicting numbering/content with 2.x specs |
| A2 `c7816378` (telemetry 043) | Conflicts with 2.x constitution implementation |
| A3 `aa3e4e38` (constitution 045) | Already implemented differently on 2.x |
| A5 `6052ca31` (telemetry lifecycle) | Rejected design |
| C2 `ec322583` (markdownlint/commitlint config) | Overlaps with hooks decision; bundled with doctrine git hooks |
| D1 `ecfbcc9b` (git hooks) | 2.x retired hooks via `m_2_0_0_retire_git_hooks.py` |
| A6/A7 telemetry code | Selectively excluded from extraction |
| A6/A7 glossary rewrites | Already on 2.x with different (more current) content |
| A6/A7 constitution conflicts | 2.x has its own constitution implementation |

---

## Conflict Resolution Summary

| File | Resolution |
|---|---|
| `.github/workflows/ci-quality.yml` | Merged: kept 2.x security scans + `if: always()`, added doctrine test/cov paths from develop |
| `pyproject.toml` | Merged: added test dependencies (mypy, ruff, bandit, pip-audit), skipped poetry section |
| `glossary/contexts/*.md` | Kept 2.x versions (more current) |
| `.kittify/memory/contexts/*.yml` | Removed (don't exist on 2.x) |
| `src/specify_cli/sync/queue.py` | Accepted develop formatting + nosec annotations |
| `src/specify_cli/cli/commands/init.py` | Kept 2.x multi-line formatting |
| `tests/specify_cli/constitution/test_schemas.py` | Kept 2.x version (different test structure) |
| `tests/specify_cli/test_cli/test_agent_feature.py` | Kept 2.x version (different test structure) |
