include "./LexicographicOrder.dfy"
include "./TumblerAdd.dfy"

module OrderPreservationUnderAddition {
  // TA1 — OrderPreservationUnderAddition

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import TA = TumblerAdd

  lemma OrderPreservationUnderAddition(a: Tumbler, b: Tumbler, w: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(b)
    requires ValidTumbler(w)
    requires LessThan(a, b)
    requires IsPositive(w)
    requires TA.ActionPoint(w) < |a.components|
    requires TA.ActionPoint(w) < |b.components|
    ensures LessThan(TA.TumblerAdd(a, w), TA.TumblerAdd(b, w)) ||
            TA.TumblerAdd(a, w) == TA.TumblerAdd(b, w)
  {
    var k := TA.ActionPoint(w);
    var ra := TA.TumblerAdd(a, w);
    var rb := TA.TumblerAdd(b, w);
    var j := FirstDivergence(a.components, b.components, 0);
    FirstDivergenceProperties(a.components, b.components, 0);

    if j > k {
      // Divergence after action point: a[k] == b[k], results are equal
      assert a.components[k] == b.components[k];
    } else {
      // j <= k < |a| and j <= k < |b|, so j < |a| and j < |b|
      // FirstDivergence: a[j] != b[j]
      // Eliminate the a[j] > b[j] case by contradiction with LessThan(a, b)
      if a.components[j] >= b.components[j] {
        assert LessThan(b, a);
        LessThanTransitive(a, b, a);
        LessThanIrreflexive(a);
      }
      // Now a[j] < b[j]; provide j as witness for LessThan(ra, rb)
      assert ra.components[j] < rb.components[j];
      assert forall i :: 0 <= i < j ==>
        i < |ra.components| && i < |rb.components| &&
        ra.components[i] == rb.components[i];
    }
  }
}
