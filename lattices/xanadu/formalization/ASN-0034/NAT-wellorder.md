**NAT-wellorder (NatWellOrdering).** ℕ is well-ordered by `<`: every nonempty subset `S ⊆ ℕ` has a least element.

Formally: for every `S ⊆ ℕ` with `S ≠ ∅`, there exists `m ∈ S` such that `m ≤ n` for every `n ∈ S`.

*Formal Contract:*
- *Axiom:* `(A S : S ⊆ ℕ ∧ S ≠ ∅ : (E m ∈ S :: (A n ∈ S :: m ≤ n)))` (least-element principle).
