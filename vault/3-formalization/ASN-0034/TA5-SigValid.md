**TA5-SigValid (SigOnValidAddresses).** For every valid address `t` satisfying T4, `sig(t) = #t`.

*Proof.* Let `t` be a valid address satisfying T4. By T4's positive-component constraint, every non-zero component of `t` is strictly positive. T4's field-segment constraint requires `t_{#t} ≠ 0`, so the last component is non-zero and hence strictly positive: `t_{#t} > 0`.

Since `t_{#t} > 0`, the tumbler `t` has at least one nonzero component, and by TA5-SIG, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`. The index `#t` belongs to this set, so `sig(t) ≥ #t`. But `sig(t) ≤ #t` by the range guarantee of TA5-SIG. Therefore `sig(t) = #t`. ∎

*Formal Contract:*
- *Precondition:* `t` satisfies T4 (valid address tumbler: at most three zero-valued field separators, every non-zero component strictly positive, field-segment constraint — no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`).
- *Guarantee:* `sig(t) = #t`.
