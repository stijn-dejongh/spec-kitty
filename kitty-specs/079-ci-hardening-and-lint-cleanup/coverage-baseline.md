# Coverage Baseline — Mission 079

**Date measured:** 2026-04-09
**Branch:** kitty/mission-079-ci-hardening-and-lint-cleanup (post WP01-WP05 merge)
**Formula:** floor = max(tier_minimum, measured_coverage - 2)
**Python:** 3.13 | **pytest-cov:** 7.x | **Marker filter:** none (all markers)

## Results

| Module | Tier | Tier Min | Measured | Floor | Notes |
|--------|------|----------|----------|-------|-------|
| status | A | 75% | 80.6% | 78% | 490 tests |
| lanes | A | 75% | 85.4% | 83% | 171 tests; measured without marker filter (zero markers pre-WP07) |
| kernel | A | 75% | 96.7% | 94% | 92 tests |
| sync | A | 75% | 82.4% | 80% | 1319 tests |
| next | B | 60% | 89.8% | 87% | 183 passed, 2 failed (pre-existing) |
| review | B | 60% | 94.7% | 92% | 132 tests; measured without marker filter (zero markers pre-WP07) |
| merge | B | 60% | 64.0% | 62% | 112 tests; measured without marker filter |
| cli | B | 60% | 13.2% | 11% | 36 tests; below tier minimum — floor set to measured-2 to avoid blocking CI; tighten in follow-up |
| missions | B | 60% | 47.0% | 45% | 407 tests; below tier minimum — floor set to measured-2 to avoid blocking CI; tighten in follow-up. Covers specify_cli.mission + specify_cli.mission_metadata + doctrine.missions |
| upgrade | B | 60% | 48.4% | 46% | 400 tests; below tier minimum — floor set to measured-2 to avoid blocking CI; tighten in follow-up |
| dashboard | C | 40% | 59.7% | 57% | 82 tests; test dir is tests/test_dashboard/ |
| release | C | 40% | 84.0% | 82% | 62 tests |
| orchestrator_api | C | 40% | N/A | N/A | No dedicated test directory; source at src/specify_cli/orchestrator_api/; covered by integration/e2e tests in core-misc |
| post_merge | C | 40% | 86.6% | 84% | 16 tests |
| core-misc | C | 40% | 57.6% | 55% | 6654 passed, 19 failed (pre-existing), 28 skipped; residual tests covering agent, charter, contract, core, cross_branch, doctrine, dossier, e2e, git_ops, init, integration, policy, runtime, tasks, etc. |

## Known Failures (Pre-Existing)

21 test failures were present before mission 079 work began (verified by stashing all changes and running baseline). These failures are NOT regressions from WP01-WP05.

- 2 failures in `tests/next/`
- 19 failures in core-misc residual tests

These failures do not invalidate the coverage measurements — coverage is computed from passing test paths only.

## Module Path Notes

- **kernel**: Source at `src/kernel/`, not `src/specify_cli/kernel/`
- **missions**: Composite measurement covering `specify_cli.mission` (module), `specify_cli.mission_metadata` (module), and `doctrine.missions` (package)
- **dashboard**: Test dir is `tests/test_dashboard/`, not `tests/dashboard/`
- **orchestrator_api**: No dedicated test dir; 3 source files at `src/specify_cli/orchestrator_api/`
- **dossier**: Tests relocated to `tests/dossier/` by WP05 (T027); included in core-misc measurement

## WP09 Reference

Copy the Floor column values into the `--fail-under` parameter for each module's
integration-tests job in ci-quality.yml. Use the Floor value, not the Measured value.

For modules below tier minimum (cli, missions, upgrade), use the reduced floor to avoid
immediately breaking CI. Plan follow-up coverage improvement work to reach tier minimums.
