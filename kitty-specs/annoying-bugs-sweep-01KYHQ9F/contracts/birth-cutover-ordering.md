# Contract: Birth-Cutover Seed Ordering

## Inputs

- PRIMARY mission directory containing legacy WP artifacts and `meta.json`.
- Canonical status directory containing transition and annotation events.
- Deterministic mission/WP/field seed identity.

## Invariants

1. For each WP with existing history, every new migration transition seed key is strictly less than
   every existing transition key for that WP.
2. For each WP with existing history, every new migration annotation seed key is strictly less than
   every existing annotation key for that WP.
3. A cutover never changes the WP's pre-cutover canonical lane.
4. A cutover never replaces a later legitimate runtime-slot value.
5. Each non-null legacy `shell_pid`, `shell_pid_created_at`, and `agent` value is present after
   reduction.
6. Seed IDs remain deterministic and a second invocation appends no duplicate.
7. Verification failure prevents `status_phase` from flipping.

## Caller Coverage

The same contract applies to:

- accept commit mode;
- merge birth cutover;
- upgrade migration;
- `migrate backfill-runtime-state` single mission;
- `migrate backfill-runtime-state` corpus mode.

`accept --no-commit` and diagnose validate convergence only; they do not exercise the stamp.

## Failure Contract

Unreadable timestamps, corrupt event streams, an unprovable strict floor, or a missing claim-slot
witness fail closed through existing cutover result/error surfaces. No caller may bypass the guard.

