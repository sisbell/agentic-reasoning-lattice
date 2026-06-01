# Channel Assignment — ASN-0047 review-184

**Date:** 2026-05-31 23:26

## Issue 1: Dangling forward reference to a nonexistent "Rationale (k = 0 conjuncts)" subsection, motivating FrontierEquivalence
Reason: Internal. FrontierEquivalence's own proof already establishes that `inc(t,0) ∉ E` turns on whether a prior K.δ event fired `(t,0)` on A's chain — i.e., on allocation history preserved by P1, not on t's component structure. The argument that a T4b parse of t alone cannot recover this is derivable from the lemma's existing forward/reverse directions; either point the reference at a consolidated statement of that fact or delete the clause.

## Issue 2: "S7a–S7d" range notation implies a nonexistent S7c
Reason: Internal. The authoritative per-state conjunction in the *Extended reachable-state invariants* section already spells "S7a ∧ S7b ∧ C1b ∧ S7d"; the fix is to replace the contracted range with that explicit form to match the body. No design intent or implementation evidence is at stake.

## Issue 3: Epistemic hedge in the J1'★ derivation does not advance the argument
Reason: Internal. The preceding sentence already names J0 + P2 as the ValidComposite★ constraints that close the gap; deleting the hedge or compressing it to one clause is a pure prose edit requiring no external input.
