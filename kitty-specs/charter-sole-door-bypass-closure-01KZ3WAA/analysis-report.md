---
schema_version: 1
artifact_type: spec-kitty.analysis-report
command: /spec-kitty.analyze
mission_slug: charter-sole-door-bypass-closure-01KZ3WAA
mission_id: 01KZ3WAAFPWQAG3R21P1RY0M6R
generated_at: '2026-08-03T14:48:32.156122+00:00'
analyzer_agent: unknown
input_artifacts:
  spec.md:
    path: /home/stijn/Documents/_code/SDD/fork/SHADOW_CLONES/spec-kitty_FOUR/kitty-specs/charter-sole-door-bypass-closure-01KZ3WAA/spec.md
    sha256: 396779d5230cfdf08b204facd195852120c83d526036c0a2e6be97938014f592
  plan.md:
    path: /home/stijn/Documents/_code/SDD/fork/SHADOW_CLONES/spec-kitty_FOUR/kitty-specs/charter-sole-door-bypass-closure-01KZ3WAA/plan.md
    sha256: 823415696594d3ce4f560c97e14879bfffc1a8734a94feed74172ac4c59694ae
  tasks.md:
    path: /home/stijn/Documents/_code/SDD/fork/SHADOW_CLONES/spec-kitty_FOUR/kitty-specs/charter-sole-door-bypass-closure-01KZ3WAA/tasks.md
    sha256: d97583ecbeba8623f2488a579b6eeb56265ed1fd66e23d2c00e4949abef9e449
  charter:
    path: /home/stijn/Documents/_code/SDD/fork/SHADOW_CLONES/spec-kitty_FOUR/.kittify/charter/charter.yaml
    sha256: ee1ff523dab5f9297c5b4062c0c84dfe2c4bbc5ac6b8b384fed0288485b86534
verdict: blocked
issue_counts:
  critical: 1
  medium: 5
  low: 0
  high: 0
  info: 0
findings:
- id: A1
  severity: critical
  category: charter
  summary: quickstart.md and WP02 use the forbidden --feature CLI flag instead of --mission (terminology canon).
- id: F1
  severity: medium
  category: inconsistency
  summary: spec.md FR-001/FR-010 and contracts/charter-doctrine-service-contract.md still cite get_ancestors(), superseded by the post-tasks squad's get_provenance()/register_overlay()-only correction.
- id: F2
  severity: medium
  category: inconsistency
  summary: spec.md FR-001 still frames profile_resolution.py:81 as a site to eliminate, contradicting the corrected WP02 T010 (confirm bootstrap case, do not migrate).
- id: F3
  severity: medium
  category: inconsistency
  summary: spec.md FR-006/Key Entities and plan.md IC-04 describe mission-type gating as touching MissionTypeProfileRepository's own file; corrected WP08 scopes to resolve_mission_type_context() only to avoid a WP06 ownership overlap.
- id: F4
  severity: medium
  category: inconsistency
  summary: spec.md FR-008's sequencing note describes the pre-restructure staged 3-kind/9-kind proof across two WPs, which no longer exists after WP01+WP07 merged.
- id: E1
  severity: medium
  category: coverage
  summary: NFR-004 (CHANGELOG entry required per DIR-009) has zero associated task across all 9 WPs.
---

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Charter | CRITICAL | quickstart.md:78; tasks/WP02-migrate-agent-profile-repository-sites.md:102 | Both use `spec-kitty agent tasks status --feature <fixture>`. The charter's Terminology Canon (§"Regression Vigilance") lists `--feature` as a forbidden CLI flag for new code/docs and requires `--mission` in every command example. Confirmed live: `spec-kitty agent tasks status --help` shows the real flag is `--mission`, not `--feature`. | Replace `--feature <fixture>` with `--mission <fixture>` in both files. |
| F1 | Inconsistency | MEDIUM | spec.md:276 (FR-001), spec.md:284 (FR-010), contracts/charter-doctrine-service-contract.md:41 | These three locations still list `get_ancestors()` as part of the lineage/mutation accessor's surface. The post-tasks adversarial squad (debugger-debbie) verified `get_ancestors()` is unused by any real call site — `projection.py` needs only `register_overlay()`; `registry.py`/`org_profiles.py` need `get_provenance()` (named nowhere in spec.md). Only the corrected WP01/WP02/WP04 task prompts carry the accurate method list. | Update FR-001, FR-010, and the contract file to name `register_overlay()` and `get_provenance()` specifically; drop `get_ancestors()`. |
| F2 | Inconsistency | MEDIUM | spec.md:276 (FR-001) | FR-001 lists `src/charter/profile_resolution.py:81` among the "5 ... sites to eliminate." The post-tasks squad found this site is a zero-argument, module-level cached function with no `repo_root` to build a factory from — a genuine bootstrap carve-out, not a migration target. WP02's T010 was corrected to "confirm and document, do not migrate." | Reword FR-001 to describe 4 sites eliminated + 1 site (`profile_resolution.py:81`) confirmed as a bootstrap carve-out and documented, not migrated — matching WP02's corrected scope. |
| F3 | Inconsistency | MEDIUM | spec.md:281 (FR-006), spec.md:317-318 (Key Entities), plan.md:236 (IC-04) | These describe mission-type activation gating as touching both `charter.mission_type_profile_repository.MissionTypeProfileRepository` and `charter.mission_type_profiles.resolve_mission_type_context()`. The post-tasks squad rescoped WP08 to touch ONLY `resolve_mission_type_context()` in `mission_type_profiles.py`, explicitly not editing `mission_type_profile_repository.py` (which is WP06's exclusive ownership for an unrelated change) to avoid a real ownership overlap. | Tighten FR-006, the Key Entities bullet, and plan.md's IC-04 to name `resolve_mission_type_context()` as the sole implementation site. |
| F4 | Inconsistency | MEDIUM | spec.md:283 (FR-008) | FR-008's "Sequencing note" says the builder-unification proof "can only assert identical output across the 3 kinds gated before FR-005 lands" and must not be scheduled before FR-005 — describing the original 3-way WP01/WP05/WP07 split where FR-008 and FR-005 landed in separate, sequenced WPs. After the post-tasks squad merged former-WP07 into WP01, WP01's T004 now proves identical output across all 9 gated properties in ONE pass, in the same WP as the 6 new properties — the staging problem this note describes no longer exists. | Remove or rewrite the sequencing note to reflect the merged WP01, where FR-008's proof is unstaged. |
| E1 | Coverage | MEDIUM | spec.md NFR-004; no matching task in tasks.md or any WP file | NFR-004 requires "CHANGELOG entry (per DIR-009)" documenting three named behaviour changes. A repo-wide grep for "CHANGELOG" across all 9 WP prompt files returns zero matches — no subtask updates `CHANGELOG.md`. | Add an explicit CHANGELOG.md update subtask (most naturally in WP01, which introduces the most user-visible behaviour change — activation gating extended to 9 kinds — or as a small addition to WP10's closeout scope). |

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| C-001 (single canonical authority) | Yes | WP01 (all) | |
| FR-001 | Yes | WP02 (T007-T010) | See F2: T010 confirms-not-migrates |
| FR-002 | Yes | WP03 (T011-T014) | |
| FR-003 | Yes | WP05 (T018-T021) | |
| FR-004 | Yes | WP06 (T022-T025) | |
| FR-005 | Yes | WP01 (T026-T032) | |
| FR-006 | Yes | WP08 (T034-T036) | See F3: file scope narrower than spec text |
| FR-007 | Yes | WP04 (T017), WP06 (T040), WP09 (T037-T039) | Split across 3 WPs by design (post-tasks squad) |
| FR-008 | Yes | WP01 (T002-T004) | See F4: sequencing note stale |
| FR-010 | Yes | WP01 (T001), WP04 (T015-T017) | See F1: method names stale in spec text |
| FR-011 | Yes | WP10 (T042-T043) | |
| NFR-001 | Yes | WP09 | |
| NFR-002 | Implicit | all WPs (Test Strategy: `mypy --strict`) | Cross-cutting, not a dedicated task — expected |
| NFR-003 | Yes | WP09 | |
| NFR-004 | **No** | — | See E1 |
| NFR-005 | Yes | WP02 (T006, T009) | |

**Charter Alignment Issues:**

- A1 above (terminology canon, `--feature` vs `--mission`) is the only direct charter-principle conflict
  found. No other MUST-level charter rule is violated by spec.md/plan.md/tasks.md as currently written.

**Unmapped Tasks:** None — every `Txxx` in `tasks.md`'s Subtask Index maps to a WP with at least one
`requirement_refs` entry, and `spec-kitty agent tasks map-requirements`'s own coverage check reports
`unmapped_functional: []`.

**Metrics:**

- Total Requirements (FR+NFR+C): 11 FR + 5 NFR + 6 C = 22
- Total Tasks: 43 subtasks across 9 WPs
- Coverage % (FR/NFR with >=1 task, excluding process-only Constraints): 15/16 = 93.75% (NFR-004 is the one gap)
- Ambiguity Count: 0 (no vague adjectives or unresolved placeholders found)
- Duplication Count: 0
- Critical Issues Count: 1 (A1)
