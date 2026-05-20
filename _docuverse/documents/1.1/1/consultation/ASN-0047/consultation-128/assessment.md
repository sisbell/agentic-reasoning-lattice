# Channel Assignment — ASN-0047 review-128

**Date:** 2026-05-19 19:46

## Issue 1: K.δ case-level `e ∉ E` is explicit for case (i), implicit for case (ii)
Reason: Purely a presentational fix — restating an existing precondition or adding a preamble clarifying that the "where" clause ranges over both cases. The substantive content (the obligation and its per-sub-case discharge mechanisms) is already in the ASN.

## Issue 2: P7a discharge in the Class (b) prose elides one inferential step
Reason: The missing inferential step (`a ∉ dom(C)` from J0; `ran(M(d)|_{s_C}) ⊆ dom(C)` from S3★; therefore `a ∉ ran(M(d)|_{s_C})`) chains existing ASN content. No design intent or implementation evidence is needed.

## Issue 3: K.δ k = 0 freshness discharge mixes axiomatic and derived T10a forms across the section without a consolidated handle
Reason: Consistent labeling fix — the direct-vs-derived T10a distinction is already established in FrontierEquivalence's body. The fix is to apply that distinction uniformly in downstream prose or add a gloss at K.δ's definition.
