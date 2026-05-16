include "./LexicographicOrder.dfy"
include "./TumblerAdd.dfy"

module StrictOrderPreservation {
  // TA1-strict — StrictOrderPreservation

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import TA = TumblerAdd

  lemma StrictOrderPreservation(a: Tumbler, b: Tumbler, w: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(b)
    requires ValidTumbler(w)
    requires LessThan(a, b)
    requires IsPositive(w)
    requires TA.ActionPoint(w) < |a.components|
    requires TA.ActionPoint(w) < |b.components|
    requires TA.ActionPoint(w) >= FirstDivergence(a.components, b.components, 0)
    ensures LessThan(TA.TumblerAdd(a, w), TA.TumblerAdd(b, w))
  {
    var k := TA.ActionPoint(w);
    var j := FirstDivergence(a.components, b.components, 0);
    FirstDivergenceProperties(a.components, b.components, 0);
    var ra := TA.TumblerAdd(a, w);
    var rb := TA.TumblerAdd(b, w);

    // j is the witness for LessThan(ra, rb): results agree before j, diverge at j
    assert ra.components[j] < rb.components[j];
    assert forall i :: 0 <= i < j ==>
      i < |ra.components| && i < |rb.components| &&
      ra.components[i] == rb.components[i];
  }
}
