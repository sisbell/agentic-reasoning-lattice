# Channel Assignment — ASN-0069 review-54

**Date:** 2026-06-02 14:54

## Issue 1: V5a (and V8b) classify the named composite K.μ~ as an elementary transition
Reason: The fix is internal. ASN-0047's classification of K.μ~ as a named composite (K.μ⁻ + K.μ⁺) is already quoted in the review and cited in the ASN; the correction is a mechanical reclassification — either drop K.μ~ from the elementary set and handle it at clause (b), or decompose it within clause (a). Both options are derivable from facts already present.

## Issue 2: V12(d) applies P4★ at the pre-fork state without establishing it is a composite boundary
Reason: The fix is internal. Whether the fork's pre-state is a composite boundary follows from ASN-0047's own composite structure (a composite begins and ends at boundaries), and the alternative — deriving `(a, d_src) ∈ R` from a per-state invariant — draws only on invariants already cited in this ASN. No design-intent or implementation evidence is required.
