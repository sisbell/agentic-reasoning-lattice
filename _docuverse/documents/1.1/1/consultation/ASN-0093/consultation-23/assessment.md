# Channel Assignment — ASN-0093 review-23

**Date:** 2026-05-31 04:58

## Issue 1: FirstEmission misattributes the anchor's T4-validity to B6(a)
Reason: Fix is internal—the correct grounding (M0 + TA5a on `inc(d, 2)`, side condition `zeros(d) ≤ 2` discharged by M0) is already stated in the B6-verification paragraph under *Sub-allocator chains are ASN-0040 sibling streams*; swap the citation accordingly in both content and link cases.

## Issue 2: Duplicate circularity parentheticals in FirstEmissionFreshness
Reason: Fix is internal—the proof already declares the cases follow one substitution rule, so the soundness caveat collapses to a single statement under that rule; no external evidence needed to remove a verbatim duplicate.

## Issue 3: Defensive use-site aside in ChainMembershipForOrigin
Reason: Fix is internal—deleting a "not needed by downstream consumers" aside requires no design intent or implementation evidence; the lemma's statement and proof stand without it.

## Issue 4: SubAllocatorAxiom prose explains why, not what
Reason: Fix is internal—reducing the axiom to its single object-level clause (`A_·(d) = S(b_·(d), 1)`) and dropping the implementation-realization disclaimer and restating sub-paragraph is pure prose pruning; the clause's content is unchanged.

## Issue 5: Intro / Scope redundancy on downstream-dependency framing
Reason: Fix is internal—consolidating two paraphrases of the same dependency rule into the Scope section requires no external input.

## Issue 6: K.σ cross-store and cross-anchor freshness repeat one argument
Reason: Fix is internal—both sub-paragraphs run the same `zeros = 2`-vs-`3` distinctness argument already grounded in C1/L1 and the anchor construction; merging them is consolidation of present material.

## Issue 7: Simultaneous-induction framing carries defensive restatement
Reason: Fix is internal—cutting the re-narration of per-transition discharges already supplied by the discharge matrix and ChainMembershipForOrigin proof needs no external evidence; the load-bearing decomposition is retained.
