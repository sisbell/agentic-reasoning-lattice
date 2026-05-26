# Channel Assignment — ASN-0091 review-9

**Date:** 2026-05-26 16:13

## Issue 1: Equality realizability claim is informally asserted but not formally witnessed
Reason: The fix is internal — the equality witness can be constructed using REARRANGE_K's own cut-sequence machinery (e.g., a 3-cut pivot of two singletons from disjoint chains, with w_α = w_β = 1, preserves cardinality). The witness lives in the same construction space as the existing RE-frag and RE-coal witnesses; no external evidence or design intent is needed.

## Issue 2: RE-sub prose conflates π pointwise fixity with M(d) preservation
Reason: The fix is a formal restructuring of claims derivable from R-PPERM/R-SPERM definitions in ASN-0084, which are already cited and present. The distinction between π-fixity and M(d)-preservation is fully resolvable from the ASN's existing formal layer; no design intent or implementation evidence is at stake.

## Issue 3: RE-proj's π-invariance under witness choice is implicit but not derived
Reason: This is a pure well-definedness derivation using the pre-image partition structure already established in the ASN's discussion of π non-uniqueness under S5. The closure argument is internal to the ASN's existing definitions.

## Issue 4: Substrate-emittable closure used silently in LP-Fin Corollary applications
Reason: The bridge fact (dom(C) ∪ dom(L) ⊆ F) is derivable from ASN-0093's sub-allocator chain discipline and ASN-0098's SubstrateEmittableAddresses definition, both already cited foundations. The fix is a one-sentence citation/bridge, not a question about Nelson's intent or Gregory's implementation.
