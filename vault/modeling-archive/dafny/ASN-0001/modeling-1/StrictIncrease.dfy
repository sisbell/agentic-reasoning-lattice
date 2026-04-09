include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module StrictIncrease {
  import opened TumblerAlgebra

  // TA-strict — StrictIncrease
  // (A a ∈ T, w > 0 : a ⊕ w > a)
  lemma StrictIncrease(a: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
    ensures LessThan(a, TumblerAdd(a, w))
  { }
}
