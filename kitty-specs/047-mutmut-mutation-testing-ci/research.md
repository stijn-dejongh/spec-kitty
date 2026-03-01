# Research: Mutmut Mutation Testing CI Integration
*Phase 0 output for [plan.md](plan.md)*

## Research Questions

1. What is the correct `pyproject.toml` configuration format for mutmut 3.x?
2. How does `mutmut export-cicd-stats` format its JSON output?
3. How should the mutation score floor be enforced (native vs. script)?
4. What is the correct sequence of mutmut commands to produce HTML + JSON reports?
5. What CI patterns already exist in `ci-quality.yml` for slow, push-only jobs?

---

## Finding 1 — mutmut 3.x pyproject.toml configuration

**Decision**: Use `[tool.mutmut]` section in `pyproject.toml`.

**Rationale**: mutmut 3.x supports configuration via `pyproject.toml` under
`[tool.mutmut]`. The 2.x setup.cfg approach (`[mutmut]`) still works but is
deprecated in favour of the standard PEP 517 approach. The project uses
`pyproject.toml` for all tooling config (ruff, mypy, pytest) so this is
consistent.

**Key settings for this project**:
```toml
[tool.mutmut]
paths_to_mutate = ["src/specify_cli/"]
runner = "python -m pytest -x --timeout=30 -q"
tests_dir = "tests/"
# Exclude generated files, migrations, and vendored code
exclude = [
    "src/specify_cli/upgrade/migrations/",
    "src/specify_cli/__pycache__/",
]
```

**Alternatives considered**:
- `setup.cfg` `[mutmut]` section — rejected (deprecated, inconsistent with project tooling style)
- Command-line flags only (no config file) — rejected (hard to reproduce locally vs. CI)

---

## Finding 2 — mutmut 3.x CLI command sequence

**Decision**: Use the following sequence to produce all required outputs.

```bash
# 1. Run mutation testing (writes to mutmut.db)
mutmut run

# 2. Export JSON stats for floor check and SonarCloud
mutmut export-cicd-stats --output out/reports/mutation/mutation-stats.json

# 3. Generate HTML report
mutmut html --output out/reports/mutation/
```

**Rationale**: `export-cicd-stats` is the standard 3.x command for machine-
readable output. `mutmut html` generates the browsable report. Both are stable
in mutmut>=3.5.0.

**mutmut exit codes**:
- `mutmut run` exits 0 when complete regardless of surviving mutants
- Surviving mutants do **not** cause a non-zero exit code by default
- Floor enforcement must be done via a separate script reading the JSON stats

**Alternatives considered**:
- `mutmut junitxml` — rejected (JUnit format less informative for mutation; HTML + JSON sufficient)
- Parsing `mutmut results` stdout — rejected (text parsing is fragile; JSON is canonical)

---

## Finding 3 — mutation-stats.json schema (mutmut export-cicd-stats)

**Decision**: Parse `killed` and `survived` fields from the JSON output.

The JSON output from `mutmut export-cicd-stats` has the following structure:

```json
{
  "summary": {
    "total": 120,
    "killed": 95,
    "survived": 18,
    "timeout": 3,
    "suspicious": 4
  },
  "mutation_score": 0.7917
}
```

`mutation_score` is `killed / (total - timeout - suspicious)` or similar
(exact formula may vary by 3.x patch). The floor check should use
`killed / (killed + survived)` as the most conservative measure to avoid
division-by-zero when all mutants time out.

**Zero-mutant edge case**: If `total == 0` (empty source scope), emit a warning
and exit 0 — no score is computable.

**Alternatives considered**:
- Using `mutation_score` directly — not used as primary because its exact
  denominator is undocumented across minor versions; recomputing from raw
  counts is more robust

---

## Finding 4 — Floor enforcement approach

**Decision**: Thin Python helper script `scripts/check_mutation_floor.py`

**Rationale**: mutmut 3.x has no built-in `--min-score` flag. Options were:

| Option | Pros | Cons |
|--------|------|------|
| Bash one-liner in CI YAML | No extra file | JSON parsing fragile in bash; hard to unit-test |
| Python helper script | Testable, readable, handles edge cases | One extra file in `scripts/` |
| Third-party wrapper (mutation-testing.io) | Rich reporting | New dependency, overkill |

The Python script is ~35 lines and handles:
- Missing/malformed JSON (fail with clear error)
- Zero-mutant case (warn + pass)
- Floor comparison with descriptive exit message
- `MUTATION_FLOOR` env var (integer 0–100, default 0)

---

## Finding 5 — Existing CI pattern for slow, push-only jobs

**Decision**: Model the new job on the existing `integration-smoke` and
`dashboard-tests` patterns already in `ci-quality.yml`.

**Pattern** (from `integration-smoke`):
```yaml
mutation-testing:
  runs-on: ubuntu-latest
  needs: unit-tests
  if: always() && (github.event_name == 'push' || (github.event_name == 'workflow_dispatch' && inputs.run_extended))
  timeout-minutes: 75
```

**Rationale**: Both `integration-smoke` and `dashboard-tests` use this exact
`if:` guard to skip on PRs while still running on push and `workflow_dispatch`.
`always()` ensures the job runs even if `unit-tests` had failures (matching
the existing pattern for parallelism). The timeout is increased to 75 min
(above the 60 min mutation run estimate) to give a safe buffer.

**Note on SonarCloud**: The `sonarcloud` job lists `mutation-testing` in its
`needs:` only if mutation reports should feed into SonarCloud. Since
SonarCloud already runs with `if: always()` and downloads existing coverage
reports, adding `mutation-testing` to `sonarcloud`'s `needs:` is optional
and deferred to FR-008 in WP02.

---

## Finding 6 — Priority squashing scope rationale

**Decision**: `status/`, `glossary/`, `merge/`, `core/` as first-campaign scope.

**Rationale**:

| Module | Why priority |
|--------|-------------|
| `status/` | 7-lane state machine; transition guards; incorrect transitions have real consequences |
| `glossary/` | Semantic integrity pipeline; wrong parsing or rendering corrupts all downstream consumers |
| `merge/` | Merge state persistence and preflight — errors here cause data loss or silent failures |
| `core/` | Core abstractions relied on by multiple subsystems |

**Deferred modules**: `cli/` (thin CLI glue, tested at integration level),
`upgrade/migrations/` (idempotent, hard to unit-test mutation independently),
`dashboard/` (UI, covered by Playwright), `missions/` (config loading, lower
correctness risk).
