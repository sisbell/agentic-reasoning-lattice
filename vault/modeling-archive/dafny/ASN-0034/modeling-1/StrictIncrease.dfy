include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module StrictIncrease {
  import opened TumblerAlgebra

  // TA-strict: a ⊕ w > a for any positive displacement w
  lemma StrictIncrease(a: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
    ensures LessThan(a, TumblerAdd(a, w))
  {
    var k := ActionPoint(w);
    var r := TumblerAdd(a, w);
    LessThanIntro(a, r, k);
  }
}
