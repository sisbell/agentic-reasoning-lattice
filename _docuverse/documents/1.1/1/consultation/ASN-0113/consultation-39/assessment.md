# Channel Assignment — ASN-0113 review-39

**Date:** 2026-06-08 10:30

## Issue 1: Unused permanence dependencies listed as relied-upon facts
Reason: Internal. The fix is a derivable consistency check — scanning W0–W20 shows no claim invokes L12/P0, and W8 already establishes the operation is a present-state query for which value-permanence is irrelevant. No design intent or implementation evidence is needed to delete an unused list entry.

## Issue 2: W8's read-set contradicts its own dependency claim
Reason: Internal. The actual read-set is fixed by the note's own definitions — `V_S(d) = {v ∈ dom(M(d)) : v₁ = S}` consults only `dom(M(d))` and the subspace projection, never `M(d)(v)`, `C`, or `L`. Reconciling the sentence to "function of `dom(M(d))` alone" follows directly from the ASN's existing definitions.
