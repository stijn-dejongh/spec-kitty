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

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | A **single `resolve_handle_to_read_path(repo_root, handle)` seam** MUST be the one entry point that converts an operator handle to a read-side surface path: it performs the **guarded** primary-meta probe + mid8 derivation (consuming 01KVGCE8's `resolve_declared_mid8` cascade) and routes through the canonical resolver. No read command may hand-roll the bootstrap. | Draft |
| FR-002 | **Every** read CLI MUST consume FR-001's seam: `agent tasks status` (`tasks.py`), `agent context` (`context.py`), `agent mission` (`mission.py`, both sites), `decision` (`decision.py`), `acceptance` (`acceptance.py`), and any `orchestrator_api` read path. After this mission, **zero** hand-rolled `repo_root / KITTY_SPECS_DIR / raw_handle` bootstraps remain in the read CLIs. | Draft |
| FR-003 | **Bare-slug coord resolution**: a bare-slug handle against a coord-topology mission MUST resolve the SAME surface (or the SAME typed error) as the write/status path. The four `coord-*/bare` cells in 01KVGCE8's `tests/missions/test_surface_resolution_equivalence.py` MUST flip from strict-xfail to GREEN (read_path agrees with surface/aggregate). | Draft |
| FR-004 | **Guarded composition**: the FR-001 seam MUST validate the handle with `assert_safe_path_segment` (or the canonical grammar seam) BEFORE any `KITTY_SPECS_DIR` path join — closing the audit-found un-guarded path-traversal-adjacent gap at the three read-CLI sites. | Draft |
| FR-005 | **Create-window preserved**: the seam MUST NOT regress the #1718 create→first-write contract — a coordination-branch-declared-but-unmaterialized mission still resolves PRIMARY for reads. A blind route-through the coord-aware surface is forbidden. | Draft |
| FR-006 | **Selection-authority guard**: a `tests/architectural/` guard MUST fail when a NEW direct `resolve_mission_read_path` call (or an empty-mid8 selection that bypasses the seam) is introduced outside the canonical-seam allowlist — so the #1868 "second selection path in parallel" regression class cannot recur. Proven load-bearing by a real-code mutation. | Draft |
| FR-007 | The three read-CLI sites currently allowlisted in 01KVGCE8's surface-resolution audit/guard as "un-guarded read-side residual (#2046)" MUST be **removed from the residual allowlist** once routed through the guarded seam (the allowlist drains to zero residual entries — the SC proof that #2046 is closed). | Draft |

### Non-Functional Requirements

| ID | Requirement | Threshold / Measure | Status |
|----|-------------|---------------------|--------|
| NFR-001 | New/changed code passes the quality gates. | `ruff` + `mypy --strict` 0 errors on changed files; no new `# noqa`/`# type: ignore`; complexity ≤ 15. | Draft |
| NFR-002 | No regression for non-bare-slug handles or the happy path. | 100% of pre-existing read-CLI + status/context/mission/decision/acceptance suites pass unchanged; the `<slug>-<mid8>` and full-`mission_id` handle classes are unaffected. | Draft |
| NFR-003 | Behavior-equivalence is provable. | The four `coord-*/bare` equivalence cells are GREEN (xfail markers removed) AND a per-read-CLI test exercises the bare-slug coord path; each guard/fix carries a mutation-killing test. | Draft |
| NFR-004 | The seam is the single read-side entry point. | A grep/audit shows exactly one `resolve_handle_to_read_path` definition and zero hand-rolled bootstraps in the read CLIs. | Draft |

### Constraints

| ID | Constraint | Status |
|----|------------|--------|
| C-001 | STACKED on 01KVGCE8 (PR #2045): this mission consumes the canonical `resolve_status_surface_with_anchor` + `resolve_declared_mid8` cascade + the equivalence matrix + the `surface_resolution_audit`/guard. MUST rebase onto `main` once 01KVGCE8 lands. | Draft |
| C-002 | Reuse the 01KVGCE8 audit/guard scaffolding (`tests/architectural/surface_resolution_audit/`, the load-bearing guard) — do NOT fork new tooling for FR-006. | Draft |
| C-003 | Migrate, don't wrap: route the read CLIs THROUGH the seam; MUST NOT add a new parallel read resolver (the #1993 / #1868 risk). | Draft |
| C-004 | MUST NOT regress the #1718 create→first-write window (FR-005) — gate the bare-slug fix on the create-window test staying green. | Draft |
| C-005 | MUST NOT prescribe a version/patch number (focus/milestone framing; PO assigns at release). | Draft |
| C-006 | Cite related artifacts/findings by canonical id/issue number. | Draft |

## Success Criteria

- **SC-001**: The four `coord-*/bare` equivalence-matrix cells (`coord-fresh/bare`, `coord-behind/bare`, `coord-empty/bare`, `coord-deleted/*`) are GREEN — read_path agrees with surface/aggregate; the strict-xfail markers are removed.
- **SC-002**: Exactly one `resolve_handle_to_read_path` seam; zero hand-rolled `KITTY_SPECS_DIR/raw_handle` bootstraps remain in the read CLIs (audit-verified).
- **SC-003**: The selection-authority guard FAILS (mutation-verified) when a new direct `resolve_mission_read_path` call is introduced outside the allowlist; passes on the adopted tree.
- **SC-004**: The #1718 create→first-write window still resolves PRIMARY for reads (mutation-verified, distinct cell).
- **SC-005**: The three read-CLI residual entries are removed from the 01KVGCE8 surface-resolution audit allowlist (residual drains to zero) — the auditable proof #2046 is closed.
- **SC-006**: A bare-slug operator read against a coord mission resolves the coord surface end-to-end (per-CLI test), and the handle is rejected on a traversal segment (FR-004).

## Key Entities

- **`resolve_handle_to_read_path` seam** — the single guarded handle→read-path entry point.
- **Read CLIs** — `tasks status`, `context`, `mission`, `decision`, `acceptance` (+ orchestrator_api reads).
- **`resolve_declared_mid8` cascade** — 01KVGCE8's primary-meta mid8 derivation the seam consumes.
- **Selection-authority guard** — the new `tests/architectural/` ratchet binding selection to the seam.

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
- The aggregate-seam `CoordAuthorityUnavailable` error-type convergence (the 2 `*/slug-mid8`
  aggregate cells — a separate WP04 public-contract concern, not the read-CLI residual).

## Tidy-First Inputs (for /plan — boy-scout squad)

Behavior-preserving cleanups that de-risk the read-CLI adoption. The plan should sequence the
seam extraction (FR-001) BEFORE the per-CLI migration (FR-002), gate the bare-slug fix (FR-003)
on the create-window test (FR-005/C-004), and reuse the audit/guard for FR-006/FR-007.

- **T1 (FR-001)** — extract `resolve_handle_to_read_path` from the duplicated bootstrap at
  `decision.py:464` / `context.py:72` / `mission.py:1327` (the canonical of the three; the
  others become call-throughs). Guard the segment (FR-004).
- **T2 (FR-002)** — migrate each read CLI to the seam; `mission.py:1378` `.is_dir()` probe and
  `tasks.py`/`acceptance.py`/orchestrator_api reads included.
- **T3 (FR-003/FR-005)** — make the seam derive mid8 for a bare slug from primary meta so coord
  is reached, WITHOUT touching the create-window primary path; flip the four `coord-*/bare`
  equivalence cells green (remove their xfail markers — coordinate with 01KVGCE8's matrix).
- **T4 (FR-006)** — add the selection-authority guard (reuse `surface_resolution_audit` machinery).
- **T5 (FR-007)** — drain the three read-CLI residual entries from the 01KVGCE8 audit allowlist.
