// ASN-0034: TA4 — PartialInverse
// (a ⊕ w) ⊖ w = a holds exactly when ActionPoint(w) = #a = #w and the
// components of a strictly before that position are zero.
include "./TumblerAdd.dfy"
include "./TumblerSub.dfy"
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./NatStrictTotalOrder.dfy"

module PartialInverse {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import opened ZeroPaddedDivergence
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  lemma PartialInverse(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires Length(a) == Length(w)
    requires ActionPoint.ActionPoint(w) == Length(w)
    requires forall i :: 1 <= i < Length(a) ==> Component(a, i) == 0
    ensures TumblerSub.TumblerSub(TumblerAdd.TumblerAdd(a, w), w) == a
  { }
}
