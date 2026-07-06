# Quickstart: Validating This Mission's Fixes

A reviewer or implementer can validate each Implementation Concern
independently — none require the full mission to be complete.

## IC-01 — Census-gate ratchet migration

```bash
# Before: exact-equality reds on any unrelated LOC change
git stash  # or add ~20 lines to a tracked worklist dir, no other change
PWHEADLESS=1 uv run pytest tests/architectural/test_ci_topology_worklist.py -q

# After the fix: same diff should NOT fail the structural half,
# and only ratchet-fail/warn on the LOC half per the direction of change
PWHEADLESS=1 uv run pytest tests/architectural/test_ci_topology_worklist.py tests/architectural/test_ratchet_baselines.py -q
```

## IC-02/IC-03 — Contract-conformance tests run for real

```bash
# Confirm both files' schema-conformance checks actually execute
# (not silently skipped) from a plain, non-worktree checkout:
PWHEADLESS=1 uv run pytest \
  tests/specify_cli/cli/commands/test_upgrade_command.py::test_project_migration_needed_project_dry_run_json_contract \
  tests/specify_cli/compat/test_messages.py -k TestRenderJson \
  -q -v
# Then deliberately revert the migration_id pattern fix (#2339) and confirm
# BOTH suites now fail loudly, proving they're live, not silently skipped.
```

## IC-04 — Sonar version tracking

```bash
# Confirm the CI job now passes a real version (inspect the workflow diff,
# then wait for or manually trigger the nightly/scheduled sonarcloud job):
gh workflow run ci-quality.yml --repo Priivacy-ai/spec-kitty
# ... then query the live analysis:
curl -s "https://sonarcloud.io/api/project_analyses/search?project=Priivacy-ai_spec-kitty&ps=1" | jq '.analyses[0].projectVersion'
# Expect: a real pyproject.toml-derived version string, not "not provided"
```

## IC-05 — Coverage-scope reconciliation

```bash
# Compare Sonar's file-level coverage component tree against the internal
# diff-coverage gate's file list for the same recent PR — the research
# task's own verification step (see research.md R3).
```

## IC-06/IC-07 — Backlog slicing

```bash
scripts/ci/sonarcloud_branch_review.sh --list-open-issues  # exact flag TBD at implementation
gh issue list --repo Priivacy-ai/spec-kitty --search "label:tech-debt label:quality label:devex milestone:3.2.x" --json number | jq length
# Cross-check the sum of ticketed live_issue_count values against the live
# SonarCloud open-issue count (NFR-004's completeness check).
```

## IC-08 — Roadmap-aligned slice fixed

```bash
# Confirm zero regressions in the three touched files:
PWHEADLESS=1 uv run pytest tests/specify_cli/cli/commands/agent/ tests/specify_cli/cli/commands/test_implement*.py tests/specify_cli/acceptance/ -q
PWHEADLESS=1 uv run pytest tests/architectural/ -q
ruff check src/specify_cli/cli/commands/agent/workflow.py src/specify_cli/cli/commands/implement.py src/specify_cli/acceptance/__init__.py
uv run mypy --strict src/specify_cli/cli/commands/agent/workflow.py src/specify_cli/cli/commands/implement.py src/specify_cli/acceptance/__init__.py
```
