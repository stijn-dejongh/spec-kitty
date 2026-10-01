# Approach: coord-artifact-single-home-01M3V4BE

Running log of how the approach evolves. One entry per change, 1-3 sentences, dated.

## Initial approach (plan, 2026-10-01)

- **Close the defect class at the write side.** Add one write-location accessor, `PlacementSeam.write_dir(kind)`, on the existing placement seam. For COORD-partition kinds of a coordination-routed Mission it owns materialize, seed and refuse. Every COORD writer moves to it, and the existing write-side rederivation gate is extended so a writer cannot fall back to a read resolver.
- **Create seeds eagerly.** Create materializes the coordination worktree and commits the creation records on the coordination branch through the existing coordination commit path.
- **Honest commits.** The commit router commits the owning-surface copy and reports a per-surface outcome. One shared renderer serves every consumer. Accept drops its raw commit.
- **Ledger reclassified.** The decision ledger is reclassified to the PRIMARY partition, with every reader that flips enumerated. `doctor decisions` gains fork detection and a non-destructive repair.
- **Sequencing.** Campsite-clean first. Every defect gets a red-first reproduction through its existing entry point before its fix. Then one end-to-end test over both coordination topologies.
- **Tests.** Targeted module tests plus the named architectural gate files only. No full heavy suites locally.

## Entries
- 2026-10-01: The scope widened by operator ruling Q4. The consolidation and `materialize` COORD writers migrate too, as a separate concern (IC-18) guarded by the #5001 terminus-integrity tests. The spec moved to revision 3 with the plan-phase folds.
