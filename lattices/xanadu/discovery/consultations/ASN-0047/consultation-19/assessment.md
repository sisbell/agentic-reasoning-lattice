# Revision Categorization — ASN-0047 review-19

**Date:** 2026-03-17 10:13



## Issue 1: S2 preservation not verified for K.μ⁺ or K.μ~
Category: INTERNAL
Reason: The fix requires adding explicit statements about functionality preservation that follow directly from the existing definitions — extension at disjoint domain elements and injectivity of π are already established in the ASN.

## Issue 2: Base case misattributes vacuity of P4 and P7
Category: INTERNAL
Reason: The correct attributions (P4 to (E₀)_doc = ∅, P7 to R₀ = ∅, P6 to dom(C₀) = ∅) are derivable from the initial state definition already given in the ASN.

## Issue 3: K.μ~ description admits no exception for the identity bijection
Category: INTERNAL
Reason: Whether to restrict π or soften the description is a notational choice resolvable from the existing formal definition and the already-stated empty-case handling — no external evidence needed.

## Issue 4: P4 proof cites J1' in the K.ρ case, but J1' is irrelevant to P4
Category: INTERNAL
Reason: The direct argument (K.ρ extends R while Contains is unchanged) is already present in the ASN text; the fix is restructuring the paragraph to lead with it rather than with the J1' reference.
