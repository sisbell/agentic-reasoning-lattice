# Regional Review — ASN-0034/OrdinalDisplacement (cycle 1)

*2026-04-23 00:06*

### OrdinalDisplacement miscites NAT-zero for `0 ∈ ℕ`
**Class**: REVISE
**Foundation**: NAT-zero axiom is `0 ∈ ℕ` and `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`; consequence is `¬(n < 0)`.
**ASN**: OrdinalDisplacement, "Component typing" paragraph: *"positions 1..m−1 are 0, with `0 ∈ ℕ` from NAT-zero's `(A n ∈ ℕ :: 0 ≤ n)`."*
**Issue**: The cited statement `(A n ∈ ℕ :: 0 ≤ n)` is not in NAT-zero's formal contract — NAT-zero states the disjunction `0 < n ∨ 0 = n`, not the ≤-form. Further, the fact actually needed is `0 ∈ ℕ`, which NAT-zero supplies directly as its first axiom clause; a universally-quantified statement `(A n ∈ ℕ :: P(n))` presupposes `0 ∈ ℕ` for the instance but does not establish it. Citing a derived, non-canonical form to ground a simple set-membership is a false attribution a precise reader cannot verify from NAT-zero as written.
**What needs resolving**: Cite the clause of NAT-zero that actually supplies `0 ∈ ℕ` (the first axiom clause), or, if a ≤-form is genuinely needed elsewhere, derive it explicitly rather than attribute it to NAT-zero.

### ActionPoint's route `w_{actionPoint(w)} ≠ 0 ⟹ 0 < w_{actionPoint(w)}` folds-then-unfolds through ≤
**Class**: REVISE
**Foundation**: NAT-zero axiom: `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`. NAT-order: `m ≤ n ⟺ m < n ∨ m = n`.
**ASN**: ActionPoint derivation: *"membership of actionPoint(w) in S gives w_{actionPoint(w)} ≠ 0; by NAT-zero, 0 ≤ w_{actionPoint(w)}; by NAT-order's definition m ≤ n ⟺ m < n ∨ m = n, this unfolds to 0 < w_{actionPoint(w)} ∨ 0 = w_{actionPoint(w)}…"*
**Issue**: NAT-zero directly states the disjunction `0 < n ∨ 0 = n` at `n = w_{actionPoint(w)}`. The proof instead folds that disjunction into `0 ≤ w_{actionPoint(w)}` (implicitly invoking NAT-order's ≤-definition) and then unfolds it back to the same disjunction via the same definition — a round-trip that attributes the ≤-form to NAT-zero (which does not state it) and adds two citation steps where none are needed. The proof reads as if the author was uncertain which axiom supplies what.
**What needs resolving**: Instantiate NAT-zero's disjunction axiom directly at `w_{actionPoint(w)} ∈ ℕ` to obtain `0 < w_{actionPoint(w)} ∨ 0 = w_{actionPoint(w)}`, then discharge the equality by `w_{actionPoint(w)} ≠ 0`. No intermediate ≤-step is required.

### OrdinalDisplacement's promotion of `n ≥ 1` to `n ≠ 0` is longer than the claim requires
**Class**: OBSERVE
**Foundation**: NAT-order (irreflexivity, ≤-definition); NAT-addcompat (`n < n+1`).
**ASN**: OrdinalDisplacement, "Promote `n ≥ 1` to `n ≠ 0`" paragraph.
**Issue**: To obtain `n ≠ 0` from `n ≥ 1`, the proof anchors `0 < 1` via NAT-addcompat, case-splits the disjunction from `n ≥ 1`, composes `<` by transitivity in one case and substitutes in the other, and closes by irreflexivity. This is correct but elaborate: `n ≥ 1` unfolded to `1 < n ∨ 1 = n` excludes `n = 0` more directly — the equality case gives `n = 1 ≠ 0` (via `0 < 1` and irreflexivity), and the strict case `1 < n` with `0 < 1` gives `0 < n` in one line. The current version's intermediate conclusion `0 < n` is not itself used downstream; only `n ≠ 0` is needed for TA-Pos. Trimming would tighten the argument without changing correctness.

VERDICT: REVISE
