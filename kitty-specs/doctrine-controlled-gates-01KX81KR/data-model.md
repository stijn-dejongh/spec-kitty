# Data Model: Doctrine-Controlled Transition Gates

All models are frozen / `extra="forbid"` unless noted. Fields marked **(new schema)** land behind a versioned evolution + migration (FR-016, C-006).

## GateBinding **(new schema — on the step contract)**
The declarative unit charter activation selects.
| Field | Type | Notes |
|-------|------|-------|
| `transition` | str | the lane/action the gate fires on (e.g. `for_review`) |
| `gate_ref` | URN | `urn:gate-handler:<id>` (Path A) or `urn:asset:<id>` (Path B) |
| `mechanism` | enum `handler\|asset` | which dispatch path |
| `on_unrunnable` | enum `warn` (default) | reserved; fail-open is the only value this mission ships |
Carried on `MissionStepContractStep` and unified `MissionStep`.

## ResolvedGate (runtime, produced by the SSOT seam)
| Field | Type | Notes |
|-------|------|-------|
| `binding` | GateBinding | source binding |
| `declaring_doctrine` | str | for observability (FR-018) |
| `dispatch` | HandlerRef \| AssetRef | resolved target |
| `activation_state` | enum `active\|inactive\|refused` | why it will/won't run |

## TransitionContext (runtime input to a gate)
The shared input shape passed to a handler's `run(ctx)` and to a Path-B asset's entrypoint. One definition, both dispatch paths.
| Field | Type | Notes |
|-------|------|-------|
| `mission_id` | str | the mission crossing the transition |
| `transition` | str | lane/action key (e.g. `for_review`) |
| `changed_files` | list[str] | the WP's changed set (input to `ScopeSource`) |
| `scope` | Scope \| None | derived scope (may be None → `no_coverage`) |
For Path-B it is passed via a controlled channel (argv/stdin/**allowlisted env** — never shell-interpolated); never the ambient process env.

## GateVerdict (emitted by a handler/asset)
| Field | Type | Notes |
|-------|------|-------|
| `status` | enum `no_new_failures\|regression\|no_coverage\|error` | |
| `blocking` | bool | only `regression && blocking` may BLOCK (C-002) |
| `message` | str | operator-facing; MUST NOT leak internal module/paths |
| `scope_evidence` | opt str | what was checked (for observability) |

## OperatorOutcome (FR-014 — reducer output; the only thing that gates the transition)
`BLOCK` | `FAULT_WARN` | `CALM_NOTICE` | `TRUST_REFUSAL` | `PASS`. See contracts/gate-verdict-and-outcomes.md for the mapping table.

## GateHandler (Path A — shipped in spec-kitty)
| Field | Type | Notes |
|-------|------|-------|
| `id` | str | `urn:gate-handler:<id>` |
| `run(ctx) -> GateVerdict` | callable | no doctrine code; no opt-in |
| `config_keys` | list[str] | e.g. `review.fail_on_pre_review_regression`, `review.test_command` (FR-017) |

## GateAsset **(new schema — executable ASSET, Path B)**
Extends the **existing** `AssetManifest` (`src/doctrine/assets/models.py`, `extra="forbid"`)
with an executable shape, keyed so non-gate assets stay inert (C-003). IC-06 **extends**
that model + `pack_validator._validate_asset_manifests` — it is NOT greenfield.
| Field | Type | Notes |
|-------|------|-------|
| `id`, `mime`, `path` | (existing) | inherited from AssetManifest |
| `entrypoint` | str | module:function or script path within the asset |
| `interpreter` | enum (allowlisted) | e.g. `python`; no shell |
| `verdict_channel` | const | GateVerdict emitted on a **dedicated, size-capped, schema-validated** channel — NOT shared stdout; stray stdout can't forge a verdict (FR-019) |

## ScopeSource (doctrine-declared strategy)
| Field | Type | Notes |
|-------|------|-------|
| `derive(changed_files) -> Scope` | callable | portable; spec-kitty's filter-group/census model is one built-in impl (FR-009) |
| built-in id | str | active only when spec-kitty's own doctrine is active (FR-012) |

## TrustEnvelope (Path-B gating; FR-007/FR-015; refuse-unconfinable v1, RD-006)
| Field | Type | Notes |
|-------|------|-------|
| `provenance` | enum `built_in\|org_pack\|third_party` | **derived** from pack-load metadata, never self-declared; **loader must stop overwriting `source_kind`** (`org_pack_loader.py:403`) so `third_party` is producible/refusable — else NFR-004a/SC-012 untestable (C-008) |
| `allow_flag` | bool | `review.allow_executable_gate_assets`, default off |
| `interpreter_allowlist` | set[str] | no shell interpolation; argv-vector |
| `env_allowlist` | set[str] | explicitly constructed child env — **never `dict(os.environ)`** inheritance (C-008) |
| `timeout_s` | int | default mirrors baseline (~300) |
| `process_group_kill` | bool=true | timeout kills the whole process group (grandchildren), not just the direct child |
| `rlimits` | policy | `setrlimit` CPU/memory/output-size caps applied before exec |
| `fs_confinement` | policy | **path-resolved (symlink-safe)** scratch/working-tree writes only |
| `capability_probe` | policy | probes fs/network confinability; if unconfinable → REFUSE (never run unconfined → TRUST_REFUSAL). Deeper OS sandbox (namespaces/landlock/seccomp) deferred — no new dep (RD-006) |

## Relationships
`StepContract` 1—* `GateBinding` —selected-by→ `CharterActivation` → `ResolvedGate`
→ dispatch(`GateHandler` | `GateAsset`+`TrustEnvelope`) → `GateVerdict`
→ `FR-014 reducer` → `OperatorOutcome` (the transition's only gate).
`ScopeSource` feeds a handler/asset that runs tests; absent/undeclared → `CALM_NOTICE`.
