// ASN-0034: TS4 — ShiftStrictIncrease
// Corollary: shifting a tumbler by any positive amount strictly increases it.
//   (A v ∈ T, n ≥ 1 : shift(v, n) > v).
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"
include "./OrdinalShift.dfy"
include "./OrdinalDisplacement.dfy"
include "./StrictIncrease.dfy"

module ShiftStrictIncrease {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened LexicographicOrder
  import OrdinalShift
  import OrdinalDisplacement
  import StrictIncrease

  lemma ShiftStrictIncrease(v: Tumbler, n: nat)
    requires InT(v)
    requires n >= 1
    ensures LexicographicOrder.LexicographicOrder(
              v, OrdinalShift.OrdinalShift(v, n))
  {
    var m := Length(v);
    var w := OrdinalDisplacement.OrdinalDisplacement(n, m);
    StrictIncrease.StrictIncrease(v, w);
  }
}
