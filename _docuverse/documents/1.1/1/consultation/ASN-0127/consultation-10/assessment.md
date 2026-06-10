# Channel Assignment — ASN-0127 review-10

**Date:** 2026-06-10 02:16

## Issue 1: Injective-reorder discovery change wrongly claimed to "respect no containment"
Reason: This is a pure logical correction — the invalid step (transferring image-incomparability to discovery-set incomparability when `findlinks` is not order-reflecting) and both repair options (weaken to an existence claim, or add the disjoint-witness hypothesis) are settled by definitions already in the note (F-MATCH's per-link existential, F-IMG-SWING's cardinality pinning, the existing "necessary but not sufficient" caveat). The counterexample's one external-looking ingredient — a content address reached by no link — is itself internal, following from K.α/K.λ being independent atomic transitions and L4's "endsets may reference any address" (no converse coverage requirement), so no design-intent or implementation evidence is needed.
