include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module AdditionWeakOrder {
  import opened TumblerAlgebra

  // TA1 — AdditionWeakOrder

  ghost predicate LessEqual(a: Tumbler, b: Tumbler) {
    a == b || LessThan(a, b)
  }

  lemma AdditionWeakOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
    requires ActionPoint(w) < |b.components|
    ensures LessEqual(TumblerAdd(a, w), TumblerAdd(b, w))
  {
    var ap := ActionPoint(w);
    var k :| LessThanAt(a, b, k);

    if k > ap {
      // Divergence after action point — a and b agree on 0..ap, results equal
      assert TumblerAdd(a, w) == TumblerAdd(b, w);
    } else {
      // Divergence at or before action point — strict order preserved
      LessThanIntro(TumblerAdd(a, w), TumblerAdd(b, w), k);
    }
  }
}
