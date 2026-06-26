# Approach Trace — coord-read-residuals-merge-lanes-and-identity-routing-01KW2M8V

**Purpose:** a running log of the approach/strategy decisions taken while running this
mission — the "how we chose to work" record (distinct from `design-trace.md`, which records
the "what the fix looks like" decisions). Seeded at spec→plan; **append during implement**;
assessed at close.

> Format per entry: `[date] [phase] DECISION — rationale — alternative rejected`

---

## Seeded during spec → plan (2026-06-26)

1. **[spec] One mission, two lanes — not two missions.** #2185 (merge/lanes) and #2186
   (identity) are kept as one mission with Lane A / Lane B. Rationale: shared resolver family,
   shared gate file (`test_gate_read_literal_ban.py`), shared canonicalizer-floor file, and a
   shared coord fixture — two missions would contend on the *same* test/gate files. Alternative
   rejected: split into two missions (worse — concurrent edits to one ratchet file + floor).

2. **[spec] Sequence the landing AFTER the implement-loop sibling; spec/plan in parallel now.**
   Rationale: the implement-loop mission deposits the #2185 `_DIR_READ_KNOWN_RESIDUALS` pins and
   widens the dir-read scanner to whole-`src`; this mission inherits both and drains Lane A pins.
   Source line numbers in the owned surfaces are stable across the sibling's merge (C-009 forbids
   it from editing them), so spec/plan can proceed in parallel. Alternative rejected: land first
   (would force this mission to duplicate the sibling's scanner-widening → guaranteed conflict).

3. **[research] 3-agent code-state research before authoring the spec.** Rationale: the tickets
   listed exact files/lines but the kind labels were suspect; parallel readers (Lane A sites,
   Lane B sites, implement-loop strategy) grounded the spec in verified facts. Payoff: caught **6
   mislabeled artifact kinds** + 3 undercounted mixed sites + the gate-blindness fact. Alternative
   rejected: spec straight from the ticket text (would have propagated the wrong kinds).

4. **[spec→plan] Post-spec adversarial squad before /plan (4 profile-loaded lenses).** Rationale:
   planning point-cut cadence; squads reliably catch undersizing/false-greens. Payoff: caught the
   **CRITICAL `build_coord` false-green** (non-divergent husk), the FR-006/C-SEQ incoherence, the
   broken Lane B pin-drain narrative, and the identity-arm blast radius — all folded into the spec
   before planning. Alternative rejected: straight to /plan on the first-draft spec.

5. **[env] Isolated fresh clone + worktree discipline.** All work runs in dedicated clones/worktrees
   off `upstream/main`; the primary clone (live implement-loop mission) and the doctrine-qol #2083
   clone are never touched. Rationale: parallel missions must not disturb in-flight work.

<!-- append during implement: rebase-onto-post-implement-loop-main, WP sequencing decisions,
     any approach pivots, the pre-merge full-gate dry run. -->
