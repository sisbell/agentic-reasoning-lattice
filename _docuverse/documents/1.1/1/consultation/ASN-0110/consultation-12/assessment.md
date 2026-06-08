# Channel Assignment — ASN-0110 review-12

**Date:** 2026-06-08 01:33

## Issue 1: RE-anon overclaims that the result yields no lower bound on the total contributing-link count
Reason: The correction is a pure consequence of RE-witness and RE-result already in the note — each link contributes at most one slot-`i` endset, so `max_i |Eᵢ|` lower-bounds the total contributing-link count. No design intent or implementation evidence is at stake; the fix is internal arithmetic.

## Issue 2: RE-reveal's single-link example overclaims result-level attribution
Reason: Whether the result determines per-link pairing is settled by RE-result/RE-anon's own indistinguishability argument (the `⟨{F₂},{F₁},∅⟩` ambiguity); qualifying or removing the "trivially attributed" claim follows from the note's existing definitions. Internal fix.
