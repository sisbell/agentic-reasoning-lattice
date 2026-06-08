# Channel Assignment — ASN-0107 review-32

**Date:** 2026-06-08 13:06

## Issue 1: W2's k-for-k swap asserts a preserved count without deriving it
Reason: The fix is internal — either derive the `K.μ⁻ → K.α/K.μ⁺/K.λ` composite using the substrate transitions and laws (D2, P0, P2) already present in the ASN, or retreat to the `k = 1` single-swap the note already concedes is clean. No design intent or implementation evidence is needed; this is a self-contained derivation/scoping choice.

## Issue 2: Trailing-suffix definition enumerates its downstream consumers
Reason: Purely a prose trim — end the sentence at the property's statement. Entirely internal, no channel needed.
