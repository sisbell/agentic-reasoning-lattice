**TA5-SigValid (SigOnValidAddresses).** For every valid address `t` satisfying T4, `sig(t) = #t`.

*Proof.* Let `t` be a valid address satisfying T4. By T4's positive-component constraint, every component that belongs to a field — that is, every non-separator component — is strictly positive. In particular, the last component of the last field satisfies `t_{#t} > 0`, since T4's non-empty field constraint guarantees the last field has at least one component, and that component is positive.

Since `t_{#t} > 0`, the tumbler `t` has at least one nonzero component, and by TA5-SIG, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`. The index `#t` belongs to this set, so `sig(t) ≥ #t`. But `sig(t) ≤ #t` by the range guarantee of TA5-SIG. Therefore `sig(t) = #t`. ∎

*Formal Contract:*
- *Precondition:* `t` satisfies T4 (valid address tumbler: at most three zero-valued field separators, every field component strictly positive, every present field non-empty).
- *Guarantee:* `sig(t) = #t`.
