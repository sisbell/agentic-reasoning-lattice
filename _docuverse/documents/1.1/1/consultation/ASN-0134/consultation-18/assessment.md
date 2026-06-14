# Channel Assignment — ASN-0134 review-18

**Date:** 2026-06-14 01:26

## Issue 1: `stale(h)` is classified as single-index, but its own realization model makes it multi-access
Reason: The contradiction and its only viable fix follow entirely from premises the note already states — §8's no-whole-state-read, A1's per-home frontier recovery (one descent per home), and §4's per-call homing that spreads `A_K`'s members across many homes — applied consistently with the note's own `targets_keyed` multi-read logic. Option (a) is self-defeating inside that logic (it would force `targets_keyed`'s reclassification), and the existing Gregory `findpreviousisagr` evidence for *single-home* frontier recovery already stands, so reclassifying multi-home `stale` as a clause-7 multi-read needs no external input — any atomicity udanax-green's loop happens to give is over-satisfaction, exactly as for clauses 2/7.

## Issue 2: V2 calls the middle condition both "strict implication" and "the genuine soundness requirement"
Reason: Pure internal logical/terminological inconsistency — the note's own banking argument proves only sufficiency (no `Q`-affecting step ⟹ verdict `= Q(Σ_{r₁})`), the reviewer's counterexamples to necessity (`g` insensitive, coincidental equality) are elementary logical observations, and the coherent repair — calling the middle condition the *weakest sufficient* condition rather than "the requirement" — is derivable from the proof already present.
