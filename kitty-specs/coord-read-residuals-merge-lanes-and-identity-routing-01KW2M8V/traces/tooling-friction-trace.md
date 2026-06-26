# Tooling-Friction Trace — coord-read-residuals-merge-lanes-and-identity-routing-01KW2M8V

**Purpose:** a running log of spec-kitty tooling friction encountered while running this
mission (a coordination-topology, dogfooding mission). Seeded at spec→plan; **append
during the implement loop**; reviewed afterward to assess the state of the tooling.
Each entry: what blocked, where, witnessed evidence, disposition.

> Format per entry: `[date] [phase] SYMPTOM — anchor — disposition (fixed PR#/ticket#/workaround/open)`

---

## Seeded during spec → plan (2026-06-26)

1. **[specify] `spec-kitty specify` refuses to run inside a git worktree.** Attempting to
   scaffold the mission from an isolated `git worktree` returned
   `{"error": "Cannot create missions from inside a worktree. Run from the project root checkout."}`.
   **Witnessed live.** Rational guard (planning belongs in a root checkout), but it forced a
   detour: no idle full clone with an `upstream` remote + a working `.venv` was available
   (the `-runtime`/`-events`/`-design` siblings lack `upstream`/venv or are mid-flight), so I
   created a **fresh dedicated clone** (`spec-kitty-coord-residuals`) and ran the
   doctrine-qol `.venv`'s `spec-kitty` binary from it. Disposition: **workaround** (fresh
   clone). Possible gap: the guard's remediation text ("Run from the project root checkout")
   doesn't help when no suitable root checkout exists — consider a `--allow-worktree` or a
   "create a planning clone" helper. **OPEN (candidate gap).**

2. **[specify/plan] coord-topology placement is non-obvious for a planning-stage mission.**
   The scaffold defaulted `topology: coord`, created a `kitty/mission-…` coordination branch,
   and `spec-commit`/`plan` wrote artifacts to the **placement ref** (and `plan.md` into a
   `.worktrees/<slug>-coord/` worktree) — so on the working branch `spec.md`/`issue-matrix.md`
   show as **untracked** even though they are committed on the placement ref. Correct
   behavior, but the working-tree view is misleading at planning time (no `-coord` execution
   has started). Disposition: **workaround/understood** — verified artifacts via
   `git show kitty/mission-…:…`. Candidate doc-gap: clarify planning-stage placement in the
   specify/plan output. **OPEN (minor).**

3. **[plan] `plan` blocks until Technical Context is substantive — good, but the block fires
   only on re-run.** First `plan` call scaffolded the template and returned `blocked`
   (`Language/Version … placeholder`); authoring + re-run returned `success`. Disposition:
   **expected** (the substantive-spec/plan guards are working as designed). No gap — recorded
   for the friction baseline.

4. **[tasks] Coord-topology scaffold split the planning surface → `finalize-tasks`/`map-requirements` blocked.** `specify` defaulted the mission to `topology: coord` and created a coordination branch + `-coord` worktree **at planning time** — contrary to the SK rule "planning happens in the main checkout, no worktrees during planning." Consequence: `spec-commit`/`plan`/`map-requirements` wrote the tasks artifacts to the **coord branch/worktree**, but `finalize-tasks --validate-only` read `tasks_dir` from the **primary** checkout (empty) → `Unmapped functional requirements: FR-001..FR-011`, even after `map-requirements --batch` reported `success`+`committed`. **Witnessed live.** This is the exact #2185/#2186 planning-surface split-brain class the mission targets — dogfooded. Disposition: **workaround = flatten** (drop `coordination_branch`, `topology=flat`, bring artifacts onto the primary branch, retire the coord worktree) → validation passed (5 WPs). Candidate gap: `specify`/`plan` should not create a coord topology for a not-yet-implementing mission, or `finalize` must read the same surface the writers used. **OPEN (candidate gap, #2185/#2186-adjacent).**

5. **[env] Version-mismatched binary compounded the surface confusion.** I was running the **doctrine-qol clone's `.venv` binary (spec-kitty 3.2.2, on `feat/doctrine-qol-2083`)** against the fresh clone's newer `upstream/main` tree. Per operator suggestion, installed SK into the fresh clone's **own `.venv` (3.2.3, version-matched)** via `uv venv && uv pip install -e .`. Disposition: **fixed** — the version-matched binary + the flatten together produced a clean `finalize`. Lesson: a separate-clone mission needs its **own** `.venv`; don't drive it with another clone's editable install.

<!-- append during implement: each routed site, any guard that blocks a legitimate edit,
     the rebase-onto-post-implement-loop-main step, pin-drain ratchet behavior, FR-009 fixture. -->
