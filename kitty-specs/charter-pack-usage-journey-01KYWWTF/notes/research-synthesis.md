# Research Synthesis — Charter Pack Usage Journey (Mission 2 of 2)

Source: 2-lens research squad (architect-alphonso = architecture + reproduced journeys; paula-patterns =
related-issues + campsite), read-only against `feat/charter-pack-usage-journey` (based on the M1
`doctrine-built-in-seam-consolidation` branch). Scope: #3104 (P1), #3105 (P2), #3118 (tech-debt).

## Root cause (reproduced end-to-end)

`charter pack apply` writes the **activation write store** (`config.yaml` `activated_*`, or the pointed-at
`charter.yaml` when a `charter:` pointer exists) but nothing compiles it into the **compiled bundle**
(`.kittify/charter/charter.yaml` — the read authority). `charter.md` is a **display-only** companion
(corroborated in-tree: `freshness/computer.py:10-13`, `compact_governance.py:47-65`). Reproduced:
- empty repo → `is_charter_empty=True` → generic-agent net fires.
- `charter pack apply minimal` → config.yaml gains `activated_*`, NO bundle, NO pointer → `is_charter_empty`
  flips **False** → `resolve_generic_fallback` returns None → router runs → **ROUTER_NO_MATCH (#3104)**;
  `charter context` → "Charter file not found"; `charter status` → available:False (**#3105**).
- `charter generate --no-from-interview` (the compile, no interview) → materializes `charter.yaml` +
  seeds `charter.md` + migrates config→`charter:` pointer → context/status/freshness all correct.

## Bridge decision — OPTION (a), validated

`compile_charter`/`write_compiled_charter` (`compiler.py:325/440`) already lower config.yaml `activated_*` →
`charter.yaml` with NO interview (exposed as the CLI command `spec-kitty charter generate`). M2 does NOT
build a compiler — it wires `apply` to the existing seam and retargets the read gates. **Reject option (b)**
(read surfaces read config.yaml directly): re-creates the multi-authority smell (5+ readers re-deriving)
and can't serve pointer-migrated projects. `charter.yaml` stays the single derived read-cache;
config.yaml/pointer the single write authority.

**Shape: `apply --compile` opt-in + truthful default output.** Auto-compiling inside `apply` is too heavy
and changes its contract — `generate` hard-requires a git worktree (`generate.py:314`), seeds `charter.md`,
creates `library/`, writes `.gitignore`, git-stages, and migrates config→pointer. So default `apply` stays
a pure additive merge (git-agnostic) but its output **names the exact next command** (`spec-kitty charter
generate`; today `pack.py:200-205` hand-waves "a compile may still be needed"); `--compile` chains
`generate --no-from-interview` after the merge (inheriting the git-worktree requirement, documented).

## Read-surface retarget list (charter.md-presence → charter.yaml authority)

HARD gates to RETARGET (produce the #3105 symptoms):
- `src/charter/context.py:286` — bootstrap gate on `CHARTER_MD` → retarget to `charter.yaml` presence;
  render `charter.md` prose only when present (graceful-degrade like `_compact_section_block`).
- `src/specify_cli/cli/commands/charter/_common.py:27 _resolve_charter_path` — raises on `charter.md`
  absent; consumed by `_status_collectors.py:62`. **Add a SIBLING `_resolve_charter_bundle_path`
  (charter.yaml)** and point only the presence/"governance exists" gates at it — do NOT retarget the
  shared `_resolve_charter_path` in place (also used by `status.py`, `resynthesize.py`).

SOFT retarget: `src/charter/context_json.py:81-93 _project_charter_json_block` — report `charter.yaml`
presence as the primary signal (charter.md becomes secondary display).

DO NOT retarget (legitimately charter.md prose — the #3094/#3095 boundary): `context.py:397-399` the
`--include section:<id>` selector renders prose that only exists in `charter.md`. Keep it bound (the
compile seeds `charter.md`, so it resolves post-bridge). Already-correct, change nothing:
`freshness/computer.py`, `compact.py`, `compact_governance.py`.

## The SECOND directive authority — retire the catalog-fallback (no-legacy-resolver-paths)

`resolver.py:233-260 _resolve_directives_selection` catalog-falls-back to `sorted(doctrine_catalog.directives)`
= ALL built-ins when `governance.selected_directives` is empty (which it is after apply+compile, since
compile writes `catalog`/activation but not the `governance.selected_directives` prose). Reproduced: apply
minimal (5 directives) + compile → `resolve_project_governance().directives` returned **29** with
`directives_source='catalog_fallback'`, while the activation-aware context bundle correctly delivered 5.
**Retire the catalog-fallback; source the fallback from the config-activated set (the compiled
catalog / `PackContext` authority)** so `resolve_project_governance` stops being a second, divergent
directive authority. (This is the RED test today.) Its 5 consumers — `prompt_builder.py:437`,
`runtime/doctor.py:133`, `context_json.py:139`, `compact.py:303`, `resolver.py:415` — carry no charter.md
pre-gate; only the fallback source changes.

## The dispatch predicate (#3104) — corrected, org-pack-safe

Seam: `executor.py:326-328` `fallback_decision or self._router.route(...)`. `resolve_generic_fallback`
short-circuits before the router; `is_charter_empty` (`empty_charter.py:48-67`) decides whether the router
runs. A PURE `charter.yaml`-presence predicate is NOT #3064-safe — it would fire the net for an org-pack
project that has routable profiles WITHOUT a bundle (regression). Correct predicate splits
governance-emptiness from dispatch-routability:
```
def is_charter_empty(repo_root) -> bool:
    if (repo_root/".kittify/charter/charter.yaml").exists():
        return False                                   # compiled bundle → configured
    pc = PackContext.from_config(repo_root)
    if pc.org_roots != ():          return False        # org packs → router-routable
    if pc.activated_agent_profiles is not None: return False  # explicit profiles → routable
    return True
```
Behaviour matrix: empty→net fires; apply-no-compile→net fires (**#3104 fix**); apply+compile→net off, router
runs (NO_MATCH honest); org-pack no-compile→net off (router matches org profiles, no regression);
agent-profile activation→net off.
- **Drops the non-routing dimensions** (directives/tactics/toolguides/procedures/paradigms/styleguides/
  step-contracts/**glossary-packs**) from the net predicate — retires WS-C's P-D (no dimension-set to keep
  set-equal) and **folds #3118** (the double config-load collapses to one `stat()` + at most one
  `PackContext.from_config`, only when the bundle is absent).
- **DECISION to record:** this **intentionally reverses the glossary-pack dimension of #3064** — a
  glossary-only project with no bundle now fires the net (generic-agent). More correct (a glossary adds no
  routable profile), but a deliberate behaviour change, not a slip. "Empty" means **bundle ABSENT**, never
  "bundle present but activations empty" (a bootstrapped-empty `charter.yaml` keeps the net OFF — pin a
  test; inspecting bundle *contents* would re-import the #3064 exhaustiveness trap).

## Related issues (fold / conflict / separate)

- **#3104, #3105 — CORE M2.** **#3118 — FOLD** (dissolved by the bundle-presence predicate).
- **#3106 — SEPARATE (M1/WP05).** Activation-vocab unification + the live glossary drift fix. NOT M2.
- **#3107 — PARTIAL FOLD:** the journey-doc portion (document apply→generate + empty-charter dispatch in the
  journey guides) folds; the inert CLI-reference parity gate is separate docs-infra.
- **#3094 / #3095 — CONFLICT-ADJACENT (boundary):** `charter context --include section:terminology-canon`
  parses `charter.md` prose (`context.py:397`) — M2 must NOT retarget the section-selector prose reader,
  only the presence gate (`context.py:286`).
- **#2831 (P0) — verify post-M2** (same disjoint-store family; may close as a side-effect; don't fold).
- **#3092 / #3045 / #2992 / #2213 / #2940 / #3009 / #3052 — SEPARATE.** #3092/#3045 are pre-existing red
  baselines (classify vs merge-base, never green-wash).

## A FOURTH config→bundle producer — must converge (cross-mission)

`m_unify_charter_activation_finalize.apply()` (`m_...finalize.py:384-396`) already mints `charter.yaml` from
bare config activation when the bundle is absent AND strips `activated_*` from config.yaml — a latent
parallel lowering to M2's `apply --compile`. **M2 must assert the two converge** (same shape) or document
the migration as the upgrade-time equivalent, so the config→bundle transform is one authority, not two.

## C-004 — hard dependency on Mission 1

M2 is sequenced AFTER M1 and its branch is BASED ON the M1 branch. Two couplings:
1. **Shared file:** M1 WP02 owns `src/charter/resolver.py` (built-in-reader migration + operator-string
   repoint at :187/:250). M2's `_resolve_directives_selection` retarget edits the same file — M2 must NOT
   repoint those operator strings (M1 owns them) and must re-verify M1's resolver changes before layering.
2. **Activation-store trust:** M2's resolver-fallback-from-activated-set trusts M1/FR-010 having unified the
   activation vocabulary onto `YAML_KEY_MAP` and fixed the live `activated_glossary_packs` drift. M2 spec
   constraint: "Depends on M1 FR-010; the resolver-fallback retarget trusts the unified activation store."

## Campsite (clean WHILE M2 edits these files — no scope creep)

- `empty_charter.py`: the composite predicate + its 20-line dimension-enumeration docstring + the
  `charter_activated_urns`/`PackContext` imports become dead — delete; update `_MATCH_REASON` to the
  bundle-presence rationale so the warning panel doesn't lie.
- `pack.py`: hoist the `resolve_builtin_pack_path` resolve-or-exit try-block duplicated 4× (list/path/apply)
  if `apply` grows a compile branch.
- `context.py:286` vs `:333/:397`: introduce a distinct bundle-presence resolution; leave prose readers on
  `CHARTER_MD` — do NOT collapse both onto one path constant (whack-a-field that would break #3094/#3095).
- Do NOT re-touch `compiler.py:529-534/627-634` duplicated constants (M1/WP05 debt) or the resolver
  operator strings (M1/WS-A).

## Journey acceptance tests (8)

1. #3104 apply-no-compile keeps the net (generic-agent, NOT ROUTER_NO_MATCH).
2. #3104 apply+compile disengages the net (router runs; NO_MATCH honest).
3. #3104 org-pack composite-safety regression guard (org pack, no bundle → net stays off).
4. #3105 context — bundle authority (renders the 5 activated directives; delete `charter.md` → still renders).
5. #3105 status — SYNCED on `charter.yaml` authority (survives `charter.md` deletion).
6. Resolver single-authority — `resolve_project_governance().directives` returns the 5 activated, not 29
   catalog-fallback (RED today).
7. Truthful output — default `apply` names `spec-kitty charter generate`; `--compile` states it compiled.
8. #3118 perf (advisory) — `is_charter_empty` on an unconfigured repo does ≤1 `PackContext.from_config` + 1
   `stat`, no URN load.

---

## OPERATOR FOLD (2026-08-01) — #3095, #3096, #3102 pulled into M2 scope

Per operator direction, three adjacent charter/doctrine tooling & CI items are folded into this mission
(now FR-010/011/012, User Story 4, SC-007). This **revises** two verdicts in the related-issues table above:

- **#3095 (+ its twin #3094) — was "CONFLICT-ADJACENT boundary", now IN SCOPE (FR-010).** The advertised
  section selectors `section:terminology-canon` / `section:code-review-checklist` (which generated prompts
  and action-context *require*) fail with "No charter section found for selector". M2 now owns making them
  resolve to the corresponding compiled section — OR stopping the doctrine templates/surface from
  advertising a selector the CLI cannot resolve. IMPORTANT: this fix stays on the `charter.md`/section
  *prose* path (`context.py:397`); it is a SEPARATE change from FR-005's presence-gate retarget, and does
  NOT collapse the prose reader onto `charter.yaml` (C-003 still holds — the two changes touch two paths).
  Plan-phase investigation: determine whether these sections should be produced by the charter compile
  (provide them) or the selectors are stale in the mission-step prompts (stop advertising) — likely the
  former for terminology-canon (maps to the glossary/terminology surface).
- **#3096 — new fold (FR-011).** Documented `spec-kitty analyze` command is absent; only `agent mission
  record-analysis` works. Missing-CLI-command-is-a-gap: expose a thin alias OR redirect the skill/mapping/
  docs to the supported command. Small, self-contained CLI-surface fix.
- **#3102 — was "SEPARATE (deferred, gated on seam work + #3101)", now IN SCOPE (FR-012).** Path-filtered
  CI workflow for `src/doctrine/**` + `src/charter/**`. Its seam-work prerequisite is satisfied once M1
  lands (M2 is based on M1); it does NOT require #3101 (wheel-split). New surface: `.github/workflows/`.

These do not change the core bridge/predicate/resolver design; they are additive. The C-001 (M1
precondition) and C-002 (shared resolver.py) constraints are unaffected.
