# Issue matrix — doctrine-silence-guards-01KYFV7Q

Per FR-037 of the spec-kitty-mission-review skill Gate-4. One row per issue referenced in spec.md.

| Issue | Title | Verdict | Evidence ref |
|-------|-------|---------|--------------|
| #2680 | `graph.yaml` monolith sharded into per-kind fragments | verified-already-fixed | The shard landed in #2680. What survives is ~10 source sites still naming the dead path — that residue is **this mission's WP07** (FR-008), not a reopening. Evidence: `git grep "doctrine/graph\.yaml" src/` → 12 files. |
| #2957 | CI shard selection never collects several `tests/specify_cli/cli` files on main | in-mission | Folded in as **WP10** (FR-013 / NFR-005 / SC-013 / IC-08). Root cause verified in-tree: `fast-tests-cli` and `integration-tests-cli` both gate on `needs.changes.outputs.cli == 'true'`, so on any main push whose diff misses the CLI paths, neither job runs. Must reach a terminal verdict before mission `done`. |

Valid `Verdict` values: `fixed`, `verified-already-fixed`, `deferred-with-followup`, `in-mission` (being fixed by a later WP in this mission; must reach a terminal verdict before mission `done`).

## Note on #2957's terminal verdict

WP10 closes the **structural** defect — no test file goes uncollected on `main`. It does **not** fix
the reds that closure will surface; those are honest pre-existing reds under ADR `2026-07-17-1` and
are reported, not repaired here (WP10/T055). So #2957's terminal verdict is expected to be `fixed`
for the collection gap, with any surfaced reds filed separately rather than folded in. Satisfying the
gate by reclassifying a surfaced red as expected would be greenwashing, and is explicitly forbidden.
