# Channel Assignment — ASN-0133 review-25

**Date:** 2026-06-14 03:32

## Issue 1: The worked example's "iff" contradicts Q5a's own strict-implication result
Reason: Fully internal — Q5a within this same note proves bounded-domain-growth ⟹ H-RF but *not* conversely, supplying the exact flag-and-retract counterexample (zero real fires, unbounded `⋃_k [D_ρ]`). The worked example's "iff" is refuted by the note's own result, and the fix (iff→if, reconcile with Q5a's open-model strict one-way implication) is dictated by content already present.

## Issue 2: The "at-most-once is registration-checkable" formulation is restated near-verbatim 4–5 times (anti-bloat)
Reason: Pure editorial consolidation — state the formulation once (Q-EXT/Q3) and the H-RF-vs-H-W point once (W/H-W), with the other sites citing rather than re-deriving. No design-intent or implementation fact is at stake.

## Issue 3: Q0's "view-stable" enumeration omits `target_of`
Reason: Internal completeness fix. The note already cites "UV's Verdicts-and-optionals clause" as the authority making verdict/optional atoms view-stable, and the note itself classifies `target_of` as a (non-monotone) verdict atom alongside the already-listed `targets_keyed` in Q-FLIP — so `target_of`'s membership in the view-stable category follows from the note's own framework; soundness is unaffected, only the enumeration is incomplete.
