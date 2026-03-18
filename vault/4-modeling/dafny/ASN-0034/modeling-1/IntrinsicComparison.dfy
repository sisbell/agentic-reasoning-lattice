include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// T2 — IntrinsicComparison
module IntrinsicComparison {
  import opened TumblerAlgebra

  // T2: The order relation T1 is computable from the two tumblers alone,
  // examining at most min(#a, #b) component pairs. Components beyond
  // min(#a, #b) do not affect the ordering result.
  ghost predicate IntrinsicComparison(a: Tumbler, b: Tumbler) {
    forall p: Tumbler, q: Tumbler ::
      |p.components| == |a.components| &&
      |q.components| == |b.components| &&
      (forall i :: 0 <= i < |a.components| && 0 <= i < |b.components| ==>
        p.components[i] == a.components[i] && q.components[i] == b.components[i])
      ==> (LessThan(p, q) <==> LessThan(a, b))
  }

  // LessThanAt is preserved when lengths match and shared-region components agree
  lemma LessThanAtTransfer(a: Tumbler, b: Tumbler, p: Tumbler, q: Tumbler, k: nat)
    requires |p.components| == |a.components|
    requires |q.components| == |b.components|
    requires forall i :: 0 <= i < |a.components| && 0 <= i < |b.components| ==>
      p.components[i] == a.components[i] && q.components[i] == b.components[i]
    requires LessThanAt(a, b, k)
    ensures LessThanAt(p, q, k)
  { }

  lemma IntrinsicComparisonHolds(a: Tumbler, b: Tumbler)
    ensures IntrinsicComparison(a, b)
  {
    forall p: Tumbler, q: Tumbler |
      |p.components| == |a.components| &&
      |q.components| == |b.components| &&
      (forall i :: 0 <= i < |a.components| && 0 <= i < |b.components| ==>
        p.components[i] == a.components[i] && q.components[i] == b.components[i])
      ensures LessThan(p, q) <==> LessThan(a, b)
    {
      if LessThan(a, b) {
        var k: nat :| LessThanAt(a, b, k);
        LessThanAtTransfer(a, b, p, q, k);
      }
      if LessThan(p, q) {
        var k: nat :| LessThanAt(p, q, k);
        LessThanAtTransfer(p, q, a, b, k);
      }
    }
  }
}
