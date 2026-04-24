**NAT-wellorder (NatWellOrdering).** ℕ is well-ordered by `<`: every nonempty subset `S ⊆ ℕ` has a least element.

Formally: for every `S ⊆ ℕ` with `S ≠ ∅`, there exists `m ∈ S` such that `m ≤ n` for every `n ∈ S`.

The axiom body invokes the non-strict companion `≤`, which is not a primitive of ℕ — it is *defined* in NAT-order by `m ≤ n ⟺ m < n ∨ m = n`.

*Formal Contract:*
- *Axiom:* `(A S : S ⊆ ℕ ∧ S ≠ ∅ : (E m ∈ S :: (A n ∈ S :: m ≤ n)))` (least-element principle).
- *Depends:*
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`), used in the inner quantifier `(A n ∈ S :: m ≤ n)` that characterizes `m` as a least element of `S`.
