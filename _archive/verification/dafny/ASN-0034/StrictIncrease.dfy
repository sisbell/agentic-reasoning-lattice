include "./LexicographicOrder.dfy"
include "./TumblerAdd.dfy"

module StrictIncrease {
  // TA-strict — StrictIncrease

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import TA = TumblerAdd

  lemma StrictIncrease(a: Tumbler, w: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TA.ActionPoint(w) < |a.components|
    ensures LessThan(a, TA.TumblerAdd(a, w))
  { }
}
