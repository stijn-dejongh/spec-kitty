# Tasks: Annoying Bugs Sweep

**Mission**: `annoying-bugs-sweep-01KYHQ9F`
**Planning branch**: `fix/annoying-bugs-sweep`
**Merge target**: `fix/annoying-bugs-sweep`

## Delivery Shape

Five file-disjoint work packages preserve the two P0s as independently reviewable and
cherry-pickable slices. WP01 and WP02 are the release-critical path and can execute in parallel.
WP03, WP04, and WP05 are independent agent-facing corrections.

## Subtask Index

| ID | Description | WP | Parallel |
|---|---|---|---|
| T001 | Commit the #2985 red-first mixed-lane reproduction and base evidence | WP01 | No |
| T002 | Derive a deterministic per-WP seed floor across transitions and annotations | WP01 | No |
| T003 | Apply the floor to every seed while preserving deterministic IDs | WP01 | No |
| T004 | Add independent claim-slot verification witnesses | WP01 | No |
| T005 | Exercise all five writing callers and idempotent convergence | WP01 | No |
| T006 | Run the focused migration/cutover quality gates | WP01 | No |
| T007 | Coordinate scope with the #2987 reporter and record the outcome | WP02 | Yes |
| T008 | Add red-first portability and non-vacuity tests | WP02 | No |
| T009 | Replace POSIX reference search with a pure-Python scanner | WP02 | No |
| T010 | Make diff/source discovery fail loudly as undeterminable | WP02 | No |
| T011 | Add the stable diagnostic contract and remediation | WP02 | No |
| T012 | Prove POSIX symbol-set compatibility and focused quality gates | WP02 | No |
| T013 | Inventory and classify tracked profile-load instructions | WP03 | Yes |
| T014 | Make the canonical profile-load skill self-sufficient via references | WP03 | No |
| T015 | Reword resolver-capable and read-only-harness surfaces correctly | WP03 | No |
| T016 | Add a non-vacuous source-tree doctrine guard | WP03 | No |
| T017 | Correct both stale claims on issue #1840 and record the permalink | WP03 | No |
| T018 | Classify every scoped `spec-kitty status` occurrence by intent | WP04 | Yes |
| T019 | Correct the canonical styleguide example | WP04 | No |
| T020 | Correct the four scoped published documentation pages | WP04 | No |
| T021 | Add command-existence and scope regression coverage | WP04 | No |
| T022 | Run terminology and documentation parity gates | WP04 | No |
| T023 | Add the standalone opener pointer to the Typer epilog | WP05 | Yes |
| T024 | Prove `profile-invocation --help` exposes `spec-kitty dispatch` | WP05 | No |
| T025 | Prove completion metadata is unchanged | WP05 | No |
| T026 | Run focused invocation CLI and static quality gates | WP05 | No |

## Work Packages

### WP01 - P0 birth-cutover seed ordering and verification

**Priority**: P0
**Prompt**: `tasks/WP01-birth-cutover-seed-ordering.md`
**Dependencies**: none
**Independent test**: a mixed terminal/non-terminal fixture genuinely seeds legacy runtime state,
reds on `upstream/main`, preserves every lane and claim slot after the fix, and converges on rerun.

T001 Commit the #2985 red-first mixed-lane reproduction and base evidence (WP01)
T002 Derive a deterministic per-WP seed floor across transitions and annotations (WP01)
T003 Apply the floor to every seed while preserving deterministic IDs (WP01)
T004 Add independent claim-slot verification witnesses (WP01)
T005 Exercise all five writing callers and idempotent convergence (WP01)
T006 Run the focused migration/cutover quality gates (WP01)

**Implementation sketch**: establish the failure through the shared cutover authority; introduce a
small deterministic ordering helper in the migration owner; use it for transition and annotation
seeds; strengthen verification from the legacy reader; then cover accept, merge, upgrade, and both
migrate modes without changing those callers unless a test proves a caller-specific defect.

**Risks**: raw timestamp strings are the reducer comparator input; an event-only fix leaves
annotations unsafe; seed suppression silently loses claim-borne values.

### WP02 - P0 portable and honest dead-code review gate

**Priority**: P0
**Prompt**: `tasks/WP02-portable-dead-code-verdict.md`
**Dependencies**: none
**Independent test**: injected subprocess `FileNotFoundError` and a non-Python/non-`src` fixture
produce a structured verdict, never a traceback or clean-zero message; supported Python results are
unchanged.

T007 Coordinate scope with the #2987 reporter and record the outcome (WP02)
T008 Add red-first portability and non-vacuity tests (WP02)
T009 Replace POSIX reference search with a pure-Python scanner (WP02)
T010 Make diff/source discovery fail loudly as undeterminable (WP02)
T011 Add the stable diagnostic contract and remediation (WP02)
T012 Prove POSIX symbol-set compatibility and focused quality gates (WP02)

**Implementation sketch**: pin the two independent faults; add a deterministic filesystem scanner;
separate discovery success from empty results; extend the existing diagnostic enum/docs; preserve
the current path filters and symbol set.

**Risks**: `git grep` closes only portability; treating every zero-symbol diff as unsupported breaks
legitimate clean reviews; changing the `"test"` substring filter expands scope.

### WP03 - Resolver-backed profile-load doctrine

**Priority**: P2
**Prompt**: `tasks/WP03-resolver-backed-profile-load-doctrine.md`
**Dependencies**: none
**Independent test**: the tracked `src/doctrine/**` denominator is non-zero, all primary load
instructions use the resolver-backed command, and every raw fallback is explicitly read-only and
caveated.

T013 Inventory and classify tracked profile-load instructions (WP03)
T014 Make the canonical profile-load skill self-sufficient via references (WP03)
T015 Reword resolver-capable and read-only-harness surfaces correctly (WP03)
T016 Add a non-vacuous source-tree doctrine guard (WP03)
T017 Correct both stale claims on issue #1840 and record the permalink (WP03)

**Implementation sketch**: use `spk-doctrine-profile-load/references/` for mechanics, point the
legacy alias toward it, update the squad/procedure sources, and add a closed-by-construction guard.

**Risks**: generated `.agents/` copies are out of scope; banning all raw reads re-breaks #2304;
inline expansion violates the canonical skill length ceiling.

### WP04 - Real status command guidance

**Priority**: P2
**Prompt**: `tasks/WP04-real-status-command-guidance.md`
**Dependencies**: none
**Independent test**: the canonical styleguide and four scoped docs contain only real commands in
concrete examples, while generic prose and changelog history remain untouched.

T018 Classify every scoped `spec-kitty status` occurrence by intent (WP04)
T019 Correct the canonical styleguide example (WP04)
T020 Correct the four scoped published documentation pages (WP04)
T021 Add command-existence and scope regression coverage (WP04)
T022 Run terminology and documentation parity gates (WP04)

**Implementation sketch**: classify before editing, use `spec-kitty agent tasks status` only where
WP status is intended, and choose the actual owning command for upgrade/environment examples.

**Risks**: blind substitution changes meaning; archived changelog content is immutable; no new
top-level `status` command may be introduced.

### WP05 - Invocation opener discoverability

**Priority**: P3
**Prompt**: `tasks/WP05-invocation-opener-discoverability.md`
**Dependencies**: none
**Independent test**: `spec-kitty profile-invocation --help` names `spec-kitty dispatch`, while the
completion manifest remains byte-identical.

T023 Add the standalone opener pointer to the Typer epilog (WP05)
T024 Prove `profile-invocation --help` exposes `spec-kitty dispatch` (WP05)
T025 Prove completion metadata is unchanged (WP05)
T026 Run focused invocation CLI and static quality gates (WP05)

**Implementation sketch**: add epilog-only help text to the existing Typer group and extend the
invocation CLI tests with a manifest non-regression assertion.

**Risks**: changing `help=` or adding an alias regenerates command metadata and violates C-007.

## Parallel Execution

- Lane candidate A: WP01.
- Lane candidate B: WP02.
- Lane candidate C: WP03.
- Lane candidate D: WP04.
- Lane candidate E: WP05.

No WP shares an owned source or test file. Finalization may consolidate lanes for operational
capacity, but no dependency is required for correctness.

