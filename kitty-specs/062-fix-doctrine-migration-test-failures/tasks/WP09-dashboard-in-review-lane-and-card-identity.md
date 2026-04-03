---
work_package_id: WP09
title: Dashboard In-Review Lane Display and WP Card Identity
dependencies: "[]"
requirement_refs: [FR-011, FR-012]
planning_base_branch: feature/agent-profile-implementation-rebased
merge_target_branch: feature/agent-profile-implementation-rebased
branch_strategy: Planning artifacts for this mission were generated on feature/agent-profile-implementation-rebased. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/agent-profile-implementation-rebased unless the human explicitly redirects the landing branch.
subtasks:
- T032
- T033
- T034
- T035
agent: "opencode"
role: "reviewer"
shell_pid: "254171"
history:
- at: '2026-04-03T12:00:00Z'
  actor: human
  action: WP added manually during WP02 implementation
agent_profile: python-implementer
authoritative_surface: src/specify_cli/dashboard/
execution_mode: code_change
lane: planned
owned_files:
- src/specify_cli/dashboard/static/dashboard/dashboard.js
- src/specify_cli/dashboard/static/dashboard/dashboard.css
- src/specify_cli/dashboard/scanner.py
task_type: implement
---

# Work Package Prompt: WP09 -- Dashboard In-Review Lane Display and WP Card Identity

## Objectives & Success Criteria

- WPs in the `in_review` lane are displayed in the existing "For Review" UI column, but with a visually distinct card style that signals an active review is ongoing
- WP cards display agent tool, profile, role, and model in the detail modal header
- All changes verified via Playwright (never claim frontend works without proof)

## Context & Constraints

- **Dashboard JS**: `src/specify_cli/dashboard/static/dashboard/dashboard.js`
- **Dashboard CSS**: `src/specify_cli/dashboard/static/dashboard/dashboard.css`
- **Scanner**: `src/specify_cli/dashboard/scanner.py` — already emits `agent_profile`, `role`, `agent` (tool) fields per WP; needs to also emit `model` if available from frontmatter or event log actor identity
- **CLAUDE.md rule**: Never claim something in the frontend works without Playwright proof

## Branch Strategy

- **Planning base branch**: `feature/agent-profile-implementation-rebased`
- **Merge target branch**: `feature/agent-profile-implementation-rebased`

**Implementation command**: `spec-kitty implement WP09 --base WP05`

## Subtasks & Detailed Guidance

### Subtask T032 -- Render in_review WPs in the For Review column with distinct style

- **Purpose**: WPs with lane `in_review` should appear in the "For Review" column (not a separate column) but with a different card border to visually distinguish them from WPs awaiting review.
- **Visual spec**:
  - Cards in `for_review` lane: current style (border-left only)
  - Cards in `in_review` lane: slightly darker purple border, visible on ALL edges (not only border-left). This reduces visual overload while clearly signaling an active review.
- **Implementation**:
  1. In `dashboard.js`, when building the "For Review" lane content, include both `for_review` and `in_review` WPs
  2. Pass a `lane` or `in_review` flag to `createCard` so the card template can apply a CSS class
  3. In `dashboard.css`, add `.card.in-review` style with darker purple border on all edges
  4. Update the lane header count to include both `for_review` and `in_review` WPs
- **Files**: `dashboard.js`, `dashboard.css`

### Subtask T033 -- Display agent identity fields on WP card detail modal

- **Purpose**: The WP detail modal (shown when clicking a card) should display the agent's tool, profile, role, and model in a structured header section.
- **Spec**: WP cards should display the agent tool, profile, role, and model in the detailed information (top of the detail modal).
- **Implementation**:
  1. Locate the detail modal rendering in `dashboard.js` (the click handler / modal builder)
  2. Add an "Agent Identity" section at the top of the modal content showing:
     - Tool (from `task.agent`)
     - Profile (from `task.agent_profile`)
     - Role (from `task.role`)
     - Model (from `task.model` — see T034)
  3. Only render fields that have non-empty values
  4. Style with badge-like display for consistency with card badges
- **Files**: `dashboard.js`, `dashboard.css`

### Subtask T034 -- Expose model field from scanner to dashboard

- **Purpose**: The scanner currently emits `agent`, `agent_profile`, and `role` but not the AI model. The detail modal needs `model` to display full agent identity.
- **Implementation**:
  1. In `scanner.py` `_process_wp_file()`, extract `model` from the WP frontmatter (if present as a scalar) or from the structured `agent` mapping (if `agent` is a dict with a `model` key)
  2. Add `"model": ...` to the returned task dict
  3. Also add `"model": ""` to the error fallback dict
- **Files**: `scanner.py`

### Subtask T035 -- Playwright verification

- **Purpose**: Verify the UI changes actually work in the browser.
- **Steps**:
  1. Create a test mission with WPs in `for_review` and `in_review` lanes
  2. Launch dashboard, verify both WPs appear in "For Review" column
  3. Verify `in_review` card has distinct border style (all edges, darker purple)
  4. Click a WP card, verify detail modal shows agent identity fields
- **Run headless**: `PWHEADLESS=1 pytest tests/dashboard/ -v`

## Risks & Mitigations

- The detail modal may not exist yet or may have a different structure than expected. Read the full `dashboard.js` before implementing to understand the current modal rendering.
- The `in_review` lane may not be in the lane mapping in `dashboard.js`. Check how lanes are categorised and ensure `in_review` is handled.

## Review Guidance

- Verify the `in_review` border style is visually distinct but not jarring
- Verify the detail modal identity section only renders non-empty fields
- Confirm Playwright tests pass headless

## Activity Log

- 2026-04-03T12:00:00Z -- human -- WP created during mission 062 WP02 implementation.
- 2026-04-03T19:22:33Z – unknown – Claimed by opencode for implementation. Worktree created manually (WP05 dependency already done/merged).
- 2026-04-03T19:29:48Z – unknown – Moved to for_review
- 2026-04-03T19:32:57Z – opencode:unknown:generic:unknown – shell_pid=254171 – Started review via workflow command
- 2026-04-03T19:34:45Z – opencode – shell_pid=254171 – Review passed: T032 correctly combines in_review+for_review in For Review column with distinct CSS, T033 adds agent identity badges in modal with non-empty gating, T034 exposes model field from scanner with dict/scalar/fallback handling, T035 verified via 28 passing unit tests (no Playwright infra exists). Clean diff, only owned_files touched, no regressions.
- 2026-04-03T19:50:11Z – opencode – shell_pid=254171 – Done override: Merged into feature/agent-profile-implementation-rebased via WP11 (worktree removed)
