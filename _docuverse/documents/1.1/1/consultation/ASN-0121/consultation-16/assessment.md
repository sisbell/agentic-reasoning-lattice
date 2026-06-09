# Channel Assignment — ASN-0121 review-16

**Date:** 2026-06-09 02:10

## Issue 1: FL-WP case (a) discharges addressability with the wrong notion of freshness
Reason: The fix is internal. Option (a) — adding the conjunct `¬(E (b,F',G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))` to the wp — is derivable entirely from the inherited `nullified` definition and the already-stated fact that an ordinary K.λ leaves `L_R^Σ` fixed; it makes the stated precondition genuinely weakest with no appeal to retraction-span discipline. Option (b)'s vacuity argument would require asserting a unit-depth retraction discipline the ASN explicitly does not invoke (working over the full ASN-0047 vocabulary), so the conservative, self-contained repair is (a).
