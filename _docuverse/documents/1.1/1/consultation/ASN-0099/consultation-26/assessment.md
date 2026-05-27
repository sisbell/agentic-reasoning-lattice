# Channel Assignment — ASN-0099 review-26

**Date:** 2026-05-27 03:11

## Issue 1: F4 realizability discharge — parametric witness construction is implicit
Reason: The fix is internal — it makes explicit a factoring already implicit in F1's definition (match factors through endset tuples) and uses K.λ's chain discipline plus L1c, both already established in the substrate. No design-intent or implementation evidence is needed; this is an exposition correction.

## Issue 2: F4 "single K.λ step" understates the base construction
Reason: The fix is internal — K.λ's subsequent-emission precondition is fully specified in ASN-0093, and the correction simply restates the discharge to acknowledge that chain index k ≥ 2 requires k−1 prior K.λ allocations as part of the base setup. No external channel is needed for this precision adjustment.
