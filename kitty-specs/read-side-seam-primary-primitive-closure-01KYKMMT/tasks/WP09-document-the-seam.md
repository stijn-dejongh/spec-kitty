---
work_package_id: WP09
title: Document the placement seam and disambiguate routing
dependencies:
- WP02
- WP08
requirement_refs:
- FR-018
- FR-019
- FR-020
- FR-024
- NFR-010
- NFR-011
planning_base_branch: fix/read-side-seam-primary-primitive-closure
merge_target_branch: fix/read-side-seam-primary-primitive-closure
branch_strategy: Planning artifacts for this mission were generated on fix/read-side-seam-primary-primitive-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into fix/read-side-seam-primary-primitive-closure unless the human explicitly redirects the landing branch.
subtasks:
- T040
- T041
- T042
- T043
- T044
phase: Phase 5 - Write it down once
history:
- at: '2026-07-28T09:27:08Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: curator-carla
authoritative_surface: docs/architecture/
create_intent:
- docs/architecture/artifact-placement-seam.md
- tests/docs/test_artifact_placement_seam_page.py
execution_mode: code_change
model: claude-sonnet-5
owned_files:
- docs/architecture/artifact-placement-seam.md
- docs/architecture/branch-target-routing.md
- docs/architecture/index.md
- docs/context/orchestration.md
- docs/development/3-2-page-inventory.yaml
- docs/development/3-2-docs-retrieval-index.yaml
- CLAUDE.md
- tests/docs/test_artifact_placement_seam_page.py
role: implementer
tags: []
task_type: implement
tracker_refs:
- '2653'
---

# Work Package Prompt: WP09 – Document the placement seam and disambiguate "routing"

## ⚡ Do This First: Load Agent Profile
Use `/ad-hoc-profile-load` to load `curator-carla` (implementer, claude).

## Objective

Write the layering down **once**, in the canonical vocabulary, so the next mission cites a design
document instead of re-running a multi-round audit.

This is the mission's **durable deliverable**. The misappropriation of the seam as "a stable API
to strangle through" has now cost three missions their discovery budget: #3014 was filed on a
false premise, this mission was re-framed twice, and the governing decisions (ADR `2026-06-24-1`
and ADR `2026-07-23-1`) **already forbade the exact anti-pattern** in prose nobody found. The
missing artifact is not a decision — it is a findable **explanation**.

## ⚠ This WP's failure mode is becoming the fifth authority it exists to replace

Four mitigations are **requirements**, not advice:

1. The page is **explanatory**. It links to the two ADRs for normative rules; it does not restate
   them (NFR-011).
2. **Every code-shape claim carries a `module:symbol` citation**, so drift is detectable by
   reading and a future rename shows up as a broken citation rather than silent rot.
3. The **competing page is narrowed in the same slice** (T041). Publishing without that creates
   two authorities answering one question — the exact defect being fixed.
4. The **byte-frozen** glossary stores are untouched.

## ⚠ The layer model must be the VERIFIED one

An earlier draft of this mission misdescribed the layering in **two load-bearing ways**.
Publishing that draft would have taught readers to strangle through `translate_surface` and re-add
discovery at the call site — *causing* the misappropriation this page prevents. The verified model
(see [data-model.md](../data-model.md) §1 and
[contracts/placement-layering.md](../contracts/placement-layering.md) C2):

| Layer | Owner | Aware of |
|---|---|---|
| **L0** entry | the caller declares a `MissionArtifactKind` through `PlacementSeam` | *what* it reads, nothing about where |
| **L1** partition classification | `mission_runtime/artifacts.py` (kind frozensets, `assert_partition_invariant`) | kind only — **topology-blind** |
| **L2a** declared decision | `mission_runtime/resolution.py:declared_read_surface` | **materialization-BLIND** |
| **L2b** affirmative decision | `mission_runtime/resolution.py:_classify_artifact_surface` | **materialization-AWARE**, consumes coord-state probing |
| **L3** discovery + **assembly** | `specify_cli/missions/_read_path_resolver` | filesystem, git, handle forms |
| **L4** translation | `mission_runtime/resolution.py:translate_surface` | **selects** an already-discovered location off `SurfaceLocations`; **refuses when absent** |

**The two corrections that must survive review:**

- **L2 is TWO functions and the divergence is load-bearing.** `declared_read_surface` is
  materialization-blind *precisely so it can disagree with an already-resolved stamp* — and that
  disagreement is what makes the `surface_cannot_hold` / #2906 guard possible. Describing "one
  decision module" is a **defect**, not a simplification.
- **L4 does NOT assemble a path.** It *selects* an already-discovered location and refuses when
  absent. **Assembly lives in L3.** Getting this wrong is what teaches the misappropriation.

Also required: **both composition roots** shown as separate roots reached through **one** seam
object — `resolve_artifact_surface` (reads) and `resolve_placement_only` (writes) (INV-4).

## Context & Constraints

- **NFR-010** — docs hygiene: registered in `docs/architecture/index.md` (**mandatory**); the two
  **gated** registries regenerated; relative links resolve; `check_docs_freshness --ci` zero
  errors. The curated `explanation-index.md` / `explanation-toc.yml` are **ungated subsets** and a
  judgement call, not a requirement.
- **FR-019 exclusions — do NOT edit**:
  `src/doctrine/glossary_packs/built-in/spec-kitty-core.glossary-pack.yaml` and
  `.kittify/glossaries/spec_kitty_core.yaml`. Both are **byte-frozen** by a seed SHA + term-count
  pin and a parity gate. The `primary`/`merge` footgun precedent is implemented purely as
  prose-glossary entries plus a Terminology Canon block — follow that precedent exactly.
- **Do not reword or renumber existing headings** that ADRs deep-link.
- **Filename must NOT be `*-routing.md`** — the word is already overloaded across ≥10 senses
  (C1/C3 of the layering contract). The page is `docs/architecture/artifact-placement-seam.md`.
- **Dependencies are real**: the page documents the layering **as landed** (WP08's structural
  finish), using **as-censused** facts (WP02's classification) — not as intended.

## Doctrine for this WP

- **`DIRECTIVE_042` + `styleguide:common-docs`** — frontmatter as per-page SSOT; the page-inventory
  rollup is a **generated, freshness-gated lockfile**, never hand-maintained.
  `Run: spec-kitty charter context --include directive:DIRECTIVE_042`
  `Run: spec-kitty charter context --include styleguide:common-docs`
  **When doing T043**, regenerate both registries with their tools; do not hand-edit a rollup.
- **`paradigm:deep-module-design`** — the one-line framing for why this page exists: a small stable
  interface should hold **every** fact a caller must know. The semi-compliance shape is what
  happens when it does not.
  `Run: spec-kitty charter context --include paradigm:deep-module-design`
  **When doing T040**, use this to explain *why* a canonical handle is not compliance — the
  interface leaked the partition decision to callers.
- **`tactic:canonical-source-unification`** — step 5: *"do not leave a non-canonical copy as a
  fallback."* This is the doctrinal basis for T041: narrowing rather than co-existing.
  `Run: spec-kitty charter context --include tactic:canonical-source-unification`
  **When doing T041**, reduce the old page's placement claims to a **link**, not a "see also".
- **`DIRECTIVE_044`** — unification, not parity with a dead quirk.
  `Run: spec-kitty charter context --include directive:DIRECTIVE_044`
  **When doing T042**, do not preserve the retired `primary target branch` alias "for
  compatibility" — that is parity with a dead quirk.

## Subtasks

### T040 — Write `docs/architecture/artifact-placement-seam.md` (FR-018)

Six **named sections** are required (contract C1):

1. **What "routing" means here** — the placement sense: mapping an artifact **kind** plus the
   mission's **topology** to a `TopologySurface`. Point at the glossary's `Routing`
   disambiguation for the other senses rather than restating them.
2. **The layer table** — one row per layer (L0, L1, L2a, L2b, L3, L4) with its **owning module**
   and what it is aware of. Use the verified model above.
3. **Both composition roots** — the read root and the write root, as separate roots reached
   through one seam object.
4. **The compliance taxonomy** — compliant tier-1 / delegating-but-lenient / semi-compliant /
   non-compliant, with the *shape* of each. **Semi-compliance is the headline concept**: canonical
   handle + caller-chosen surface, which looks routed and is not, and which a handle-hygiene gate
   cannot catch. Say which gate does and does not catch it (US7.4).
5. **Honest bounds** — the surface members with **no production producer**
   (`LANE`/`CONSOLIDATED`/`TEMP`), and the frozenset still carrying the retired `PLACEMENT` word
   as residual rename debt. **Named, not laundered** (INV-5).
6. **Citations** — ADR `2026-06-24-1` (kind-and-topology-aware placement) and ADR `2026-07-23-1`
   (`TopologySurface` vocabulary + the forbidden-conditioning rule) as the **governing decisions**.

**Every code-shape claim carries a `module:symbol` citation.** Verify each citation resolves in the
tree as landed by WP08 — a citation to a deleted symbol is worse than none.

### T041 — Narrow `branch-target-routing.md` to the branch sense (FR-020, SC-017)

**Purpose**: that page currently asserts **per-artifact-kind placement rules** — the new page's
core claim — under a *branch*-sense title, in vocabulary the glossary explicitly **retires**
("primary target branch"), with no read path. Leaving both is the two-authority failure this
mission exists to end.

**Steps**:
1. Remove its per-artifact-kind placement claims and its pre-`TopologySurface` "How the routing
   decision is made" section — or reduce them to a **link** to the new page.
2. Remove the retired `primary target branch` alias.
3. Keep and sharpen the **branch** sense, which that page legitimately owns.

**Validation** (SC-017): it no longer asserts kind-level placement rules, no longer uses the
retired alias, and links out for the placement sense.

### T042 — Add the `Routing` disambiguation and the Terminology Canon line (FR-019)

Two edits, mirroring exactly how the `primary`/`merge` footgun is implemented:

1. **`docs/context/orchestration.md`** — a `Routing` disambiguation **extending** (not restating)
   the existing `PRIMARY partition` / `COORD partition` / `Topology Surface` entries, which already
   frame partition as an artifact-kind routing concept.
2. **`CLAUDE.md`** — a Terminology Canon line, alongside the existing `primary`/`merge` footgun
   block. Cross-reference **#2653**, which shares this surface (cross-reference only, no closing
   keyword).

**Governed senses** — each with a **"do NOT use when"** guard: placement, branch-target, commit,
dispatch/profile, sync fan-out, **model/task routing** (`src/doctrine/model_task_routing/` — the
highest-collision sense in agent-authored prose), and scope routing.

**Explicitly scope out by name**: event routing, HTTP request routing, significance routing bands.
**Naming an exclusion is disambiguation; silence is not** — that is the whole reason the count is
≥10 senses rather than the 5 an earlier draft assumed.

**Do NOT** touch the two byte-frozen glossary stores (see Constraints).

### T043 — Register the page and regenerate the gated registries (NFR-010, SC-013)

**Steps**:
1. Add the page to `docs/architecture/index.md` (**mandatory**).
2. Regenerate **both gated** registries with their tools — never by hand:
   `docs/development/3-2-page-inventory.yaml` (via the inventory lockfile writer) and
   `docs/development/3-2-docs-retrieval-index.yaml` (via the docs-index writer).
3. Verify relative links resolve — adding or moving a docs page breaks `../` links; run the
   relative-link check.
4. `PYTHONPATH=. uv run python scripts/docs/check_docs_freshness.py --ci` → **zero errors**.
5. Confirm the **frozen stores are untouched-green** — that is the proof neither was edited:
   `test_glossary_pack_parity.py` and `test_glossary_pack_no_regression.py`.

### T044 — Add the docs test asserting the page's required sections and citations (SC-012)

Write `tests/docs/test_artifact_placement_seam_page.py` asserting **structurally**:

- each of the six named sections from T040 is present;
- the layer table has a row per layer, each naming an **owning module path**;
- the `Routing` disambiguation table covers every **governed** sense, each with a "do NOT use
  when" guard, plus the infrastructural senses named as out of scope;
- the compliance-idiom table is present;
- **both** governing ADRs are cited;
- both composition roots appear;
- the honest bounds appear (unwired surface members; the residual `PLACEMENT` rename debt).

Keep the assertions about **structure and citations**, not prose wording — a test that pins
sentences will fight every future edit. The **comprehension** check belongs to a human (User Story
7's Independent Test), not to this test.

## Branch Strategy

- Planning/base branch: **`fix/read-side-seam-primary-primitive-closure`**
- Final merge target: **`fix/read-side-seam-primary-primitive-closure`**
- Worktree allocated **per computed lane** from `lanes.json` by `spec-kitty implement WP09`.
  Never hand-construct it; never `git stash` inside a lane worktree.

## Test strategy

```bash
PYTHONPATH=. uv run python scripts/docs/check_docs_freshness.py --ci   # expect 0 errors
PWHEADLESS=1 uv run pytest tests/docs/ tests/architectural/test_no_legacy_terminology.py -q
# proof the frozen stores were NOT edited:
PWHEADLESS=1 uv run pytest tests/architectural/test_glossary_pack_parity.py \
  tests/architectural/test_glossary_pack_no_regression.py -q
```

The terminology guard is a **CI-only** gate for prose changes — it passes local doctrine runs and
fails at CI if skipped. Run it before handing off.

## Definition of Done

- The page exists with all **six** named sections, the **verified** layer model (L2 as two
  functions; L4 selecting, not assembling), both composition roots, the compliance taxonomy with
  semi-compliance explained, the honest bounds named, and **both** ADRs cited (T040).
- **Every** code-shape claim carries a `module:symbol` citation that resolves in the tree as
  landed by WP08.
- `branch-target-routing.md` no longer asserts kind-level placement rules, no longer uses the
  retired alias, and links out (T041, SC-017).
- `Routing` disambiguation in the prose glossary + Terminology Canon line in `CLAUDE.md`, covering
  all **governed** senses with "do NOT use when" guards and naming the infrastructural senses as
  out of scope (T042).
- **Neither byte-frozen glossary store edited** — proven by parity + no-regression gates being
  **untouched-green** (T043, SC-013).
- Page registered in `docs/architecture/index.md`; both gated registries regenerated with their
  tools; relative links resolve; `check_docs_freshness --ci` **zero errors** (T043).
- The docs test asserts structure and citations, not prose wording (T044, SC-012).
- Terminology guard green.
- #2653 cross-referenced (no closing keyword).
- Finish: commit, `mark-status T040 T041 T042 T043 T044 --status done`, then `move-task WP09 --to
  for_review` and **wait** for the synchronous pre-review gate.

## Risks

- **Becoming the fifth authority.** The four mitigations above are requirements. If you find
  yourself restating an ADR's normative rule, link instead.
- **Publishing the WRONG layer model** would actively teach the misappropriation this page
  prevents. Re-read the two corrections; a reviewer will check them specifically.
- **Editing a byte-frozen store** breaks a SHA + term-count pin and a parity gate. The precedent
  is prose glossary + Canon line only.
- **Hand-editing a generated rollup** (`3-2-page-inventory.yaml`) will drift and fail freshness.
  Regenerate.
- **Adding a docs page breaks `../` links** elsewhere. Run the relative-link check.
- **Do not name the file `*-routing.md`** — the word already carries ≥10 senses.

## Reviewer guidance

1. **Check L2 and L4 specifically.** Does the page show L2 as **two** functions with the
   divergence explained as load-bearing? Does it say L4 **selects** rather than assembles? These
   two errors are the reason this page exists.
2. Pick three `module:symbol` citations at random and resolve them in the tree. Does each exist
   **after** WP08's deletions?
3. Read `branch-target-routing.md`: does it still assert kind-level placement, or still use
   `primary target branch`?
4. Confirm the glossary parity + no-regression gates are **untouched-green** — that is the
   evidence no frozen store was edited.
5. Are both registries **regenerated** (by tool) rather than hand-edited?
6. **The human check**: can you, without re-reading this mission's spec, state (a) what routing
   means here vs branch-target routing, (b) which layer decides placement, (c) why a canonical
   handle is not compliance? If not, the page has not met User Story 7.
