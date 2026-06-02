# Channel Assignment — ASN-0070 review-15

**Date:** 2026-06-02 15:06

## Issue 1: F-canonical proves uniqueness but not existence
Reason: The fix is internal — it adds the existence construction using machinery already present in the ASN (the consecutivity characterization from Step 2, ordinal-displacement spans, and S8 NormalizationExistence from ASN-0053's cited foundations). No design intent or implementation evidence is required.

## Issue 2: F1 postcondition asserts component depth unconditionally
Reason: The fix is internal — the vacuous-subspace convention (`Σ_V^S = ⟨⟩` when `V_S(d) = ∅`) is already established in The Setting and the V-restricted denotation section; F1 only needs to mirror that existing caveat.
