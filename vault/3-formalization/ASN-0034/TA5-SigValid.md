**TA5-SigValid (SigOnValidAddresses).** For every valid address `t` satisfying T4, `sig(t) = #t`.

*Proof.* Let `t` be a valid address satisfying T4. T4's field-segment constraint requires `t_{#t} ≠ 0`, so the last component is non-zero; and since `t_{#t} ∈ ℕ` by T0, `t_{#t} ≠ 0` entails `t_{#t} > 0`.

Since `t_{#t} > 0`, the tumbler `t` has at least one nonzero component, and by TA5-SIG, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`. The index `#t` belongs to this set, so `sig(t) ≥ #t`. But `sig(t) ≤ #t` by the range guarantee of TA5-SIG. Therefore `sig(t) = #t`. ∎

*Formal Contract:*
- *Precondition:* `t` satisfies T4 (valid address tumbler: at most three zero-valued field separators, field-segment constraint — no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`). Positivity of non-zero components is supplied by T0's carrier ℕ.
- *Depends:* T4 (HierarchicalParsing) — invoked at the proof opening to extract the field-segment constraint `t_{#t} ≠ 0` ("T4's field-segment constraint requires `t_{#t} ≠ 0`, so the last component is non-zero"); without T4 the rightmost component could be zero and the equality `sig(t) = #t` would fail. T0 (CarrierSetDefinition) — invoked immediately after T4 to convert "non-zero" into strict positivity ("since `t_{#t} ∈ ℕ` by T0, `t_{#t} ≠ 0` entails `t_{#t} > 0`"); T0's carrier ℕ supplies the discreteness that licenses this step. TA5-SIG (LastSignificantPosition) — invoked twice: first to unfold `sig(t)` as the maximum-position formula ("by TA5-SIG, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`") which gives `sig(t) ≥ #t` from `t_{#t} > 0`'s membership, and second for the range guarantee `sig(t) ≤ #t` ("`sig(t) ≤ #t` by the range guarantee of TA5-SIG"); the two bounds combine to `sig(t) = #t`.
- *Guarantee:* `sig(t) = #t`.
