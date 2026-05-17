// ASN-0034: TA-MTO — ManyToOne
// For displacement w and tumblers a, b with #a ≥ k and #b ≥ k (k = actionPoint(w)):
//   a ⊕ w = b ⊕ w ⟺ (∀ i : 1 ≤ i ≤ k : aᵢ = bᵢ).
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./WellDefinedAddition.dfy"
include "./CanonicalRepresentation.dfy"
include "./NatAdditionCancellation.dfy"

module ManyToOne {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened WellDefinedAddition
  import opened CanonicalRepresentation
  import opened NatAdditionCancellation
  import opened NatCarrierSet

  lemma ManyToOne(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    requires ActionPoint.ActionPoint(w) <= Length(b)
    ensures TumblerAdd.TumblerAdd(a, w) == TumblerAdd.TumblerAdd(b, w) <==>
      (forall i :: 1 <= i <= ActionPoint.ActionPoint(w) ==>
        Component(a, i) == Component(b, i))
  { }
}
