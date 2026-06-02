# Channel Assignment — ASN-0047 review-297

**Date:** 2026-06-01 22:43

## Issue 1: J4 fork claims K.δ leaves M unchanged, contradicting K.δ's own Document effect
Reason: Internal inconsistency. The correct justification — K.δ's Document case effect `dom(M') = dom(M) ∪ {e}` with `M'(e) = ∅` — is already stated verbatim in the K.δ definition; the fix substitutes that explicit effect for the wrong totality-convention appeal. No external evidence or design intent needed.

## Issue 2: Temporal-scope (per-state vs composite-boundary) distinction stated three times in full
Reason: Pure editorial deduplication — consolidate three restatements of an already-settled internal distinction to one canonical site with pointers. No channel input required.

## Issue 3: S8★ per-subspace discharge duplicated between its definition and the Class (a) prose
Reason: Editorial deduplication internal to the ASN — trim the Class (a) prose to per-transition preservation deltas and cite the S8★ definition for the two-route construction. The construction and the preservation steps are both already present in the ASN.

## Issue 4: NodeRootedForest carries a global use-site justification rather than asserting its structure
Reason: Editorial reframing derivable from the ASN's own content — drop the use-site meta-claim and add a one-clause reconciliation between NodeRootedForest's "forest" framing and NodeLineage's single-prefix-root, both of which are already defined here (inc-descent vs prefix-nesting). No external input needed.
