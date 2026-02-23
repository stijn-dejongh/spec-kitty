# Prompt Documentation: Agent Profile System Specify

**Agent:** claude-opus
**Date:** 2026-02-23T14:00:00+01:00
**Task:** Retrospective specification of agent profile feature branch

## Original Prompt (verbatim)

> This feature branch is based on 2.x, and contains cherry picks from previously created work, which was stored in a removed specification. I wish to align this with the spec kitty architecture and approach. Review the commits in this branch, summarize their intent and main additions. Then, help me align it to the canonical kitty approaches.

### Follow-up instructions (verbatim)

> Full alignment pass, with new WPs for wheel, migration, and CI workflow updates.

> Yes, then conduct an interview regarding the spec, as you normally would. Review the glossary during spec creation. Adhere to directives 014 and 015 after finalizing the spec.

> Ensure the specification mentions the addition of the Agent Profiles as a way to fill the gap between `exploration` and `structured approach` (ad-hoc requests that need to be as-compliant as possible with the doctrine/constitution governance, but without the need to launch a full mission). Then: create the logs for this step (investigation and spec outline). Then conduct a spec/feature interview with me, talking me through the main points of the spec and asking me for clarifications if needed. I would like to add in a Quality of Life WP: adding a REPO_MAP and SURFACES file, based on a template file (way of working and templates to be added to src/doctrine). Cfr: `doctrine_ref/templates/structure` and description of creating such artefacts in `doctrine_ref/agents/bootstrap-bill.agent.md`.

## SWOT Analysis

### Strengths

- **Clear context**: The user provided the branch name, base branch, and the fact that it contains cherry-picks — this immediately scoped the investigation
- **Iterative refinement**: Each follow-up message added precision (target branch, glossary review, directive adherence, positioning framing, QoL WP)
- **Reference pointing**: The user pointed to specific files (`doctrine_ref/templates/structure`, `bootstrap-bill.agent.md`) rather than leaving the agent to guess

### Weaknesses

- **Implicit target branch**: The initial prompt didn't specify `2.x` as the comparison base — the agent initially compared against `main`, requiring a correction
- **Directive numbers ambiguous**: "Directives 014 and 015" could refer to either the shipped profile references (Acceptance Criteria Completeness / Research Time-boxing) or the doctrine_ref directives (Work Log / Store Prompts). The agent had to search both locations.

### Opportunities

- The "exploration vs structured approach" framing was added mid-session — including this in the initial prompt would have saved a round-trip
- A future `/spec-kitty.specify --retrospective` mode could streamline this workflow by skipping the main-branch enforcement and pre-populating WP status from git history

### Threats

- None identified — the prompt was effective for the task

## Improvement Suggestions

1. **Include base branch in initial prompt**: "Compare against `2.x`, not `main`" would have avoided the correction
2. **Specify directive source**: "Directives 014 and 015 from `doctrine_ref/directives/`" removes ambiguity
3. **Front-load the positioning framing**: Including the exploration-to-structured-approach motivation in the initial prompt would produce a better first-draft spec

## Pattern Recognition

- **Retrospective specification**: This is a recurring need — cherry-picked work that needs post-hoc traceability. Consider formalizing this as a workflow variant.
- **Multi-source terminology**: When directive/glossary terms exist in multiple locations (shipped profiles, doctrine_ref, glossary/), explicit source qualification prevents wasted search cycles.
