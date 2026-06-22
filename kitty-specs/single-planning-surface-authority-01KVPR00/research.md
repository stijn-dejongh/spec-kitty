# Research: Single planning-surface authority + worktree repair

Phase 0 decisions. The design was pre-decided by a 3-agent live-evidence squad
(architect-alphonso / paula-patterns / debugger-debbie); this records the decisions,
rationale, and alternatives considered.

## D-1 — Adopt the existing write authority; do NOT build a new resolver
- **Decision**: Route every planning-artifact commit + status-event emission through
  `resolve_placement_only` (`src/mission_runtime/resolution.py:761`).
- **Rationale**: The write-authority SSOT already exists and is documented "byte-identical
  to what the full resolver assembles." #1716 is **non-adoption** by sibling commands — the
  same structural class the #2065 read-side mission already solved by adoption, not rewrite.
- **Alternatives considered**: (a) a new unified write resolver — rejected (C-003: a second
  resolver is exactly the split-brain pattern); (b) per-command point-patches — rejected
  (re-introduces the divergence the next command hits).

## D-2 — `_resolve_existing_for_slug` gates coord-preference on declared coordination
- **Decision**: Thread a `declares_coordination` signal (primary `meta.json`
  `coordination_branch` presence) so `CoordState.MATERIALIZED` is necessary-but-not-
  sufficient. A flattened mission never prefers an orphaned coord worktree.
- **Rationale**: Live repro (debbie) shows the read-path leg returns STALE-COORD for
  composed/bare-mid8/ULID handles on a flattened mission, while the surface + aggregate
  legs already gate on `coordination_branch is None → primary`. The read-path leg trusts
  on-disk existence alone; that is the divergence.
- **Alternatives considered**: (a) auto-prune the orphaned worktree on read — rejected
  (a read authority mutating topology is surprising; that is the `worktree repair` verb's
  job, D-4); (b) flatten always removes the coord worktree — good hygiene but does not make
  the resolver safe against a *pre-existing* orphan, so the gate is still required.

## D-3 — Differential gate gains a `flattened-stale-coord` topology row
- **Decision**: Add `flattened-stale-coord` (primary meta has NO `coordination_branch` +
  stale `-coord` worktree on disk) × every handle form to
  `tests/missions/test_surface_resolution_equivalence.py`, asserting all legs → PRIMARY,
  without weakening `type(a) is type(b)` AND `error_code`.
- **Rationale**: The gate is the convergence safety net but under-feeds topologies — this
  is the exact case #2062 hits and the same under-feeding class as the #2065 bare-mid8
  BLOCKER. A green gate that never feeds the broken topology is a partial proof.

## D-4 — One `agent worktree repair` (recreate-or-prune) verb
- **Decision**: Register `spec-kitty agent worktree repair --mission <slug>` forwarding to
  `CoordinationWorkspace.resolve()` — recreate a *missing* coord worktree, prune an
  *orphaned* one. Repoint each recovery hint to the command that fixes its failure class.
- **Rationale**: #1890 needs RECREATE; #2062 needs ORPHAN-PRUNE — two halves of one missing
  verb. `doctor workspaces --fix` is husk-only (removes `.worktrees/` entries lacking a
  `.git`); a pure repoint would point operators at a no-op (worse than "command not found").
- **Alternatives considered**: (a) pure string repoint to `doctor workspaces --fix` —
  rejected (factually wrong for coord-missing/sparse classes); (b) keep the string and only
  add an alias — partial; the recreate capability must actually exist.

## D-5 — Command-reference guard scans Python literals + ADRs, self-tested
- **Decision**: New architectural guard scanning `src/specify_cli/**/*.py` literals +
  `architecture/**/*.md` for `spec-kitty <tokens>` invocations vs registered Typer
  commands (reuse `_build_live_app`/registered-path machinery in
  `test_docs_cli_reference_parity.py`), with a planted-phantom self-test.
- **Rationale**: The existing guard only scans doctrine markdown bash-fences — it is blind
  to Python string literals + ADRs, which is exactly why the #1890 phantom survived #2008.
- **Gate-unmask discipline (NFR-003)**: the guard catches offenders only after it lands;
  pair with a full-suite dry-run + the self-test proving it FAILS on a planted literal
  before relying on it. Never ship a mission-diff-scoped assertion to main.

## D-6 — `is_committed` collapse is gated, not eager
- **Decision**: Collapse the 3-leg OR to a single-surface check (FR-011) ONLY after the
  write authority is singular (D-1) AND the IC-01 safety net + a live flattened-mission
  repro are green (NFR-001).
- **Rationale**: The 3-leg OR is a load-bearing workaround for the authority split;
  flattened/coord-fresh/legacy missions each hit a different leg. Collapsing before
  convergence is proven would regress live missions mid-flight (live-evidence rule).

## D-7 — `safe-commit` keeps its generic responsibility, loses the planning one
- **Decision**: Retire `safe-commit` from planning prompts (→ `spec-commit`); keep
  `safe-commit` for non-mission operator files (NFR-002).
- **Rationale**: `safe-commit._resolve_commit_target` is mission-blind (resolves from
  `HEAD`); overloading it with mission-awareness risks its legitimate generic use. Separate
  the two responsibilities rather than overload one command.

## Open items
- None requiring a decision marker. All scope is pre-decided; #2062 carries C-002 (no
  close without live repro) which is an acceptance constraint, not an open question.
