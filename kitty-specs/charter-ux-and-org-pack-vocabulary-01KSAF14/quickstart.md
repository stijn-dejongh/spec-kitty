# Quickstart — Operator smoke flow

**Mission**: `charter-ux-and-org-pack-vocabulary-01KSAF14`

This document describes the operator-facing smoke flow that proves the mission landed. Each step has a deterministic expected output.

---

## Pre-requisites

- A fresh clone of a Spec Kitty project that ships only `.kittify/charter/charter.md` (no synthesized doctrine yet).
- A second fixture pack repo with a tactic declaring `enhances: <built-in-id>`.

---

## Step 1 — Fresh-checkout freshness reporting (FR-001..FR-005, FR-009)

```bash
cd <fresh-project-clone>
spec-kitty charter status --json | jq '.freshness'
```

**Expected**:
```json
{
  "charter_source":  {"state": "fresh",   "last_change": "...", "remediation": null},
  "synced_bundle":   {"state": "missing", "last_change": null,  "remediation": "spec-kitty charter sync"},
  "synthesized_drg": {"state": "missing", "last_change": null,  "remediation": "spec-kitty charter synthesize"}
}
```

```bash
spec-kitty charter lint --json | jq '.graph_state'
```

**Expected**: `"built_in_only"` (lint falls back to built-in DRG; FR-002).

---

## Step 2 — Preflight detects degradation (FR-006..FR-008)

```bash
spec-kitty charter preflight --json | jq '.passed,.blocked_reason'
```

**Expected**:
```
false
"synthesized_drg missing; run \`spec-kitty charter synthesize\`"
```

Run preflight with auto-refresh on:
```bash
spec-kitty charter preflight --auto-refresh --json | jq '.auto_refresh_applied,.auto_refresh_actions'
```

**Expected**:
```
true
["spec-kitty charter sync", "spec-kitty charter synthesize"]
```

---

## Step 3 — Synthesize bootstrap contract (FR-009)

After Step 2's auto-refresh, the synthesizer either produced `graph.yaml` or set `built_in_only: true` in the manifest:

```bash
ls .kittify/doctrine/graph.yaml 2>&1
yq '.built_in_only' .kittify/charter/synthesis-manifest.yaml
```

**Expected**: either the graph file exists, OR the manifest reports `true`. Downstream `charter status` reports `synthesized_drg.state = "fresh"` or `"built_in_only"`.

---

## Step 4 — Pack-authoring vocabulary (FR-010..FR-014)

In the fixture pack:

```bash
spec-kitty doctrine pack validate <pack-dir> --json | jq '.issues[] | select(.category=="same_id_collision")'
```

**Before the declaration is added**: a `same_id_collision` ADVISORY with the new reworded message.

Add `enhances: <built-in-id>` to one of the pack tactics, then re-validate:

```bash
spec-kitty doctrine pack validate <pack-dir> --json | jq '.issues[] | select(.category=="same_id_collision")'
```

**Expected**: empty result (advisory suppressed; FR-013).

Inspect the auto-emitted DRG edge:

```bash
spec-kitty doctrine pack validate <pack-dir> --json | jq '.drg_fragment.edges[] | select(.relation=="enhances")'
```

**Expected**: a DRG edge with `relation: "enhances"`, `source: tactic:<pack-id>`, `target: tactic:<built-in-id>` (FR-014).

Mistake test: change the field to reference a non-existent ID:

```bash
spec-kitty doctrine pack validate <pack-dir> --json | jq '.issues[] | select(.category=="unknown_target")'
```

**Expected**: a hard `unknown_target` error (FR-012).

---

## Step 5 — Vocabulary cutover (FR-015, FR-016)

```bash
spec-kitty charter status --json | grep -c '"shipped"'
spec-kitty charter lint --json   | grep -c '"shipped"'
spec-kitty agent profile list --json 2>/dev/null | grep -c '"shipped"' || true
spec-kitty doctrine pack validate <pack-dir> --json | grep -c '"shipped"' || true
```

**Expected**: every count is **0**. The architectural regression test `tests/architectural/test_no_shipped_layer_label.py` enforces this on every CI run (FR-016).

---

## Step 6 — End-to-end success criteria

After running Steps 1-5:

- ✅ Fresh-clone freshness reports the missing DRG with a single canonical remediation.
- ✅ Preflight blocks or auto-refreshes deterministically.
- ✅ Pack authors can declare `enhances`/`overrides` without spurious advisories.
- ✅ `"shipped"` no longer appears as a layer label in any public JSON.

If any step fails, the mission is not landed.
