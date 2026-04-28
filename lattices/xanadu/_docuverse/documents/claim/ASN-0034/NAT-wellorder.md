**NAT-wellorder (NatWellOrdering).** ℕ is well-ordered by `<`: every nonempty subset `S ⊆ ℕ` has a least element.

Formally: for every `S ⊆ ℕ` with `S ≠ ∅`, there exists `m ∈ S` such that `m ≤ n` for every `n ∈ S`.

*Formal Contract:*
- *Axiom:* `(A S : S ⊆ ℕ ∧ S ≠ ∅ : (E m ∈ S :: (A n ∈ S :: m ≤ n)))` (least-element principle).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the carrier-side clause `S ⊆ ℕ` of the axiom and as the ambient set whose elements `S` ranges over and from which the bound variables `m, n ∈ S` of the inner quantifiers `(E m ∈ S :: ...)` and `(A n ∈ S :: ...)` draw their values (since `S ⊆ ℕ`).
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`), used in the inner quantifier `(A n ∈ S :: m ≤ n)` that characterizes `m` as a least element of `S`.
