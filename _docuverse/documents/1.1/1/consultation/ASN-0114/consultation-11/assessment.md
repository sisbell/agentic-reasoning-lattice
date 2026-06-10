# Channel Assignment — ASN-0114 review-11

**Date:** 2026-06-09 21:48

## Issue 1: `coverage(·)` applied to span-sets is the foundation operator on the wrong type
Reason: Pure notational bridge between two operators the note already cites — ASN-0053's `⟦·⟧` for span-sets and ASN-0043/0098's `coverage` on endsets. The justification ("both reduce to the union over the same spans, so sequence-vs-set and span order are immaterial") is definitional and already gestured at in the note; no design intent or implementation evidence is required.

## Issue 2: F7 carves out slot 3 by convention without citing L3 or deriving the consequence
Reason: Both ingredients are already in the ASN — L3 (`Σ.L(a).e₃ ≠ ∅`) is cited in the substrate section, and the second S2 collapse (`coverage(eᵢ) = ∅ ⟺ eᵢ = ∅`) is established at F7. The fix is a one-step combination yielding `coverage(Σ.L(a).e₃) ≠ ∅`, hence `followlink(Σ, a, 3) ≠ ⟨⟩`; it re-cites an established foundation claim rather than re-justifying it, so it is internally derivable.

## Issue 3: isolated methodology editorializing
Reason: Purely editorial — delete or fold a standalone meta-sentence into the adjacent counterexample. No design-intent or implementation question is involved.
