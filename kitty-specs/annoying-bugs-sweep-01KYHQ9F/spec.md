# Mission Specification: Annoying Bugs Sweep

**Mission Branch**: `fix/annoying-bugs-sweep`
**Created**: 2026-07-27
**Status**: Draft (revised post-squad)
**Input**: Operator request — "Address these all in an annoying bugs mission": #2985, #1840, #2983, #2984.
**Change mode**: `bulk_edit` (recorded in `meta.json`; see Change Classification)

> **Revision note.** A post-spec adversarial squad (architect / debugger / reviewer / planner lenses)
> returned 3 CRITICAL findings and one disqualifying scope reversal against the first draft. All
> confirmed findings are folded in here. The most important: the first draft's causal model of the
> P0 was **factually wrong**, and its "zero raw reads" requirement silently reversed a binding
> constraint on #1840. Both are corrected below. Squad evidence is cited inline so the corrections
> are auditable rather than asserted.

## Intent Summary

Four defects share one shape: **a surface that looks authoritative but silently misdirects.**

One misdirects *data* — a birth-cutover seed can supersede a work package's terminal lane, so a
finished WP reads back as `claimed` (#2985, P0, confirmed live on `main` at `d0a5bacf7`). Three
misdirect *agents* — profile-load surfaces instruct raw `.agent.yaml` reads that bypass doctrine
resolution (#1840), a plain-language styleguide teaches a command that does not exist (#2983), and
the invocation lifecycle opens under one command path but closes under another (#2984).

The unifying acceptance property: **no shipped surface may confidently assert something false.**
For #2985 the false assertion is machine state; for the other three it is an instruction to an agent.

### The P0 mechanism (corrected)

The first draft claimed the seed is "appended after the terminal transition" and that "the reducer
replays in order, so the last transition wins". **This is false.** `src/specify_cli/status/reducer.py:315`
is `sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))` — **file position is
discarded entirely.** The real chain is a timestamp collision plus a lexical tiebreak:

1. `backfill_runtime_state.py::_claim_anchors` anchors a claim seed to the WP's first transition
   *into* `claimed`; when the WP never explicitly entered `claimed`, it **falls back to the WP's
   earliest transition of any lane** — which for a finished WP is its terminal transition.
2. The seeded `planned -> claimed` is therefore stamped with a timestamp **byte-identical** to the
   terminal event's `at`.
3. `reducer.py::_should_apply_event` has a same-timestamp precedence layer, but it arbitrates only
   rollback-vs-forward. `done` (forward) vs seeded `claimed` (forward) matches neither branch and
   falls through to "apply".
4. The tie therefore resolves on lexical `event_id`. A seed id is
   `deterministic_ulid(mission_id|wp_id|field)` — a hash-derived ULID whose first character is
   uniform over `0-7`, whereas real ULIDs begin `01`. **The seed usually wins.**

Two consequences the first draft missed. First, whether any given WP rewinds is a per-`(mission_id,
wp_id, field)` hash outcome, so this fires on *some* terminal WPs rather than all — the profile of a
bug that escapes notice. Second, any fix that merely changes where the row is written is a **no-op
that reads as a fix**; the lever must be the anchor, the seed set, or the precedence rule.

Primary actor is a Spec Kitty operator or a delegated agent. The rule that must always hold: a work
package that has legitimately reached a terminal lane never silently leaves it, and no shipped prompt
surface instructs a mechanism that cannot work.

### Priority vocabulary

Tracker priorities (`P0`–`P3`) and user-story ranks are distinct scales. Stories below are ranked
`US-High` / `US-Med` / `US-Low` to avoid the collision the first draft had (US1 labelled "P1" while
its issue is the P0).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A finished work package stays finished (Rank: US-High · issue #2985, P0)

An operator runs `spec-kitty accept` on a mission whose work packages are approved or done. A
birth-cutover seed carrying the terminal event's own timestamp wins the `(at, event_id)` tiebreak and
supersedes the terminal lane, so the WP reads back as `claimed`. Accept stops converging, the mission
cannot proceed to lane consolidation, and the corrupting write lands in the acceptance commit —
persisted, not transient.

**Why this rank**: the only defect here that corrupts user data, on the terminal lifecycle seam, live
on `main` today.

**Independent Test**: on a synthetic mission carrying genuinely unseeded legacy runtime state AND
terminal transitions, run accept; assert no WP's canonical lane changed, all runtime slots are
populated, and `verify_backfill` is `ok`.

**Acceptance Scenarios**:

1. **Given** a mission with ≥3 WPs — mixed terminal and non-terminal, at least one whose claim anchor
   collides with its terminal transition's `at` — **When** `spec-kitty accept` runs on the
   real-commit path, **Then** every WP's canonical lane is unchanged, and no seeded transition sorts
   at-or-after any WP's terminal transition under the reducer's `(at, event_id)` order.
2. **Given** that mission after a first successful accept, **When** accept runs again, **Then** the
   gate converges (`summary.ok`) with no outstanding work packages, in each mutating mode
   (`commit`, `no_commit`); `diagnose` is read-only and expected to be a no-op — state which and why.
3. **Given** any accept run, **When** it completes, **Then** no appended event changes any WP's
   canonical lane. *(Quantified on lane-delta, not event count — the first draft's "unless the stamp
   had genuinely new runtime state" escape clause was satisfied by the bug itself.)*
4. **Given** a mission that has genuinely never been cut over and carries no terminal transitions,
   **When** the stamp runs, **Then** it still seeds runtime state and `CutoverResult.flipped` is
   `True` — the fix must not disable the feature.
5. **Given** a WP carrying **both** a terminal transition **and** genuinely unseeded legacy runtime
   state, **When** accept runs, **Then** (a) its canonical lane is still terminal, (b) every legacy
   runtime slot is populated in the reduced snapshot, and (c) `verify_backfill` reports `ok`.
   *(This is the anti-disable oracle: a fix of the shape "skip the seed whenever the WP is terminal"
   satisfies scenarios 1–4 while silently discarding `shell_pid`/`agent`/`assignee`/`subtasks`/`review`
   — the same data-loss class as the P0.)*
6. **Given** a terminal WP, **When** an explicit forced transition re-opens it, **Then** that still
   succeeds — the fix must not freeze terminal WPs.
7. **Given** the same mission processed by the merge seam rather than accept, **When** the cutover
   runs, **Then** the second seam is a no-op **and its own verify still passes**.

---

### User Story 2 - A delegated agent loads the profile it was actually assigned (Rank: US-Med · issue #1840, P2)

Shipped prompt surfaces instruct agents to read a profile's `.agent.yaml` directly. That bypasses
doctrine resolution — `specializes_from` lineage, pack overlays, and `enhances` (field-merge) versus
`overrides` (full replacement). For a shallow-lineage built-in the raw read coincides; for a
pack-extended profile it silently yields a **different** profile with no error.

**Why this rank**: silent divergence with no failure signal, growing with the 3.3.x pack ecosystem.
Held at the issue's current `priority:P2` — the escalation to P1 flagged in #1840's triage is
**still the operator's open call** and is not resolved by this spec. Scope is taken at full depth
regardless, because the guard is the cheap part and is what prevents recurrence.

**Independent Test**: enumerate every tracked doctrine prompt surface; assert none instructs a raw
`.agent.yaml` read **as the primary mechanism**, and that a guard fails when one is reintroduced.

**Acceptance Scenarios**:

1. **Given** any tracked doctrine prompt surface, **When** it instructs an agent how to load an
   assigned profile, **Then** the **primary** mechanism named is resolver-backed
   (`spec-kitty agent profile show <id>` or `spec-kitty charter context --include agent-profile:<id>`).
2. **Given** a harness that cannot shell out to the CLI, **When** a surface offers a raw-read
   fallback, **Then** that fallback is explicitly scoped to such harnesses and carries an inline
   resolution-divergence caveat. *(C-006 — see below. An unscoped ban re-breaks open P1 #2304.)*
3. **Given** the `adversarial-squad` skill and its governing procedure — the highest-traffic
   occurrence, and the one this mission's own review executed verbatim — **When** a delegate is
   dispatched, **Then** the instruction names the resolver command as primary, with the #2304-scoped
   fallback available to read-only harnesses.
4. **Given** a contributor reintroduces an unscoped raw-read instruction, **When** the suite runs,
   **Then** a guard fails and names the offending file.
5. **Given** the canonical `spk-doctrine-profile-load` skill, **When** an agent follows it, **Then**
   it is self-sufficient — the substantive mechanics live in the canonical skill and the legacy alias
   points to it, not the reverse. *(Restated: the first draft asserted a mutual-deferral loop that
   does not exist. `ad-hoc-profile-load` does not defer back. The real defect is directional —
   the canonical name is a ~20-line stub whose detail lives in the deprecated alias.)*
6. **Given** the #1840 ticket body, **When** an implementer reads it, **Then** it no longer states
   that reading the YAML directly is the reliable mechanism, nor implies #1636's commands are missing.

---

### User Story 3a - The styleguide names a real command (Rank: US-Low · issue #2983, P2)

The plain-language styleguide's `good_example` instructs `spec-kitty status`, which does not exist.
Agents copy `good_example` blocks — that is their function.

**Acceptance Scenarios**:

1. **Given** `plain-language.styleguide.yaml`'s `good_example`, **When** an agent runs the command it
   names, **Then** the command exists (`spec-kitty agent tasks status`).
2. **Given** the published `docs/` surfaces that carry the same phantom command, **When** they are
   swept, **Then** they name a real command or are explicitly recorded as out of scope.

---

### User Story 3b - The invocation opener is discoverable from the closer (Rank: US-Low · issue #2984, P3)

An operator opens an Op with top-level `spec-kitty dispatch` but closes it with
`spec-kitty profile-invocation complete`. Looking for the opener where the closer lives yields
"No such command" — which is exactly how #2984 was filed as a CLI defect when the CLI was fine.

**Acceptance Scenarios**:

1. **Given** `spec-kitty profile-invocation --help`, **When** an operator looks for how to open an
   invocation, **Then** the help text names `spec-kitty dispatch` explicitly.

*(Split from 3a: the two share no file, no test, and are independently shippable.)*

### Edge Cases

- A mission that has genuinely never been cut over — the stamp must still work (scenario 4).
- A terminal WP re-opened by an explicit forced transition — must remain possible (scenario 6).
- **Already-seeded corpora.** Seed ids namespace on `mission_id|wp_id|field` and exclude `at`, while
  verify compares the full payload. A fix that re-anchors the seed makes every previously-seeded
  mission fail verify permanently, with no repair path. Must be addressed (FR-010).
- Coordination topology: three surfaces, not two — seed write + anchor read + verify + snapshot land
  on COORD; `tasks/` frontmatter reads from PRIMARY; `status_phase` writes to PRIMARY. The
  terminal-lane knowledge the fix needs exists only on the COORD leg, and the two seams resolve COORD
  through *different* resolvers.
- A `.agent.yaml` path cited as **data** (schema example, `applies_to` list, cross-reference) is not
  a load instruction; the guard must discriminate on the surrounding imperative.
- A profile with no lineage, where raw and resolved reads coincide — the guard still rejects the
  unscoped *instruction*: correctness by coincidence is not correctness.

## Requirements *(mandatory)*

### Functional Requirements

| ID | US | Title | Statement | Priority | Status |
|----|----|-------|-----------|----------|--------|
| FR-001 | US1 | No seeded value supersedes current WP state | As an operator, I want no seeded historical event to supersede **any** WP's current lane or runtime slots, so finished work stays finished. Universally quantified over WPs, and over lane **and** annotation slots. | High | Open |
| FR-002 | US1 | Accept converges on an unchanged tree | As an operator, I want a second accept on an unchanged tree to converge, in each mutating mode, with the stamp reporting success (`error is None`). | High | Open |
| FR-003 | US1 | Cutover remains functional | As a maintainer, I want the cutover to still seed genuinely-absent runtime state and still flip `status_phase`, so the fix does not disable the feature. | High | Open |
| FR-004 | US1 | All writing cutover callers behave consistently | As a maintainer, I want every writing caller of the shared cutover authority to hold FR-001, so the fix is not accept-only. | High | Open |
| FR-005 | US1 | Seed set and verify predicate share one source | As a maintainer, I want `verify_backfill`'s `seeded_wps` predicate derived from the same source as the seed builder, so suppressing a seed cannot make `status_phase` permanently un-flippable. | High | Open |
| FR-006 | US1 | Reproduction is collected by a named CI job | As a maintainer, I want the #2985 reproduction asserted to be selected by a named CI job, so this P0 cannot silently return. | High | Open |
| FR-007 | US2 | Resolver-backed command is the primary mechanism | As a delegated agent, I want every profile-load instruction to name a resolver-backed command as primary, so I load the profile I was actually assigned. | Medium | Open |
| FR-008 | US2 | Read-only-harness fallback preserved and scoped | As an agent in a harness that cannot shell out, I want a scoped raw-read fallback with an inline divergence caveat, so #2304 is not re-broken. | Medium | Open |
| FR-009 | US2 | Canonical profile-load skill is self-sufficient | As an agent, I want the canonical skill to hold the mechanics and the legacy alias to point at it, not the reverse. | Medium | Open |
| FR-010 | US1 | Already-seeded corpora remain flippable | As an operator with an already-seeded corpus, I want the fix not to strand my missions on a permanent verify failure. | High | Open |
| FR-011 | US2 | #1840 ticket body no longer misdirects | As an implementer, I want the stale advice struck. *(verification_method: manual — permalink to the edited comment pasted in the PR body.)* | Medium | Open |
| FR-012 | US3a | Styleguide and docs name real commands | As an agent, I want doctrine and published docs to name commands that exist. | Low | Open |
| FR-013 | US3b | Invocation opener discoverable from closer | As an operator, I want `profile-invocation --help` to name `spec-kitty dispatch`. | Low | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Red-first proof, pinned | A NEW test reproducing the lane supersession is committed, with its node id named in the PR body, demonstrated failing at `git merge-base HEAD upstream/main` and passing after. Citing a pre-existing failing test does not satisfy this. | Reliability | High | Open |
| NFR-002 | Every new branch tested | Every new branch or helper carries a focused test named in the PR body. Self-contained: the repo's enforced `diff-cover --include critical_paths` does **not** cover `migration/`, `cli/`, or `acceptance/`, so the 90% gate cannot be appealed to at the fix site. | Maintainability | High | Open |
| NFR-003 | Guard is enumerable and fail-closed | The raw-read guard scans **tracked** surfaces only (`src/doctrine/**`, plus the generator's render path), asserts a non-zero scanned-file count per root, and names each offending file. It must not reference `.agents/**`, which is gitignored and absent from the repo. | Reliability | Medium | Open |
| NFR-004 | Attribution, not green-washing | Every test greened is first confirmed failing at the merge base, evidenced by a committed baseline artifact. Pre-existing reds are reported as such and left alone. | Process | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Single cutover authority, full caller set | No forked writer. The authority has **five** writing callers, not two: accept, merge, the `spec-kitty upgrade` migration (`m_zz_runtime_state_backfill.py`, which passes no `status_feature_dir` and so collapses both legs), `migrate backfill-runtime-state` (single + corpus). Any not covered must be scoped out with a reason. | Technical | High | Open |
| C-002 | **OPEN QUESTION** — reducer precedence lever | The first draft ruled out "making the reducer order-independent", which misnames the lever: the reducer is already order-independent, and `_should_apply_event` already carries a same-timestamp precedence layer. Squad split — architect says bar it (governs every WP in every mission; rollback precedence is load-bearing for parallel-worktree merges), debugger says it is a ~5-line well-fenced rule. **Reopened by operator decision: `/plan` evaluates anchor-clamping, seed-suppression, and precedence on evidence.** | Technical | High | Open |
| C-003 | No new top-level `status` | #2983 is resolved by correcting the surfaces, not by minting a top-level `status`. Note a `spec-kitty.status` **slash command** does ship in the agent surface, which plausibly explains the example — that split is not a reason to add a CLI verb. | Technical | Medium | Open |
| C-004 | Historical artifacts immutable | Archived `kitty-specs/` snapshots referencing retired commands are excluded. | Technical | Medium | Open |
| C-005 | P0 file-set separability | The P0 work package's **changed-file set is disjoint** from every papercut work package's, `CHANGELOG.md` excepted, whose P0 stanza is authored as a self-contained block. Verified disjoint at spec time. Dependency-freedom alone is insufficient — the operator bought disjointness. | Process | High | Open |
| C-006 | Read-only-harness fallback preserved | A raw `.agent.yaml` read may remain **only** where scoped to harnesses that cannot invoke the CLI, with an inline resolution-divergence caveat. An unscoped ban re-breaks open **P1 #2304**. | Technical | High | Open |
| C-007 | No `profile-invocation dispatch` alias | #2984 is fixed by help text only. The alias option would regenerate `_completion_manifest.json`, breaking C-005 disjointness. | Technical | Medium | Open |

### Key Entities

- **Status event**: an append-only record in `status.events.jsonl`. The reducer imposes a **total
  order on `(at, event_id)`** — file position is not semantically significant. Same-`at` events are
  arbitrated by `_should_apply_event`, which today handles only rollback-vs-forward.
- **Birth-cutover seed**: a synthesized historical event. Id is `deterministic_ulid(mission_id|wp_id|
  field)` — hash-derived, excludes `at`, so re-runs are idempotent but re-anchoring breaks verify.
  Its `at` comes from the anchor chain: `_claim_anchors` (first `claimed`, else **earliest transition
  of any lane**) → `_synthesize_claim_anchor` (`shell_pid_created_at`, else `meta.json.created_at`).
- **Profile-load surface**: any shipped prompt artifact instructing an agent how to obtain a profile.
- **Resolver-backed profile read**: obtained through `AgentProfileRepository` resolution, honouring
  lineage, overlays and `enhances`/`overrides` — as opposed to a raw file read.

## Success Criteria *(mandatory)*

- **SC-001**: On a **synthetic drifted fixture** containing missions that genuinely still need seeding
  AND carry terminal transitions, zero terminal WPs change lane after accept — with an explicit
  non-vacuity assertion that the fixture reds on the unfixed code. *(The committed dogfood corpus is
  a dead oracle: a dry-run over all 324 missions yields 323 "nothing new to seed" and 1 "no tasks/
  directory" — zero can seed, so zero can rewind, before any fix.)*
- **SC-002**: A second accept on an unchanged tree converges in each mutating mode.
- **SC-003**: Zero tracked doctrine prompt surfaces name a raw `.agent.yaml` read as the **primary**
  profile-load mechanism; any remaining fallback is #2304-scoped and caveated.
- **SC-004**: The styleguide `good_example` and the published `docs/` occurrences name real commands.
- **SC-005**: `"dispatch"` appears in `profile-invocation`'s help output.
- **SC-006**: The #2985 reproduction's node id is named in the PR body, with committed evidence of
  failing at the merge base and passing after.

## Assumptions

- The lever is the anchor chain, the seed set, or the same-timestamp precedence rule — **not** file
  placement, which the corrected mechanism shows is inert. C-002 is open; `/plan` decides on evidence.
- `spec-kitty agent tasks status` is the replacement for #2983. Both resolver commands named in US2
  were verified to exist (`profiles_cmd.py:319`, `charter/context.py:28-30`).
- #2984's CLI is not defective; verified working during triage.

## Out of Scope

- **#2304** (read-only harness cannot invoke the CLI) — not solved here; C-006 ensures this mission
  does not *worsen* it.
- **#2399** structural profile loading. Complementary; #1840 is its prompt-level stopgap. The guard is
  expected to **survive** #2399, because prompt surfaces still ship to harnesses outside the
  structural path.
- **#2957 / CI shard vacuity** at large. FR-006 closes the hole for *this* P0 only.
- **#2400** (#1840's parent epic), **#2961** (skills prescribing a retired path — same defect class as
  #2983, deferred to keep this mission bounded), **#2527 / #2748 / #2690** (generated-skill
  propagation, which owns the half of #1840 that NFR-003 deliberately does not enforce).
- Archived `kitty-specs/` snapshots (C-004).

## Delivery sequencing note

Three P0s are open concurrently: #2985 (this mission), #2962, #2939. #2985 is sequenced first because
it is the only one that **persists** corruption into an acceptance commit, and it is a fresh
regression from a just-merged PR, so the fix window is cheapest now.

## Change Classification

Classified **`bulk_edit`** (`meta.json`), reversing the first draft's declination.

The first draft argued the occurrences were "prose requiring individually authored replacements
rather than a uniform identifier substitution". That answers a question DIRECTIVE_035 does not ask.
Its predicate is *"does this require changing the same existing string in more than one file?"* — and
the path literal `src/doctrine/agent_profiles/built-in/…` changes in at least four tracked files, with
`manual_review` being a first-class action precisely for individually-authored replacements. The
directive's tie-break is *"if uncertain, treat as bulk edit"*. The declination was also recorded only
in prose, so it was not machine-visible — contradicting its own claim to be reviewable.

The occurrence map and the guard are **orthogonal, not substitutable**: the map enumerates today's set
(including the benign `.agent.yaml` data-references that must be classified `do_not_change`); the
guard prevents tomorrow's. Both are in scope. `occurrence_map.yaml` is produced at plan.
