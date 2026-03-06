include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module StrictSubtractionPreservesOrder {

  import opened TumblerAlgebra

  // TA3-strict — StrictSubtractionPreservesOrder
  // (A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)
  lemma StrictSubtractionPreservesOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    requires |a.components| == |b.components|
    ensures LessThan(TumblerSubtract(a, w), TumblerSubtract(b, w))
  {
    var len := Max(|a.components|, |w.components|);
    var pa := Pad(a.components, len);
    var pb := Pad(b.components, len);
    var pw := Pad(w.components, len);

    assert pa != pb;
    var d := FirstDiff(pa, pb);

    LessThanIntro(TumblerSubtract(a, w), TumblerSubtract(b, w), d);
  }
}
