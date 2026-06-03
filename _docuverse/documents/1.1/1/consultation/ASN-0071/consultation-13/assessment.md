# Channel Assignment — ASN-0071 review-13

**Date:** 2026-06-02 22:50

## Issue 1: find-predicate interaction with the link subspace is never discharged
Reason: The fix is a one-line dual of the source-side confinement argument the ASN already proves, combined with the disjointness `dom(L) ∩ dom(C) = ∅` which the review itself supplies as ASN-0047 L14; both ingredients are already cited and present, so the discharge is derivable internally.

## Issue 2: worked scenario never verifies the exclusion (negative) direction of the predicate
Reason: Adding a third document `d_C` referencing a distinct I-address uses only ASN-0047 transitions (K.δ, K.α, K.μ⁺) already exercised in the scenario and the F-find definition; the construction and the empty-intersection check are fully derivable from the ASN's own content.
