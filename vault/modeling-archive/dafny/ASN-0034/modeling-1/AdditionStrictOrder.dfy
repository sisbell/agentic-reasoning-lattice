include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module AdditionStrictOrder {
  import opened TumblerAlgebra

  // TA1-strict — AdditionStrictOrder
  // (A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)

  lemma AdditionStrictOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
    requires ActionPoint(w) < |b.components|
    requires LessThan(a, b)
    requires exists d :: 0 <= d <= ActionPoint(w) &&
               d < |a.components| && d < |b.components| &&
               a.components[d] != b.components[d] &&
               (forall j :: 0 <= j < d ==> a.components[j] == b.components[j])
    ensures LessThan(TumblerAdd(a, w), TumblerAdd(b, w))
  {
    var k :| LessThanAt(a, b, k);
    LessThanIntro(TumblerAdd(a, w), TumblerAdd(b, w), k);
  }
}
