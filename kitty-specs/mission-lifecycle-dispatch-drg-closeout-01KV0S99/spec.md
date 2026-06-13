# Mission Specification — Mission lifecycle, dispatch & DRG closeout

**Mission type:** software-dev · **Branch (planning = merge target):** `feat/mission-lifecycle-dispatch-drg-closeout` (PR-bound; lands on `upstream/main`).

## Intent

Three residuals surfaced by the mission-#133 post-merge audit are tracked but unclosed because each has a delivered portion plus an unfinished tail. This mission finishes the tails so the tickets close honestly:

- **#1802 (epic) — post-mission lifecycle:** pre-mission ingestion shipped (#687, #1220 closed); the **post-mission follow-through** half has no command surface — there is no first-class way to record follow-up commits/PRs against a merged mission, nor to re-open a merged mission for residual work. Operator decision (discovery): **deliver** that surface.
- **#1804 (epic) — ops execution layer:** substantially delivered (governed `do`/`ask`/`advise`, git-tracked Op records, open/close lifecycle). Blocked from closing only by child **#1810** (collapse the trio into a single `spec-kitty dispatch`). Operator decision: **implement** the collapse with back-compat aliases.
- **#1863 — DRG curation:** the extractor reference-walk shipped (#133 WP08); ~26 orphan nodes remain, incl. a confirmed stale `java-conventions.styleguide.yaml` → `java-implementer` reference. Operator decision: **fix the stale ref + mechanically-clear orphans, document the rest** as an accepted residual.

The mission's success is defined as **#1863, #1802, and #1804 reaching honest closure.**

## User Scenarios & Testing

- **Post-mission follow-up (#1802):** A maintainer whose mission already merged discovers a follow-up fix. They invoke the post-mission follow-up surface to record the follow-up as a first-class, traceable artifact (follow-up commit/PR linked to the original mission) **without** re-running the full mission lifecycle. Success: the follow-up is attributed to the original mission and visible in mission status/history.
- **Mission re-open (#1802):** A maintainer needs to resume a merged mission for a residual slice. They re-open it through the lifecycle surface; the mission returns to an actionable state with its identity and history intact. Success: re-opening is explicit, recorded, and reversible — never a silent state edit.
- **Unified dispatch (#1810/#1804):** An operator runs `spec-kitty dispatch --profile <p> "<request>"` and gets the same governed Op behavior previously split across `do`/`ask`/`advise`. Running the legacy `spec-kitty do/ask/advise` still works unchanged (delegating to dispatch). Success: identical governed-Op outcome via either surface; no break to in-flight governed workflows.
- **DRG curation (#1863):** A doctrine maintainer regenerates the graph; the orphan count is the documented residual (not 26), the `java-implementer` stale reference is gone, and any remaining orphans are explicitly listed with a rationale. Success: deterministic regen, reduced+documented orphan set, freshness test green.

### Edge cases

- Re-opening a mission whose branch/worktree was deleted post-merge must fail closed with a structured error + remediation, never a silent partial state.
- `dispatch` invoked with a legacy alias must record the same Op identity/lifecycle as the canonical command (no divergent telemetry).
- A DRG orphan that references a genuinely-absent artifact must be either repaired (author/point-to a real artifact) or pruned with a recorded reason — never left dangling silently.

## Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | **#1802 post-merge follow-up surface:** a first-class command path to record follow-up work (commit/PR) against an already-merged mission, attributed to the original `mission_id` and surfaced in mission status/history. | draft |
| FR-002 | **#1802 mission re-open:** an explicit, recorded, reversible path to return a merged/closed mission to an actionable lifecycle state, preserving `mission_id` and history; fail-closed when the mission's worktree/branch is unrecoverable. | draft |
| FR-003 | **#1802 closure:** either #1802's full epic scope is delivered by FR-001/FR-002, or the residual (if any beyond the delivered surface) is split into a fresh scoped child ticket so #1802 closes honestly. | draft |
| FR-004 | **#1810 single dispatch mechanism (desired end-state):** ONE governed-invocation mechanism (profile resolution, Op open/close, governed context, record) — `do`/`ask`/`advise` stop being three parallel implementations and become thin entry points over the single `dispatch` mechanism. The consolidation is at the *mechanism* layer, not just a CLI rename. | draft |
| FR-005 | **#1810 CLI aliases retained as first-class UX (BINDING):** `spec-kitty do`, `ask`, and `advise` remain as sensible, supported CLI entry points (the verbs carry useful intent/UX signal) — they are NOT deprecated, they delegate to the one mechanism and record identical Op identity/lifecycle. `spec-kitty dispatch` is the canonical mechanism name; the three verbs are kept aliases by deliberate UX choice. No breaking change to existing governed workflows or scripts. | draft |
| FR-006 | **#1810 propagation:** the `dispatch` command + alias surfaces propagate to all configured agents' command/skill copies via the canonical migration path (not hand-edited copies), keeping the 19-agent surfaces and the command-skills manifest consistent. | draft |
| FR-007 | **#1804 closure:** with #1810 delivered (FR-004/005/006), epic #1804 closes; any remaining ops-layer children that are genuine refinements (not gaps) are noted as out-of-scope follow-ups. | draft |
| FR-008 | **#1863 stale-ref + mechanical orphan repair:** fix the `java-conventions.styleguide.yaml` → `java-implementer` stale reference (repaint to a real profile or prune), and resolve every mechanically-clear orphan (typo/path/casing/retired-id) among the ~26. | draft |
| FR-009 | **#1863 deterministic regen + documented residual:** regenerate `graph.yaml` deterministically; drive orphan count to the documented minimum; list any residual orphans that need genuine doctrine authoring with a per-orphan rationale (and a follow-up ticket if non-empty), then close #1863. | draft |

## Non-Functional Requirements

- **NFR-001:** behavior-preserving for the alias surfaces — `do/ask/advise` outputs, exit codes, JSON envelopes, and Op records are byte/contract-identical before vs after the collapse (pinned by tests).
- **NFR-002:** new/touched code passes ruff + mypy `--strict` with zero new issues/suppressions; terminology canon enforced (`spec-kitty dispatch`, Mission, no forbidden terms).
- **NFR-003:** `graph.yaml` regeneration is deterministic and no-op-stable (re-running on an unchanged tree leaves it byte-identical) — consistent with umbrella #1914.
- **NFR-004:** fail-closed over silent fallback for the lifecycle surfaces (re-open / follow-up resolve through declared authorities — `mission_id`, git registry — never a name-derived guess).
- **NFR-005:** every closed ticket (#1863/#1802/#1804) carries pinning regression coverage for the behavior that closes it.

## Constraints

- **C-001:** runs on `feat/mission-lifecycle-dispatch-drg-closeout` (off `upstream/main`); PR-bound.
- **C-002 (BINDING):** the dispatch collapse must NOT break the governed-Op surface this very workflow depends on — `spec-kitty do --profile … ` must keep working throughout. Aliases land in the same change as the unified command; never a window where the trio is broken.
- **C-003:** #1863's residual must be *documented* (listed orphans + rationale), never silently accepted; if non-empty, a curation follow-up ticket is filed before closing #1863.
- **C-004:** the `dispatch` propagation edits SOURCE templates / migration only (per repo doctrine), never the generated agent copies directly.
- **C-005:** out of scope (do not fold): the no-op-stability remediation (PR #1913 / #1914), #1916 (ensure_identity relocation), #1907 (dev-tooling), and the API-surface epic #1010.

## Success Criteria

- **SC-1:** **#1810 closed** — `spec-kitty dispatch` ships; `do/ask/advise` aliases behave identically (NFR-001 pins); 19-agent + skills surfaces consistent.
- **SC-2:** **#1804 closed** — its blocking child #1810 delivered; epic verified substantially-complete.
- **SC-3:** **#1802 closed** — post-merge follow-up + mission re-open surfaces delivered (or residual honestly split into a child); pre-mission half already shipped.
- **SC-4:** **#1863 closed** — `java-implementer` stale ref resolved; orphan count reduced to the documented residual; graph regen deterministic + freshness-green.
- **SC-5:** full architectural + affected suites green; no regression to the governed-Op flow or existing mission lifecycle.

## Domain Language

- **Dispatch** — the single governed-invocation *mechanism* (`spec-kitty dispatch` is its canonical command). `do`/`ask`/`advise` are retained CLI aliases over that one mechanism — kept as first-class UX (the verbs carry intent), not deprecated.
- **Post-mission follow-through** — first-class follow-up work (commit/PR) recorded against an already-merged mission, distinct from re-running the mission.
- **Mission re-open** — returning a merged/closed mission to an actionable lifecycle state, preserving `mission_id` and history.
- **DRG orphan** — a doctrine-graph node with no resolved inbound/outbound reference edge (a reference that does not wire into the graph).

## Assumptions

- The post-mission lifecycle surface extends the existing mission-state model rather than introducing a parallel one; exact command shape is a plan-phase decision.
- `dispatch` is additive (new canonical command + aliases), NOT a rename — `do/ask/advise` strings remain valid, so this is not a bulk-edit/occurrence-map mission.
- #1863's "mechanically-clear" orphans are those resolvable without authoring new doctrine content (stale path/id/casing, retired-artifact references); genuine content gaps are the documentable residual.
