# Channel Assignment — ASN-0042 review-49

**Date:** 2026-05-14 08:20

## Issue 1: Worked example's sub-account namespace + subsequent delegation contradicts O18
Reason: The fix is derivable from the ASN's own content. O18 (DelegationBaptizes) is already stated in the ASN with the freshness conjunct `pfx(π') ∈ Σ'.B ∖ Σ.B`; the contradiction is purely internal to the worked example's narrative against an established axiom. Resolving it requires only restructuring the conditional's framing — no design intent or implementation evidence is needed.

## Issue 2: O1's preconditions over-restrict the predicate's domain
Reason: The fix is derivable from the ASN's own content. The well-formedness argument preceding the formal contract already establishes that only `T4(pfx(π))` and T3's component determinacy are needed for `owns(π, a) ≡ pfx(π) ≼ a` to be decidable on arbitrary `a ∈ T`. Reconciling the precondition with the postcondition is a mechanical alignment of the contract with the proof already given.
