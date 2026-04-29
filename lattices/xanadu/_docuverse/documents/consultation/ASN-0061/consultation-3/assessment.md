# Revision Categorization — ASN-0061 review-3

**Date:** 2026-03-21 11:00



## Issue 1: D-CF justifications cite wrong or incomplete sources
Category: INTERNAL
Reason: The fix requires correcting citation targets from P0/J2 to the elementary transition frame conditions (K.μ⁻, K.μ⁺) and stating `ran(M'(d)) ⊆ ran(M(d))` explicitly — all derivable from ASN-0047 definitions already referenced in the composite transition section.

## Issue 2: Composite transition decomposition invalid when R = ∅
Category: INTERNAL
Reason: The fix requires adding a conditional branch (R = ∅ → K.μ⁻ only; R ≠ ∅ → K.μ⁻ + K.μ⁺) and verifying coupling constraints for the single-step case — all derivable from the existing ASN-0047 elementary transition definitions and the already-established postconditions.
