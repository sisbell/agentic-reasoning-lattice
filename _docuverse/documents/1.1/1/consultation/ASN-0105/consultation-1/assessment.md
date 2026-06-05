# Channel Assignment — ASN-0105 review-1

**Date:** 2026-06-04 18:24

## Issue 1: Subspace-confinement argument needs an action-point constraint the precondition does not impose
Reason: Internal. The fix is to strengthen precondition 3 with `actionPoint(ℓ) = #ℓ = m` and rewrite the T5/T12 derivation accordingly — pure tumbler arithmetic against foundation facts already cited in the ASN. The confinement-as-caller-obligation rationale is already established (Gregory Q19), so no new design intent or implementation evidence is required.

## Issue 2: R5 references an undefined symbol and is stated vaguely
Reason: Internal. Restating R5 as `if reach(σ) > max(A) then #ρ = |A|` guarded by `A ≠ ∅`, or folding it into R4, follows directly from R0/R4 already proven in the note. No external channel needed.

## Issue 3: No concrete worked example
Reason: Internal. The example uses author-constructed tumbler values to instantiate R0–R3, R7, R8 — all the claims and machinery are already in the ASN; verifying the produced sequence requires only the note's own definitions.
