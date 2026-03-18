include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module MutualInverseProof {

  import opened TumblerAlgebra

  // TA4 — MutualInverse
  lemma MutualInverse(a: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires |a.components| > 0
    requires |w.components| == |a.components|
    requires ActionPoint(w) == |a.components| - 1
    requires forall i :: 0 <= i < ActionPoint(w) ==> a.components[i] == 0
    ensures Subtractable(TumblerAdd(a, w), w)
    ensures TumblerSubtract(TumblerAdd(a, w), w) == a
  { }
}
