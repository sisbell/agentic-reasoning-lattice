# Regional Review — ASN-0034/OrdinalDisplacement (cycle 3)

*2026-04-23 00:17*

### TA-Pos "Note on notation" is defensive prose citing forward-referenced concepts
**Class**: OBSERVE
**Foundation**: N/A (TA-Pos body)
**ASN**: TA-Pos: *"The predicate `Pos(t)` is not written `t > 0`, because `>` is reserved elsewhere for a lexicographic ordering on tumblers under which a zero tumbler may strictly exceed another zero tumbler: the length-1 tumbler `0` is a proper prefix of the length-2 tumbler `0.0`, and under the prefix rule of that ordering `0 < 0.0`, so `0.0 > 0` even though `Zero(0.0)` holds. … The lexicographic ordering and its prefix rule alluded to here are supplied by claims outside this region and enter no obligation of TA-Pos."*
**Issue**: The note is a defensive justification for a naming choice (`Pos(t)` rather than `t > 0`), hinging on a lexicographic ordering the reader is told is defined elsewhere and imposes no obligation on TA-Pos. It invites the reader to hold external, unverified content in mind only to discharge a naming objection. The note does not state what `Pos` means, how it is defined, or any consequence; it argues against a counterfactual spelling. The explicit disclaimer ("enter no obligation of TA-Pos") confirms that the argument is not load-bearing for the claim. This is defensive essay content in a claim slot.

### ActionPoint's set-builder for S drops the `i ∈ ℕ` typing used elsewhere
**Class**: OBSERVE
**Foundation**: TA-Pos uses `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))` and `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)` — every bound index carries an explicit `i ∈ ℕ`. TA-Pos's prose justifies this as "keep[ing] parity with the `(A n ∈ ℕ :: …)` form used by the sibling NAT axioms."
**ASN**: ActionPoint Definition: *"the unique m ∈ S such that (A n ∈ S :: m ≤ n), where S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}."*
**Issue**: The set-builder for S leaves `i` untyped, departing from the parallel-typing convention TA-Pos explicitly adopts for the same index role. The derivation recovers `S ⊆ ℕ` via T0, but the comprehension notation itself is less rigorous than the parallel existential in TA-Pos that it inherits from. Stylistic inconsistency only, recovered by prose.

### OrdinalDisplacement "whose minimum is m" skips the minimum predicate's discharge
**Class**: OBSERVE
**Foundation**: ActionPoint's Definition requires the unique `m ∈ S` with `(A n ∈ S :: m ≤ n)`, not merely `m ∈ S`.
**ASN**: OrdinalDisplacement: *"since δ(n, m)ᵢ = 0 for 1 ≤ i < m and δ(n, m)ₘ = n ≠ 0, this set equals {m}, whose minimum is m."*
**Issue**: The proof shows S_δ = {m} and concludes "whose minimum is m" in a single step. ActionPoint's Definition demands `(A n ∈ S_δ :: m ≤ n)`; at S_δ = {m} this requires `m ≤ m`, which unfolds to `m < m ∨ m = m` via NAT-order's ≤-definition and closes by `m = m`. The step is one-line obvious but the proof walks analogous unfolds elsewhere (e.g., the `n ≥ 1 ⟹ n ≠ 0` promotion). Uniform detail would invoke NAT-order's ≤-definition here too.

### NAT-order prose ends with a style-comparison sentence that advances no content
**Class**: OBSERVE
**Foundation**: N/A (NAT-order body)
**ASN**: NAT-order: *"NAT-closure follows the same register for the arithmetic primitive, opening its axiom slot with the signature `+ : ℕ × ℕ → ℕ` before the unit-membership and left-identity clauses."*
**Issue**: This sentence is a cross-ASN observation about presentational register; it neither introduces, constrains, nor derives anything about `<`. A reader following NAT-order's content must skip past it to continue to the formal contract. Classic meta-prose that belongs in an editorial note, not in the axiom body.

VERDICT: OBSERVE

## Result

Regional review converged after 3 cycles.

*Elapsed: 806s*
