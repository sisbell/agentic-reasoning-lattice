// B0a — BaptismalClosure (ASN-0040)
include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module BaptismalClosure {
  import opened TumblerAlgebra
  import TumblerHierarchy

  datatype BaptismalState = BaptismalState(B: set<Tumbler>)

  // n-th element of sibling stream S(p, d): [p_1, ..., p_{#p}, 0^{d-1}, n]
  function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  // B6 — valid baptism parameters
  predicate ValidBaptismParams(p: Tumbler, d: nat) {
    TumblerHierarchy.ValidAddress(p) &&
    d >= 1 && d <= 2 &&
    TumblerHierarchy.ZeroCount(p.components) + d <= 4
  }

  // t is the next element in S(p, d) not yet in B,
  // with all predecessors present (contiguous prefix)
  ghost predicate ProducedByBaptism(B: set<Tumbler>, p: Tumbler, d: nat, t: Tumbler) {
    ValidBaptismParams(p, d) &&
    exists n :: n >= 1 &&
      t == StreamElement(p, d, n) &&
      (forall i :: 1 <= i < n ==> StreamElement(p, d, i) in B) &&
      t !in B
  }

  // B0a — every newly baptized tumbler was produced by a valid baptism
  ghost predicate BaptismalClosure(before: BaptismalState, after: BaptismalState) {
    forall t :: t in after.B && t !in before.B ==>
      exists p: Tumbler, d: nat :: ProducedByBaptism(before.B, p, d, t)
  }
}
