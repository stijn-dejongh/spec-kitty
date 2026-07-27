# Mission Specification: Annoying Bugs Sweep

**Mission Branch**: `fix/annoying-bugs-sweep`
**Created**: 2026-07-27
**Status**: Draft
**Input**: Operator request — "Address these all in an annoying bugs mission": #2985, #1840, #2983, #2984.

## Intent Summary

Four defects share one shape: **a surface that looks authoritative but silently misdirects.**

One misdirects *data* — `spec-kitty accept` writes a historical claim event after a work package's terminal transition, so a finished WP reads back as `claimed` (#2985, P0, confirmed live on `main` at `d0a5bacf7`). Three misdirect *agents* — profile-load surfaces instruct raw `.agent.yaml` reads that bypass doctrine resolution (#1840), a plain-language styleguide teaches a command that does not exist (#2983), and the invocation lifecycle opens under one command path but closes under another (#2984).

The unifying acceptance property: **no shipped surface may confidently assert something false.** For #2985 the false assertion is machine state; for the other three it is an instruction to an agent.

Primary actor is a Spec Kitty operator or a delegated agent. The rule that must always hold: a work package that has legitimately reached a terminal lane never silently leaves it, and no shipped prompt surface instructs a command or mechanism that cannot work.

**Scope decisions confirmed with the operator:**
- Single mission covering all four, with the P0 sequenced first so it can be cherry-picked out if it must land ahead of the rest.
- #1840 taken at full depth: surface fixes **plus** the regression guard.
- Landing branch cut fresh from `upstream/main`, PR-bound.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A finished work package stays finished (Priority: P1)

An operator runs `spec-kitty accept` on a mission whose work packages are all approved or done. Today, if any WP carries legacy frontmatter runtime state, the accept-time birth-cutover seeds a historical `planned -> claimed` transition and appends it *after* that WP's real terminal transition. The reducer replays in order, so the WP's canonical lane resolves to `claimed`. Accept stops converging, the mission cannot proceed to lane consolidation, and the corrupting write is captured in the acceptance commit — persisted, not transient.

**Why this priority**: It is the only defect here that corrupts user data. It fires on the terminal lifecycle seam, at the exact moment a mission is supposed to become final, and it is live on `main` today.

**Independent Test**: Accept a mission whose WPs carry legacy frontmatter runtime state; assert every WP's canonical lane after accept is unchanged, and that a second accept converges.

**Acceptance Scenarios**:

1. **Given** a mission whose WP01 has reached `done` and carries legacy frontmatter runtime state, **When** `spec-kitty accept` runs on the real-commit path, **Then** WP01's canonical lane is still `done` and no `planned -> claimed` transition for WP01 has been appended after its terminal transition.
2. **Given** that same mission after a first successful accept, **When** `spec-kitty accept` runs a second time, **Then** the gate converges (`summary.ok`) and reports no outstanding work packages.
3. **Given** a mission being accepted, **When** accept completes, **Then** the mission event count is unchanged by the cutover stamp unless the stamp had genuinely new runtime state to record.
4. **Given** a mission that has genuinely never been cut over and carries no terminal transitions, **When** the cutover stamp runs, **Then** it still seeds the runtime state it is responsible for — the fix must not disable the feature.

---

### User Story 2 - A delegated agent loads the profile it was actually assigned (Priority: P2)

An orchestrator delegates work to a subagent under a named profile. Shipped prompt surfaces instruct the agent to read the profile's `.agent.yaml` directly. That read bypasses doctrine resolution — `specializes_from` DRG lineage, pack overlays, and `enhances` (field-merge) versus `overrides` (full replacement) semantics. For a built-in profile with shallow lineage the raw read happens to match; for a pack-extended or specialized profile it silently yields a *different* profile, with no error and no warning.

**Why this priority**: Silent divergence with no failure signal, and the blast radius grows with the 3.3.x pack ecosystem. Not P1 because built-in profiles have shallow lineage today, so the divergence is largely latent, and #2399 tracks the structural fix that would make prompt wording moot.

**Independent Test**: Grep every shipped prompt surface for an instruction to read `agent_profiles/**/*.agent.yaml` as a profile-load mechanism; assert zero hits, and that a guard test fails if one is reintroduced.

**Acceptance Scenarios**:

1. **Given** any shipped doctrine prompt surface, **When** it instructs an agent how to load an assigned profile, **Then** it names a resolver-backed command (`spec-kitty agent profile show <id>` or `spec-kitty charter context --include agent-profile:<id>`) and never a raw `.agent.yaml` read.
2. **Given** the `spk-doctrine-profile-load` and `ad-hoc-profile-load` skills, **When** an agent follows either, **Then** exactly one is canonical and the other explicitly defers to it — neither defers back to the other.
3. **Given** a contributor reintroduces a raw-YAML profile-load instruction, **When** the test suite runs, **Then** a guard test fails and names the offending file.
4. **Given** the #1840 ticket body, **When** an implementer reads it, **Then** it no longer states that reading the profile YAML directly is the reliable mechanism, and no longer implies #1636's commands are missing.

---

### User Story 3 - Shipped guidance names commands that exist (Priority: P3)

An agent follows the plain-language styleguide's `good_example`, which instructs `spec-kitty status`. No such command exists in 3.2.6. Separately, an operator opens a governed Op with top-level `spec-kitty dispatch` but closes it with `spec-kitty profile-invocation complete`; looking for the opener where the closer lives yields "No such command", and a competent operator correctly stops rather than hand-rolling — which is exactly how #2984 came to be filed as a CLI defect when the CLI was fine.

**Why this priority**: Wasted agent passes and false bug reports, rather than data loss or silent divergence. Cheap to fix.

**Independent Test**: Assert every command named as a runnable instruction in shipped doctrine resolves against the live command surface; and that `profile-invocation --help` names the opener.

**Acceptance Scenarios**:

1. **Given** the plain-language styleguide's `good_example`, **When** an agent runs the command it names, **Then** the command exists and does what the example claims.
2. **Given** an operator inspecting `spec-kitty profile-invocation --help`, **When** they look for how to open an invocation, **Then** the help text names `spec-kitty dispatch` explicitly.
3. **Given** any command string used as a runnable instruction in shipped doctrine, **When** the guard runs, **Then** every such string resolves against the live command surface.

### Edge Cases

- A mission that has genuinely never been cut over, with no terminal transitions — the stamp must still do its job. This guards against "fixing" the P0 by disabling the feature.
- A WP that legitimately re-opens from a terminal lane via an explicit forced transition — must remain possible. Only the *seeded historical* transition is suppressed.
- Coordination topology, where the seed write leg and the read leg are different directories — the fix must hold on both, since the accept and merge seams are required to produce byte-identical payloads.
- A profile with no lineage at all, where a raw read and a resolved read coincide — the guard must still reject the raw-read *instruction*: correctness by coincidence is not correctness.
- A command named in doctrine prose that is deliberately illustrative or hypothetical rather than runnable — the guard must not fire on it.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Terminal lane is never rewound by a seeded transition | As an operator, I want a work package that reached `done`/`approved` to still read that way after `accept`, so my mission can proceed to consolidation. | High | Open |
| FR-002 | Accept converges on an unchanged tree | As an operator, I want a second `accept` on an unchanged tree to converge, so the terminal seam is idempotent. | High | Open |
| FR-003 | Cutover stamp remains functional for genuine cutovers | As a maintainer, I want the birth-cutover to still seed runtime state where it is genuinely absent, so the fix does not disable the feature it repairs. | High | Open |
| FR-004 | Both cutover seams behave identically | As a maintainer, I want the accept seam and the merge seam to agree after the fix, so the byte-identical-payload contract still holds. | High | Open |
| FR-005 | Profile-load surfaces name a resolver-backed command | As a delegated agent, I want every profile-load instruction to route through doctrine resolution, so I load the profile I was actually assigned. | Medium | Open |
| FR-006 | Profile-load skill supersession is single-directional | As an agent, I want exactly one canonical profile-load skill, so following the current one does not bounce me back to its own legacy alias. | Medium | Open |
| FR-007 | The #1840 ticket body no longer misdirects | As an implementer, I want the ticket's stale advice struck, so I do not implement the very anti-pattern the ticket exists to remove. | Medium | Open |
| FR-008 | Styleguide examples name real commands | As an agent, I want doctrine examples to name commands that exist, so I do not burn a pass on a phantom command. | Low | Open |
| FR-009 | Invocation opener is discoverable from the closer | As an operator, I want `profile-invocation --help` to name `spec-kitty dispatch`, so I can find how to open an Op from where I close one. | Low | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Red-first proof for the P0 | A test reproducing the lane rewind is committed and demonstrated failing against `d0a5bacf7`, then passing after the fix. Both results recorded. | Reliability | High | Open |
| NFR-002 | No new uncovered branches | Every new branch or helper introduced carries a focused test in the same PR; diff coverage on changed lines is at or above the repository's 90% gate. | Maintainability | High | Open |
| NFR-003 | Guard is enumerable, not sampled | The raw-YAML guard scans 100% of shipped doctrine prompt surfaces (`src/doctrine/**` plus the deployed `.agents/skills/**` mirror), not a sampled subset, and names each offending file on failure. | Reliability | Medium | Open |
| NFR-004 | Fix is attributed, not green-washed | Every test this mission turns green is first confirmed failing on the merge base; any pre-existing red is reported as pre-existing and left alone. | Process | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Single cutover authority | The fix must not fork a second writer: the accept and merge seams continue to share one authority, per the existing byte-identical-payload requirement. | Technical | High | Open |
| C-002 | Reducer order-independence is out of scope | Making the reducer order-independent for historical seeds is explicitly **not** the chosen lever — largest blast radius, likely wrong. Recorded as a rejection rather than silently omitted. | Technical | High | Open |
| C-003 | No new top-level `status` command | #2983 is resolved by correcting the example, not by minting a top-level `status`; nothing canonical asks for that command. | Technical | Medium | Open |
| C-004 | Historical artifacts stay immutable | Archived mission artifacts under `kitty-specs/` that reference retired commands are immutable snapshots and are excluded from the sweep. | Technical | Medium | Open |
| C-005 | P0 separable | The P0 work is sequenced first and carries no dependency on the papercut work packages, so it can be cherry-picked out if it must land ahead of them. | Process | High | Open |

### Key Entities

- **Status event**: An append-only record in `status.events.jsonl` carrying `from_lane`/`to_lane`, an actor, and optional `policy_metadata`. Order in the file is semantically significant — the reducer replays sequentially and the last transition wins.
- **Birth-cutover seed**: A synthesized historical event reconstructing a work package's pre-eviction runtime state. Its id is a content-namespaced deterministic ULID, so a re-run seeds nothing — but a genuinely absent seed is always written, including when it is no longer chronologically appropriate.
- **Profile-load surface**: Any shipped prompt artifact (skill, procedure, tactic, command template) that instructs an agent how to obtain an assigned agent profile.
- **Resolver-backed profile read**: A profile obtained through `AgentProfileRepository` resolution, honouring `specializes_from` lineage, pack overlays, and `enhances`/`overrides` semantics — as opposed to a raw file read of `.agent.yaml`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Accepting a mission carrying legacy frontmatter runtime state leaves 100% of terminal work packages in their terminal lane — zero rewinds across the dogfood corpus.
- **SC-002**: A second `accept` on an unchanged tree converges in every mutating acceptance mode, matching pre-#2978 behaviour.
- **SC-003**: Zero shipped doctrine prompt surfaces instruct a raw `.agent.yaml` read as a profile-load mechanism, verified by an enumerating guard rather than by inspection.
- **SC-004**: Zero command strings used as runnable instructions in shipped doctrine fail to resolve against the live command surface.
- **SC-005**: An operator who knows only `profile-invocation complete` can discover the opener without leaving `--help`.
- **SC-006**: The #2985 reproduction fails on the merge base and passes after the fix, with both results recorded.

## Assumptions

- The correct lever for #2985 is at the seeding/stamping layer, not the reducer. Three candidate shapes are recorded on the issue; choosing between them is a plan-phase decision, but C-002 rules out the reducer option.
- `spec-kitty agent tasks status` is the replacement surface named by #2983's fix. No top-level `status` is being restored (C-003).
- The #1840 census is accurate as posted and enumerates the full occurrence set. The guard (FR-005/NFR-003) is what converts that from a point-in-time claim into an enforced invariant.
- #2984 is resolved as an ergonomics fix. The CLI is not defective — verified working during triage — so no command is being restored.

## Out of Scope

- #2399's structural fix (tooling loads the profile so prompt wording stops mattering). Complementary and tracked separately; #1840 is explicitly its stopgap.
- Restoring a top-level `spec-kitty status` command (C-003).
- The CI detection gap noted on #2985 — CI reported green while the reproduction fails deterministically on the merged commit. Likely #2957's blast radius; called out there, not fixed here.
- Rewriting archived mission artifacts that reference retired commands (C-004).

## Notes on change classification

This mission rewrites the same *anti-pattern* (a raw-YAML profile-load instruction) across several prompt surfaces, which is adjacent to a bulk edit. It is deliberately **not** classified `bulk_edit`: the occurrences are prose requiring individually authored replacements rather than a uniform identifier substitution, and there is no cross-file breakage risk of the kind DIRECTIVE_035 exists to prevent. Completeness is instead enforced structurally by the FR-005/NFR-003 guard, which is a stronger check than an occurrence map because it keeps holding after this mission ends. Flagged here so the choice is reviewable rather than implicit.
