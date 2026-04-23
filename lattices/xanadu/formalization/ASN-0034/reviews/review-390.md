# Regional Review — ASN-0034/ActionPoint (cycle 3)

*2026-04-22 23:27*

### ActionPoint derivation of `wᵢ = 0` glosses the `i ≤ #w` step
**Class**: OBSERVE
**Foundation**: n/a (internal to ActionPoint derivation)
**ASN**: ActionPoint *Derivation*: "For any i with 1 ≤ i < actionPoint(w), wᵢ = 0: otherwise i would be a member of S with i < actionPoint(w), contradicting (A n ∈ S :: actionPoint(w) ≤ n)."
**Issue**: For i to be a member of S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}, the prose must also secure `i ≤ #w`. From the hypothesis only `1 ≤ i < actionPoint(w)` is given; the `i ≤ #w` conjunct comes by chaining `i < actionPoint(w)` with the already-established `actionPoint(w) ≤ #w` via transitivity/≤-unfolding — a step the prose skips. It is also implicit that the contradiction step (`i < actionPoint(w)` vs. `actionPoint(w) ≤ i`) is discharged by the same irreflexivity+transitivity case analysis walked earlier for uniqueness, but here it is invoked in one line. Inconsistent rigor relative to the uniqueness argument within the same derivation.

### Set-builder notation for S does not type the bound variable
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: ActionPoint: "S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}".
**Issue**: TA-Pos writes its sibling bounded quantifiers with explicit typing: `(E i ∈ ℕ : 1 ≤ i ≤ #t : …)`. ActionPoint's set-builder leaves the ambient type of `i` implicit and then argues "a subset of ℕ by T0's commitment" post-hoc in prose. Parity with TA-Pos would write `S = {i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}`, making the ⊆-ℕ claim immediate from the set-builder rather than a derivation step.

VERDICT: OBSERVE

## Result

Regional review converged after 3 cycles.

*Elapsed: 661s*
