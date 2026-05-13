# Channel Assignment — ASN-0043 review-47

**Date:** 2026-05-13 09:19

## Issue 1: L9 proof's allocator chain incomplete for the empty-state case
Reason: The fix is a mechanical enumeration of the allocator spawn chain from `d'` to `a` using T10a/TA5a from ASN-0034, with each `k' > 0` step discharged against the established `zeros` count. The worked example already executes this chain in three steps; the L9 proof needs the same rigor, and all the required machinery is in ASN-0034 and the ASN's own content.

## Issue 2: L11b's precondition omits S0–S3 but the verification of L14a invokes S3
Reason: This is an internal consistency fix between L11b's stated precondition and its proof's invocation of S3. The choice between (a) adding S0–S3 to the precondition (mirroring L9) and (b) deriving `a' ∉ ran(Σ.M(d))` from L14a-on-Σ plus freshness is a formal-model decision, not a question of design intent or implementation evidence.

## Issue 3: L9 verification list does not address L11b's preservation in Σ'
Reason: This is proof bookkeeping — adding an explicit note that L9 and L11b are model-level meta-lemmas preserved by recursive application of the same construction. Purely internal to the ASN's proof structure.
