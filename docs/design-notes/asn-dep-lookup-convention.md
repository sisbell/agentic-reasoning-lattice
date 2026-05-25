# ASN-Dep Lookup Convention

*Settled 2026-05-24 during the foundation-loader refactor.*

## Problem

The substrate carries `citation.depends` links for several distinct
purposes (ASN foundation deps, cascade anchors on reviews, claim-side
derivation chains). The links share a type name but their conventions
differ on **which address holds the link**. Asking "what are the
foundation deps of ASN X?" by querying the wrong address returns
empty silently — no exception, no log line, no observable failure
until something downstream produces wrong output.

This pattern caused two production bugs in the same session:

1. The foundation loader queried `citation.depends from=note_addr`;
   under the post-migration convention citations are on `inquiry_addr`;
   loader returned empty foundation strings; reviews ran with no
   foundation; LLM produced findings against incomplete context.
2. The cascade-anchor emitter in `note_review` queried the same wrong
   address; no anchor was emitted; `is_note_cascade_fresh` became
   vacuously true forever; upstream foundation advances stopped
   flagging dependent notes as stale.

Both fixed; the convention below prevents recurrence.

## The rule

**To ask "what are ASN X's foundation deps?" go through ONE entry
point in `lib.shared.foundation`:**

| Need | Helper | Returns |
|---|---|---|
| Dep ASN ids | `foundation_dep_ids(session, asn_id)` | `list[int]` |
| Dep note base addresses | `foundation_dep_addrs(session, asn_id)` | `list[Address]` |
| Dep content (prose) | `load_foundation(asn_id)` | `str` (or raises) |

All three route through the same internal `_resolve_declared_deps`:

```
ASN_id
  ├─ inquiry exists → read frontmatter `depends:`
  │                   validate substrate citation.depends matches
  │                   return ids/addrs/content
  └─ no inquiry    → LEGACY fallback (log to stderr)
                      read citation.depends from note_addr
                      return ids/addrs/content
```

Hard-fail on any unresolvable dep. Empty list only when `depends: []`
is declared explicitly (foundation ASN case).

## Anti-patterns

**DON'T** call `note_dep_asn_ids(store, note_addr)` for dep lookups.
That helper queries one substrate side only and returns empty for
HEALTHY ASNs (their citations are on inquiry_addr). It exists for two
legitimate internal uses:

1. The LEGACY fallback inside `_resolve_declared_deps`
2. The audit (`citation_depends_audit.py`) which inspects both sides
   on purpose

Any other call site is a bug-in-waiting.

**DON'T** call `depends(session, X)` where X is a note_addr for the
purpose of getting foundation deps. `depends()` is a general substrate
predicate; its semantics depend on X:

- `X = review_addr` → returns the cascade-anchor targets the review
  emitted (canonical use; see `is_note_cascade_fresh`)
- `X = claim_addr` or `version_head(claim_addr)` → returns the claim's
  own cross-ASN citations (claim-side cascade-fresh)
- `X = note_addr` → returns ONLY note-side `citation.depends` (empty
  for HEALTHY ASNs); use `foundation_dep_ids` / `foundation_dep_addrs`
  instead

**DON'T** infer ASN structural relationships from filesystem paths
(e.g., "they share ASN-NNNN in their paths so they're related").
Substrate is the source of truth; path patterns are a naming
convention. See also `feedback_substrate_is_source_of_truth` in
operator memory.

## When you're writing new code

If you find yourself reaching for `note_dep_asn_ids` or
`depends(session, X)` or `active_links("citation.depends", ...)` —
ask:

- Am I trying to get "what deps does ASN N declare"? Use
  `foundation_dep_ids` / `foundation_dep_addrs`.
- Am I inspecting raw substrate state for diagnostic / audit / debug
  purposes? Direct queries are fine, but document the intent.
- Am I working with cascade anchors on review docs? `depends(session,
  review_addr)` is correct. Document that the source is the review.
- Am I working with claim-side citations? Different convention
  entirely (`aggregate_asn_deps`, claim-scoped helpers). Out of scope
  here.

## Reference

- `scripts/lib/shared/foundation.py` — `load_foundation`,
  `foundation_dep_ids`, `foundation_dep_addrs`, `_resolve_declared_deps`
- `scripts/lib/lattice/labels.py` — `note_dep_asn_ids` (substrate-side
  only; legitimate uses documented in its docstring)
- `scripts/lib/predicates/citations.py` — `depends` / `dependents`
  general predicates
- `scripts/diagnostics/citation_depends_audit.py` — substrate-state
  audit, classifies every active ASN
