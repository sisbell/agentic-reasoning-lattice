**NAT-wellorder (NatWellOrdering).** ℕ is well-ordered by `<`: every nonempty subset `S ⊆ ℕ` has a least element.

Formally: for every `S ⊆ ℕ` with `S ≠ ∅`, there exists `m ∈ S` such that `m ≤ n` for every `n ∈ S`.

The axiom body invokes the non-strict companion `≤`, which is not a primitive of ℕ — it is *defined* in NAT-order by `m ≤ n ⟺ m < n ∨ m = n`. NAT-order is therefore declared in the Depends slot so that the axiom body can be read without silently importing the definition. The set-theoretic primitives `⊆`, `∈`, and `≠ ∅` carry their standard first-order meaning (subset, membership, nonemptiness) in the ambient register shared across the ASN; they are not axiomatized by any NAT dependency and no NAT axiom is cited to ground them.

*Formal Contract:*
- *Axiom:* `(A S : S ⊆ ℕ ∧ S ≠ ∅ : (E m ∈ S :: (A n ∈ S :: m ≤ n)))` (least-element principle).
- *Depends:*
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`), used in the inner quantifier `(A n ∈ S :: m ≤ n)` that characterizes `m` as a least element of `S`.
