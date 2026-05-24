# Revision Categorization — ASN-0051 review-6

**Date:** 2026-03-20 21:45

## Issue 1: SV6 precondition "within the element field" is informal
Category: INTERNAL
Reason: The T4 field decomposition and zeros(s) are already defined in the foundation ASNs. The fix is to restate the informal gloss using the position p₃ of the third zero component — purely a precision improvement derivable from existing definitions.

## Issue 2: Resolution change under reordering — claimed without proof, contradicted by worked example
Category: INTERNAL
Reason: The formal relationship resolve_{Σ'} = π(resolve_Σ) follows directly from K.μ~'s definition already in ASN-0047, and a proper witness can be constructed from the existing definitions of resolve and reordering. The worked example annotation is editorial.

## Issue 3: SV7 formal content is subsumed by SV8
Category: INTERNAL
Reason: The logical subsumption is visible from the two properties' statements within this ASN. Reformulating SV7 to capture the "no coupling step" claim requires only checking that no link-propagation operation exists in the ASN-0047 repertoire — derivable from the existing operation definitions.

## Issue 4: Bilateral vitality — vacuous case unaddressed
Category: INTERNAL
Reason: L3 already permits empty endsets as an established foundation axiom. The fix is to acknowledge the vacuous case and note that a (∅, ∅, Θ) link is a pure type annotation with no content vitality to lose — this follows from the existing definitions without requiring design-intent consultation.

## Issue 5: SV13(e) omits non-arrangement transitions
Category: INTERNAL
Reason: The frame conditions of K.α, K.δ, and K.ρ are explicitly stated in ASN-0047. The fix is mechanical — add a sentence noting these transitions hold M constant, so resolve is trivially preserved.
