---
work_package_id: WP03
title: Resolver-backed profile-load doctrine
dependencies: []
requirement_refs:
- C-005
- C-006
- FR-007
- FR-008
- FR-009
- FR-011
- NFR-003
planning_base_branch: fix/annoying-bugs-sweep
merge_target_branch: fix/annoying-bugs-sweep
branch_strategy: Planning artifacts for this mission were generated on fix/annoying-bugs-sweep. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into fix/annoying-bugs-sweep unless the human explicitly redirects the landing branch.
subtasks:
- T029
- T013
- T014
- T015
- T016
- T017
phase: Phase 2 - Agent guidance
history:
- at: '2026-07-27T13:34:24Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: src/doctrine/skills/
create_intent:
- src/doctrine/skills/spk-doctrine-profile-load/references/profile-load-mechanics.md
- tests/architectural/test_profile_load_resolver_guidance.py
execution_mode: code_change
model: gpt-5.6-sol
owned_files:
- src/doctrine/skills/ad-hoc-profile-load/SKILL.md
- src/doctrine/skills/spk-doctrine-profile-load/SKILL.md
- src/doctrine/skills/spk-doctrine-profile-load/references/profile-load-mechanics.md
- src/doctrine/skills/adversarial-squad/SKILL.md
- src/doctrine/procedures/built-in/adversarial-squad-deployment.procedure.yaml
- tests/architectural/test_profile_load_resolver_guidance.py
- tests/doctrine/test_spk_skill_pack.py
role: curator
tags: []
tracker_refs:
- '#1840'
---

# Work Package Prompt: WP03 - Resolver-backed profile-load doctrine

## ⚡ Do This First: Load Agent Profile

Use `/ad-hoc-profile-load`, resolve `doctrine-daphne` through
`spec-kitty agent profile show doctrine-daphne`, then load
`spec-kitty charter context --action implement --json`.

- **Profile**: `doctrine-daphne`
- **Role**: `curator`
- **Agent/tool**: `codex`

## Objective

Make every resolver-capable profile-load instruction use the canonical resolver command as its
primary mechanism, while preserving the explicit read-only-harness fallback required by #2304.

## Context And Constraints

- Edit canonical `src/doctrine/**` sources only; never `.agents/**`.
- Detailed mechanics belong in
  `spk-doctrine-profile-load/references/profile-load-mechanics.md`; keep the canonical SKILL body
  within the enforced 80-line limit.
- `ad-hoc-profile-load` is the legacy alias and must point toward the canonical authority.
- Raw `.agent.yaml` reads may remain only for a harness unable to invoke the CLI, with an inline
  warning that overlays, lineage, and overrides can diverge.
- Issue #1840 contains two stale claims; both must be corrected.

## Branch Strategy

- **Planning base**: `fix/annoying-bugs-sweep`
- **Merge target**: `fix/annoying-bugs-sweep`
- Use the finalized lane workspace.

## Subtasks

### T029 - Open the WP: tracker, ownership, and campsite

Before edits, assign #1840 to the current Human-in-Charge and add a tracker comment naming this
mission. Record the links for PR evidence. Re-check the intended diff against C-005 and every other
WP, then scout the owned doctrine/test surfaces for domain-matched stale duplication, length, and
Sonar findings. Apply required behavior-preserving cleanup first with focused tests, or record a
clean bounded finding. Stop and revise ownership before touching an undeclared source.

### T013 - Inventory and classify

Enumerate tracked instruction occurrences under `src/doctrine/**`. Classify each as
resolver-capable, read-only fallback, benign data/path reference, or stale primary guidance.
The test denominator must be concrete and non-zero.

### T014 - Canonical skill mechanics

Write a concise reference explaining:

1. `spec-kitty agent profile show <profile-id>` for the resolved profile;
2. `spec-kitty charter context --action <action> --json` for action-scoped governance;
3. which initialization, specialization, and directives to apply;
4. the narrowly scoped read-only fallback and divergence warning.

Wire the reference through the canonical skill's reference mechanism and keep the alias direction
canonical.

### T015 - Correct prompt/procedure wording

Update the adversarial squad skill and deployment procedure so delegated reviewers resolve profiles
through the CLI and charter context. Preserve profile-loaded behavior; naming a persona alone is
still insufficient.

### T016 - Structural guard

Add a focused architectural test that scans exactly `src/doctrine/**`, asserts a non-zero file count,
and reports every offending path. Make the predicate semantic enough to allow benign path mentions
and the caveated read-only fallback, while rejecting raw reads presented as primary.

Include a self-mutation test or fixture proving the guard turns red when an offending instruction is
introduced.

### T017 - Correct issue #1840

Edit the ticket body/comment to strike both the raw-read recommendation and the false zero-command
claim. Link the canonical commands and paste the permalink into the mission/PR evidence.

## Validation

```bash
PWHEADLESS=1 pytest tests/architectural/test_profile_load_resolver_guidance.py -q
PWHEADLESS=1 pytest tests/doctrine/test_spk_skill_pack.py -q
PWHEADLESS=1 pytest tests/architectural/test_docs_cli_reference_parity.py -q
PWHEADLESS=1 pytest tests/architectural/test_no_legacy_terminology.py -q
ruff check tests/architectural/test_profile_load_resolver_guidance.py tests/doctrine/test_spk_skill_pack.py
```

## Definition Of Done

- Canonical mechanics are self-sufficient and under the skill length ceiling.
- Every primary instruction is resolver-backed.
- Every surviving raw fallback is explicitly bounded and caveated.
- The guard is non-vacuous, enumerable, and self-proving.
- #1840 no longer misdirects and has recorded evidence.
- The actual changed-file set remains disjoint from every other WP.

## Reviewer Guidance

Reject edits to generated skill copies, an unconditional raw-read ban, a grep with zero denominator,
or a canonical skill that still depends on the legacy alias for mechanics.
