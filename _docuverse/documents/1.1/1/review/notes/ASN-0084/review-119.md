# Review of ASN-0084

I traced the full argument chain — the singleton-tumbler identification, the region partition, both postconditions, the four permutation/commutativity lemmas, R-BLK's split/classify/reassemble pipeline, and R-CANON — plus all six worked examples by hand. The arithmetic in every example reconciles with the explicit π formulas and displacement claims. The invariant-preservation audit discharges each S-invariant correctly, and the anti-bloat scan confirms the forward-reference accretions named in the prior declined findings (OrdShiftHom (a)/(b) miscitation, cross-phase content displacement) have already been removed.

Specific things I checked and found sound:

- **Coverage/exhaustiveness** in R-PIV and R-SWP: the half-open ordinal ranges [p, p+w_β), [p+w_β, p+w_β+w_μ), … tile [c₀, c_{n−1}) exactly, with p+w_α+w_β = ord(c₂) (3-cut) and p+w_β+w_μ+w_α = ord(c₃) (4-cut). Width positivity (w ≥ 1 from CS2 strictness) keeps every region non-empty.
- **Surjectivity** of π via finite self-injection (S8-fin) — images verified to land in dom(M(d)).
- **R-CANON** forward/backward extension proofs: both correctly force the candidate-extension position to the start/end of a neighboring run, yielding a mergeable pair and contradicting the no-merge hypothesis. The r ≠ r″ disjointness step (ord(u) = ord(v)−1 < ord(v)) holds.
- **R-BLK Phase 1** progressive refinement: split offsets are computed against the *current* sub-run start, correct under sequential cut processing; the "Outside ⋃V(b_k)" branch fires only at c_{n−1} via EXT-VAC.
- **Cross-group disjointness** in R-BLK via T10 (ASN-0034): [1] and [2] are non-nesting, so subspace-S and non-S V-extents are disjoint — valid.
- **Boundary/empty-exterior** and **non-S pass-through** are each exercised by a dedicated example with the frame conditions (R-FRAME-P/S(a)) doing the work.

## OUT_OF_SCOPE

### Topic 1: Weakest precondition for the post-state invariant suite Q
**Why out of scope**: The ASN proves R-PRE is *sufficient* for the invariant suite but explicitly defers the *weakest* precondition to its Open Questions. Computing wp(REARRANGE_K, Q) is a genuine refinement, not a gap in the present sufficiency argument.

### Topic 2: k-cut generalization (k > 4) and composition of rearrangements
**Why out of scope**: New territory (the natural permutation class for k cuts; closure of rearrangements under composition) already named as Open Questions; not an error in the 3-/4-cut treatment.

VERDICT: CONVERGED
