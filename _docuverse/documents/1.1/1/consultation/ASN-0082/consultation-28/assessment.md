# Channel Assignment — ASN-0082 review-28

**Date:** 2026-05-15 09:52

## Issue 1: I3 lacks an explicit S7 preservation lemma
Reason: The fix is purely formal — add an I3-S7 lemma mirroring S7-post, with the proof derivable from I3-C (already stated in the ASN) plus the observation that S7a/b/c are predicates over dom(C). No design-intent question (preserving structural attribution under arrangement-only operations is already implicit in I3-C) and no implementation evidence needed.

## Issue 2: OrdinalOrderEquivalence proof — "same positions with the same values"
Reason: This is a wording fix for an index-correspondence issue in an internal lemma's proof. The reviewer supplies the exact rephrasing, and the index shift is determined entirely by the definitions of ord and T1 already cited in the ASN. No external input needed.

## Issue 3: Proof ordering — D-SEQ-post forward-references S8-depth-post and S8a-post
Reason: This is a structural reorganization of the lemma sequence, with the dependency-respecting order already specified by the reviewer. Pure editorial fix derivable from the existing proof dependencies.

## Issue 4: D-CTG-post boundary argument — "adjacent ordinals" claim under-justified
Reason: The fix expands the existing boundary argument into an explicit verification of D-CTG's quantifier using L, Q₃, and D-CTG's definition — all already present in the ASN. The reviewer's "Required" section gives the full expansion. No design or implementation evidence needed.
