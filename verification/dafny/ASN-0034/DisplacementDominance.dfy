// ASN-0034: TA-dom — DisplacementDominance
// Corollary re-exporting TumblerAdd's dominance guarantee:
//   (A a, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a : a ⊕ w ≥ w).
include "./TumblerAdd.dfy"
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"

module DisplacementDominance {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened LexicographicOrder

  lemma DisplacementDominance(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    ensures
      var r := TumblerAdd.TumblerAdd(a, w);
      LexicographicOrder.LexicographicOrder(w, r) || w == r
  { }
}
