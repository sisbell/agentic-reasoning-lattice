# Channel Assignment — ASN-0047 review-327

**Date:** 2026-06-02 04:19

## Issue 1: ChildSpawnFreshness reverse direction skips the cross-node exclusion that its sibling lemma FrontierEquivalence performs
Reason: The fix is the ASN's own FrontierEquivalence reverse-direction pattern — scope to the node-rooted subtree via T10/NodeRootedForest before applying GlobalUniqueness. All needed machinery (NodeRootedForest, T10, CrossNodeAccountBase, the parallel FrontierEquivalence text) is already present in the ASN, so the repair is purely internal.

## Issue 2: Revision-state meta-prose in the S8★/K.μ~ discharge elaboration
Reason: Pure editorial deletion of self-referential revision-history prose; the substantive three-family grouping already stands in the same paragraph, so no design intent or implementation evidence is required.
