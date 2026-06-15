# Channel Assignment — ASN-0133 review-59

**Date:** 2026-06-15 00:12

## Issue 1: Fire dischargeability rests on an unnamed registered-home hypothesis
Reason: Internal. The gate requirement (`K.λ_sh` needs `d ∈ dom(Σ.M)`, the surface excludes `K.σ`/`K.α`, `Sh-conf` for Binary needs `|F|=|G|=1`) is operational-semantics content already supplied by the note's cited dependencies ASN-0126/0128; naming the precondition and adding a registered home to `Σ₀` is a formal modeling choice derivable from that machinery, with no appeal to Xanadu design intent or implementation behavior.

## Issue 2: Cross-rule re-arm is asserted, deferred to a mismatched Open Question, and uses undefined terminology
Reason: Internal. Re-pointing the deferral (OQ4→OQ2), defining-or-dropping "lower rule," and constructing a minimal two-non-SF-trigger mutual-re-arm pair all draw on the note's own falsifier inventory (Q-FLIP's deposit re-armer flipping an active-view `∃`-trigger ⊥→⊤, PD1/PD2 from ASN-0129) — no design-intent or code evidence is implicated.

## Issue 3: Anti-bloat residue
Reason: Internal. Both fixes are pure deletions of redundant prose (an excluded-case parenthetical the regime's own standing hypothesis forbids, and a duplicated chain/audit remark) — editorial removals requiring no external channel.
