# Channel Assignment — ASN-0127 review-9

**Date:** 2026-06-10 01:58

## Issue 1: Reorder motion wrongly claimed to never be a containment
Reason: The false universal is refuted by F-IMG-SWING within this very note — its non-injective witness already exhibits a proper-containment image swing (`{a} ⊊ {a,b}`) — so the fix (scope the no-containment/direct-witness claim to the injective swing, treat non-injective reorders as monotone single-step containments where F-IMONO applies) is an internal consistency repair using only material already proven here. Non-injectivity via content sharing (M13/M14) is already a committed feature of the note's model and is cited throughout (F-UDIST, F-VDIST, F-IMG-SWING).

## Issue 2: Discovery-set cardinality change under reorder is asserted but never witnessed
Reason: The required witness is a construction in the worked illustration using only the note's own primitives, and the pattern of two links sharing a coverage target is already exhibited (L_1 and L_2 both reach `a_3`), so adding a second link on `a_2` to realize the 1→2 swing on `W₀={v₁}` is derivable from the ASN's own machinery with no design or implementation input.

## Issue 3: Imprecise foundation citation for the I-run structure of an image
Reason: This is a citation correction to a sibling note's lemma labels, and the review itself already identifies B3 (consistency, `M(d)(vⱼ+k) = aⱼ+k`) as what makes each block's I-extent a contiguous run; the fix is spec bookkeeping, not a question of Nelson's design intent or Gregory's implementation evidence.
