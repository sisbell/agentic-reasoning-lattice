# Revision Categorization — ASN-0064 review-3

**Date:** 2026-03-21 19:18

## Issue 1: F1 proof claims V(βⱼ) is convex in T1, which is false
Category: INTERNAL
Reason: The fix is a proof reformulation using depth-restricted order or direct ordinal-increment argument — all ingredients (T1, S0, block definitions) are already present in the ASN and its references.

## Issue 2: F1 proof does not verify T12 well-formedness of constructed I-spans
Category: INTERNAL
Reason: The missing verification step follows mechanically from T12 and TA0, which are already cited. Adding one sentence with the width/action-point check completes the proof.

## Issue 3: F2 mislabeled as INV
Category: INTERNAL
Reason: This is a labeling error — the distinction between INV (transition-preserved state predicate) and LEMMA (consequence of definitions) is internal to the project's classification conventions.

## Issue 4: F6 conflates specification property with implementation commitment
Category: INTERNAL
Reason: The separation into LEMMA (type-signature consequence) and DESIGN (Nelson's performance commitment) uses only material already quoted in the ASN. No new evidence about intent or implementation is needed.

## Issue 5: F11 frame asserts L' = L but L is not in the formal system state
Category: INTERNAL
Reason: The ASN already acknowledges the identical gap for LinkEntityCoherence. The fix is to apply the same caveat to F11 or restate it as a pure function — both options are derivable from the ASN's own discussion.
