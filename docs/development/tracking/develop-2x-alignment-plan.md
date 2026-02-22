# Develop -> 2.x Branch Alignment Plan

**Date:** 2026-02-22
**Status:** In Progress
**Branch:** `2.x` (target), `develop` -> `develop_reference` (source)

---

## Context

The `develop` branch diverged from `2.x` with 30 commits (23 unique after deduplication).
The `2.x` branch advanced 165 commits ahead of the merge base. To prevent further divergence,
we align develop onto 2.x by renaming the old develop to `develop_reference` and creating a
new `develop` from the current `2.x` HEAD, then selectively cherry-picking valuable changes.

**Merge base:** `2cf1ccd446aaa7ce67db27d1facadaec322185d3`

---

## Step 1: Branch Housekeeping

- [ ] Rename local `develop` to `develop_reference`
- [ ] Rename remote `origin/develop` to `origin/develop_reference`
- [ ] Create new local `develop` from `2.x` HEAD
- [ ] Push new `develop` to origin

---

## Step 2: Cherry-Pick Commits (14 commits, in dependency order)

### Feature Implementations

| Order | Hash | Message | Group | Status |
|---|---|---|---|---|
| 1 | `2247ff8e` | feat(agent-profile): feature 047 model + terminology | A4 | [ ] |
| 2 | `20ec1756` | feat(doctrine): governance layer + feature 053 | A6 | [ ] |
| 3 | `80cde0e9` | feat(doctrine): template ownership consolidation | A7 | [ ] |

### CI/Quality Infrastructure

| Order | Hash | Message | Group | Status |
|---|---|---|---|---|
| 4 | `d922de51` | ci(quality): staged test execution + commitlint fix | C1 | [ ] |
| 5 | `73449358` | chore(quality): tiered domain coverage | C3 | [ ] |
| 6 | `c0be4e86` | ci(quality): unit-tests if: always() | C4 | [ ] |
| 7 | `5c7a0259` | fix(ci): skip sonarcloud on test failure | C5 | [ ] |
| 8 | `741dbe26` | ci(workflow): decouple tests from lint | C6 | [ ] |
| 9 | `7badf6fe` | fix(ci): test failures + deprecation warnings | C7 | [ ] |

### Tests & Documentation

| Order | Hash | Message | Group | Status |
|---|---|---|---|---|
| 10 | `b8036582` | test(doctrine): behavioral tests for missions | E1 | [ ] |
| 11 | `93cc2e6a` | docs(test): architectural context (part 1) | E2 | [ ] |
| 12 | `af46fcb6` | docs(test): architectural context (part 2) | E3 | [ ] |
| 13 | `3877cf89` | doc(style): prefer absolute paths | E4 | [ ] |

### Cleanup

| Order | Hash | Message | Group | Status |
|---|---|---|---|---|
| 14 | `8fbaca2b` | chore: clean up stale agent-strategy remnants | F1 | [ ] |

---

## Step 3: Partial Extraction from A1

- [ ] Extract architecture journey docs (A1b) from `d82a9db8`:
  - `architecture/journeys/README.md`
  - `architecture/journeys/001-project-onboarding-bootstrap.md`
  - `architecture/journeys/002-system-architecture-design.md`
  - `architecture/journeys/003-system-design-and-shared-understanding.md`
- [ ] Extract design templates (A1d) from `d82a9db8`:
  - `architecture/design/templates/stakeholder-persona-template.md`
  - `architecture/design/templates/user-journey-template.md`

---

## Step 4: Reapply Fresh (separate commits, NOT cherry-pick)

- [ ] Run `ruff format` on 2.x codebase
- [ ] Run `markdownlint --fix` on 2.x codebase
- [ ] Run mypy strict typing pass on 2.x codebase

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
| B1-B3 (formatting/typing) | Reapply fresh instead of cherry-pick (Step 4) |

---

## Risk Notes

- A6 (`20ec1756`, +15,627 lines) is the largest cherry-pick. Expect conflicts in `src/doctrine/` and agent template directories.
- A7 depends on A6 content. Must cherry-pick in order.
- C1 modifies `ci-quality.yml` which already exists on 2.x. Manual conflict resolution likely needed.
- C7 fixes test names and schemas that may differ between branches. Verify applicability.
