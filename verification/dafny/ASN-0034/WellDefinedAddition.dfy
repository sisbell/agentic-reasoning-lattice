// ASN-0034: TA0 — WellDefinedAddition
// Corollary packaging TumblerAdd's first two postconditions:
//   (A a, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a : a ⊕ w ∈ T ∧ #(a ⊕ w) = #w).
include "./TumblerAdd.dfy"
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./NatStrictTotalOrder.dfy"

module WellDefinedAddition {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened NatStrictTotalOrder

  lemma WellDefinedAddition(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    ensures InT(TumblerAdd.TumblerAdd(a, w))
    ensures Length(TumblerAdd.TumblerAdd(a, w)) == Length(w)
  { }
}
