**NAT-zero (NatZeroMinimum).** `0` is the minimum of ℕ: `(A n ∈ ℕ :: 0 ≤ n)`.

In words: every natural number is at least `0`. Equivalently, `0` is a lower bound of ℕ — the least element under `≤`.

This is an independent axiom, not derivable from the other NAT-* axioms. NAT-order supplies strict total order on ℕ — irreflexivity, transitivity, trichotomy — but these properties do not identify `0` as the minimum: they hold equally well with `0` in any position of the order. NAT-wellorder guarantees that every nonempty subset of ℕ, and hence ℕ itself, has a least element, but it does not name that element `0`. NAT-zero closes that gap by fixing `0` as a lower bound, which permits downstream proofs to instantiate NAT-discrete's axiom `m ≤ n < m + 1 ⟹ n = m` at `m = 0` with a secured premise `0 ≤ n`.

Downstream proofs cite NAT-zero whenever they need `0 ≤ n` for some `n ∈ ℕ` — for instance, when combining with NAT-discrete to conclude `n ≠ 0 ⟹ n ≥ 1`, an inference that requires both `n ≠ 0` and the lower-bound premise `0 ≤ n`.

*Formal Contract:*
- *Axiom:* `(A n ∈ ℕ :: 0 ≤ n)` (zero is a lower bound of ℕ).
