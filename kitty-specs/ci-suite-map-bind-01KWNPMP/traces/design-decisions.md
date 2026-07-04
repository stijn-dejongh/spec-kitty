# Design Decisions

> Capture the rationale that would otherwise evaporate.

**Prompting questions**
- What decision was made?
- What alternatives were considered?
- What was the rationale — why this option over the others?

---

## Entries

<!-- YYYY-MM-DD — Decision: [what]. Alternatives: [what else]. Rationale: [why this one]. -->

- 2026-07-04 — SEED (backfilled same-day). Planning-time decisions live in spec.md's **Adjudicated Decisions 1–8** (single canonical authority — not duplicated here): parsed-model CI-validated invariants over generator; 3-state marker model with unit/contract hard-ineligible; residual job over 11k-dup unit-or-contract job; HiC 7a ready_for_review trigger; HiC 7b output-derived catch-all via the run_all OR-seam; Decision 8 two-authority rule; FR-011 blocking-needs-only scope with C-005; FR-012 narrowed to non-ci-quality workflows. Entries below are IMPLEMENT-time decisions only.
- 2026-07-04 — Decision: WP02 script is stricter than the letter of the prompt — phantom group in `job_groups` → exit 2; release-required job absent from `needs` → exit 2. Alternatives: silently ignore unknown refs (bash parity). Rationale: the phantom/unreachable-reference class IS this mission's disease (FR-003/FR-004); reviewer endorsed as Decision-8 drift protection, not scope creep.
- 2026-07-04 — Decision: WP02's Decision-8 guard is a NEGATIVE source scan (test asserts the script contains no `fast-tests-`/`integration-tests-`/`e2e-cross-cutting` fragments; only sanctioned constant is `quarantine-visibility`). Alternatives: assert an expected job→group table (positive literal pin). Rationale: refactor-stable arch-test standing rule — negative invariants survive cleanups; positive literal mirrors are the anti-pattern this repo keeps paying for.
- 2026-07-04 — Decision: WP02 tests drive `main()` in-process over stdin JSON (no subprocess). Alternatives: subprocess CLI tests. Rationale: preserves the `fast` marker semantics (no process-spawn latency) while still exercising the full contract (exit codes, stdout table, stderr diagnostics).
- 2026-07-04 — Decision: exit-code contract 0=pass / 1=fail / 2=contract-violation-or-C-005 — and WP03's wiring must treat 2 as hard failure, never soft. Alternatives: collapse to 0/1. Rationale: a C-005 tripwire or malformed input must be distinguishable from an honest red so workflow debugging doesn't misread structural drift as test failure.
- 2026-07-04 — Decision: issue-matrix rows for census-cited prior PRs (#2294/#2319) use reference-only `verified-already-fixed` entries. Alternatives: widen the gate's scan exclusions (code change out of mission scope). Rationale: cheap, honest, keeps the approve gate green without touching guard code mid-mission; matches the existing #2109/#2047 row pattern.
- 2026-07-04 — Decision: WP01 exposes 5 formerly-private parse helpers as public names (`parse_pytest_invocation`, `path_matches`, `substitute_matrix`, `join_continuations`, `strip_to_command`) clearing 9 SLF001s, and the module is READ-ONLY for the rest of the mission. Alternatives: keep private + suppress. Rationale: downstream WPs (03/04) consume these seams; public naming is the honest contract and the campsite list mandated it (real fix over suppression).
- 2026-07-04 — Decision (WP01, discovered): treat YAML 1.1's `on:` → boolean-True key explicitly in the workflow model (`_on_section` takes `dict[Any, Any]`). Rationale: real mypy catch — PyYAML parses bare `on` as `True`, and pretending the key is `str` hides it. Also: pytest 9.0.3's `Expression.compile` raises plain `SyntaxError` (ParseError removed) — WP04's loud-fail fixtures must expect that.
