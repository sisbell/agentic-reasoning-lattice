include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ReverseInverseProof {

  import opened TumblerAlgebra

  // Reverse inverse (ASN-0001: ReverseInverse, derived from TA4, TA3)
  lemma ReverseInverse(a: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires Subtractable(a, w)
    requires |a.components| > 0
    requires |w.components| == |a.components|
    requires ActionPoint(w) == |a.components| - 1
    requires forall i :: 0 <= i < ActionPoint(w) ==> a.components[i] == 0
    ensures ActionPoint(w) < |TumblerSubtract(a, w).components|
    ensures TumblerAdd(TumblerSubtract(a, w), w) == a
  { }
}
