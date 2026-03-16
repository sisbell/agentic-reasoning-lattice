include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module UnboundedExtent {
  import opened TumblerAlgebra

  // B9 — UnboundedExtent
  //
  // Derived from T0(a) (unbounded components) and B1 (contiguous prefix).

  // Closed form of sibling stream S(p, d): cₙ = p ++ zeros(d-1) ++ [n]
  ghost function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  // DIVERGENCE: The ASN states UnboundedExtent over the full operational
  // model: registries reachable by baptism sequences with B6 constraints.
  // The Dafny model captures the structural core: the stream is injective
  // (distinct indices give distinct elements), so hwm is unbounded.
  // Operational reachability depends on Bop (baptism adds next) and
  // B1 (contiguous prefix). B6 (valid depth) constrains which (p, d)
  // pairs produce T4-valid addresses; it is not needed for injectivity.
  lemma UnboundedExtent(p: Tumbler, d: nat, M: nat)
    requires d >= 1
    ensures forall i, j :: 1 <= i < j <= M ==>
      StreamElement(p, d, i) != StreamElement(p, d, j)
  {
    forall i, j | 1 <= i < j <= M
      ensures StreamElement(p, d, i) != StreamElement(p, d, j)
    {
      var last := |p.components| + d - 1;
      assert StreamElement(p, d, i).components[last] == i;
      assert StreamElement(p, d, j).components[last] == j;
    }
  }
}
