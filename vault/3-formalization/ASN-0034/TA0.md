### Well-definedness of addition

**TA0 (WellDefinedAddition).** For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

The precondition `k ≤ #a` is essential: the constructive definition copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`. A displacement whose action point exceeds `#a` — one with more leading zeros than `a` has components — would attempt to "stay at" hierarchical levels that the start position does not have, and the operation is undefined.

*Proof.* Since `w > 0`, at least one component of `w` is nonzero, so the action point `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` is well-defined. The precondition `k ≤ #a` ensures that TumblerAdd's piecewise construction is applicable: the prefix-copy region `i < k` indexes valid positions within `a`, and the action-point component `aₖ` exists. By TumblerAdd, each component of the result lies in ℕ and `#(a ⊕ w) = #w ≥ 1`, so `a ⊕ w ∈ T`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) ≤ #a
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w
