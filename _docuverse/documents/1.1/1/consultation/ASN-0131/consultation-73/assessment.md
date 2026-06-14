# Channel Assignment — ASN-0131 review-73

**Date:** 2026-06-14 12:01

## Issue 1: `addressable` is wrongly said to depend on the arrangement
Reason: Internal — the fix is a self-contained definitional correction. `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)` is a function of `Σ.L` alone (the note states `nullified` is, and `dom(Σ.L)` trivially is), and the note relies on exactly this elsewhere; dropping "and the present arrangement" needs no design intent or implementation evidence.

## Issue 2: RE-EDIT mis-frames the depth-2 caveat as a scope on delete-stability
Reason: Internal — both facts the fix must separate are already in the note with citations: the stability argument depends only on M-only confinement (holds at any depth), and ASN-0082 supplies a concrete insert at `#p ≥ 2` and a concrete delete only at `#p = 2`. The fix is presentation restructuring over present material, not a question about design or implementation.

## Issue 3: redundant recap sentence in the Σ.L-evolution bridge
Reason: Internal — a purely editorial cut of a closing sentence that restates the distinction the preceding sentence already established; no external input required.
