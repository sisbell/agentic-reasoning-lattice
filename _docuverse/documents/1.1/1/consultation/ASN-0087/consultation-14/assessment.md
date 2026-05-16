# Revision Categorization — ASN-0063 review-14

**Date:** 2026-03-21 22:59



## Issue 1: CL11 invariant enumeration incomplete
Category: INTERNAL
Reason: The fix is adding blanket coverage statements for invariants already known to be trivially preserved by properties established in the ASN itself (C' = C, K.λ well-formedness, L12, vacuous coupling). All required information is present in the ASN and its referenced definitions.

## Issue 2: K.μ⁺ amendment absent from Properties Introduced table
Category: INTERNAL
Reason: The amendment is fully defined and justified in the body text; the fix is adding a row to the summary table to reflect what is already written. No external evidence is needed.

## Issue 3: CL3 postcondition omits two frame conditions
Category: INTERNAL
Reason: Both E' = E and R' = R are already established by the frame conditions of K.λ and K.μ⁺_L defined in this ASN. The fix is adding two clauses to CL3 that follow directly from the composite steps' frames.

## Issue 4: CREATELINK precondition silent on direct I-span inputs
Category: INTERNAL
Reason: The well-formedness requirement (T12) for direct I-span inputs is already derivable through K.λ's precondition requiring (F, G, Θ) ∈ Link. The fix is making this implicit constraint explicit in the CREATELINK precondition block — no external design intent or implementation evidence is needed.
