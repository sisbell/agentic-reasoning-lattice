# Channel Assignment — ASN-0133 review-42

**Date:** 2026-06-14 13:43

## Issue 1: "cannot in fact diverge" overstates a result the same paragraph makes hypothesis-conditional
Reason: Internal — the note already supplies everything the fix needs: the bounded-input hypothesis is named "the registry's one honest hypothesis on its environment," and the text already states that `[D_{ρ_P}]` grows by environment deposits of `tgt`/`attn` the types do not close. Qualifying "cannot diverge" to "no internal divergence route" and scoping "producer-domain growth is closed" to `ρ_R`'s emissions is a consistency repair against the note's own open-model thesis (Q5a, type-isolation argument), requiring neither design intent nor implementation evidence.

## Issue 2: H-FAIR's definition is padded with a forward-pointer and a twice-stated principle (anti-bloat)
Reason: Internal — pure anti-bloat trim. Dropping the "Q6 reads the discharge at this strength" forward-pointer and the redundant "Without this escape…" restatement, and stating the registry-not-environment principle once, removes repetition already present in the text. No design or implementation question bears on which sentences are redundant.
