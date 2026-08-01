# Implementation Plan: Charter Pack Usage Journey

**Branch**: `feat/charter-pack-usage-journey` | **Date**: 2026-08-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/charter-pack-usage-journey-01KYWWTF/spec.md`
**Research basis**: [notes/research-synthesis.md](./notes/research-synthesis.md) (authoritative design input — 2-lens research squad + revision-squad refresh vs landed M1)

## Summary

`charter pack apply` writes the activation store (`config.yaml` `activated_*`) but nothing compiles it into
the read-authority bundle (`.kittify/charter/charter.yaml`), and several read/dispatch surfaces gate on the
wrong artifact. The result: applying a pack *disables* the safe generic-agent dispatch fallback (#3104),
leaves `charter context`/`charter status` reporting "not found" (#3105), and lets `resolve_project_governance`
report all 29 built-in directives instead of the 5 activated (US3). This mission **wires `apply` to the
existing compile seam** (opt-in `--compile`, truthful default output), **retargets the presence read-gates**
onto `charter.yaml`, **rewrites the dispatch predicate** to key on compiled-bundle-presence + direct
routability (org-pack safe), and **retires the resolver catalog-fallback** so governance has one directive
authority. Folded in per operator direction: make advertised charter section selectors resolve (#3095/#3094),
reconcile the `spec-kitty analyze` surface (#3096), and add a path-filtered CI workflow for
`src/doctrine/**` + `src/charter/**` (#3102). No new compiler is built — the config→bundle lowering
(`compile_charter`/`write_compiled_charter`, exposed as `charter generate`) already exists.

## Technical Context

**Language/Version**: Python 3.11+ (project standard; 3.12 idioms permitted)
**Primary Dependencies**: Typer (CLI), ruamel.yaml (config/bundle I/O), `spec_kitty_events`/`spec_kitty_tracker` (public imports only) — no new runtime deps
**Storage**: On-disk governance artifacts under `.kittify/charter/` (`charter.yaml` compiled bundle = read authority; `charter.md` display-only companion; `config.yaml` `activated_*` = write store)
**Testing**: `pytest` (targeted node-ids locally, `-n auto --dist loadfile` for parallel); the 8 journey acceptance tests (synthesis §"Journey acceptance tests") are the behavioral regression net; `ruff` + `mypy` zero-new-issue gate
**Target Platform**: Linux/macOS developer + CI (GitHub Actions)
**Project Type**: single (CLI + library — `src/charter/`, `src/specify_cli/`, `src/doctrine/`)
**Performance Goals**: `is_charter_empty` on an unconfigured repo ≤ 1 `PackContext.from_config` + 1 `stat`, no URN load (NFR-001, folds #3118)
**Constraints**: opt-in `--compile` (default `apply` stays git-agnostic, C-004); presence-gate retarget and section-selector fix stay two distinct paths (C-003); must not revert M1's landed `resolver.py:187/:250` operator strings (C-002); classify reds vs merge-base, never green-wash (C-005)
**Scale/Scope**: ~7 code modules + 1 CI workflow + journey docs; 12 FR / 4 NFR / 5 C; behavioral (no bulk edit, no occurrence_map)

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Loaded via `spec-kitty charter context --action plan` (mode: compact). Relevant governing principles and how
this plan satisfies them:

- **Single canonical authority** — the mission's *entire thesis* is collapsing a divergent second authority:
  one compiled bundle (`charter.yaml`) as the read authority, one write store (`config.yaml`/pointer), one
  directive authority (activated set, retiring the catalog-fallback). ✅ Aligned, not in tension.
- **No legacy resolver paths** — FR-007 retires the catalog-fallback branch rather than adding a
  no-canonical-field fallback. ✅
- **ATDD-first / red-first** — journey test #6 (resolver returns 5 not 29) is RED on the current tree; it is
  authored first and drives FR-007. The 8 journeys are executable acceptance tests (NFR-002). ✅
- **Campsite cleaning** — the dead composite-predicate docstring + `charter_activated_urns` imports in
  `empty_charter.py`, and the 4× duplicated resolve-or-exit block in `pack.py`, are cleaned *while editing
  those files* (synthesis §Campsite) — scoped, no creep. ✅
- **Canonical sources** — wires the existing `charter generate` compile seam; does not hand-roll a compiler
  or reconstruct paths the resolver should provide. ✅
- **Terminology adherence** — no `feature*` terms introduced; run `test_no_legacy_terminology.py` before
  pushing doctrine/prose (FR-009/FR-010/FR-011 touch prose + templates). ✅
- **Behaviour-change transparency** — the deliberate reversal of #3064's glossary-pack dimension is recorded
  (NFR-004, SC-005) with a pinning test, not slipped. ✅

No violations to justify — Complexity Tracking left empty.

## Project Structure

### Documentation (this mission)

```
kitty-specs/charter-pack-usage-journey-01KYWWTF/
├── plan.md              # This file
├── spec.md              # Mission spec (12 FR / 4 NFR / 5 C)
├── research.md          # Phase 0 — the one open plan decision (FR-010 content-vs-advertise)
├── notes/
│   └── research-synthesis.md   # Authoritative design input (squad + revision refresh)
├── contracts/           # Phase 1 — behavioral contracts for the predicate + bridge + resolver
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root)

```
src/
├── charter/
│   ├── empty_charter.py          # is_charter_empty predicate (IC-01) — rewrite to bundle-presence + routability
│   ├── context.py                # build_charter_context presence gate (IC-03) — retarget to charter.yaml; keep prose readers on charter.md
│   ├── context_json.py           # _project_charter_json_block (IC-03) — soft-retarget present-signal
│   ├── resolver.py               # _resolve_directives_selection / resolve_project_governance (IC-04) — retire catalog-fallback; DO NOT touch M1's :187/:250 strings
│   ├── compiler.py               # compile_charter / write_compiled_charter — REUSED, not modified (bridge target)
│   └── context_renderers/
│       └── section_bodies.py     # render_critical_section_include (IC-06) — the #3095/#3094 section-selector engine
├── specify_cli/
│   └── cli/commands/charter/
│       ├── pack.py               # apply (IC-02) — add --compile bridge + truthful output; hoist resolve-or-exit block
│       ├── _common.py            # NEW sibling _resolve_charter_bundle_path (IC-03) — do NOT retarget _resolve_charter_path in place
│       └── _status_collectors.py # _collect_charter_sync_status (IC-03) — route presence gate through the sibling resolver
├── specify_cli/cli/commands/     # analyze surface reconciliation (IC-07, #3096)
└── specify_cli/upgrade/migrations/m_unify_charter_activation_finalize.py  # fourth producer — convergence ASSERTED (IC-05), not modified

tests/
├── charter/                      # journey acceptance tests (NFR-002) — predicate, bridge, resolver, presence-gate
└── ...                           # convergence test (IC-05), perf spy (NFR-001)

.github/workflows/                # path-filtered doctrine/charter CI (IC-08, #3102)
docs/                             # charter journey guides (IC-09, FR-009) + analyze-surface docs (IC-07)
.agents/skills/spec-kitty.analyze/ # OR the skill/mapping redirect (IC-07 alternative)
```

**Structure Decision**: Single-project layout. Governance code lives in `src/charter/` (library) and
`src/specify_cli/cli/commands/charter/` (CLI surface); the compile seam in `src/charter/compiler.py` is
reused unchanged. All file:line anchors below are **symbol-anchored** — `context.py` has drifted twice
(M1's #3116 shim removal shifted it), so implementers resolve by symbol, using the synthesis re-anchor table
as a hint, and re-verify against HEAD before editing (C-002).

## Complexity Tracking

*No Charter Check violations — not applicable.*

## Implementation Concern Map

> **Note**: Implementation concerns are NOT work packages. `/spec-kitty.tasks` translates these into
> executable WPs — one concern may become one WP or split; small concerns may merge.

### IC-01 — Dispatch-net predicate: bundle-presence + org-pack-safe routability

- **Purpose**: Rewrite `is_charter_empty` so applying a pack without compiling keeps the generic-agent
  safety net, while a compiled bundle or a routable org/profile config disengages it — fixing #3104 without
  regressing org-pack projects.
- **Relevant requirements**: FR-001, FR-002, NFR-001 (folds #3118), NFR-004, SC-001, SC-005.
- **Affected surfaces**: `src/charter/empty_charter.py` (`is_charter_empty` `:48-67`, `_MATCH_REASON`);
  campsite-delete the dead 20-line dimension-enumeration docstring + `charter_activated_urns`/unused
  `PackContext` imports.
- **Sequencing/depends-on**: none (foundational; other concerns can proceed in parallel).
- **Risks**: A pure `charter.yaml`-presence predicate is NOT #3064-safe — MUST split governance-emptiness
  from dispatch-routability (`org_roots != ()`, `activated_agent_profiles is not None`). Pin the
  bootstrapped-empty-bundle-keeps-net-OFF behaviour (SC-005) so a future contents-inspecting "improvement"
  can't re-import the #3064 exhaustiveness trap. Record the deliberate glossary-dimension reversal (NFR-004).

### IC-02 — `apply --compile` bridge + truthful default output

- **Purpose**: Chain the existing compile seam after the config merge (opt-in `--compile`), and make default
  `apply` name the exact next command instead of hand-waving — giving the operator a signalled path from
  "activated" to "governance delivered".
- **Relevant requirements**: FR-003, FR-004, SC-004; journey tests 2 & 7.
- **Affected surfaces**: `src/specify_cli/cli/commands/charter/pack.py` (`apply` `:200-205` output;
  `--compile` flag chaining `charter generate --no-from-interview` / `compile_charter`+`write_compiled_charter`);
  campsite-hoist the 4× duplicated `resolve_builtin_pack_path` resolve-or-exit try-block.
- **Sequencing/depends-on**: none (reuses `compiler.py`; introduces no compiler code).
- **Risks**: `--compile` inherits `charter generate`'s **git-worktree requirement** (`generate.py:313`) —
  document it; default `apply` MUST stay git-agnostic pure-merge (C-004). Do not auto-compile.

### IC-03 — Read-surface presence-gate retarget (charter.yaml authority)

- **Purpose**: Make `charter context` / `charter status` reflect the operator's activations once the bundle
  is compiled — retarget the *presence* gates from display-only `charter.md` onto authoritative
  `charter.yaml`, without entangling the prose readers.
- **Relevant requirements**: FR-005, FR-006, SC-002; journey tests 4 & 5 (incl. `charter.md`-deletion).
- **Affected surfaces**: `src/charter/context.py` (`build_charter_context` `CHARTER_MD` presence gate — render
  `charter.md` prose only when present, graceful-degrade); `src/specify_cli/cli/commands/charter/_common.py`
  (**NEW** sibling `_resolve_charter_bundle_path`, do NOT retarget the shared `_resolve_charter_path:27`);
  `_status_collectors.py:62` (route presence through the sibling — its `charter.yaml`-aware logic at `:65-76`
  is dead today because `:62` raises first); `src/charter/context_json.py` (soft-retarget present-signal).
- **Sequencing/depends-on**: none.
- **Risks**: **C-003** — must NOT collapse the presence gate and the prose readers (`context.py` section
  reader, prose body reads) onto one shared path constant (whack-a-field that breaks #3094/#3095). Two paths
  stay two paths.

### IC-04 — Single directive authority: retire the catalog-fallback

- **Purpose**: Stop `resolve_project_governance` from being a second, divergent directive authority — when
  the authored selection is empty (as after apply+compile), source directives from the config-activated set,
  never the full built-in catalog.
- **Relevant requirements**: FR-007, US3, SC-003; journey test 6 (RED today).
- **Affected surfaces**: `src/charter/resolver.py` — `_resolve_directives_selection` catalog-fallback
  (`:258-260`) and `resolve_project_governance` (`:289`, builds unfiltered catalog at `:316`, constructs no
  `PackContext`). Thread `PackContext.from_config(repo_root).activated_directives`. Structural root: the
  activation-aware `DoctrineService` wrapper (`:57-139`) filters paradigms/procedures/agent_profiles but has
  **no `directives` property** — this concern adds that missing directives filter.
- **Sequencing/depends-on**: none, but **shares `resolver.py` with M1's landed changes** — re-verify M1's
  `:187`/`:250` operator strings at HEAD and do NOT revert them (C-002). Trusts M1/FR-010's unified
  activation vocabulary (C-001, landed).
- **Risks**: The 5 consumers (`prompt_builder.py:437`, `runtime/doctor.py:133`, `context_json.py:139`,
  `compact.py:303`, `resolver.py:415`) carry no `charter.md` pre-gate — only the fallback *source* changes;
  verify no consumer depended on the 29-catalog behaviour.

### IC-05 — Fourth-producer convergence assertion

- **Purpose**: Keep the config→bundle transform one authority — assert `apply --compile` and the
  `spec-kitty upgrade` finalize migration produce a convergent `charter.yaml` shape (or document the
  migration as the upgrade-time equivalent).
- **Relevant requirements**: FR-008 (narrowed post-M1 — assert transform *shape* only; vocabulary is already
  one authority via M1's `ACTIVATION_YAML_KEYS`).
- **Affected surfaces**: test-only; references `m_unify_charter_activation_finalize.apply()` (`:391-415`) and
  `write_compiled_charter`. No production edit to the migration.
- **Sequencing/depends-on**: IC-02 (asserts the bridge's output shape).
- **Risks**: Narrow — do not re-unify the vocabulary (M1 owns it, C-005). Just pin the transform-shape parity.

### IC-06 — Advertised section selectors resolve (#3095/#3094)

- **Purpose**: Make `charter context --include section:terminology-canon` / `section:code-review-checklist`
  (required by generated `implement`/`review` prompts) resolve — or stop the doctrine surface advertising a
  selector the CLI cannot resolve.
- **Relevant requirements**: FR-010, SC-007 (partial); acceptance US4.1.
- **Affected surfaces**: `src/charter/context_renderers/section_bodies.py::render_critical_section_include`
  (`:282`; slugifies `ACTION_CRITICAL_SECTIONS` incl. `"Terminology Canon"`/`"Code Review Checklist"`)
  reached via `build_charter_context_include`'s `kind=="section"` branch. **This stays on the
  `charter.md`/section prose path (C-003)** — it does NOT retarget that reader to `charter.yaml`. Possibly
  the compile (to *produce* the sections) or the mission-step prompt templates in `src/doctrine/` (to stop
  advertising).
- **Sequencing/depends-on**: IC-02 (the compile seeds `charter.md`, so selectors can resolve post-bridge).
- **Risks**: **This is a CONTENT question**, not a resolver gap — Phase 0 must decide "produce the sections
  in the compiled charter" vs "stop advertising in the prompts". Bias: *produce* for terminology-canon (it
  maps to the glossary/terminology surface); confirm code-review-checklist has a doctrine source before
  committing. If touching `src/doctrine/` prompts, run `test_no_legacy_terminology.py`.

### IC-07 — `spec-kitty analyze` surface reconciliation (#3096)

- **Purpose**: Make the documented `spec-kitty analyze` surface and the CLI agree — no documented-but-absent
  command.
- **Relevant requirements**: FR-011, SC-007 (partial); acceptance US4.2.
- **Affected surfaces**: EITHER a thin `spec-kitty analyze` alias to the supported `agent mission
  record-analysis` flow (`src/specify_cli/cli/commands/`), OR the `spec-kitty.analyze` skill +
  command-skills manifest + docs redirected to the supported command.
- **Sequencing/depends-on**: none.
- **Risks**: If exposing an alias, it must route through the canonical `record-analysis` flow (no
  reimplementation — missing-CLI-command-is-a-gap → trace source). If redirecting, update all 19 agent
  surfaces consistently (skill + manifest + docs).

### IC-08 — Path-filtered doctrine/charter CI workflow (#3102)

- **Purpose**: Give PRs touching `src/doctrine/**` / `src/charter/**` fast isolated feedback (DRG
  freshness/sharding, charter-context resolution, the architectural/adversarial gates) and spare unrelated
  PRs that cost/noise.
- **Relevant requirements**: FR-012, SC-007 (partial); acceptance US4.3.
- **Affected surfaces**: `.github/workflows/` (new path-filtered workflow; `paths:` on `src/doctrine/**` +
  `src/charter/**`).
- **Sequencing/depends-on**: none (its seam-work prerequisite is satisfied by M1 landing; does NOT require
  #3101 wheel-split).
- **Risks**: Path-filter un-skip semantics — a PR that changes neither path must still pass (skip-with-green,
  not skip-with-fail). Do not duplicate gates the main CI already runs in a way that double-charges.

### IC-09 — Journey documentation (#3107 partial fold)

- **Purpose**: Document the `apply` → `generate` two-step and the empty-charter dispatch behaviour in the
  charter journey guides, so the operator-facing story matches the new behaviour.
- **Relevant requirements**: FR-009.
- **Affected surfaces**: charter journey guides under `docs/`; freshen page-inventory + docs-index if pages
  are added.
- **Sequencing/depends-on**: IC-01, IC-02, IC-03 (documents their delivered behaviour).
- **Risks**: The inert CLI-reference parity gate of #3107 is **out of scope** (docs-infra, C-005) — document
  the journey only. Run `test_no_legacy_terminology.py` on prose changes.
