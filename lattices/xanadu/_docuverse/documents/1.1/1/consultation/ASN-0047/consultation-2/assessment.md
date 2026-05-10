# Revision Categorization — ASN-0047 review-2

**Date:** 2026-03-17 02:21

## Issue 1: K.μ⁺ frame omits C' = C, contradicting P5 proof
Category: INTERNAL
Reason: The fix is adding an omitted frame condition that is already implied by K.μ⁺'s definition (it modifies only M(d)). Purely mechanical correction within the ASN's own formalism.

## Issue 2: P4 proof conflates elementary and composite transition analysis
Category: INTERNAL
Reason: The proof restructuring requires only definitions already present in the ASN — the review itself spells out the three-step composition argument needed. No external evidence about design intent or implementation behavior is required.

## Issue 3: R's definition claims historical fidelity that K.ρ's precondition does not enforce
Category: INTERNAL
Reason: The Nelson and Gregory evidence already cited in the ASN both point to tight coupling ("accumulates entries from every content addition"; "every previous arrangement remains reconstructable"). Option (a) — adding the reverse coupling K.ρ only when K.μ⁺ provides the pair — follows directly from the ASN's own definitions and the evidence already incorporated. The over-approximation is an unintended gap in the formalization, not a deliberate design choice.
