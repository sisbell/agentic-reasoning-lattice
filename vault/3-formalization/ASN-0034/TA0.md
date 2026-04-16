**TA0 (WellDefinedAddition).** TumblerAdd's piecewise construction yields a well-defined tumbler: for `a, w ∈ T` where `Pos(w)` and `actionPoint(w) ≤ #a`, the result `a ⊕ w` lies in `T`.

The precondition `actionPoint(w) ≤ #a` is essential: TumblerAdd's construction copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`. A displacement whose action point exceeds `#a` — one with more leading zeros than `a` has components — would attempt to "stay at" hierarchical levels that the start position does not have, and the operation is undefined.

*Proof.* Since `Pos(w)`, at least one component of `w` is nonzero, so the action point `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` is well-defined. The precondition `k ≤ #a` ensures that TumblerAdd's piecewise construction is applicable: the prefix-copy region `i < k` indexes valid positions within `a`, and the action-point component `aₖ` exists. By TumblerAdd, each component of the result lies in ℕ and `#(a ⊕ w) = #w ≥ 1`, so `a ⊕ w ∈ T`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a
- *Depends:* TumblerAdd (TumblerAdd) — the proof delegates entirely to TumblerAdd's piecewise construction: component membership in ℕ and the result-length identity `#(a ⊕ w) = #w` are TumblerAdd postconditions.
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w
