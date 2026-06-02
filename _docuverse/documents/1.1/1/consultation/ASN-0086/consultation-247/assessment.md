# Channel Assignment — ASN-0086 review-247

**Date:** 2026-06-01 22:28

## Issue 1: (UZ) introduced as "used throughout" but never used
Reason: Internal bookkeeping fix — the note's own text shows (UZ) is never referenced and every zero-count argument is done directly. Deleting it or citing a use site is decidable from the ASN alone.

## Issue 2: Phantom precondition "P2" introduced only to be dismissed (wp Case 1)
Reason: Internal — Nullify's preconditions (P0, P1, P-tgt) and R-Scope's arity-independence are both stated in the note; restating without the invented P2 label needs no external evidence.

## Issue 3: R3 proof skips the `|Σ'.L(a)| = 3` conjunct
Reason: Internal — R2 (value preserved exactly) and the four-conjunct TypedRelation definition are both present in the ASN, so the missing arity clause is derivable directly.

## Issue 4: Discipline-discharge induction lists Observe_K among transition cases
Reason: Internal — the `→ ≡ K.σ ∪ K.α ∪ K.λ` definition and the triple-restriction of `L_R` (the `|Σ.L(a)| = 3` conjunct) are both stated in the note, so dropping Observe_K and adding the triple-only clause is self-contained.
