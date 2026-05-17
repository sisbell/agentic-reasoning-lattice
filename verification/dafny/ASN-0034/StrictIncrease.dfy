// ASN-0034: TA-strict — StrictIncrease
// Corollary re-exporting TumblerAdd's strict-increase guarantee:
//   (A a ∈ T, w > 0 : actionPoint(w) ≤ #a : a ⊕ w > a).
include "./TumblerAdd.dfy"
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"

module StrictIncrease {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened LexicographicOrder

  lemma StrictIncrease(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    ensures
      var r := TumblerAdd.TumblerAdd(a, w);
      LexicographicOrder.LexicographicOrder(a, r)
  { }
}
