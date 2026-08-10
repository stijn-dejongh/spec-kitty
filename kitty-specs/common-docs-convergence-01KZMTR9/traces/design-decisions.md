# Design Decisions

> Capture design choices and their rationale as they are made (1–3 sentences per dated entry).

**Prompting questions**
- What decision was made, and what were the alternatives?
- Why was this option chosen?
- What constraint or invariant does it protect?

---

## Entries

<!-- YYYY-MM-DD — 1–3 sentences: the decision and why. -->
- 2026-08-10 — D1: `docs/context/audience/` is the docs persona SSOT; do not copy built-in personas
  over it (DIRECTIVE_044). D2: audience-based how-to routing (config made audience-aware). D3: redirect
  map is DERIVED / baseline IMMUTABLE / own cumulative occurrence-map spine (NFR-010). D5: rewrites
  bounded + fact-guarded (NFR-009), split from mechanical moves. D6: shared manifests single-threaded
  through IC-11. See research.md for full rationale + alternatives.
