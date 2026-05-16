# Revision Categorization — ASN-0063 review-16

**Date:** 2026-03-21 23:46



## Issue 1: ExtendedReachableStateInvariants — D-CTG and D-MIN unverified for K.μ⁺, K.μ⁻, K.μ~
Category: INTERNAL
Reason: D-CTG and D-MIN are structural invariants defined in ASN-0036 and ASN-0047. The fix requires tightening preconditions or adding preservation arguments using definitions already present in those ASNs and this one — no design intent or implementation evidence is needed.

## Issue 2: CL11 S8 verification — link-subspace runs omitted
Category: INTERNAL
Reason: The fix is a completeness gap in the proof text. The argument that existing link-subspace runs are unchanged follows from K.μ⁺_L's frame condition and the new position's properties, all of which are already defined in this ASN.

## Issue 3: CL2 derivation gap
Category: INTERNAL
Reason: The fix is a precision issue in the proof reference — CL1's proof constructs exactly `resolve(d, Ψ)`, and the derivation needs to cite the construction rather than the existential statement. All material is present in the ASN.

## Issue 4: Link-subspace withdrawal — singleton imprecision
Category: INTERNAL
Reason: The singleton case is a logical edge case derivable from D-MIN's definition (vacuous satisfaction for empty sets). The fix requires only qualifying the existing claim with the `|V_{s_L}(d)| = 1` case.

## Issue 5: CREATELINK valid composite not explicitly verified
Category: INTERNAL
Reason: All pieces for the ValidComposite verification are already present in the ASN — K.λ's frame, K.μ⁺_L's preconditions, and the coupling constraint analysis. The fix is consolidating these into an explicit verification block at the composite definition site.
