# Channel Assignment — ASN-0094 review-80

**Date:** 2026-05-25 17:15

## Issue 1: Sh-conf's "iff" success condition contradicts per-K discipline gating
Reason: Internal formal correction. The fix restates Sh-conf's success condition to reconcile with the per-K discipline gating and EffectiveWpSimplification's `wp_eff`, both already present in the ASN.

## Issue 2: "FDD subsumes Sh4" claim not formalized
Reason: Internal formalization. The derivation (FDD's from-slot uniqueness + R1 → slot-pair distinct) is already present in prose; promoting it to a named corollary is mechanical from the ASN's own content.

## Issue 3: Missing concrete walkthrough for Provenance shape
Reason: Internal walkthrough construction. The Provenance shape's mechanics (partial `to₁⁻`, `⊥`-filtering in `to_addrs_K`, `pair_K` on empty-G) are fully specified; the walkthrough exercises existing framework machinery against pre-allocated addresses.

## Issue 4: Missing concrete walkthrough for SHCD single-home rejection
Reason: Internal walkthrough construction. The single-home commitment's gate-1 literal-equality test and `latest_K_for_addr`'s `emission_order` via chain-index are fully specified; the walkthrough exhibits admission/rejection mechanics already derivable.

## Issue 5: Reviser drift in Sh4's "Universal scope" paragraph
Reason: Internal copyedit. Delete or condense the paragraph to a one-line parenthetical.

## Issue 6: Reviser drift in BundledDirectedPair's "Coverage class disjointness from R"
Reason: Internal copyedit. Tighten to one sentence or relocate to a general note at the catalog or Sh-conf section.

## Issue 7: Missing concrete walkthroughs for Tuple-Classifier and Resolution shapes
Reason: Internal walkthrough construction. Tuple-Classifier's G-side partition rejection mirrors Classifier's (already walked); Resolution's standalone admission uses the same five-template base family as DirectedPair's shape-mate — both derivable from existing structure.

## Issue 8: Sh4 contract correctness paragraph contains internal expository redundancy
Reason: Internal copyedit. Drop the tightening sub-paragraph or move to an aside; the framework's preservation theorems need only the post-filter exact-equality correctness.
