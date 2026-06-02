# Channel Assignment — ASN-0086 review-234

**Date:** 2026-06-01 20:20

## Issue 1: Two sections defer to "Worked Sketch Step 4" for the self-emit branch
Reason: Purely editorial — both sites already prove the self-emit branch intrinsically (Nullify def via `a = b ∈ dom(Σ'.L)`, WP Case 1 via `A_rel^{Σ'} = A_rel^Σ ∪ {e}`), so removing the forward pointers requires only the ASN's own reasoning. No design intent or implementation evidence is at stake.

## Issue 2: R5 proof reuses `d` with two distinct bindings
Reason: A self-contained variable-binding cleanup; the ASN itself establishes that any allocated home suffices (R0 quantifies over any `d ∈ dom(Σ.M)`), so the fix is derivable from the note's existing content without external channels.
