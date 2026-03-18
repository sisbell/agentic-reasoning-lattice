include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ContiguousPrefix {
  import opened TumblerAlgebra

  // B1 — ContiguousPrefix
  // (A p, d, n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))
  // Equivalently: children(B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

  // Closed-form n-th element of sibling stream S(p, d)
  function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  ghost predicate ContiguousPrefix(B: set<Tumbler>) {
    forall p: Tumbler, d: nat, n: nat ::
      d >= 1 && n >= 1 && StreamElement(p, d, n) in B ==>
      forall i :: 1 <= i < n ==> StreamElement(p, d, i) in B
  }
}
