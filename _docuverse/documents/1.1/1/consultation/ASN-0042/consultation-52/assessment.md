# Channel Assignment — ASN-0042 review-52

**Date:** 2026-05-14 09:29

## Issue 1: Worked example creates two inconsistent trajectories for Σ_0
Reason: This is an internal consistency choice between two framings of the worked example's initial state. The ASN already specifies the seeded contents and Bop semantics needed; fix is editorial selection between options (a) and (b).

## Issue 2: "delegated_Σ*" is defined informally
Reason: This is a formal definition cleanup using standard reflexive-transitive closure machinery. The base relation R_Σ and its closure are derivable from existing definitions in the ASN.

## Issue 3: "AccountLevelPermanence" name overpromises
Reason: The formal scope (all π ∈ Π_Σ) and Nelson's already-cited "User 3.2" example (which extends sovereignty recursively to sub-accounts) both indicate generality. Naming choice between rename and restrict is editorial, derivable from existing content.

## Issue 4: O10 worked example's Σ_pre construction omits required B1 verification
Reason: Presentation-level rigor decision — either trace per-transition B6/B1 obligations or state upfront that only cumulative state is verified. ASN-0040's B6 and B1 contracts are already imported; the trajectory's parameters are all specified.

## Issue 5: O3's corollary on monotonic refinement is stated for "all transitions" without restricting to address-preserving ones
Reason: Pure precondition tightening — add a ∈ Σ.B so ω_Σ(a) is well-defined. The fix follows directly from O2's own domain restriction.

## Issue 6: Property table for O2 omits load-bearing dependencies
Reason: Citation audit. The proof body of O2 explicitly cites Prefix (PrefixRelation) and T3 (CanonicalRepresentation); the missing dependencies are visible in the existing derivation text.
