# Channel Assignment — ASN-0119 review-19

**Date:** 2026-06-09 18:52

## Issue 1: Invariant-preservation ledger omits S8★, the one value-dependent invariant REARRANGE actually transforms
Reason: The review prescribes the exact fix — cite ASN-0084's R-BLK (RunDecompositionTransformation) and R-CANON (CanonicalityOfMergeNormalForm), which already establish that the post-state admits the unique maximal-run partition guaranteed by S8★. This is a mechanical cross-reference to existing lemmas in a sibling ASN the reviser already imports throughout; it requires neither design intent nor implementation evidence.

## Issue 2: Defensive proof-method justification in the Links section (anti-bloat)
Reason: Pure anti-bloat deletion — cut the ~130-word meta-commentary to a brief clause noting the RA1 derivation also covers the trivial no-op, letting the intro carry the K.μ~ atomicity distinction. The review specifies exactly what to keep and remove; no external channel is involved.
