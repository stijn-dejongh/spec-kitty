# Contract — Canonical `compat-planner.json` Path Resolution

> Mission: `ci-hygiene-and-sonar-debt-remediation-01KWV531`
> Closes: FR-003, FR-004 | Data model: [../data-model.md §3](../data-model.md#3-contractpathresolution-new-shared-test-fixture-ic-02)

## Contract

A single, shared resolution helper (see [research.md R2](../research.md#r2--canonical-contract-path-resolution-helper-placement-ic-02)
for placement) that both `tests/specify_cli/cli/commands/test_upgrade_command.py`
and `tests/specify_cli/compat/test_messages.py` call instead of maintaining
independent hardcoded parent-walks.

### Behavior

1. Starting from the helper's own module `__file__`, walk parent directories
   upward until one is found containing `pyproject.toml` at its top level.
   This is the repository root, regardless of whether the caller is running
   from a plain clone, a CI runner's nested work directory, or a
   `.worktrees/<name>/` checkout.
2. From that root, descend to
   `kitty-specs/cli-upgrade-nag-lazy-project-migrations-01KQ6YDN/contracts/compat-planner.json`.
3. If the resulting path exists, return it.
4. If it does not exist (or no ancestor directory contains `pyproject.toml`
   within a bounded number of hops — see Edge Cases below), **raise** with a
   message naming the paths tried. Never return `None`, never silently skip
   the caller's schema-conformance assertion.

### Edge Cases

- **No `pyproject.toml` found within, say, 10 parent hops**: raise — this
  indicates something is fundamentally wrong with the checkout (not this
  helper's job to guess further), and a loud failure is strictly better than
  the current silent no-op.
- **`pyproject.toml` exists but the `kitty-specs/...` path underneath it is
  missing** (e.g. a partial/shallow clone that excludes `kitty-specs/`):
  raise with a message distinguishing "found repo root, but the contract file
  itself is missing" from "couldn't find repo root at all" — different root
  causes, different remediation.

### Verification

- Unit test: run the helper from three simulated working directories (a
  flat clone layout, a `.worktrees/<name>/` layout, and a CI-runner-shaped
  `/home/runner/work/<repo>/<repo>` layout) and confirm all three resolve to
  the same real file.
- Regression guard: both consuming test files' schema-conformance assertions
  must be proven red-first against a deliberately-reverted contract (e.g. a
  temporarily narrowed `migration_id` pattern) before this fix, and green
  after — per DIRECTIVE_034.
