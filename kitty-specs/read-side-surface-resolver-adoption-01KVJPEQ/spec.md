# Mission Specification: Read-Side Surface-Resolver Adoption

**Mission slug**: `read-side-surface-resolver-adoption-01KVJPEQ`
**Mission type**: software-dev (consolidation / desync closeout — read-side)
**Target / merge branch**: `feat/read-side-surface-resolver-adoption` → `main` (via PR). **STACKED on 01KVGCE8 / PR #2045** — branched off `pr/single-mission-surface-resolver`; rebase onto `main` once 01KVGCE8 lands.
**Status**: Draft
**Source**: GitHub #2046 (child of epic #2007; follow-on to mission 01KVGCE8, surfaced by its post-merge adversarial squad — architect-alphonso + patterns-paula)

## Purpose

Mission 01KVGCE8 made `coordination/surface_resolver.resolve_status_surface_with_anchor`
the canonical surface-**selection** authority — but only for the write/status path. The
**operator read CLIs** (`agent tasks status`, `agent context`, `agent mission`, `decision`,
`acceptance`) still call the lower primitive `resolve_mission_read_path` directly and each
**hand-rolls a pre-resolver primary-`meta.json` bootstrap**
(`repo_root / KITTY_SPECS_DIR / raw_handle` → `load_meta` → `mission_id` → `resolve_mid8`).
For a **bare-slug** handle against a **coord-topology** mission this bootstrap is mid8-blind
(`resolve_mid8(slug, mission_id=None)` → `""`), so the read silently resolves the **primary
checkout** — the stale split-brain surface the desync epic (#2007) exists to kill. The audit
also found these joins are **un-guarded** (no `assert_safe_path_segment`), a path-traversal-adjacent
hardening gap.

This mission **adopts the canonical resolver across every read command** behind ONE guarded seam,
closing the read-side residual (the four `coord-*/bare` strict-xfail cells in 01KVGCE8's
equivalence matrix flip green) and adds a **selection-authority guard** so the bypass class
cannot recur.

## User Scenarios & Testing

**Primary actor:** an operator (or agent) running a read command that locates a mission's
on-disk surface — `spec-kitty agent tasks status <handle>`, `agent context`, `agent mission`,
`decision`, `acceptance`.

**Primary scenario (the residual to close):** an operator runs a read command with a **bare slug**
(no `-<mid8>` tail) against a mission that has a coordination worktree. Today the command silently
reads the **primary** checkout (a stale, possibly split-brain surface). After this mission, the read
command resolves the **same** surface as the write/status path (the coordination worktree, or a
coherent hard-fail) — identical to `<slug>-<mid8>` and full-`mission_id` handles.

**Exception / edge cases:**
- **Create→first-write window** (coordination branch declared, worktree not yet materialized) →
  the read MUST still resolve **PRIMARY** (the #1718 contract). The fix derives mid8 from the
  primary-anchored meta WITHOUT routing a blind read through the coord-aware surface.
- **Ambiguous handle** → the single seam raises `MISSION_AMBIGUOUS_SELECTOR` (no silent pick),
  preserved through the `mission_runtime` boundary (the 01KVGCE8 FR-005 behavior).
- A **new callsite** invokes `resolve_mission_read_path` directly (mid8-blind) outside the
  canonical-seam set → fails CI (the selection-authority guard).
- An attacker-controlled `raw_handle` containing path-traversal segments → rejected by the
  seam's `assert_safe_path_segment` before any path join.

## Domain Language

| Canonical term | Meaning | Avoid |
|----------------|---------|-------|
| read-side surface resolution | locating a mission's authoritative on-disk surface from a handle, for a READ command | "path resolution" (conflates write/validation) |
| `resolve_handle_to_read_path` | the single guarded seam: handle → (validated, mid8-derived) read path via the canonical resolver | "the bootstrap" (the duplicated thing being removed) |
| pre-resolver bootstrap | the hand-rolled `KITTY_SPECS_DIR/raw_handle`→`load_meta`→`mid8` block being eliminated | — |
| selection-authority guard | the CI guard binding surface-SELECTION (not just path-shape) to the canonical seam | — |

## Requirements

### Functional Requirements

> **Defect framing (squad-corrected):** the disease is **bespoke mid8 cascades that feed `resolve_mission_read_path` (or compose a read surface) OUTSIDE one seam** — NOT merely raw `KITTY_SPECS_DIR/<handle>` path-joins. Some sites (`tasks.py:4047` blind `resolve_mid8(slug, mission_id=None)`; `acceptance.py` own cascade) have NO raw join yet carry the defect; a raw-join-only measure is fakeable. The audit confirms **6+ parallel cascades**; only `orchestrator_api/_resolve_mission_dir` is already correct (the reference prototype).

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | A **single `resolve_handle_to_read_path(repo_root, handle)` seam** in `src/specify_cli/missions/_read_path_resolver.py` (the blessed path-constructor home) MUST be the one entry point converting an operator handle to a read-side surface path: **guarded** segment validation (FR-004) → primary-`meta.json` probe → `resolve_declared_mid8` derivation → route through `resolve_mission_read_path` (the worktree-existence-gated primitive). It MUST be **lifted from the working prototype `orchestrator_api/commands.py:_resolve_mission_dir` (lines ~285-347)** — including its fail-closed coord-declared topology gate — NOT re-invented from the mid8-blind CLI bootstraps. | Draft |
| FR-002 | **Every read path that derives mid8 to reach a mission surface MUST consume FR-001's seam** — eliminating the bespoke-cascade defect, not just raw joins. The audited residual targets (raw-join read-CLI bootstraps): `context.py:72`, `mission.py:1327`, `mission.py:1378`, `decision.py:464` (**four** — FR-007 must match). The additional bespoke-cascade sites surfaced by the squad: `workflow.py:302-324` (`_mid8_for_mission_read_path`, 3 read callers), `mission_runtime/resolution.py:_mid8_from_primary_meta`, and `runtime_bridge.py:2431-2450` (`_resolve_runtime_feature_dir`) — see C-007 for the runtime carve-out decision. Sites already `routed-through-resolver` (`tasks.py`, `acceptance.py`, `orchestrator_api`) are **re-pointed to the named seam only if its signature changes**, NOT bootstrap-removal targets. | Draft |
| FR-003 | **Bare-slug coord resolution (primitive leg)**: the bare-slug `read_path` mid8-derivation MUST be fixed so the **two** cells whose ONLY divergence is read_path mid8-blindness — `coord-fresh/bare` and `coord-behind/bare` in 01KVGCE8's `tests/missions/test_surface_resolution_equivalence.py` — flip strict-xfail → GREEN. The diff to that test MUST be limited to **removing those two `xfail` markers**; any edit to `_assert_equivalent`, `_observe`, the `Outcome` shape, or the `_MATRIX` builders VOIDS the proof. (`coord-empty/bare` + `coord-deleted/bare` carry a SECOND, out-of-scope aggregate divergence — see FR-008.) | Draft |
| FR-004 | **Guarded composition**: the FR-001 seam MUST validate the handle with `assert_safe_path_segment` (`core/paths.py:40`) BEFORE any `KITTY_SPECS_DIR` join — closing the audit-found **un-guarded** path-traversal-adjacent gap at `context.py:72`/`mission.py:1327/1378`/`decision.py:464` (none pre-validate today). | Draft |
| FR-005 | **Create-window preserved (binding invariant)**: the seam MUST route through `resolve_mission_read_path` (worktree-existence-gated), **NEVER** `resolve_status_surface_with_anchor` (coord-composing). A coordination-branch-DECLARED-but-UNMATERIALIZED mission still resolves PRIMARY for reads even when mid8 is non-empty (the create-window→primary decision is gated on coord-worktree existence on disk, NOT mid8 presence — verified). Proven by `tests/specify_cli/missions/test_read_path_resolver_transitional.py` AND the matrix `test_create_first_write_window_resolves_primary` cell **both staying green with assertions unchanged**, plus a mutation that routes a declared-unmaterialized coord through the surface → both FAIL. | Draft |
| FR-006 | **Selection-authority guard — TWO halves (do NOT over-claim AST):** (a) a `tests/architectural/` **AST callsite ratchet** (extending the 01KVGCE8 `surface_resolution_audit` machinery, C-002) MUST fail when a NEW direct `resolve_mission_read_path` call OR a NEW bespoke `resolve_mid8(slug, …)`/`KITTY_SPECS_DIR/<handle>` mid8-cascade is introduced in a read path OUTSIDE the seam allowlist; (b) a **seam runtime fail-closed gate** MUST raise on an empty-mid8 selection against a declared coord (mirroring `_resolve_mission_dir:336`), tested by mutation. Proven load-bearing by TWO mutations on TWO axes: a new bypass call FAILS the ratchet; reverting PASSES; and the ratchet PASSES on the adopted tree but **would have FAILED on the pre-mission tree** (it actually discriminates). Reusing the existing raw-path-JOIN guard alone does NOT satisfy FR-006. | Draft |
| FR-007 | **Residual allowlist drains BY FIX, not by blinding**: the **four** read-CLI residual entries (`context.py:72`, `mission.py:1327`, `mission.py:1378`, `decision.py:464`) MUST drain from 01KVGCE8's `_ALLOWLISTED_RAW_JOINS` **because `discover_rows()` re-discovers zero raw-join rows there after the seam replaces the inline joins** — with `audit.py`'s `SLUG_NAMES ⊇ {mission_slug, feature_slug, slug, raw_handle, handle}` UNCHANGED (or only widened). A diff that removes `raw_handle`/`handle` from `SLUG_NAMES`, narrows the net, or edits `discover_rows()` VOIDS FR-007. (Reconciles the prior "three"; `decision.py:464` is the 4th.) | Draft |
| FR-008 | **Aggregate-seam cells stay out of scope (scope-honesty)**: `coord-empty/bare`, `coord-deleted/bare`, and the two `*/slug-mid8` aggregate cells MUST NOT be claimed fully green by this mission — they carry the WP04 `CoordAuthorityUnavailable` error-type divergence (this spec's Out of Scope). For the two `*/bare` cells, the seam fix flips their READ_PATH leg; their `xfail` reason MUST be **narrowed** from `_XFAIL_READPATH_MID8_OUT_OF_SCOPE` to a reason naming only the *remaining* aggregate divergence (proving the read leg was fixed without faking the aggregate convergence). | Draft |
| FR-007 | The three read-CLI sites currently allowlisted in 01KVGCE8's surface-resolution audit/guard as "un-guarded read-side residual (#2046)" MUST be **removed from the residual allowlist** once routed through the guarded seam (the allowlist drains to zero residual entries — the SC proof that #2046 is closed). | Draft |

### Non-Functional Requirements

| ID | Requirement | Threshold / Measure | Status |
|----|-------------|---------------------|--------|
| NFR-001 | New/changed code passes the quality gates. | `ruff` + `mypy --strict` 0 errors on changed files; no new `# noqa`/`# type: ignore`; complexity ≤ 15. | Draft |
| NFR-002 | No regression for non-bare-slug handles or the happy path. | 100% of pre-existing read-CLI + status/context/mission/decision/acceptance suites pass unchanged; the `<slug>-<mid8>` and full-`mission_id` handle classes are unaffected. | Draft |
| NFR-003 | Behavior-equivalence is provable. | The `coord-fresh/bare` + `coord-behind/bare` cells are GREEN (xfail markers removed, assertions unchanged) AND a per-read-CLI end-to-end test exercises the bare-slug coord path; each guard/fix carries a mutation-killing test. | Draft |
| NFR-004 | The seam is the single read-side entry point — **rename-resistant**. | Exactly one `resolve_handle_to_read_path` definition; `discover_rows()` (with `SLUG_NAMES` unchanged-or-widened) finds zero raw-join bootstraps in the read CLIs; AND an audit assertion forbids any surviving `load_meta(repo_root / KITTY_SPECS_DIR / <any-var>)` two-line shape (catches a bootstrap renamed off the slug-token net). | Draft |

### Constraints

| ID | Constraint | Status |
|----|------------|--------|
| C-001 | STACKED on 01KVGCE8 (PR #2045): consumes the canonical `resolve_status_surface_with_anchor` + `resolve_declared_mid8` + the equivalence matrix + the `surface_resolution_audit`/guard. MUST rebase onto `main` once 01KVGCE8 lands; **after rebase, re-verify the four `_ALLOWLISTED_RAW_JOINS` keys and the four `*/bare` xfail rows still exist before draining/flipping** (they shift if 01KVGCE8 is revised). | Draft |
| C-002 | Reuse + **extend** the 01KVGCE8 audit/guard scaffolding (`tests/architectural/surface_resolution_audit/`, the load-bearing guard) for FR-006 — do NOT fork new tooling, but the AST ratchet MUST add a NEW selection-callsite discriminator (the existing raw-JOIN guard alone is insufficient). | Draft |
| C-003 | Migrate, don't wrap: route the read paths THROUGH the seam; MUST NOT add a new parallel read resolver (the #1993 / #1868 risk). | Draft |
| C-004 | MUST NOT regress the #1718 create→first-write window (FR-005) — gate the FR-003 work on `test_read_path_resolver_transitional.py` + the matrix create-window cell staying green (assertions unchanged). | Draft |
| C-005 | MUST NOT prescribe a version/patch number (focus/milestone framing; PO assigns at release). | Draft |
| C-006 | Cite related artifacts/findings by canonical id/issue number. | Draft |
| C-007 | **Runtime-bridge carve-out decision (squad F-2):** `runtime/next/runtime_bridge.py:2431-2450` has its own mid8 cascade but lives behind the Shared-Package-Boundary (`runtime/next` must not import the `specify_cli` seam). Plan MUST decide explicitly: fold it in (if the seam can live at a boundary-safe location) OR carve it out in Out of Scope with the package-boundary rationale — NO silent omission. | Draft |

## Success Criteria

- **SC-001 (primitive leg)**: `coord-fresh/bare` and `coord-behind/bare` flip strict-xfail → GREEN, with the `test_surface_resolution_equivalence.py` diff limited to removing those two `xfail` markers (no edit to `_assert_equivalent`/`_observe`/`Outcome`/`_MATRIX`). `coord-empty/bare` + `coord-deleted/bare` are NOT claimed green (FR-008); their xfail reasons are narrowed to the remaining aggregate divergence.
- **SC-002 (CLI end-to-end — the proof the matrix CANNOT give)**: a per-read-CLI test drives `agent context`/`agent mission`/`decision`/`acceptance` with a **bare slug against a coord-fresh mission** and asserts the resolved dir equals the **coordination-worktree** dir (NOT primary), using a production-shaped 26-char ULID mission_id. (The equivalence matrix tests resolver primitives, never a CLI — without this, SC-001 is satisfiable with zero CLI change.)
- **SC-003 (seam single + rename-resistant)**: exactly one `resolve_handle_to_read_path`; `discover_rows()` (SLUG_NAMES unchanged-or-widened) finds zero read-CLI bootstraps; the `load_meta(KITTY_SPECS_DIR/<any-var>)`-shape assertion finds none.
- **SC-004 (selection-authority guard — two axes)**: (a) inject a NEW direct `resolve_mission_read_path(...)` (or bespoke `resolve_mid8`) call into a read CLI outside the seam → the AST ratchet FAILS; revert → PASSES; (b) the ratchet PASSES on the adopted tree but **would have FAILED on the pre-mission tree** (it discriminates); (c) the seam's runtime empty-mid8-against-declared-coord gate raises (mutation-verified).
- **SC-005 (create-window preserved)**: `test_read_path_resolver_transitional.py` + the matrix create-window cell both stay GREEN with assertions unchanged; a mutation routing a declared-unmaterialized coord through the surface makes both FAIL.
- **SC-006 (residual drains by FIX)**: the **four** read-CLI residual entries drain from `_ALLOWLISTED_RAW_JOINS` because `discover_rows()` (SLUG_NAMES retaining `{raw_handle, handle}`) re-discovers zero raw joins there; a re-injected `KITTY_SPECS_DIR/raw_handle` join into a read CLI on the adopted tree makes the guard FAIL (proving the net was not silently narrowed).

## Key Entities

- **`resolve_handle_to_read_path` seam** — the single guarded handle→read-path entry point in `_read_path_resolver.py`.
- **`orchestrator_api/commands.py:_resolve_mission_dir` (≈285-347)** — the **working reference prototype**: read primary meta → `resolve_declared_mid8` → fail-closed coord-declared gate → `resolve_mission_read_path`. The seam is lifted from here.
- **Read paths to adopt** — `context.py`, `mission.py` (×2), `decision.py` (raw-join residual); `workflow.py:_mid8_for_mission_read_path`, `mission_runtime/resolution.py:_mid8_from_primary_meta`, `runtime_bridge.py:_resolve_runtime_feature_dir` (bespoke cascades; runtime per C-007). Already-routed: `tasks.py`, `acceptance.py`, `orchestrator_api`.
- **`resolve_declared_mid8`** — `surface_resolver.py:453`, the primary-meta mid8 derivation the seam consumes.
- **Selection-authority guard** — the extended `surface_resolution_audit` AST ratchet + the seam's runtime empty-mid8 gate.

## Findings / Issue Matrix (seed — expanded by the adjacent-issues squad at plan)

| Issue | Role | Verdict |
|-------|------|---------|
| #2046 | Driver (this mission brief — read-side desync residual) | in-mission |
| #2007 | Parent epic (read/write desync) — the READ side closed by this mission | in-mission |
| #1868 | Canonical seams "exist in name only" — FR-006 selection-authority guard binds read selection to the seam | in-mission |
| #1993 | Extraction-without-adoption shadow-path risk — C-003 routes through, no new parallel resolver | in-mission |
| #1718 | Create→first-write window — FR-005 must NOT regress it | in-mission |

## Assumptions

- 01KVGCE8 (PR #2045) lands before this mission's implementation; its `resolve_declared_mid8`
  cascade + equivalence matrix + audit/guard are the foundation. If 01KVGCE8 is revised in review,
  rebase this mission's planning artifacts.
- The bare-slug→coord resolution is achievable by deriving mid8 from the primary-anchored meta
  (the topology-blind anchor 01KVGCE8 established) — NOT by routing a blind read through the
  coord-aware surface (which would regress #1718).
- The read CLIs are terminal operator commands; consolidating their bootstrap behind one seam is
  behavior-preserving for non-bare-slug handles.

## Out of Scope

- The WRITE/status path (already canonical via 01KVGCE8).
- Any version/patch-number assignment (C-005).
- New topology states or SaaS-side surface authority.
- The aggregate-seam `CoordAuthorityUnavailable` error-type convergence (the two `*/slug-mid8`
  cells AND the aggregate leg of `coord-empty/bare` + `coord-deleted/bare`) — a separate WP04
  public-contract concern (FR-008), NOT the read-CLI residual. **Scope-honesty note:** this mission
  closes **#2007's READ side** (the four `*/bare` read_path mid8-blindness cells); the aggregate
  error-type convergence (2 cells) remains the named follow-on. A still-RED aggregate cell after
  this mission is NOT incomplete #2046 work.

## Tidy-First Inputs (for /plan — boy-scout squad)

Behavior-preserving cleanups that de-risk the read-side adoption. **Sequence (squad F-5):**
extract the seam (T1) → migrate the read paths (T2) → derive-mid8 + flip cells by
*post-migration re-derivation* (T3), NOT literal line-number edits → guard (T4) → drain by
re-running `discover_rows()` on the migrated tree (T5). After rebase onto landed 01KVGCE8/main,
re-verify the allowlist keys + xfail rows BEFORE draining/flipping (C-001).

- **T1 (FR-001)** — extract `resolve_handle_to_read_path` into `_read_path_resolver.py`, **lifted from
  the working `orchestrator_api/_resolve_mission_dir` prototype** (NOT from the mid8-blind CLI
  bootstraps). Guard the segment (FR-004). Reuse the orchestrator's fail-closed coord-declared gate.
- **T2 (FR-002)** — migrate the read paths to the seam: the four raw-join residuals
  (`context.py:72`, `mission.py:1327/1378`, `decision.py:464`) + the bespoke cascades
  (`workflow.py:302-324`, `mission_runtime/resolution.py:_mid8_from_primary_meta`;
  `runtime_bridge.py` per the C-007 decision). Re-point already-routed `tasks.py`/`acceptance.py`/
  `orchestrator_api` only if the seam signature changes.
- **T3 (FR-003/FR-005/FR-008)** — seam derives mid8 from primary meta so coord is reached, routing
  through `resolve_mission_read_path` (worktree-existence-gated), NEVER the surface; flip
  `coord-fresh/bare` + `coord-behind/bare` green (remove exactly those 2 xfail marks); narrow the
  `coord-empty/bare` + `coord-deleted/bare` reasons to the remaining aggregate divergence.
- **T4 (FR-006)** — extend the `surface_resolution_audit` AST machinery with a selection-callsite
  ratchet (new direct `resolve_mission_read_path`/bespoke-`resolve_mid8` calls fail) + the seam's
  runtime empty-mid8 gate. Two-axis mutation + pre/post-tree discrimination.
- **T5 (FR-007)** — drain the FOUR read-CLI residual entries by re-derivation (SLUG_NAMES retains
  `{raw_handle, handle}`); re-injection mutation proves the net was not narrowed.
