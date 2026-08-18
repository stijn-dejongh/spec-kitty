# Data Model: Worktree-Aware Root Resolution & Verdict Parity

This mission is behavior-fixing, not schema-adding. The "entities" below are the value objects and invariants the fix introduces or hardens. No persistent storage schema changes; the append-only `status.events.jsonl` format is unchanged (only its audit registration and round-trip guarantee are hardened).

## Entities & Value Objects

### CheckoutKind (new value object)

Classifies the checkout that owns a given working directory. The single source of truth the resolver family consults.

| Field | Type | Meaning |
|-------|------|---------|
| `kind` | enum `{ PRIMARY, LINKED_WORKTREE, STANDALONE_CLONE }` | The classification. |
| `checkout_root` | Path | The root of the *invoking* checkout (where a write should land). |
| `primary_root` | Path \| None | The primary checkout this worktree points into; `None` for `STANDALONE_CLONE` and `PRIMARY` (a clone/primary is its own primary). |
| `git_dir` | Path | Resolved `.git` location (directory for primary/clone; pointer target for a linked worktree). |

**Invariants**
- INV-1: A `STANDALONE_CLONE` (`.git` is a directory, no linking pointer to another checkout) is classified `STANDALONE_CLONE`, never re-anchored to an unrelated `primary_root`. (spec FR-001, SC-003)
- INV-2: For a `LINKED_WORKTREE`, `checkout_root` is the worktree itself; `primary_root` is the main checkout. Write-target resolution defaults to `checkout_root`, never `primary_root`. (spec FR-001)
- INV-3: Classification is a pure function of the filesystem/git state at the invoking CWD; it performs no re-anchoring side effect.

### WriteTarget (new value object)

The decision a mission-state-writing command makes before touching disk.

| Field | Type | Meaning |
|-------|------|---------|
| `target_root` | Path \| None | Where the write lands; `None` when the command must refuse. |
| `decision` | enum `{ WRITE_INVOKING, REFUSE }` | Outcome. |
| `refusal_path` | Path \| None | On `REFUSE`, the checkout path the command *would* have written to — named in the error message. (spec FR-002, NFR-003) |

**Invariants**
- INV-4: `decision == REFUSE ⇒ refusal_path is not None` and the emitted message contains it verbatim. (NFR-003, 100% of refusal paths)
- INV-5: `decision == WRITE_INVOKING ⇒ target_root == CheckoutKind.checkout_root`. No write lands outside the invoking checkout. (SC-001)

### ReviewResult (existing — parity hardening)

The structured verdict carried on a status transition. Already projected by the reducer (`407ea376c4`); this mission does not change its projection (C-001), only its **entry parity** and **audit registration**.

| Field | Type | Meaning |
|-------|------|---------|
| `verdict` | enum (approve/reject/…) | The review decision. |
| `review_ref` | str \| None | Reference to the review artifact. |
| `evidence` | str \| None | Optional evidence pointer. |

**Invariants**
- INV-6: `_parse_review_result_json` is the single validator; `agent status emit --review-result-json` and `orchestrator-api transition` both route through it (identical validation). (spec FR-010)
- INV-7: A WP can reach `done` (incl. the `in_review` exit) via `agent status emit` alone, carrying a `ReviewResult`. (spec FR-010, FR-013, SC-004)
- INV-8: **Round-trip** — no field present in a persisted snapshot is absent from a replay of its event log. (spec FR-015, SC-005)
- INV-9: A review-carrying event row audits clean — `review_result` is a registered shape; no `UNKNOWN_SHAPE`. (spec FR-014, SC-005)

### ForReviewCommitGate (existing — unified)

The invariant guarding the `for_review` transition.

**Invariants**
- INV-10: The gate is one shared implementation enforced identically on both CLI surfaces. (spec FR-011, SC-004)
- INV-11: The gate is topology-aware — a standalone clone is evaluated on commit state, not failed on topology. (spec FR-011)

### ShapeRegistry row (existing — hardened)

The audit descriptor for a persisted event/coordination-key row.

**Invariants**
- INV-12: `review_result` and the coordination-key shape are registered. (FR-014, FR-016)
- INV-13: The drift test makes a real assertion — it fails if a persisted shape is unregistered (no tautology). (FR-016)
- INV-14: After the writer migration, persisted coordination-key rows carry the registered shape (no `UNKNOWN_SHAPE`). (FR-018)

## State Transitions (verdict path — unchanged machine, unified entry)

The 9-lane machine is unchanged. What changes is that **both** entry surfaces can drive the `in_review → approved` edge with a `ReviewResult`:

```
in_progress → for_review → in_review → approved → done
                  ▲             │
        (for_review gate,       │ (ReviewResult path,
         shared+topology-aware) │  both surfaces — FR-013)
```

## Relationships

- `WriteTarget` is derived from `CheckoutKind` (INV-5).
- Every resolver-family function (`find_repo_root`, `resolve_canonical_root`, `predict_lane_worktree`, `locate_project_root`, `_get_main_repo_root`) consumes `CheckoutKind` rather than re-deriving `.git` classification (single canonical authority).
- `ForReviewCommitGate` and `_parse_review_result_json` are shared dependencies of both CLI surfaces (no per-surface copy).
