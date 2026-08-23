# Behavioural Contracts — fail-loud / single-source seams

No HTTP/API surface changes in this mission. The contracts here are the
**boundary behaviours** each fix must guarantee, expressed as testable
pre/postconditions. These are the acceptance anchors the WPs implement red-first.

## C-IC1 — DRG node-kind recognition is enum-derived

- **Given** the canonical `NodeKind` enum with N members
- **Then** `_DRG_NODE_KINDS == {k.value for k in NodeKind}` (exact set equality)
- **And** for every `k in NodeKind`, a URN `"{k.value}:some-id"` passes the
  membership gate at `topic_resolver.py:236` (is recognized as a DRG node kind)
- **Regression**: adding a hypothetical member to `NodeKind` requires **no** edit
  to `topic_resolver.py` for the drift-guard test to stay green.

## C-IC2 — one profile-reference surface; no inert declared field

- **Given** any agent profile
- **Then** authoring a `context-sources` block causes a **load-time rejection**
  (pydantic `extra="forbid"`), not silent acceptance
- **And** artefact references authored pre-migration under
  `context-sources.{directives,tactics,toolguides,styleguides}` are present on the
  corresponding `*-references` field post-migration (no reference lost)
- **And** the DRG edges + rendered delivery for each shipped profile are unchanged
  for content already delivered before the change (C-006)
- **And** all 25 shipped profiles carry 0 `context-sources` blocks after migration.

## C-IC3 — governance-profile selection fails loud (both tiers)

- **Given** a `governance-profile.yaml` (built-in OR org tier) with a `selected_*`
  entry naming a nonexistent artifact id
- **When** the DRG is generated / doctrine is loaded
- **Then** a loud error names the offending `mission_type:field=id`
  (`assert_governance_scope_edges_resolve` semantics), not a silently-pruned edge
- **And** valid selections mint scope edges unchanged (no false positive).

## C-IC4 — org `drg/fragment.yaml` is folded on every seam

- **Given** an org pack shipping only `drg/fragment.yaml` (the canonical org shape,
  e.g. `packs/internal/`)
- **When** doctrine is loaded via the `org_roots=` seam (executor /
  `action_doctrine_bundle`)
- **Then** the pack's fragment nodes and edges are folded into the merged DRG
  (not dropped)
- **And** when a root genuinely has no DRG at all, a real "no graph" warning is
  emitted (the false suppression when a fragment exists is removed)
- **And** passing both `org_roots` and `org_fragments` does not double-fold.

## C-IC5 — chain delivers every declared kind; misconfig fails loud

- **Given** the built-in + spec-kitty-internal chain (≥2 layers) registered
- **When** doctrine is loaded/merged/activated across consumer seams
- **Then** every kind the internal pack declares (glossary pack, procedure,
  directive) and its `refines` edges reach the consumer
- **And** a deliberately-misconfigured variant of the internal pack (e.g. a
  fragment naming a nonexistent refine target, or a malformed required key) is
  reported loudly instead of counted as success
- **Closes** #3530 (leaving the explicitly-non-child #3412 open).
