include "./LexicographicOrder.dfy"
include "./TumblerSub.dfy"

module OrderPreservationUnderSubtractionStrict {
  // TA3-strict — OrderPreservationUnderSubtractionStrict

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import TS = TumblerSub

  // Helper: components of TumblerSub agree at positions where a and b agree
  lemma SubComponentBeforeDivergence(
    a: Tumbler, b: Tumbler, w: Tumbler, i: nat
  )
    requires ValidTumbler(a) && ValidTumbler(b) && ValidTumbler(w)
    requires TS.GreaterOrEqual(a, w) && TS.GreaterOrEqual(b, w)
    requires i < |a.components| && i < |b.components|
    requires a.components[i] == b.components[i]
    requires forall p :: 0 <= p < i ==>
               p < |a.components| && p < |b.components| &&
               a.components[p] == b.components[p]
    ensures i < |TS.TumblerSub(a, w).components|
    ensures i < |TS.TumblerSub(b, w).components|
    ensures TS.TumblerSub(a, w).components[i] == TS.TumblerSub(b, w).components[i]
  { }

  // Helper: at value divergence, ra[j] < rb[j] strictly
  lemma SubComponentAtDivergenceStrict(
    a: Tumbler, b: Tumbler, w: Tumbler, j: nat
  )
    requires ValidTumbler(a) && ValidTumbler(b) && ValidTumbler(w)
    requires TS.GreaterOrEqual(a, w) && TS.GreaterOrEqual(b, w)
    requires j < |a.components| && j < |b.components|
    requires a.components[j] < b.components[j]
    requires forall p :: 0 <= p < j ==>
               p < |a.components| && p < |b.components| &&
               a.components[p] == b.components[p]
    ensures j < |TS.TumblerSub(a, w).components|
    ensures j < |TS.TumblerSub(b, w).components|
    ensures TS.TumblerSub(a, w).components[j] < TS.TumblerSub(b, w).components[j]
  { }

  lemma OrderPreservationUnderSubtractionStrict(a: Tumbler, b: Tumbler, w: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(b)
    requires ValidTumbler(w)
    requires LessThan(a, b)
    requires TS.GreaterOrEqual(a, w)
    requires TS.GreaterOrEqual(b, w)
    requires |a.components| == |b.components|
    ensures LessThan(TS.TumblerSub(a, w), TS.TumblerSub(b, w))
  {
    var ra := TS.TumblerSub(a, w);
    var rb := TS.TumblerSub(b, w);
    var j := FirstDivergence(a.components, b.components, 0);
    FirstDivergenceProperties(a.components, b.components, 0);

    // Equal lengths rule out T1 case (ii) and equality, so divergence is within bounds
    if j == |a.components| {
      assert forall i :: 0 <= i < |a.components| ==> a.components[i] == b.components[i];
      assert a.components == b.components;
      LessThanIrreflexive(a);
    }

    // Positions before j agree
    forall i | 0 <= i < j
      ensures i < |ra.components| && i < |rb.components| &&
              ra.components[i] == rb.components[i]
    {
      SubComponentBeforeDivergence(a, b, w, i);
    }

    // At j: strict inequality
    SubComponentAtDivergenceStrict(a, b, w, j);

    // Witness j for LessThan(ra, rb)
    assert ra.components[j] < rb.components[j];
  }
}
