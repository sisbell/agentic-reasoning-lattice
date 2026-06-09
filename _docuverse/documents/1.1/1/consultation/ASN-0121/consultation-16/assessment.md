# Channel Assignment — ASN-0121 review-16

**Date:** 2026-06-09 02:11

## Issue 1: FL-WP case (a) discharges addressability with the wrong notion of freshness
Reason: The fix is internal. The reviewer's option (a) — adding the conjunct `¬(E (b,F',G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))` to the wp — follows directly from unfolding the ASN-0086 `nullified` definition the ASN already imports and uses; restricting "unconditionally" to genuine freshness needs no design-intent or implementation evidence. (Option (b)'s vacuity proof would require importing ASN-0086's retraction-span discipline, which this ASN explicitly avoids invoking, so the conservative weakest-precondition fix is to carry the conjunct rather than assert it away.)
