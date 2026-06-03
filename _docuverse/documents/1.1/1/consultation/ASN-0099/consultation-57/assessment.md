# Channel Assignment — ASN-0099 review-57

**Date:** 2026-06-03 09:43

## Issue 1: Silent-projection "uniqueness" is overclaimed
Reason: The fix is internal — the missing conjunct (faithfulness on present V-positions) and the corrected uniqueness statement are derivable from `image`'s own definition already in the ASN; no design-intent or implementation evidence is required to either weaken the prose or restore the predicate.

## Issue 2: F13 proof stops at the per-slot condition
Reason: The fix is internal — lifting the per-slot biconditional to the comprehension via `(E i : Pᵢ ∨ Qᵢ) ⟺ (E i : Pᵢ) ∨ (E i : Qᵢ)` is a pure logical step over F1's existential, fully derivable from the ASN's own definitions.

## Issue 3: V-side additivity asserted "directly" with no derivation
Reason: The fix is internal — the four-step chain (F12 unfold → F20 image-union → F13 set-additive → F12 refold) composes claims already present in this ASN, requiring no external channel.
