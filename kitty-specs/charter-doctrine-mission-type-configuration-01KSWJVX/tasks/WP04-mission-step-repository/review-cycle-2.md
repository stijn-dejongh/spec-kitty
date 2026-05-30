---
affected_files: []
cycle_number: 2
mission_slug: charter-doctrine-mission-type-configuration-01KSWJVX
reproduction_command:
reviewed_at: '2026-05-30T20:01:36Z'
reviewer_agent: unknown
verdict: rejected
wp_id: WP04
review_artifact_override_at: "2026-05-30T20:08:15Z"
review_artifact_override_actor: "operator"
review_artifact_override_wp_id: "WP04"
review_artifact_override_reason: "Review passed (reviewer-renata, cycle 2): cycle 1 blocking org-layer path issue resolved — _resolve_org_layer now uses pack_root/mission-steps/{mt_id}/{step_id}/step.yaml per spec, built-in root guard added in both _resolve_org_layer and _collect_org_step_ids helper, regression test test_builtin_pack_root_in_pack_roots_does_not_double_resolve added, docstrings and test fixture corrected, all 29 tests pass"
---

# WP04 Review — Cycle 1

**Reviewer:** reviewer-renata (claude:opus)
**Date:** 2026-05-30
**Verdict:** CHANGES REQUESTED

## Summary

The `MissionStepRepository` implementation is well-structured, the
compound-key isolation guarantee is correctly enforced via `StepKey`,
the three-layer precedence (project > org > built-in) is in place, and
all 28 unit tests pass. The MissionStep field mapping from `step.yaml`
to the WP01 Pydantic model is correct (the `extra="forbid"` configuration
on `MissionStep` is honored because only mapped keys are forwarded for
validation).

However, there is **one blocking path-correctness issue** that violates
the human-mandated severity rule (incorrect/stale file paths in
documentation are BLOCKING). Please address before re-review.

---

## BLOCKING — Org-layer path convention deviates from spec

### Where

- `src/doctrine/missions/mission_step_repository.py`
  - Module docstring, lines 5-6
  - Method `_resolve_org_layer`, docstring lines ~303-305
  - Method body, lines ~307-309
  - Method `resolve_all_for_mission_type`, lines ~253
- `tests/doctrine/missions/test_mission_step_resolver.py`
  - `_write_org_step` helper, line 79

### What the spec / data-model says

`kitty-specs/charter-doctrine-mission-type-configuration-01KSWJVX/data-model.md` line 224:

```
<org-pack-root>/mission-steps/           ← org-layer MissionStep overrides
```

`kitty-specs/.../tasks/WP04-mission-step-repository.md` subtask T025:

> Iterate over `pack_context.pack_roots` in order. For each root, check
> `{root}/mission-steps/{mission_type_id}/{step_id}/step.yaml`.

`spec.md` line 224 likewise documents the org-pack path as
`<org-pack-root>/mission-steps/`.

### What the implementation does

`_resolve_org_layer` and `resolve_all_for_mission_type` look for org-layer
files at:

```
{pack_root}/missions/mission-steps/{mission_type_id}/{step_id}/step.yaml
```

with an extra `missions/` segment that does not appear in any spec or
data-model document. The module docstring (lines 5-6) and method docstring
both encode this incorrect convention.

### Why it matters

1. The WP04 task spec, the data-model document, and `spec.md` are the
   authoritative contract for the org-pack layout. The implementation
   contradicts them.
2. The module docstring is end-user/developer documentation and contains
   a stale/incorrect path. Under the human-mandated severity rule,
   that alone is a blocking finding.
3. WP05 (action-index resolution), WP06 (PackContext consumer), and any
   future org pack producer will now have to choose between obeying the
   documented convention (and breaking against this repository) or
   following this repository's hidden convention (and breaking against
   the documented contract). This is a real cross-WP integration risk.

### What I think happened

I suspect the implementer noticed that `PackContext.pack_roots` from
WP06 (lane-i) is `(<builtin_doctrine_root>, *<org_pack_roots>)` — i.e.
the built-in root `src/doctrine/` is the first entry. Because the
built-in mission-steps live at `src/doctrine/missions/mission-steps/`,
adding `missions/` to the lookup makes the built-in pack_root "just
work" when iterated by the org-layer loop. But that conflates two
distinct layouts: the built-in layout (which lives under
`src/doctrine/missions/`) and the org-pack layout (which the spec
defines as `<org-pack-root>/mission-steps/`, flat).

### How to fix

Pick one of these two paths. Either is acceptable; both unblock review.

**Option A (preferred — match the documented contract):**

- Change `_resolve_org_layer` to look at
  `{pack_root}/mission-steps/{mission_type_id}/{step_id}/step.yaml`
  (drop the `missions/` segment).
- Apply the same change inside `resolve_all_for_mission_type` (the
  collector block for org-layer step_ids).
- In the org-layer loop, **skip the first entry of `pack_roots`** if it
  equals `self._builtin_root.parent` — the built-in root is handled by
  `_resolve_builtin_layer` and must not be re-scanned at the org layer.
  Add a regression test for: "built-in pack_root present in
  pack_roots does not double-count or shadow the built-in layer."
- Update the module docstring (lines 5-6) and `_resolve_org_layer`
  docstring to say `{pack_root}/mission-steps/...` (no `missions/`).
- Update `_write_org_step` and any test fixture so the org tests still
  pass with the correct path.

**Option B (amend the spec to match the implementation):**

- Update `data-model.md` line 224 and `spec.md` line 224 to read
  `<org-pack-root>/missions/mission-steps/`.
- Update the WP04 task spec T025 wording to match.
- Note in the module docstring that the org-pack layout intentionally
  mirrors the built-in layout (`missions/mission-steps/`) so that
  `PackContext.pack_roots` (which includes the built-in root) can be
  iterated uniformly.
- This must be done in coordination with the mission owner — changing
  spec/data-model is a wider scope and should not be done unilaterally
  inside WP04 unless explicitly authorized.

I recommend Option A. It keeps WP04 honest with the existing
charter/spec and avoids retroactively redefining the org-pack contract.

---

## Non-blocking observations (for awareness, not required to address)

1. **Module docstring claim about `extra="forbid"`** — Lines 82-86 say
   "we strip unknown keys before validation." The behavior is correct
   (the mapping dict filters keys before `model_validate`), but the
   word "strip" suggests an active operation. Consider rewording to
   "we only forward known keys to validation" for accuracy. Not blocking.

2. **`resolve_all_for_mission_type` org-layer scan duplication** — Once
   the path fix above lands, the collector inside
   `resolve_all_for_mission_type` will also need its `missions/` segment
   dropped (line 253 in the current source). Already covered by the fix
   guidance above; flagged here so it is not missed.

3. **Test coverage gap** — There is no test that explicitly verifies
   the built-in pack_root entry in `pack_context.pack_roots` does not
   double-resolve at the org layer. Add one as part of the fix.

---

## Acceptance Criteria Status

- [x] `MissionStepRepository.resolve()` returns a layered result —
      correct in principle, but **org-layer path is wrong**.
- [x] Compound-key isolation: software-dev/review shadow does not affect
      documentation/review. (Verified by `TestCompoundKeyIsolation`.)
- [x] `resolve()` returns `None` for unknown steps (does not raise).
- [x] `__all__` declared.
- [x] Tests pass (28/28).
- [ ] **Path convention matches data-model.md / spec.md / WP04 task spec.**
- [ ] `mypy --strict` — not re-run in this review; assumed clean from
      implementer's report.

---

## Re-review checklist

When the fix is ready, please ensure:

1. `_resolve_org_layer` and `resolve_all_for_mission_type` use
   `{pack_root}/mission-steps/...` (no `missions/`), OR the spec/data-model
   are updated per Option B with explicit mission-owner approval.
2. Module docstring and method docstrings reflect the chosen convention.
3. A new test asserts that the built-in pack_root in `pack_roots` does
   not cause double-resolution at the org layer.
4. All 28 existing tests still pass plus the new regression test.
