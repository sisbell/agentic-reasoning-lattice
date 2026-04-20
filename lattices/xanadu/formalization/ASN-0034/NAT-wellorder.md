**NAT-wellorder (NatWellOrdering).** ℕ is well-ordered by `<`: every nonempty subset `S ⊆ ℕ` has a least element.

Formally: for every `S ⊆ ℕ` with `S ≠ ∅`, there exists `m ∈ S` such that `m ≤ n` for every `n ∈ S`. This least-element principle is what makes `min(S)` well-defined whenever `S` is nonempty.

Well-ordering is an independent axiom. Strict total order and discreteness alone do not entail it — ℤ with the usual `<` is strictly totally ordered and discrete but not well-ordered. Downstream proofs cite NAT-wellorder when constructing an index by taking the minimum of a nonempty set, or when running an induction that relies on descent being impossible indefinitely.

*Formal Contract:*
- *Axiom:* `(A S : S ⊆ ℕ ∧ S ≠ ∅ : (E m ∈ S :: (A n ∈ S :: m ≤ n)))` (least-element principle).
