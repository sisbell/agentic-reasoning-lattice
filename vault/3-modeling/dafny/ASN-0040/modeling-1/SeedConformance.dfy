include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// B₀ conf. — SeedConformance
module SeedConformance {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // n-th element of sibling stream S(p, d): [p_1, ..., p_{#p}, 0^{d-1}, n]
  function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  // B₀ conf. — SeedConformance
  // (A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d))
  // and (A t ∈ B₀ : t satisfies T4)
  ghost predicate SeedConformance(B0: set<Tumbler>) {
    (forall t :: t in B0 ==> TumblerHierarchy.ValidAddress(t)) &&
    (forall p: Tumbler, d: nat, n: nat ::
      d >= 1 && n >= 1 && StreamElement(p, d, n) in B0 ==>
      (forall i :: 1 <= i < n ==> StreamElement(p, d, i) in B0))
  }
}
