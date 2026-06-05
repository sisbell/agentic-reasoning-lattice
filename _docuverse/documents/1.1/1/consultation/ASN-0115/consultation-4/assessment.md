# Channel Assignment — ASN-0115 review-4

**Date:** 2026-06-05 06:05

## Issue 1: R7 Repeatability assumes comparability that the hypothesis does not supply
Reason: This is a proof-structure gap, not a question of design intent or implementation behavior — both fixes (restrict the hypothesis to `Σ →* Σ'`, or argue branch-local allocation breaks shared-value equality) are settled by the ASN's own model: SequentialTransitionAxiom (ASN-0047), state-determined allocation, and S0/L12. Derivable internally.

## Issue 2: Finiteness of `act(ρ, Σ)` asserted without its premise
Reason: Purely a citation correction — finiteness comes from `dom(Σ.M(d))` being finite (S8-fin, ASN-0036), with T1 supplying only the order. No design or implementation evidence needed.
