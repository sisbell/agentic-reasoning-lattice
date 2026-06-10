# Channel Assignment — ASN-0126 review-91

**Date:** 2026-06-10 05:06

## Issue 1: "permanently inert substrate" overstates the empty-registry consequence
Reason: Internal fix. The correction is supplied by the ASN's own frame conditions in Registry permanence — `K.σ` extends `dom(Σ.M)`, `K.α` extends `dom(Σ.C)`, and only `K.λ_sh` (the registry-gated step) extends `dom(Σ.L)` — so scoping "inert" to the link store is a re-derivation from material already present, not a question of design intent or implementation behavior.

## Issue 2: the retraction section's central guarantee is grounded only by its failure mode
Reason: Internal fix. The success-path instance is the satisfying case of R-Scope's P-tgt hypothesis (first disjunct, `a ∈ A_rel^Σ`) under R0a's prefix-antichain — both already cited and exercised in the note's failure analysis; the positive leaf example instantiates the same three-move transfer in the conforming direction, requiring no new design or evidence input.

## Issue 3: the empty-from/Nullify exclusion is established, then re-established, deferring twice to the same downstream section
Reason: Internal fix. This is a DRY/anti-bloat prose deduplication confined to the note — collapse the second paragraph's re-derivation onto the first and keep only the new operation-set conclusion `{Emit_K, Observe_K, Nullify_Binary}`; no design intent or implementation evidence bears on it.
