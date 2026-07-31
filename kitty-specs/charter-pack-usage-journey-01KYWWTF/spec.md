# Mission Specification: Charter Pack Usage Journey

**Mission**: `charter-pack-usage-journey-01KYWWTF`
**Type**: software-dev (behavioural / usability)
**Status**: Draft
**Purpose (TL;DR)**: Make `charter pack apply` actually deliver usable governance — so applying a pack no
longer silently breaks dispatch or leaves `charter context`/`charter status` reporting the charter as missing.

> Research basis: a 2-lens research squad (architect-alphonso — architecture + reproduced all 8 journeys
> end-to-end; paula-patterns — related-issues + campsite) scoped this mission. Full synthesis in
> `notes/research-synthesis.md`. This is **Mission 2 of 2**; Mission 1
> (`doctrine-built-in-seam-consolidation`, #3119/#3106/#3116/#3120/#3090) is the sibling and a
> hard precondition (see C-001).

## User Scenarios & Testing *(mandatory)*

The user is an **operator** setting up governance on a project, and the **runtime dispatch** that routes
their requests. The failure: applying a charter pack today delivers *less* usable governance than doing
nothing — it disables the safe dispatch fallback and the governance surfaces still report "not found".

### User Story 1 - Applying a pack keeps dispatch safe (Priority: P1, #3104)

An operator on an unconfigured project runs `spec-kitty charter pack apply minimal` to get started. Today
that flips the "is the charter configured?" check to true (config.yaml now has activation keys) but
activates **no routable agent profile** — so the generic-agent dispatch safety net switches off and the
next unmatched `spec-kitty dispatch` hard-fails with `ROUTER_NO_MATCH`. Applying a pack must never leave
dispatch *worse* than an empty project: an unmatched request must still fall back to the warned generic
agent until the project actually has routable governance.

**Why this priority**: it is a P1 regression where the documented "get started" remedy actively breaks the
thing it is meant to help.

**Acceptance**:
1. **Given** an empty project, **when** an unmatched request is dispatched, **then** it falls back to the
   warned generic agent (baseline).
2. **Given** `charter pack apply minimal` **without** a compile, **when** the same unmatched request is
   dispatched, **then** it **still** falls back to the generic agent — **not** `ROUTER_NO_MATCH`.
3. **Given** a project whose pack has been compiled into the bundle, **when** an unmatched request is
   dispatched, **then** the router runs and `ROUTER_NO_MATCH` is the *honest* signal (the project opted in).
4. **Given** a project configured with an **org pack** (routable profiles, no compiled bundle), **when** an
   unmatched request is dispatched, **then** the net stays disengaged and the router reaches the org
   profiles (no regression — the fix must not fire the net for genuinely-routable projects).

### User Story 2 - Applying a pack (and compiling) delivers working governance (Priority: P1, #3105)

After applying a pack, the operator checks `charter context --action implement` and `charter status`.
Today both report the charter as **missing** — they gate on the display-only `charter.md`, which `apply`
never creates, instead of the authoritative compiled bundle `charter.yaml`. The governance read surfaces
must reflect the operator's activations once the bundle is compiled, and `apply` must tell the operator the
exact step to get there.

**Why this priority**: without this, `apply` is a dead end — the operator has no signalled path from
"activated" to "governance actually delivered".

**Acceptance**:
1. **Given** a pack applied and compiled, **when** `charter context --action implement` runs, **then** it
   renders the pack's activated directive/tactic set (not "Charter file not found", not the full catalog).
2. **Given** a compiled bundle is present, **when** the display-only `charter.md` is deleted, **then**
   `charter context` and `charter status` **still** work — proving the gate is on `charter.yaml`, not
   `charter.md`.
3. **Given** a pack applied and compiled, **when** `charter status` runs, **then** it reports the charter as
   available/synced.
4. **Given** an operator runs `apply` **without** `--compile`, **when** they read its output, **then** it
   names the exact next command (`spec-kitty charter generate`) — no vague "a compile may be needed".
5. **Given** `charter context --include section:<id>` (a prose selector), **when** it runs, **then** it
   still reads `charter.md` prose — this mission must **not** entangle the prose readers (#3094/#3095).

### User Story 3 - Governance has one directive authority (Priority: P2)

The resolver that several surfaces use (`resolve_project_governance`) silently falls back to **all** built-in
directives when the authored governance selection is empty — which it is after a pack-apply+compile. So a
project that activated 5 directives is reported by that path as having all 29. Governance must have **one**
directive authority (the activated set), not a divergent catalog-fallback second source.

**Why this priority**: it is a correctness divergence (5 vs 29) that undermines the whole point of activating
a curated pack, and it is the load-bearing "no legacy resolver paths" cleanup C-004 depends on.

**Acceptance**:
1. **Given** a pack activating 5 directives, applied + compiled, **when** `resolve_project_governance` runs,
   **then** its directives are the 5 activated (from the compiled catalog / activation authority), **not**
   the 29-directive built-in catalog-fallback.

### Edge Cases

- **"Empty" means the compiled bundle is ABSENT**, never "bundle present but activations empty". A
  `charter generate` on a bare project bootstraps a near-empty `charter.yaml`; the dispatch predicate must
  treat that as *not* empty (the operator opted into a compiled bundle → `ROUTER_NO_MATCH` is honest). A
  future "improvement" that inspects bundle *contents* would re-import the #3064 exhaustiveness trap — a
  test must pin the bootstrapped-empty-bundle-keeps-net-OFF behaviour.
- `apply --compile` inherits `charter generate`'s **git-worktree requirement**; default `apply` stays
  git-agnostic (pure additive merge). Both paths are journey-tested.
- A **fourth** config→bundle producer already exists (the `spec-kitty upgrade` finalize migration mints
  `charter.yaml` from bare config and strips `activated_*`). `apply --compile` must **converge** with it —
  same shape — so the config→bundle transform stays one authority.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | Fix the dispatch-net predicate (`is_charter_empty`) so it keys on **compiled-bundle presence** (`.kittify/charter/charter.yaml`) plus the direct dispatch-routability sources (`org_roots`, `activated_agent_profiles`) — NOT the config activation aggregate — so `apply`-without-compile keeps the generic-agent net, while a compiled bundle or a routable org/profile config disengages it. | Draft |
| FR-002 | The predicate must be org-pack/profile safe: a project with an org pack or explicit agent-profile activation (routable without a compiled bundle) does **not** fire the net (no regression); a glossary-only/directive-only project with no bundle **does** fire it. | Draft |
| FR-003 | Wire `charter pack apply --compile` to chain the **existing** compile seam (`charter generate --no-from-interview` / `compile_charter`+`write_compiled_charter`) after the config merge — introducing no new compiler code; the flag inherits and documents `generate`'s git-worktree requirement. | Draft |
| FR-004 | Make default `apply` output **truthful**: name the exact next command (`spec-kitty charter generate`) required to deliver governance, replacing today's vague "a compile may still be needed". | Draft |
| FR-005 | Retarget the charter **presence** read gates from the display-only `charter.md` onto the authoritative `charter.yaml`: the context bootstrap gate (`context.py:286`, rendering `charter.md` prose only when present) and the status/context presence path via a **new sibling** bundle-path resolver (`_resolve_charter_bundle_path`) — the shared `_resolve_charter_path` is NOT retargeted in place (it serves prose consumers). | Draft |
| FR-006 | Soften the JSON project-charter "present" signal (`context_json._project_charter_json_block`) to report `charter.yaml` (authority) presence as primary; `charter.md` presence becomes a secondary display field. | Draft |
| FR-007 | Retire the legacy catalog-fallback in `resolve_project_governance` (`_resolve_directives_selection`): when the authored governance selection is empty, source directives from the config-activated set (the compiled catalog / activation authority), never `sorted(doctrine_catalog.directives)` — so `resolve_project_governance` is not a second, divergent directive authority. | Draft |
| FR-008 | Assert `apply --compile` and the upgrade finalize migration produce a **convergent** `charter.yaml` shape (or explicitly document the migration as the upgrade-time equivalent) — the config→bundle transform is one authority, not two. | Draft |
| FR-009 | Fold the journey-doc portion of #3107: document the `apply` → `generate` two-step and the empty-charter dispatch behaviour in the charter journey guides. | Draft |

### Non-Functional Requirements

| ID | Requirement | Threshold / Measure | Status |
|----|-------------|---------------------|--------|
| NFR-001 | The dispatch-net predicate is single-load on the hot path (folds #3118). | `is_charter_empty` on an unconfigured repo performs at most one `PackContext.from_config` + one `stat`, with **no** `charter_activated_urns` URN load (advisory, load-counting spy). | Draft |
| NFR-002 | Every journey is regression-guarded. | The 8 journeys in `notes/research-synthesis.md` §"Journey acceptance tests" are executable tests (dispatch-net ×3 incl. org-pack safety, context/status bundle-authority ×2 incl. charter.md-deletion, resolver single-authority, truthful output, perf). | Draft |
| NFR-003 | No new lint/type regressions. | `ruff` + `mypy` zero new issues on all changed modules. | Draft |
| NFR-004 | Behaviour-change decisions are explicit, not slipped. | The spec/PR record the deliberate reversal of #3064's glossary-pack dimension (glossary-only + no bundle now fires the net) and the "empty = bundle absent" definition. | Draft |

### Constraints

| ID | Constraint | Status |
|----|------------|--------|
| C-001 | **Hard precondition — Mission 1 (`doctrine-built-in-seam-consolidation`) must complete first.** M2's branch is based on M1's; M2's resolver-fallback-from-activated-set trusts M1/FR-010 (activation-vocabulary unification + the live `activated_glossary_packs` drift fix). Do not implement M2's resolver retarget until M1's FR-010 has landed. | Active |
| C-002 | **Shared-file coordination:** M1 WP02 owns `src/charter/resolver.py` (built-in-reader migration + the operator-string repoint at :187/:250). M2 edits the same file (`_resolve_directives_selection`, :233-260) — M2 must **not** touch M1's operator strings and must re-verify M1's resolver changes before layering the fallback retarget. | Active |
| C-003 | **Do NOT retarget the `charter.md` prose readers.** `context.py:397` (`--include section:<id>`) and the prose body reads (`:333`) legitimately need `charter.md`; only the *presence* gates move to `charter.yaml` (the #3094/#3095 boundary). Do not collapse both onto one path constant. | Active |
| C-004 | **`apply --compile` is opt-in.** Default `apply` stays a git-agnostic pure additive merge; auto-compiling would change apply's contract (git-worktree requirement, `charter.md` seed, `library/`, gitignore, git-stage, config→pointer migration). | Active |
| C-005 | Out of scope: #3106 (activation-vocab — M1/WP05), #3107's inert CLI-reference parity gate (docs-infra), #2831/#3092/#3045/#2992/#2213 and the other pre-existing/unrelated reds (classify vs merge-base, never green-wash). | Active |

### Key Entities

- **Activation write store** — `config.yaml` `activated_*` (or the pointed-at `charter.yaml` when a `charter:`
  pointer exists); written by `charter pack apply`.
- **Compiled bundle** — `.kittify/charter/charter.yaml` (`governance`/`directives`/`catalog`/`metadata`); the
  authoritative read cache; written by the compile seam.
- **Display companion** — `.kittify/charter/charter.md`; prose only, never a governance authority.
- **Dispatch net** — the generic-agent fallback gated by `is_charter_empty`; must key on routability, not
  config-activation presence.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After `charter pack apply` (no compile), an unmatched dispatch **never** returns
  `ROUTER_NO_MATCH` — it falls back to the generic agent 100% of the time (the #3104 fix), while an org-pack
  or agent-profile project is unaffected (no net-fire regression).
- **SC-002**: After `apply` + compile, `charter context`/`charter status` report the pack's governance
  (not "not found"), and continue to work with `charter.md` deleted — proving the authority is `charter.yaml`.
- **SC-003**: `resolve_project_governance` returns the **activated** directive set, never the full built-in
  catalog-fallback (5, not 29, for the minimal pack).
- **SC-004**: `apply` output names the exact next command; `apply --compile` compiles the bundle in one step.
- **SC-005**: The deliberate #3064 glossary-dimension reversal and "empty = bundle absent" are recorded, and
  a test pins the bootstrapped-empty-bundle-keeps-net-OFF behaviour.
- **SC-006**: M2's diff does not touch M1/WP05's vocab surface, the `charter.md` prose readers, or the
  pre-existing/unrelated reds (C-005).

## Assumptions

- The config→bundle compile already exists (`compile_charter`/`write_compiled_charter`, exposed as
  `charter generate`); M2 wires and retargets, it does not build a compiler.
- `charter.yaml` is the authoritative governance read source and `charter.md` is display-only (corroborated
  in-tree: `freshness/computer.py`, `compact_governance.py`).
- Mission 1 completes on `feat/relocate-builtin-doctrine-packs` and lands its FR-010 before M2 implements
  the resolver retarget (C-001).
