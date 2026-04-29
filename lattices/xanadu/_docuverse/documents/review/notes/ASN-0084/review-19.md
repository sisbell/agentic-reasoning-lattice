# Review of ASN-0084

I checked every proof in detail: the postcondition well-definedness arguments (R-PIV, R-SWP), the bijection constructions (R-PPERM, R-SPERM), the displacement analysis (R-DISP), the permutation-shift commutativity (R-COMM), the canonical block decomposition uniqueness proof (parts a–d), and the block decomposition transformation (R-BLK). I also verified both worked examples position-by-position, including the merge checks and displacement calculations.

The proofs are thorough: every case is shown explicitly (no "by similar reasoning"), every invariant conjunct from ASN-0036 is addressed in the invariant preservation argument, edge cases (single-position regions, blocks spanning region boundaries) are handled by the split/classify/reassemble phases, and the two worked examples provide concrete verification against explicit values.

The canonical block decomposition uniqueness proof deserves particular note — it avoids I-address subtraction by formulating the backward extent via forward-checking, carefully uses TS2 (shift injectivity) and TS4/TS5 for the identity argument in part (b), and establishes merge-order independence through the deterministic nature of maximal blocks. The four-step structure (unique maximal block per position → overlap implies identity → merge convergence → maximality precludes merge) is complete.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Zero-sum displacement as a formal lemma
The total displacement across the affected range sums to zero (verified algebraically for both 3-cut and 4-cut). Stating this as a named lemma would make it citable by downstream ASNs on rearrangement composition.
**Why out of scope**: Derivable from the existing R-DISP analysis — a convenience property, not a gap.

### Topic 2: Involution property of the pivot
Two successive 3-cut pivots with the same cut sequence compose to the identity permutation. This follows from R-PPERM but belongs in a future ASN on rearrangement composition.
**Why out of scope**: Composition semantics is new territory, already identified in the open questions.

### Topic 3: Block count bounds under rearrangement
The 4-cut example shows a merge opportunity arising post-rearrangement (B,C reconnect with H). Characterizing when rearrangements increase vs decrease the canonical block count — and bounding the increase relative to the number of cuts — would be valuable for complexity analysis.
**Why out of scope**: Already identified as an open question; requires analysis beyond the scope of this ASN.

VERDICT: CONVERGED
